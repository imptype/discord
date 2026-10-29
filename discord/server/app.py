import orjson
from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
from .handler import handler
from ..models.params import Payload
from ..core import AppBase, HTTPStatus

class App(AppBase):
  def __init__(self, public_key, token = None, application_id = None, reload = False):
    super().__init__(token, application_id, reload)
    self.verify_key = VerifyKey(bytes.fromhex(public_key))
    self.pending_interactions = {} # {interaction id: (response_future, response_ack_future)}

  async def run_lifespan(self, receive, send):
    while True:
      event = await receive()
      if event['type'] == 'lifespan.startup':
        try:
          await self.startup_lifespans()
        except Exception as e: # noqa: BLE001
          await self.shutdown_lifespans()
          return await send({'type': 'lifespan.startup.failed', 'message': str(e)})
        await send({'type': 'lifespan.startup.complete'})
      elif event['type'] == 'lifespan.shutdown':
        await self.shutdown_lifespans()
        await send({'type': 'lifespan.shutdown.complete'})
        return

  async def respond(self, send, status, obj = None): # obj is a Payload (json or multipart), or a plain dict or None
    if isinstance(obj, Payload):
      content_type, body = obj.encode()
    else:
      content_type = 'application/json'
      body = orjson.dumps(obj) if obj else b''
    await send({'type': 'http.response.start', 'status': status,
      'headers': [
        (b'content-type', content_type.encode()),
        (b'content-length', str(len(body)).encode())
      ]})
    await send({'type': 'http.response.body', 'body': body})

  async def __call__(self, scope, receive, send):
    if scope['type'] == 'lifespan':
      return await self.run_lifespan(receive, send)
    if scope['type'] != 'http':
      return
    if scope['path'] != '/interactions' or scope['method'] != 'POST':
      return await self.respond(send, HTTPStatus.NOT_FOUND_404, {'error': 'not found'})

    body = b''
    while True: # TODO: add security
      event = await receive()
      body += event.get('body', b'')
      if not event.get('more_body'):
        break

    headers = {k.decode().lower(): v.decode() for k, v in scope['headers']}
    try:
      self.verify_key.verify(headers.get('x-signature-timestamp', '').encode() + body,
        bytes.fromhex(headers.get('x-signature-ed25519', '')))
    except BadSignatureError, ValueError:
      return await self.respond(send, HTTPStatus.UNAUTHORIZED_401, {'error': 'invalid signature'})

    payload = orjson.loads(body)
    response_ack_future = self.loop.create_future()
    try:
      status, body = await handler(self, payload, response_ack_future)
      await self.respond(send, status, body)
    finally:
      if not response_ack_future.done():
        response_ack_future.set_result(None)
