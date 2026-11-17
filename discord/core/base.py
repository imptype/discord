from ..ext import CogMixin, Lifespan, LifespanMixin, SchedulerMixin, SignalMixin, TaskMixin
from .http import HTTPClient
from .command import CommandMixin
from .factory import ModelFactory
from .component import ComponentMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin, SignalMixin, TaskMixin, SchedulerMixin):
  def __init__(self, token = None, application_id = None, reload = False):
    super().__init__(http = HTTPClient(token, application_id), reload = reload)
    self.lifespan_handlers[Lifespan(self.task_lifespan)] = None
    self.model = ModelFactory(self)

  async def sync(self):
    body = [command.to_json() for command in self.registry.values()]
    return await self.http.bulk_overwrite_global_commands(self.http.application_id, body)
