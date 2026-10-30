import time
import asyncio
import inspect
from contextlib import AsyncExitStack, asynccontextmanager
from ..abc import BaseHandler

class Lifespan(BaseHandler): # recognized by Cog
  def __init__(self, callback, name = None):
    if not inspect.isasyncgenfunction(callback):
      raise ValueError(f'a lifespan must be an async generator function (it needs a single yield): {callback!r}')
    super().__init__(callback, name)

def lifespan(callback = None, *, name = None): # @discord.lifespan syntax
  def wrap(callback):
    return Lifespan(callback, name)
  return wrap(callback) if callback else wrap

class LifespanMixin:
  def __init__(self, registrars, http):
    registrars[Lifespan] = (self.add_lifespans, self.remove_lifespans)
    self.http = http # made by AppBase, entered on startup
    self.stack = AsyncExitStack()
    self.lifespan_handlers = {} # {LifespanHandler: manager, or None if not running}, ordered
    self.loop: asyncio.AbstractEventLoop # event loop
    self.started_at = None # time.time() of app start

  def lifespan(self, callback = None): # @app.lifespan syntax
    def wrap(callback): # lets you add by object too (for sync context)
      handler = callback if isinstance(callback, Lifespan) else Lifespan(callback)
      if self.started_at:
        raise ValueError(f'cannot use @app.lifespan syntax when already started, use "await app.add_lifespans()" instead for: {handler.name}')
      self.lifespan_handlers.setdefault(handler, None)
      return handler
    return wrap(callback) if callback else wrap

  async def enter_lifespan(self, handler): # used on startup_lifespans and add_lifespans
    manager = asynccontextmanager(handler.callback)()
    await manager.__aenter__()
    self.lifespan_handlers[handler] = manager

  async def add_lifespans(self, *handlers):
    for handler in handlers:
      if not isinstance(handler, Lifespan):
        raise ValueError(f'not a lifespan: {handler!r}')
      if self.lifespan_handlers.get(handler):
        raise ValueError(f'lifespan already running: {handler.name}')
    for handler in handlers:
      self.lifespan_handlers.setdefault(handler, None)
      if self.started_at:
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
    self.loop = asyncio.get_running_loop()
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
      if manager:
        self.stack.push_async_exit(manager)
    self.lifespan_handlers = dict.fromkeys(self.lifespan_handlers)
    self.started_at = None
    await self.stack.aclose()
