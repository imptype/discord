import asyncio
import logging
from http import HTTPStatus

log = logging.getLogger(__name__)

async def serve(app, host, port):
  async def callback(reader, writer):
    try:

      # 1. Read first line: "POST /interactions HTTP/1.1" -> ['POST', '/interactions', 'HTTP/1.1']
      method, path, version = (await reader.readline()).decode().strip().split(' ', 2)

      # 2. Build header lines until empty line.
      headers = [] # (name, value)
      length = 0
      while line := (await reader.readline()).strip():
        k, v = line.split(b': ', 1) # [b'Content-Type', b'application/json']
        headers.append((k := k.lower(), v))
        if k == b'content-length':
          length = int(v)

      # 3. Read body based on content length.
      body = await reader.readexactly(length)

      scope = {
        'type': 'http',
        'method': method,
        'path': path,
        'headers': headers
      }

      async def receive():
        return {
          'type': 'http.request',
          'body': body
        }

      async def send(event):
        if event['type'] == 'http.response.start':
          status = HTTPStatus(event['status']) # .value = 200, .phrase = OK
          log.info(f'{address} - {method} {path} {version} {status.value} {status.phrase}')
          writer.write(b'\n'.join((
            f'HTTP/1.1 {status.value} {status.phrase}'.encode(),
            b'connection: close',
            *(k + b': ' + v for k, v in event['headers'])
          )) + b'\n\n')
        else:
          writer.write(event['body'])

      await app(scope, receive, send)
    finally:
      writer.close()

  log.info('waiting for app startup')
  await app.startup_lifespans()
  log.info('app startup complete')
  try:
    server = await asyncio.start_server(callback, host, port)
    address = f'{host}:{port}'
    log.info(f'listening on {address}')
    async with server:
      await server.serve_forever()
  finally:
    log.info('shutting down')
    await app.shutdown_lifespans()
    log.info('app shutdown complete')
