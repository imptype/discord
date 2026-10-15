import aiohttp

class HTTPClient:
  base = 'https://discord.com/api/v10'

  def __init__(self, token = None, application_id = None):
    self.token = token
    self.application_id = application_id
    self.session = None

  async def start(self):
    headers = {'authorization': f'Bot {self.token}'} if self.token else {}
    self.session = aiohttp.ClientSession(headers = headers)
    return self.session

  async def close(self):
    if self.session:
      await self.session.close()
      self.session = None

  async def request(self, method, route, **kwargs):
    session = self.session or await self.start()
    async with session.request(method, self.base + route, **kwargs) as response:
      response.raise_for_status()
      return await response.json()
