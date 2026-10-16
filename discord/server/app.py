import orjson
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from ..base import AppBase
from .handler import handler
from ..enums import HTTPStatus
from ..lifespan import Lifespan

class App(AppBase):
  def __init__(self, public_key, token = None, application_id = None):
    super().__init__(token, application_id)
    self.verify_key = VerifyKey(bytes.fromhex(public_key))
    self.lifespan = Lifespan(self.http)

  async def run_lifespan(self, receive, send):
    while True:
      event = await receive()
      if event['type'] == 'lifespan.startup':
        try:
          await self.lifespan.startup()
        except Exception as e: # noqa: BLE001
          await self.lifespan.shutdown()
          return await send({'type': 'lifespan.startup.failed', 'message': str(e)})
        await send({'type': 'lifespan.startup.complete'})
      elif event['type'] == 'lifespan.shutdown':
        await self.lifespan.shutdown()
        await send({'type': 'lifespan.shutdown.complete'})
        return

  async def __call__(self, scope, receive, send):
    if scope['type'] == 'lifespan':
      return await self.run_lifespan(receive, send)
    if scope['type'] != 'http':
      return
    if scope['path'] != '/interactions' or scope['method'] != 'POST':
      return await self.json(send, HTTPStatus.NOT_FOUND_404, {'error': 'not found'})

    body = b''
    while True:
      event = await receive()
      body += event.get('body', b'')
      if not event.get('more_body'):
        break

    headers = {k.decode().lower(): v.decode() for k, v in scope['headers']}
    try:
      self.verify_key.verify(headers.get('x-signature-timestamp', '').encode() + body,
        bytes.fromhex(headers.get('x-signature-ed25519', '')))
    except (BadSignatureError, ValueError):
      return await self.json(send, HTTPStatus.UNAUTHORIZED_401, {'error': 'invalid signature'})

    payload = orjson.loads(body)
    await self.json(send, HTTPStatus.OK_200, await handler(self, payload))

  async def json(self, send, status, obj):
    await send({'type': 'http.response.start', 'status': status,
      'headers': [(b'content-type', b'application/json')]})
    await send({'type': 'http.response.body', 'body': orjson.dumps(obj)})
