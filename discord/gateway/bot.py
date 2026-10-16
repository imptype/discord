import asyncio
import logging
from ..base import AppBase
from .intents import Intents
from ..lifespan import Lifespan
from .connection import Connection
from .event import Event, ANY_EVENT

log = logging.getLogger(__name__)

DEFAULT_INTENTS = Intents.default()

class Bot(AppBase):
  def __init__(self, token, application_id = None, intents = DEFAULT_INTENTS):
    super().__init__(token, application_id)
    self.lifespan = Lifespan(self.http)
    self.intents = intents
    self.connection = Connection(self.http, token, intents, self.on_event)
    self.handlers = {}
    self.tasks = set()

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
      log.warning(f'{name}() will never fire: missing intents, enable one of {names}')
    self.handlers.setdefault(gateway_name, set()).add(func)
    return func

  def spawn(self, coro):
    task = asyncio.create_task(coro)
    self.tasks.add(task)
    task.add_done_callback(self.tasks.discard)

  async def on_event(self, name, data):
    if name == 'READY':
      self.http.application_id = data['application']['id']
    elif name == 'INTERACTION_CREATE':
      self.spawn(self.run_command(data, is_from_http = False))

    for handler in self.handlers.get(name, ()):
      self.spawn(handler(data))

    for handler in self.handlers.get(ANY_EVENT, ()):
      self.spawn(handler(name, data))
