from .cog import CogMixin
from .command import CommandMixin
from .factory import ModelFactory
from .lifespan import LifespanMixin
from .component import ComponentMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin):
  def __init__(self, token = None, application_id = None, reload = False):
    registrars = {} # {object: (add, remove)}, used by cog
    CommandMixin.__init__(self, registrars)
    LifespanMixin.__init__(self, registrars, token, application_id)
    ComponentMixin.__init__(self, registrars, self.loop)
    CogMixin.__init__(self, registrars, reload)
    self.model = ModelFactory(self)
    self.tasks = set() # holds running asyncio tasks

  async def sync(self):
    body = [command.to_json() for command in self.registry.values()]
    return await self.http.bulk_overwrite_global_commands(self.http.application_id, body)
