import copy
import types
import logging
from .command import BaseCommand, Handler

log = logging.getLogger(__name__)

class Cog:
  def __init__(self, app):
    self.app = app

  async def cog_load(self):
    pass

  async def cog_unload(self):
    pass

class CogMixin:
  def __init__(self):
    self.cogs = {} # loaded cogs {Cog: instance}
    self.cog_handlers = {} # {Cog: [copy.copy of handlers]}
    self.extra_registrars = {} # discord.Bot sets this

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
