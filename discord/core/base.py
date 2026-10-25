from .http import HTTPClient
from .factory import ModelFactory
from .lifespan import LifespanMixin
from .component import ComponentMixin

class AppBase(LifespanMixin, ComponentMixin):
  def __init__(self, token = None, application_id = None, reload = False):
    super().__init__(reload)
    self.http = HTTPClient(token, application_id)
    self.model = ModelFactory(self)

  async def sync(self):
    body = [command.to_json() for command in self.registry.values()]
    return await self.http.bulk_overwrite_global_commands(self.http.application_id, body)
