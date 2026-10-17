import asyncio
import logging
from typing import cast
from ..base import AppBase
from .intents import Intents
from ..lifespan import Lifespan
from ..proxy import CommandProxy
from .connection import Connection
from .event import Event, EventIntents, ANY_EVENT
from ..command import CommandNamespace, MessageCommand, command

log = logging.getLogger(__name__)

DEFAULT_INTENTS = Intents.default()

class BotCommandProxy(CommandProxy):
  def __call__(self, *args, **kwargs):
    return self.__getattr__('__call__')(*args, **kwargs)

class Bot(AppBase):
  def __init__(self, token, application_id = None, intents = DEFAULT_INTENTS, prefix = '!'):
    super().__init__(token, application_id)
    self.lifespan = Lifespan(self.http)
    self.intents = intents
    self.prefix = prefix
    self.connection = Connection(self.http, token, intents, self.on_event)
    self.event_handlers = {}
    self.command_handlers = {}
    self.tasks = set()

  def set_proxy(self):
    self.command = cast(CommandNamespace, BotCommandProxy(self, command))

  def run(self):
    try:
      asyncio.run(self.start())
    except KeyboardInterrupt:
      pass

  async def start(self):
    try:
      await self.lifespan.startup()
      await self.connection.run()
    finally:
      await self.lifespan.shutdown()

  def add_commands(self, *commands):
    super().add_commands(*[command for command in commands if not isinstance(command, MessageCommand)])
    intents = EventIntents.MESSAGE_CREATE.value
    for command in commands: # noqa: F402
      if not isinstance(command, MessageCommand):
        continue
      if not self.intents & intents:
        names = ' / '.join(flag.name for flag in intents if flag.name)
        log.warning(f'message command {command.name}() will never run: missing intents, enable one of {names}')
      elif self.intents & Intents.GUILD_MESSAGES and not self.intents & Intents.MESSAGE_CONTENT:
        log.warning(f'message command {command.name}() may never run: missing intent, enable MESSAGE_CONTENT')
      self.command_handlers[command.name] = command

  def event(self, func = None, *, name = None):
    def wrap(f):
      event = f if isinstance(f, Event) else Event(f, name)
      self.add_events(event)
      return event
    return wrap(func) if func else wrap

  def add_events(self, *events):
    for event in events:
      if not isinstance(event, Event):
        raise ValueError(f'not an event: {event!r}')
    for event in events:
      member = EventIntents.__members__.get(event.gateway_name)
      if not member and event.gateway_name != ANY_EVENT:
        log.warning(f'{event.name} is not a valid gateway event')
      elif member and member.value and not self.intents & member.value:
        names = ' / '.join(flag.name for flag in member.value if flag.name)
        log.warning(f'event handler {event.name}() will never run: missing intents, enable one of {names}')
      self.event_handlers.setdefault(event.gateway_name, set()).add(event)

  def spawn(self, coro):
    task = asyncio.create_task(coro)
    self.tasks.add(task)
    task.add_done_callback(self.tasks.discard)

  def handle_message_command(self, data):
    if data.get('webhook_id') or data.get('author', {}).get('bot'):
      return
    content = data.get('content', '')
    if not content.startswith(self.prefix):
      return
    parts = content[len(self.prefix):].split(maxsplit = 1)
    if not parts:
      return
    command = self.command_handlers.get(parts[0].lower())
    if command:
      self.spawn(command(data))

  async def on_event(self, name, data):
    if name == 'READY':
      self.http.application_id = data['application']['id']
    elif name == 'INTERACTION_CREATE':
      self.spawn(self.run_command(data, is_from_http = False))
    elif name == 'MESSAGE_CREATE':
      self.handle_message_command(data)

    for handler in self.event_handlers.get(name, ()):
      self.spawn(handler(data))

    for handler in self.event_handlers.get(ANY_EVENT, ()):
      self.spawn(handler(name, data))
