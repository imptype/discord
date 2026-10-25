import asyncio
from typing import Any
import orjson
import aiohttp
from .api import Route, API
from ..models.params import Payload

URL = 'https://discord.com/api/v10'
USER_AGENT = 'DiscordBot (https://github.com/imptype/discord, v0.1.1)'

class HTTPClient(API):
  def __init__(self, token = None, application_id = None):
    super().__init__()
    self.token = token
    self.application_id = application_id
    self.cleanup_task = None

  @classmethod
  def implicit(cls): # init without context manager
    self = cls()
    self.session = aiohttp.ClientSession(json_serialize_bytes = orjson.dumps)
    async def cleanup():
      try:
        await asyncio.get_running_loop().create_future()
      finally:
        await self.session.close()
    self.cleanup_task = asyncio.create_task(cleanup())
    return self

  async def __aenter__(self):
    self.session = aiohttp.ClientSession(json_serialize_bytes = orjson.dumps)
    return self

  async def __aexit__(self, *exc_info):
    await self.session.close()

  async def request(
    self,
    route: Route,
    *,
    body: Any = None,
    authorize: bool | str = False,
    reason: str | None = None,
    **params: Any
  ):
    headers = {'User-Agent': USER_AGENT}
    if isinstance(authorize, str):
      headers['Authorization'] = authorize # used as is, like 'Bearer <token>'
    elif authorize:
      headers['Authorization'] = f'Bot {self.token}'
    if reason:
      headers['X-Audit-Log-Reason'] = reason
    data = None
    json = None
    if isinstance(body, Payload):
      headers['Content-Type'], data = body.encode()
    else:
      json = body

    # aiohttp doesn't convert booleans in query string
    params = {
      k: str(v).lower() if isinstance(v, bool) else v
      for k, v in params.items() if v is not None
    }

    response = await self.session.request(
      route.method,
      f'{URL}{route.path}',
      params = params,
      headers = headers,
      data = data,
      json = json
    )
    if response.status >= 400:
      text = await response.text()
      raise ValueError(f'HTTP {response.status}: {text}')
    if response.status == 204:
      return None
    return await response.json(loads = orjson.loads)
