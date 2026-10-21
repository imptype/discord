from datetime import datetime, UTC
from functools import cached_property

DISCORD_EPOCH = 1420070400000

def snowflake_time(id):
  return datetime.fromtimestamp(((int(id) >> 22) + DISCORD_EPOCH) / 1000, tz = UTC)

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
