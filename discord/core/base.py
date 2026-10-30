from .http import HTTPClient
from .command import CommandMixin
from .factory import ModelFactory
from .component import ComponentMixin
from ..ext import CogMixin, LifespanMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin):
  def __init__(self, token = None, application_id = None, reload = False):
    registrars = {} # {object: (add, remove)}, used by cog
    CommandMixin.__init__(self, registrars)
    LifespanMixin.__init__(self, registrars, HTTPClient(token, application_id))
    ComponentMixin.__init__(self, registrars, self.loop)
    CogMixin.__init__(self, registrars, reload)
    self.model = ModelFactory(self)
    self.tasks = set() # holds running asyncio tasks

  async def sync(self):
    body = [command.to_json() for command in self.registry.values()]
    return await self.http.bulk_overwrite_global_commands(self.http.application_id, body)
