import sys
import time
import random
import asyncio
import logging
from enum import IntEnum
import orjson
import aiohttp
from ..log import format_json

log = logging.getLogger(__name__)

QUERY = '/?v=10&encoding=json'
URL = f'wss://gateway.discord.gg{QUERY}'

class CloseCode(IntEnum):
  AUTHENTICATION_FAILED = 4004
  INVALID_SHARD = 4010
  SHARDING_REQUIRED = 4011
  INVALID_API_VERSION = 4012
  INVALID_INTENTS = 4013
  DISALLOWED_INTENTS = 4014
FATAL_CODES = set(CloseCode)

class ReconnectCode(IntEnum):
  UNKNOWN_ERROR = 4000

class ResetCode(IntEnum):
  INVALID_SEQUENCE = 4007
  SESSION_TIMED_OUT = 4009
RESET_CODES = set(ResetCode)

class Opcode(IntEnum):
  DISPATCH = 0
  HEARTBEAT = 1
  IDENTIFY = 2
  RESUME = 6
  RECONNECT = 7
  INVALID_SESSION = 9
  HELLO = 10
  HEARTBEAT_ACK = 11

def format_debug(payload, redact = None):
  op = payload['op']
  try:
    name = Opcode(op).name
  except ValueError:
    name = 'UNKNOWN'
  text = f'op {int(op)} {name}'
  event = payload.get('t')
  if event:
    seq = payload.get('s')
    text += f' seq={seq} {event}'
  data = format_json(payload.get('d'), redact = redact)
  return f'{text} {data}'

class Connection:
  ws: aiohttp.ClientWebSocketResponse

  def __init__(self, http, token, intents, on_event):
    self.http = http
    self.token = token
    self.masked_token = f'REDACTED_TOKEN_{len(token)}_CHARS'
    self.intents = intents
    self.on_event = on_event
    self.sequence = None
    self.session_id = None
    self.resume_url = None
    self.heartbeat_task = None
    self.acked = True
    self.last_beat = None

  async def run(self):
    while True:
      close_code = None
      failed = False
      try:
        close_code = await self.session()
      except (TimeoutError, aiohttp.ClientError) as e:
        log.warning(f'connection error: {e!r}')
        failed = True

      log.warning(f'closed (code {close_code})')
      if close_code in FATAL_CODES:
        raise ConnectionError(f'gateway closed with fatal code {CloseCode(close_code).name}')

      if close_code in RESET_CODES:
        self.reset()

      if failed or not self.session_id:
        log.warning('reconnecting in 5s')
        await asyncio.sleep(5)
      else:
        log.warning('resuming now')

  async def session(self):
    self.acked = True
    self.last_beat = None
    url = f'{self.resume_url}{QUERY}' if self.resume_url else URL
    log.info(f'connecting to {url}')
    self.ws = await self.http.session.ws_connect(url)
    try:
      async for message in self.ws:
        if message.type == aiohttp.WSMsgType.TEXT:
          await self.handle(orjson.loads(message.data))
    finally:
      if self.heartbeat_task:
        self.heartbeat_task.cancel()
        self.heartbeat_task = None
      await self.ws.close(code = ReconnectCode.UNKNOWN_ERROR)
    return self.ws.close_code

  async def handle(self, payload):
    if log.isEnabledFor(logging.DEBUG):
      log.debug(f'receive {format_debug(payload)}')
    op = payload['op']
    if payload.get('s') is not None:
      self.sequence = payload['s']

    if op == Opcode.HELLO:
      interval = payload['d']['heartbeat_interval'] / 1000
      log.info(f'connected, heartbeat is every {interval:.1f}s')
      self.heartbeat_task = asyncio.create_task(self.heartbeat(interval))
      if self.session_id:
        await self.resume()
      else:
        await self.identify()
    elif op == Opcode.HEARTBEAT:
      log.info(f'server asked for heartbeat {self.since_beat()}')
      await self.beat()
    elif op == Opcode.HEARTBEAT_ACK:
      log.info(f'heartbeat ack {self.since_beat()}')
      self.acked = True
    elif op in (Opcode.RECONNECT, Opcode.INVALID_SESSION):
      log.warning(f'server sent {Opcode(op).name}, reconnecting')
      if op == Opcode.INVALID_SESSION and not payload['d']:
        self.reset()
      await self.ws.close(code = ReconnectCode.UNKNOWN_ERROR)
    elif op == Opcode.DISPATCH:
      event = payload['t']
      if event == 'READY':
        self.session_id = payload['d']['session_id']
        self.resume_url = payload['d']['resume_gateway_url']
      elif event == 'RESUMED':
        log.info('resumed')
      await self.on_event(event, payload['d'])

  async def heartbeat(self, interval):
    await asyncio.sleep(interval * random.random())
    while True:
      if not self.acked:
        log.warning('no heartbeat ack, connection is dead')
        await self.ws.close(code = ReconnectCode.UNKNOWN_ERROR)
        return
      self.acked = False
      await self.beat()
      await asyncio.sleep(interval)

  def since_beat(self):
    return self.last_beat and f'{time.monotonic() - self.last_beat:.1f}s' or 'N/A'

  async def beat(self):
    log.info(f'heartbeat {self.since_beat()}')
    self.last_beat = time.monotonic()
    await self.send({'op': Opcode.HEARTBEAT, 'd': self.sequence})

  async def identify(self):
    properties = {'os': sys.platform, 'browser': 'idiscord', 'device': 'idiscord'}
    shown = ' '.join(f'{key}={value}' for key, value in properties.items())
    log.info(f'identify using auth token with properties {shown}')
    log.info(str(self.intents))
    await self.send({'op': Opcode.IDENTIFY, 'd': {
      'token': self.token,
      'intents': self.intents,
      'properties': properties
    }})

  async def resume(self):
    log.info(f'resume session {self.session_id} from seq={self.sequence} using {self.resume_url}')
    await self.send({'op': Opcode.RESUME, 'd': {
      'token': self.token,
      'session_id': self.session_id,
      'seq': self.sequence
    }})

  def reset(self):
    self.session_id = None
    self.resume_url = None
    self.sequence = None

  async def send(self, payload):
    data = orjson.dumps(payload).decode()
    if log.isEnabledFor(logging.DEBUG):
      log.debug(f'send {format_debug(payload, redact = {self.token: self.masked_token})}')
    await self.ws.send_str(data)
