from .factory import ModelFactory
from .component import ComponentMixin

class AppBase(ComponentMixin):
  def __init__(self, token = None, application_id = None, reload = False):
    super().__init__(token, application_id, reload)
    self.model = ModelFactory(self)
    self.tasks = set() # holds running asyncio tasks

  async def sync(self):
    body = [command.to_json() for command in self.registry.values()]
    return await self.http.bulk_overwrite_global_commands(self.http.application_id, body)
