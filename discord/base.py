from typing import cast
from . import command
from .http import HTTPClient
from .proxy import CommandProxy
from .interaction import Interaction

class AppBase:
  def __init__(self, token = None, application_id = None):
    self.http = HTTPClient(token, application_id)
    self.command = cast(command, CommandProxy(self, command))
    self.registry = {}

  def add_command(self, command):
    self.registry[command.name] = command
    return command

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
