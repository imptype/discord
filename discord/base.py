import copy
import types
import logging
from typing import cast
from .cog import Cog
from .http import HTTPClient
from .proxy import CommandProxy
from .interaction import Interaction
from .command import BaseCommand, CommandNamespace, Handler, InteractionCommand, command

log = logging.getLogger(__name__)

class AppBase:
  def __init__(self, token = None, application_id = None):
    self.http = HTTPClient(token, application_id)
    self.registry = {}
    self.extra_handlers = {}
    self.set_proxy()

  def set_proxy(self):
    self.command = cast(CommandNamespace, CommandProxy(self, command))

  def add_commands(self, *commands):
    for command in commands: # noqa: F402
      if not isinstance(command, InteractionCommand):
        raise ValueError(f'not an interaction command: {command!r}')
    for command in commands:
      self.registry[command.name] = command

  async def add_cogs(self, *cogs):
    registrars = {BaseCommand: self.add_commands, **self.extra_handlers}
    for cog in cogs:
      if not (isinstance(cog, type) and issubclass(cog, Cog)):
        raise ValueError(f'not a cog: {cog!r}')
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
      for kind, register in registrars.items():
        register(*[handler for handler in handlers if isinstance(handler, kind)])
      instances.append(instance)
    return instances

  async def sync(self):
    body = [c.to_json() for c in self.registry.values()]
    return await self.http.request('PUT', f'/applications/{self.http.application_id}/commands', json = body)

  async def run_command(self, payload, is_from_http):
    name = payload['data']['name']
    command = self.registry.get(name)

    if command is None:
      raise ValueError(f'unknown command: {name}')

    interaction = Interaction(payload, self, is_from_http)
    await command(interaction)
    return interaction
