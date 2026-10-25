import time
import inspect
from contextlib import AsyncExitStack, asynccontextmanager
from .cog import CogMixin
from .command import Handler
from .http import HTTPClient

class Lifespan(Handler): # recognized by Cog
  def __init__(self, func, name = None):
    if not inspect.isasyncgenfunction(func):
      raise ValueError(f'a lifespan must be an async generator function (it needs a single yield): {func!r}')
    super().__init__(func, name)

def lifespan(func = None, *, name = None): # @discord.lifespan syntax
  def wrap(f):
    return Lifespan(f, name)
  return wrap(func) if func else wrap

class LifespanMixin(CogMixin):
  def __init__(self, token, application_id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.http = HTTPClient(token, application_id)
    self.stack = AsyncExitStack()
    self.lifespan_handlers = {} # {LifespanHandler: manager, or None if not running}, ordered
    self.started_at = None # time.time() of app start

  def lifespan(self, func = None): # @app.lifespan syntax
    def wrap(f):
      handler = f if isinstance(f, Lifespan) else Lifespan(f)
      if self.started_at is not None:
        raise ValueError(f'cannot use @app.lifespan syntax when already started, use "await app.add_lifespans()" instead for: {handler.name}')
      self.lifespan_handlers.setdefault(handler, None)
      return handler
    return wrap(func) if func else wrap

  def registrars(self):
    return super().registrars() | {Lifespan: (self.add_lifespans, self.remove_lifespans)}

  async def enter_lifespan(self, handler): # used on startup_lifespans and add_lifespans
    manager = asynccontextmanager(handler.func)()
    await manager.__aenter__()
    self.lifespan_handlers[handler] = manager

  async def add_lifespans(self, *handlers):
    for handler in handlers:
      if not isinstance(handler, Lifespan):
        raise ValueError(f'not a lifespan: {handler!r}')
      if self.lifespan_handlers.get(handler) is not None:
        raise ValueError(f'lifespan already running: {handler.name}')
    for handler in handlers:
      self.lifespan_handlers.setdefault(handler, None)
      if self.started_at is not None:
        try:
          await self.enter_lifespan(handler)
        except Exception:
          del self.lifespan_handlers[handler]
          raise

  async def remove_lifespans(self, *handlers):
    for handler in handlers:
      if not isinstance(handler, Lifespan):
        raise ValueError(f'not a lifespan: {handler!r}')
    for handler in handlers:
      if manager := self.lifespan_handlers.pop(handler, None):
        await manager.__aexit__(None, None, None)

  async def startup_lifespans(self):
    self.started_at = time.time()
    try:
      await self.stack.enter_async_context(self.http)
      for handler in list(self.lifespan_handlers):
        await self.enter_lifespan(handler)
    except Exception:
      await self.shutdown_lifespans()
      raise

  async def shutdown_lifespans(self):
    for manager in self.lifespan_handlers.values():
      if manager is not None:
        self.stack.push_async_exit(manager)
    self.lifespan_handlers = dict.fromkeys(self.lifespan_handlers)
    self.started_at = None
    await self.stack.aclose()
