from ..abc import PartialModel

class PartialGuild(PartialModel):
  async def fetch(self):
    return await self.app.model.http.guild(self.id)

class Guild(PartialGuild):
  def __init__(self, app, payload):
    guild_id = payload['id']

    super().__init__(app, guild_id)
    self.data = payload
    self.name = payload.get('name')