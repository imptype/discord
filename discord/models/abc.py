from datetime import datetime, UTC

DISCORD_EPOCH = 1420070400000

def snowflake_time(id):
  return datetime.fromtimestamp(((int(id) >> 22) + DISCORD_EPOCH) / 1000, tz = UTC)

class Snowflake:
  def __init__(self, id):
    self.id = int(id)
    self.created_at = snowflake_time(self.id)

class PartialModel(Snowflake):
  def __init__(self, app, id):
    super().__init__(id)
    self.app = app

  async def fetch(self):
    pass
