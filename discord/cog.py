import sys
import copy
import types
import logging
import importlib
from .command import BaseCommand, Handler

log = logging.getLogger(__name__)

SETUP = 'setup'
TEARDOWN = 'teardown'

class Cog:
  def __init__(self, app):
    self.app = app

  async def cog_load(self): ...
  async def cog_unload(self): ...

class CogMixin:
  def __init__(self):
    self.cogs = {} # loaded cogs {Cog: instance}
    self.cog_handlers = {} # {Cog: [copy.copy of handlers]}
    self.extra_registrars = {} # discord.Bot sets this
    self.extensions = {} # loaded extensions {name: [Cog]}

  def add_commands(self, *commands): ...
  def remove_commands(self, *commands): ...

  def registrars(self):
    return {BaseCommand: (self.add_commands, self.remove_commands), **self.extra_registrars}

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
      found = {}
      for cls in reversed(cog.__mro__):
        for name, value in vars(cls).items():
          if isinstance(value, Handler):
            found[name] = value
      handlers = []
      for name, value in found.items():
        handler = copy.copy(value)
        handler.func = types.MethodType(value.func, instance)
        if any(isinstance(handler, kind) for kind in registrars):
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
        raise ValueError(f'extension already loaded: {name}')
    for name in names:
      module = importlib.import_module(name)
      setup = getattr(module, SETUP, None)
      if setup is None:
        sys.modules.pop(name, None)
        raise ValueError(f'extension {name} has no {SETUP}(app)')
      before = set(self.cogs)
      try:
        await setup(self)
      except Exception:
        await self.remove_cogs(*[cog for cog in self.cogs if cog not in before])
        sys.modules.pop(name, None)
        raise
      self.extensions[name] = [cog for cog in self.cogs if cog not in before]

  async def unload_extensions(self, *names):
    for name in names:
      if name not in self.extensions:
        raise ValueError(f'extension not loaded: {name}')
    for name in names:
      cogs = self.extensions.pop(name)
      await self.remove_cogs(*[cog for cog in cogs if cog in self.cogs])
      teardown = getattr(sys.modules.pop(name, None), TEARDOWN, None)
      if teardown:
        await teardown(self)
