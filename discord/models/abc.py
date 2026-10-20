from typing import Any
from datetime import datetime, UTC
from functools import cached_property
import orjson
import aiohttp

DISCORD_EPOCH = 1420070400000
MISSING: Any = object()

def snowflake_time(id):
  return datetime.fromtimestamp(((int(id) >> 22) + DISCORD_EPOCH) / 1000, tz = UTC)

def make_form(body, files):
  attachments = []
  for index, file in enumerate(files):
    attachment = {'id': index, 'filename': file.filename}
    if file.description:
      attachment['description'] = file.description
    attachments.append(attachment)

  payload = {**body, 'attachments': attachments}
  form = aiohttp.FormData()
  form.add_field('payload_json', orjson.dumps(payload).decode(), content_type = 'application/json')
  for index, file in enumerate(files):
    form.add_field(f'files[{index}]', file.data, filename = file.filename, content_type = file.content_type)
  return form

class Snowflake:
  def __init__(self, id):
    self.id = int(id)

  @cached_property
  def created_at(self):
    return snowflake_time(self.id)

class PartialModel(Snowflake):
  def __init__(self, app, id):
    super().__init__(id)
    self.app = app

  async def fetch(self): ...
