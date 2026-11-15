"""
discord.py - stripped down version of our library, for Python 3.14 (This was AI assisted).
"""

import os
import sys
import json
import asyncio
import logging
import argparse
import importlib
from http import HTTPStatus
from datetime import datetime, UTC
from functools import reduce
from contextlib import asynccontextmanager
from crypto import ed25519_verify

DISCORD_EPOCH = 1420070400000
EPHEMERAL = 1 << 6
URL = 'https://discord.com/api/v10'
USER_AGENT = 'DiscordBot (https://github.com/imptype/discord, v0.3.2a1)'

log = logging.getLogger('discord')

class Response:
  def __init__(self):
    self.body = None

  async def send(self, content = None, *, ephemeral = False):
    data = {'content': content}
    if ephemeral:
      data['flags'] = EPHEMERAL
    self.body = {'type': 4, 'data': data}

class Interaction:
  def __init__(self, data):
    self.data = data
    self.id = int(data['id'])
    self.created_at = datetime.fromtimestamp(((self.id >> 22) + DISCORD_EPOCH) / 1000, tz = UTC)
    self.response = Response()

class Command:
  def __init__(self, callback, name, description):
    self.callback = callback
    self.name = name
    self.description = description or name

  def to_json(self):
    return {'name': self.name, 'type': 1, 'description': self.description}

  async def __call__(self, interaction):
    return await self.callback(interaction)

class App:
  def __init__(self, public_key, token = None, application_id = None):
    self.verify_key = bytes.fromhex(public_key)
    self.token = token
    self.application_id = application_id
    self.registry = {}
    self.lifespans = []
    self.managers = [] # entered lifespans, exited in reverse on shutdown
    self.command = self # lets @app.command.slash() work

  def run(self, host = '127.0.0.1', port = 8000): # used by the cli, not by Workers
    try:
      asyncio.run(serve(self, host, port))
    except KeyboardInterrupt:
      pass

  def slash(self, callback = None, *, name = None, description = None):
    def wrap(callback):
      command = Command(callback, name or callback.__name__, description)
      self.registry[command.name] = command
      return command
    return wrap(callback) if callback else wrap

  def lifespan(self, callback = None): # @app.lifespan syntax, an async generator with a single yield
    def wrap(callback):
      self.lifespans.append(callback)
      return callback
    return wrap(callback) if callback else wrap

  async def startup_lifespans(self):
    for callback in self.lifespans:
      manager = asynccontextmanager(callback)()
      await manager.__aenter__()
      self.managers.append(manager)

  async def shutdown_lifespans(self):
    while self.managers:
      await self.managers.pop().__aexit__(None, None, None)

  async def sync(self):
    if not self.token or not self.application_id:
      raise ValueError('token and application_id are required to sync commands')
    import aiohttp # only needed here, so the rest of the app imports without it
    headers = {'Authorization': f'Bot {self.token}', 'Content-Type': 'application/json', 'User-Agent': USER_AGENT}
    body = json.dumps([command.to_json() for command in self.registry.values()])
    async with aiohttp.ClientSession() as session:
      async with session.put(f'{URL}/applications/{self.application_id}/commands', headers = headers, data = body) as response:
        text = await response.text()
        if response.status >= 400:
          raise ValueError(f'HTTP {response.status}: {text}')
        return json.loads(text)

  def verify(self, headers, body):
    try:
      return ed25519_verify(self.verify_key, headers.get('x-signature-timestamp', '').encode() + body,
        bytes.fromhex(headers.get('x-signature-ed25519', '')))
    except ValueError:
      return False

  async def respond(self, send, status, obj):
    body = json.dumps(obj).encode()
    await send({'type': 'http.response.start', 'status': status,
      'headers': [(b'content-type', b'application/json'), (b'content-length', str(len(body)).encode())]})
    await send({'type': 'http.response.body', 'body': body})

  async def __call__(self, scope, receive, send):
    if scope['type'] == 'lifespan':
      while True:
        event = await receive()
        if event['type'] == 'lifespan.startup':
          try:
            await self.startup_lifespans()
          except Exception as e:
            await self.shutdown_lifespans()
            return await send({'type': 'lifespan.startup.failed', 'message': str(e)})
          await send({'type': 'lifespan.startup.complete'})
        elif event['type'] == 'lifespan.shutdown':
          await self.shutdown_lifespans()
          await send({'type': 'lifespan.shutdown.complete'})
          return
    if scope['type'] != 'http':
      return
    if scope['path'] != '/interactions' or scope['method'] != 'POST':
      return await self.respond(send, 404, {'error': 'not found'})

    body = b''
    while True:
      event = await receive()
      body += event.get('body', b'')
      if not event.get('more_body'):
        break

    headers = {k.decode().lower(): v.decode() for k, v in scope['headers']}
    try:
      valid = self.verify(headers, body)
    except Exception:
      valid = False
    if not valid:
      return await self.respond(send, 401, {'error': 'invalid signature'})

    payload = json.loads(body)
    if payload['type'] == 1: # PING
      return await self.respond(send, 200, {'type': 1})

    command = self.registry.get(payload['data']['name']) if payload['type'] == 2 else None
    if command is None:
      return await self.respond(send, 400, {'error': 'unknown interaction'})
    interaction = Interaction(payload)
    await command(interaction)
    if interaction.response.body is None:
      return await self.respond(send, 500, {'error': 'interaction failed'})
    await self.respond(send, 200, interaction.response.body)

