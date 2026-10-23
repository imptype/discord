from .abc import PartialModel
from .params import send_params

class PartialChannel(PartialModel):
  def __init__(self, app, channel_id, guild = None):
    super().__init__(app, channel_id)
    self.guild = guild

  async def fetch(self):
    return await self.app.model.http.channel(self.id, self.guild)

  async def send(self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None):
    body = send_params(content, embed = embed, embeds = embeds, file = file,
      files = files, view = view, components = components, flags = flags)
    if view is not None:
      self.app.add_views(view)
    if components:
      self.app.add_components(*components)
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
