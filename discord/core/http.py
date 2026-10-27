import asyncio
import urllib.error
import urllib.parse
import urllib.request
from typing import Any
import orjson
import aiohttp
from .api import Route, API
from ..models import Payload

URL = 'https://discord.com/api/v10'
USER_AGENT = 'DiscordBot (https://github.com/imptype/discord, v0.1.1)'

class HTTPClient(API):
  def __init__(self, token = None, application_id = None, use_sync = False):
    super().__init__()
    self.token = token
    self.application_id = application_id
    self.use_sync = use_sync # init for SyncWebhook
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
      headers['Authorization'] = authorize # supports 'Bearer <token>' string
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

    if self.use_sync: # used by SyncWebhook
      if json is not None:
        headers['Content-Type'] = 'application/json'
        data = orjson.dumps(json)
      url = f'{URL}{route.path}'
      if params:
        url += f'?{urllib.parse.urlencode(params)}'
      request = urllib.request.Request(url, data = data, headers = headers, method = route.method)
      try:
        with urllib.request.urlopen(request) as response:
          status = response.status
          content = response.read()
      except urllib.error.HTTPError as error: # urllib raises on 4xx/5xx unlike aiohttp
        status = error.code
        content = error.read()
    else:
      response = await self.session.request(
        route.method,
        f'{URL}{route.path}',
        params = params,
        headers = headers,
        data = data,
        json = json
      )
      status = response.status
      content = await response.read()

    if status >= 400:
      raise ValueError(f'HTTP {status}: {content.decode()}')
    if status == 204:
      return None
    return orjson.loads(content)