async def serve(app, host, port):
  address = f'{host}:{port}'

  async def callback(reader, writer):
    try:

      # 1. Read first line: "POST /interactions HTTP/1.1" -> ['POST', '/interactions', 'HTTP/1.1']
      method, path, version = (await reader.readline()).decode().strip().split(' ', 2)

      # 2. Build header lines until empty line
      headers = [] # (name, value)
      length = 0
      while line := (await reader.readline()).strip():
        k, v = line.split(b':', 1)
        k = k.strip().lower()
        v = v.strip()
        headers.append((k, v))
        if k == b'content-length':
          length = int(v)

      # 3. Read body based on content length
      body = await reader.readexactly(length)

      scope = {'type': 'http', 'method': method, 'path': path, 'headers': headers}

      async def receive():
        return {'type': 'http.request', 'body': body}

      async def send(event):
        if event['type'] == 'http.response.start':
          status = HTTPStatus(event['status'])
          log.info(f'{address} - {method} {path} {version} {status.value} {status.phrase}')
          writer.write(b'\r\n'.join((
            f'HTTP/1.1 {status.value} {status.phrase}'.encode(),
            b'connection: close',
            *(k + b': ' + v for k, v in event['headers'])
          )) + b'\r\n\r\n')
        else:
          writer.write(event['body'])

      await app(scope, receive, send)
      await writer.drain()
    except Exception:
      log.exception('request failed')
    finally:
      writer.close()

  log.info('waiting for app startup')
  await app.startup_lifespans()
  log.info('app startup complete')
  try:
    server = await asyncio.start_server(callback, host, port)
    log.info(f'listening on {address}')
    async with server:
      await server.serve_forever()
  finally:
    log.info('shutting down')
    await app.shutdown_lifespans()
    log.info('app shutdown complete')

def main(argv = None):
  parser = argparse.ArgumentParser(prog = 'discord', description = 'A CLI to run the app locally, without Workers.')
  parser.add_argument('app', help = 'the location of the ASGI app, for example `main:app`')
  parser.add_argument('--host', default = '127.0.0.1', help = 'the host string, default is `127.0.0.1`')
  parser.add_argument('--port', type = int, default = 8000, help = 'the port number, default is `8000`')
  parser.add_argument('--log-level', default = 'info', choices = ['debug', 'info', 'warning', 'error', 'critical'],
    help = 'override log level, default is `info`')
  args = parser.parse_args(argv)

  logging.basicConfig(level = getattr(logging, args.log_level.upper()), format = '[%(asctime)s][%(levelname)s][%(name)s] %(message)s', datefmt = '%H:%M:%S')

  sys.path.insert(0, os.getcwd())
  module, attribute = args.app.split(':')
  app = reduce(getattr, attribute.split('.'), importlib.import_module(module))
  app.run(args.host, args.port)

if __name__ == '__main__':
  sys.modules['discord'] = sys.modules[__name__] # so "import discord" in main.py is this same module, not a second copy
  main()
