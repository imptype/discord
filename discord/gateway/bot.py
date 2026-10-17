import asyncio
import logging
from typing import cast
from ..base import AppBase
from .intents import Intents
from ..lifespan import Lifespan
from ..proxy import CommandProxy
from .connection import Connection
from .event import Event, ANY_EVENT
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

  def add_command(self, command):
    if not isinstance(command, MessageCommand):
      return super().add_command(command)
    intents = Event.MESSAGE_CREATE.value
    if not self.intents & intents:
      names = ' / '.join(flag.name for flag in intents if flag.name)
      log.warning(f'message command {command.name}() will never run: missing intents, enable one of {names}')
    elif self.intents & Intents.GUILD_MESSAGES and not self.intents & Intents.MESSAGE_CONTENT:
      log.warning(f'message command {command.name}() may never run: missing intent, enable MESSAGE_CONTENT')
    self.command_handlers[command.name] = command

  def event(self, func = None, *, name = None):
    def wrap(f):
      return self.add_event(f, name)
    return wrap(func) if func else wrap

  def add_event(self, func, name = None):
    name = name or getattr(func, 'name', func.__name__) # getattr for @discord.event
    if not name.startswith('on_'):
      raise ValueError(f'event name must start with on_: {name}')
    gateway_name = name[3:].upper()
    member = Event.__members__.get(gateway_name)
    if not member and gateway_name != ANY_EVENT:
      log.warning(f'{name} is not a valid gateway event')
    elif member and member.value and not self.intents & member.value:
      names = ' / '.join(flag.name for flag in member.value if flag.name)
      log.warning(f'event handler {name}() will never run: missing intents, enable one of {names}')
    self.event_handlers.setdefault(gateway_name, set()).add(func)
    return func

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
