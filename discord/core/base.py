from contextlib import AsyncExitStack, asynccontextmanager
from .cog import CogMixin
from .http import HTTPClient
from .command import CommandMixin
from .factory import ModelFactory
from .component import ComponentMixin

class Lifespan:
  def __init__(self, http):
    self.http = http
    self.callback = None
    self.stack = AsyncExitStack()

  def __call__(self, callback):
    self.callback = asynccontextmanager(callback)
    return callback

  async def startup(self):
    await self.stack.enter_async_context(self.http)
    if self.callback:
      await self.stack.enter_async_context(self.callback())

  async def shutdown(self):
    await self.stack.aclose()

class AppBase(CogMixin, CommandMixin, ComponentMixin):
  def __init__(self, token = None, application_id = None, reload = False):
    super().__init__(reload)
    self.http = HTTPClient(token, application_id)
    self.model = ModelFactory(self)
    self.lifespan = Lifespan(self.http)

  async def sync(self):
    body = [command.to_json() for command in self.registry.values()]
    return await self.http.bulk_overwrite_global_commands(self.http.application_id, body)
