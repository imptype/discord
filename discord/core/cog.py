import os
import sys
import copy
import types
import asyncio
import logging
import importlib
from typing import TYPE_CHECKING
from .command import BaseCommand, Handler

log = logging.getLogger(__name__)

SETUP = 'setup'
TEARDOWN = 'teardown'
RELOAD_INTERVAL = 1

class Cog:
  def __init__(self, app):
    self.app = app

  async def cog_load(self): ...
  async def cog_unload(self): ...

class CogMixin:
  def __init__(self, reload = False):
    super().__init__()
    self.reload = reload
    self.cogs = {} # loaded cogs {Cog: instance}
    self.cog_handlers = {} # {Cog: [copy.copy of handlers]}
    self.extra_registrars = {} # discord.Bot sets this
    self.extensions = {} # loaded extensions {name: [Cog]}
    self.extension_files = {} # {name: (path, mtime)} used when reload is on
    self.reload_task = None

  if TYPE_CHECKING:
    def add_commands(self, *commands): ... # implemented by CommandMixin
    def remove_commands(self, *commands): ...

  def registrars(self):
    return {BaseCommand: (self.add_commands, self.remove_commands)} | self.extra_registrars

  async def add_cogs(self, *cogs):
    registrars = self.registrars()
    for cog in cogs:
      if not (isinstance(cog, type) and issubclass(cog, Cog)):
        raise ValueError(f'not a cog: {cog!r}')
      if cog in self.cogs:
        raise ValueError(f'cog already loaded: {cog.__name__}')
    instances = []
    for cog in cogs:
      instance = cog(self)
      await instance.cog_load()
      found = {
        name: value
        for cls in reversed(cog.__mro__)
        for name, value in vars(cls).items()
        if isinstance(value, Handler)
      }
      handlers = []
      for name, value in found.items():
        handler = copy.copy(value)
        handler.func = types.MethodType(value.func, instance)
        if isinstance(handler, tuple(registrars)):
          handlers.append(handler)
        else:
          log.warning(f'{cog.__name__}.{name}() was not loaded: {type(handler).__name__} is not supported by {type(self).__name__}')
      for kind, (add, _) in registrars.items():
        add(*[handler for handler in handlers if isinstance(handler, kind)])
      self.cogs[cog] = instance
      self.cog_handlers[cog] = handlers
      instances.append(instance)
    return instances

  async def remove_cogs(self, *cogs):
    registrars = self.registrars()
    for cog in cogs:
      if cog not in self.cogs:
        raise ValueError(f'cog not loaded: {cog!r}')
    for cog in cogs:
      instance = self.cogs.pop(cog)
      handlers = self.cog_handlers.pop(cog)
      for kind, (_, remove) in registrars.items():
        remove(*[handler for handler in handlers if isinstance(handler, kind)])
      await instance.cog_unload()

  async def load_extensions(self, *names):
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
        self.extension_files[name] = (path, os.stat(path).st_mtime)
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
          current = os.stat(path).st_mtime
        except OSError:
          continue
        if current == mtime:
          continue
        log.warning(f'detected change in extension {name!r}, reloading...')
        try:
          if name in self.extensions:
            await self.unload_extensions(name)
          await self.load_extensions(name)
          log.warning(f'extension {name!r} was reloaded!')
        except Exception:
          log.exception(f'failed to reload extension {name!r}')
          self.extension_files[name] = (path, current)
    self.reload_task = None
