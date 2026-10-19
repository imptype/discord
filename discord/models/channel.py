from .abc import PartialModel

class PartialChannel(PartialModel):
  def __init__(self, app, channel_id, guild = None):
    super().__init__(app, channel_id)
    self.guild = guild

  async def fetch(self):
    return await self.app.model.http.channel(self.id, self.guild)

  async def send(self, content = None, *, embed = None, embeds = None):
    if embed is not None and embeds is not None:
      raise ValueError('cannot send both embed and embeds')

    body = {}
    if content is not None:
      body['content'] = content
    if embed:
      embeds = [embed]
    if embeds:
      body['embeds'] = [embed.to_json() for embed in embeds]

    data = await self.app.http.create_message(self.id, body)
    return self.app.model.message(data)

class Channel(PartialChannel):
  def __init__(self, app, payload, guild = None):
    channel_id = payload['id']
    guild_id = payload.get('guild_id')

    if guild is None and guild_id:
      guild = app.model.partial_guild(guild_id)

    super().__init__(app, channel_id, guild)
    self.data = payload
    self.name = payload.get('name') # none for DMs