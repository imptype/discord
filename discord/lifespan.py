from contextlib import AsyncExitStack, asynccontextmanager

class Lifespan:
  def __init__(self, http):
    self.http = http
    self.callback = None
    self.stack = AsyncExitStack()

  def __call__(self, callback):
    self.callback = asynccontextmanager(callback)
    return callback

  async def startup(self):
    await self.http.start()
    self.stack.push_async_callback(self.http.close)
    if self.callback:
      await self.stack.enter_async_context(self.callback())

  async def shutdown(self):
    await self.stack.aclose()
