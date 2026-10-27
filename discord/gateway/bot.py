import time
import asyncio
import logging
from typing import cast
from .intents import Intents
from .connection import Connection
from .event import CustomEvent, Event, EventIntents
from ..core import AppBase, CommandNamespace, CommandProxy, InteractionType, PrefixCommand, command_namespace

log = logging.getLogger(__name__)

DEFAULT_INTENTS = Intents.default()

class BotCommandProxy(CommandProxy):
  def __call__(self, *args, **kwargs):
    return self.__getattr__('__call__')(*args, **kwargs)

class Bot(AppBase):
  def __init__(self, token, application_id = None, intents = DEFAULT_INTENTS, prefix = '!', reload = False):
    super().__init__(token, application_id, reload)
    self.intents = intents
    self.prefix = prefix
    self.connection = Connection(self.http, token, intents, self.on_event)
    self.event_handlers = {}
    self.command_handlers = {}
    self.extra_registrars = {Event: (self.add_events, self.remove_events)}
    self.tasks = set()
    self.ready_at = None # time.time() of the latest READY

  def set_proxy(self):
    self.command = cast(CommandNamespace, BotCommandProxy(self, command_namespace))

  def run(self):
    try:
      asyncio.run(self.start())
    except KeyboardInterrupt:
      pass

  async def start(self):
    try:
      await self.startup_lifespans()
      await self.connection.run()
    finally:
      await self.shutdown_lifespans()

  def add_commands(self, *commands):
    super().add_commands(*[command for command in commands if not isinstance(command, PrefixCommand)])
    intents = EventIntents.MESSAGE_CREATE.value
    for command in commands:
      if not isinstance(command, PrefixCommand):
        continue
      name = command.callback.__name__
      if command.name != name:
        name = f'"{command.name}" {name}'
      if not self.intents & intents:
        names = ' / '.join(flag.name for flag in intents if flag.name)
        log.warning(f'gateway command {name}() will never run: missing intents, enable one of {names}')
      elif self.intents & Intents.GUILD_MESSAGES and not self.intents & Intents.MESSAGE_CONTENT:
        log.warning(f'gateway command {name}() may never run: missing intent, enable MESSAGE_CONTENT')
      self.command_handlers[command.name] = command

  def remove_commands(self, *commands):
    super().remove_commands(*[command for command in commands if not isinstance(command, PrefixCommand)])
    for command in commands:
      if isinstance(command, PrefixCommand) and self.command_handlers.get(command.name) is command:
        del self.command_handlers[command.name]

  def event(self, func = None, *, name = None):
    def wrap(f):
      event = Event(f, name)
      self.add_events(event)
      return event
    return wrap(func) if func else wrap

  def add_events(self, *events):
    for event in events:
      if not isinstance(event, Event):
        raise ValueError(f'not an event: {event!r}')
    for event in events:
      name = event.callback.__name__
      if event.name != name:
        name = f'"{event.name}" {name}'
      member = EventIntents.__members__.get(event.gateway_name)
      if not member and event.gateway_name not in CustomEvent.__members__:
        log.warning(f'{event.name} is not a valid gateway event')
      elif member and member.value and not self.intents & member.value:
        names = ' / '.join(flag.name for flag in member.value if flag.name)
        log.warning(f'event handler {name}() will never run: missing intents, enable one of {names}')
      self.event_handlers.setdefault(event.gateway_name, set()).add(event)

  def remove_events(self, *events):
    for event in events:
      if not isinstance(event, Event):
        raise ValueError(f'not an event: {event!r}')
    for event in events:
      handlers = self.event_handlers.get(event.gateway_name, set())
      handlers.discard(event)
      if not handlers:
        self.event_handlers.pop(event.gateway_name, None)

  def spawn(self, coro):
    task = asyncio.create_task(coro)
    self.tasks.add(task)
    task.add_done_callback(self.tasks.discard)

  def handle_gateway_command(self, message):
    data = message.data
    if data.get('webhook_id') or data.get('author', {}).get('bot'):
      return
    if not message.content.startswith(self.prefix):
      return
    parts = message.content.removeprefix(self.prefix).split(maxsplit = 1)
    if not parts:
      return
    if command := self.command_handlers.get(parts[0].lower()):
      arguments = parts[1] if len(parts) > 1 else ''
      self.spawn(command(self.model.context(message, arguments)))

  async def on_event(self, name, data):
    payload = data # what handlers receive, a model if one exists for the event
    match name:
      case 'READY':
        self.http.application_id = data['application']['id']
        is_first_ready = self.ready_at is None
        self.ready_at = time.time()
        if is_first_ready:
          for handler in self.event_handlers.get(CustomEvent.FIRST_READY, ()):
            self.spawn(handler(payload))
      case 'INTERACTION_CREATE':
        match data['type']:
          case InteractionType.APPLICATION_COMMAND:
            self.spawn(self.run_command(data, is_from_http = False))
          case InteractionType.MESSAGE_COMPONENT:
            self.spawn(self.run_component(data, is_from_http = False))
          case InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
            self.spawn(self.run_autocomplete(data, is_from_http = False))
          case InteractionType.MODAL_SUBMIT:
            self.spawn(self.run_modal(data, is_from_http = False))
      case 'MESSAGE_CREATE':
        payload = self.model.message(data)
        self.handle_gateway_command(payload)

    for handler in self.event_handlers.get(name, ()):
      self.spawn(handler(payload))

    for handler in self.event_handlers.get(CustomEvent.ANY_EVENT, ()):
      self.spawn(handler(name, payload))
