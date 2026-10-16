import aiohttp
from .enums import HTTPStatus

URL = 'https://discord.com/api/v10'

class HTTPClient:
  def __init__(self, token = None, application_id = None):
    self.token = token
    self.application_id = application_id
    self.session = None

  async def start(self): # TODO: don't auth every request, use api params
    headers = {'authorization': f'Bot {self.token}'} if self.token else {}
    self.session = aiohttp.ClientSession(headers = headers)
    return self.session

  async def close(self):
    if self.session:
      await self.session.close()
      self.session = None

  async def request(self, method, route, **kwargs):
    session = self.session or await self.start()
    async with session.request(method, URL + route, **kwargs) as response:
      response.raise_for_status()
      if response.status == HTTPStatus.NO_CONTENT_204:
        return None
      return await response.json()
