import sys
import asyncio
import inspect
import logging
import importlib
from pathlib import Path
from .abc import BaseHandler
from ..ui import Interactable

log = logging.getLogger(__name__)

SETUP = 'setup'
TEARDOWN = 'teardown'
RELOAD_INTERVAL = 1

class Cog:
  def __init__(self, app):
    self.app = app
    self.instances = {} # {name: instance} to access the persistent view object in a cog

  async def cog_load(self): ...
  async def cog_unload(self): ...

class CogMixin:
  def __init__(self, registrars, reload = False):
    self.registrars = registrars
    self.reload = reload
    self.cogs = {} # loaded cogs {Cog: instance}
    self.cog_handlers = {} # {Cog: [copy.copy of handlers]}
    self.extensions = {} # loaded extensions {name: [Cog]}
    self.extension_files = {} # {name: (path, mtime)} used when reload is on
    self.reload_task = None

  async def run_registrars(self, handlers, remove = False): # bool indexes (add, remove)
    for kind, functions in self.registrars.items():
      result = functions[remove](*[handler for handler in handlers if isinstance(handler, kind)])
      if inspect.isawaitable(result):
        await result

  async def add_cogs(self, *cogs):

    # 1. Find the handlers this app can register (commands, views, modals, Bot can do events too)
    kinds = tuple(self.registrars)

    # 2. Put each cog into a (Cog class, cog_instance/None) pair, to support Cog and Cog(app) syntax
    pairs = [] # [(Cog class, cog_instance/None)]
    for cog in cogs:
      cls = cog if isinstance(cog, type) else type(cog)
      if not issubclass(cls, Cog):
        raise ValueError(f'not a cog: {cog!r}')
      if cls in self.cogs:
        raise ValueError(f'cog already loaded: {cls.__name__}')
      pairs.append((cls, None if isinstance(cog, type) else cog))

    # 3. For each cog, do this!
    for cog, cog_instance in pairs:

      # 3.1. Instantiate if the cog is a Class
      if not cog_instance:
        cog_instance = cog(self)
        if not hasattr(cog_instance, 'instances'): # helps set .instances without super().__init__()
          cog_instance.instances = {}

      # 3.2. Find stuff that should be loaded from the cog and add it to found dict
      found = {} # {name: handler instance | interactable instance | nested class}
      for base in reversed(cog.__mro__): # read base clases first so subclass overrides / is what u expect
        for name, value in vars(base).items():
          if isinstance(value, (BaseHandler, Interactable)): # is a @discord.modal, @discord.button, etc
            found[name] = value
          elif (
            isinstance(value, type) # is a class (which is defined in this cog class)
            and issubclass(value, kinds) # is relevant, is a registerable thing like a View or Modal
            and not name.startswith('_') # allows _ class name prefix to opt out (for abstract base classes)
          ):
            found[name] = value # results in class Panel(discord.View), class Ok(discord.Button), etc

      # 3.3. Convert each found item into a Handler (or an instance if it's a class)
      handlers = []
      for name, value in found.items():

        # 3.3.1. Nested class = instantiate and set .cog add to coginstance.instances
        if isinstance(value, type):
          handler = value.__new__(value)
          handler.cog = cog_instance # lets you refer to the outer cog containing the class
          value.cog = cog_instance # helps set a reused persistent view's default timeout to none
          try:
            handler.__init__() # u can access .app through self.cog.app
          except TypeError as e:
            raise ValueError(f'{cog.__name__}.{name} cannot be loaded, persistent __init__() must not have any required arguments: {e}') from e
          cog_instance.instances[name] = handler

        # 3.3.2. @decorator = bind it to the cog instance and set it as self.<name>
        else:
          handler = value.bind(cog_instance)
          setattr(cog_instance, name, handler) # allows self.<handler> ref (unlike classes)

        # 3.3.3. Warn if it could not be loaded (Events can only be used by Bot not App)
        if isinstance(handler, kinds):
          handlers.append(handler)
        else:
          log.warning(f'{cog.__name__}.{name}() was not loaded: {type(handler).__name__} is not supported by {type(self).__name__}')

      # 3.4. Cache them and run cog_load(), and undo if it errors
      self.cogs[cog] = cog_instance
      self.cog_handlers[cog] = handlers
      try:
        await cog_instance.cog_load()
      except Exception:
        del self.cogs[cog]
        del self.cog_handlers[cog]
        raise

      # 3.5. Register handlers with the app, and undo if it errors
      try:
        await self.run_registrars(handlers)
      except Exception:
        await self.remove_cogs(cog)
        raise

  async def remove_cogs(self, *cogs):
    for cog in cogs:
      if cog not in self.cogs:
        raise ValueError(f'cog not loaded: {cog!r}')
    for cog in cogs:
      cog_instance = self.cogs.pop(cog)
      handlers = self.cog_handlers.pop(cog)
      await self.run_registrars(handlers, remove = True)
      await cog_instance.cog_unload()

  async def load_extensions(self, *names):
    caller = sys._getframe(1).f_globals.get('__file__') # the file that called this
    if caller and (folder := str(Path(caller).resolve().parent)) not in sys.path:
      sys.path.insert(0, folder) # so 'cogs.modal' resolves next to the caller, like running the file directly
    await self.import_extensions(*names)

  async def import_extensions(self, *names): # also used by the reloader, which must not touch sys.path
    for name in names:
      if not isinstance(name, str):
        raise ValueError(f'not an extension name: {name!r}')
      if name in self.extensions:
        raise ValueError(f'extension already loaded: {name!r}')
    for name in names:
      module = importlib.import_module(name)
      if (setup := getattr(module, SETUP, None)) is None:
        sys.modules.pop(name, None)
        raise ValueError(f'extension {name!r} has no {SETUP}(app)')
      before = set(self.cogs)
      try:
        await setup(self)
      except Exception:
        await self.remove_cogs(*[cog for cog in self.cogs if cog not in before])
        sys.modules.pop(name, None)
        raise
      self.extensions[name] = [cog for cog in self.cogs if cog not in before]
      if self.reload and (path := getattr(module, '__file__', None)):
        path = Path(path)
        self.extension_files[name] = (path, path.stat().st_mtime)
        if self.reload_task is None:
          self.reload_task = asyncio.create_task(self.watch_extensions())

  async def unload_extensions(self, *names):
    for name in names:
      if name not in self.extensions:
        raise ValueError(f'extension not loaded: {name!r}')
    for name in names:
      cogs = self.extensions.pop(name)
      self.extension_files.pop(name, None)
      await self.remove_cogs(*[cog for cog in cogs if cog in self.cogs])
      if teardown := getattr(sys.modules.pop(name, None), TEARDOWN, None):
        await teardown(self)

  async def watch_extensions(self):
    while self.extension_files:
      await asyncio.sleep(RELOAD_INTERVAL)
      for name, (path, mtime) in list(self.extension_files.items()):
        if name not in self.extension_files:
          continue
        try:
          current = path.stat().st_mtime
        except OSError:
          continue
        if current == mtime:
          continue
        log.warning(f'detected change in extension {name!r}, reloading...')
        try:
          if name in self.extensions:
            await self.unload_extensions(name)
          await self.import_extensions(name)
          log.warning(f'extension {name!r} was reloaded!')
        except Exception:
          log.exception(f'failed to reload extension {name!r}')
          self.extension_files[name] = (path, current)
    self.reload_task = None
