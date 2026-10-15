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

  async def run(self, receive, send):
    while True:
      event = await receive()
      if event['type'] == 'lifespan.startup':
        try:
          await self.startup()
        except Exception as e: # noqa: BLE001
          await self.shutdown()
          return await send({'type': 'lifespan.startup.failed', 'message': str(e)})
        await send({'type': 'lifespan.startup.complete'})
      elif event['type'] == 'lifespan.shutdown':
        await self.shutdown()
        await send({'type': 'lifespan.shutdown.complete'})
        return
