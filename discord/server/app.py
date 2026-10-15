from typing import cast
import orjson
from nacl.exceptions import BadSignatureError
from nacl.signing import VerifyKey
from .. import command
from ..http import HTTPClient
from .enums import Status
from .handler import handler
from .lifespan import Lifespan
from .proxy import CommandProxy

class App:
  def __init__(self, public_key, token = None, application_id = None):
    self.verify_key = VerifyKey(bytes.fromhex(public_key))
    self.http = HTTPClient(token, application_id)
    self.command = cast(command, CommandProxy(self, command))
    self.registry = {}
    self.lifespan = Lifespan(self.http)

  def add_command(self, command):
    self.registry[command.name] = command
    return command

  async def sync(self):
    body = [c.to_json() for c in self.registry.values()]
    return await self.http.request('PUT', f'/applications/{self.http.application_id}/commands', json = body)

  async def __call__(self, scope, receive, send):
    if scope['type'] == 'lifespan':
      return await self.lifespan.run(receive, send)
    if scope['type'] != 'http':
      return
    if scope['path'] != '/interactions' or scope['method'] != 'POST':
      return await self.json(send, Status.NOT_FOUND_404, {'error': 'not found'})

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
      return await self.json(send, Status.UNAUTHORIZED_401, {'error': 'invalid signature'})

    payload = orjson.loads(body)
    await self.json(send, Status.OK_200, await handler(self, payload))

  async def json(self, send, status, obj):
    await send({'type': 'http.response.start', 'status': status,
      'headers': [(b'content-type', b'application/json')]})
    await send({'type': 'http.response.body', 'body': orjson.dumps(obj)})
