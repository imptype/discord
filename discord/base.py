from typing import cast
from .http import HTTPClient
from .proxy import CommandProxy
from .interaction import Interaction
from .command import CommandNamespace, InteractionCommand, command

class AppBase:
  def __init__(self, token = None, application_id = None):
    self.http = HTTPClient(token, application_id)
    self.registry = {}
    self.set_proxy()

  def set_proxy(self):
    self.command = cast(CommandNamespace, CommandProxy(self, command))

  def add_commands(self, *commands):
    for command in commands: # noqa: F402
      if not isinstance(command, InteractionCommand):
        raise ValueError(f'not an interaction command: {command!r}')
    for command in commands:
      self.registry[command.name] = command

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
