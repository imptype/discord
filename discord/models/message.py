from .. import MISSING
from .abc import PartialModel
from .enums import MessageFlags
from .params import edit_params

class PartialMessage(PartialModel):
  def __init__(self, app, message_id, channel):
    super().__init__(app, message_id)
    self.channel = channel

  async def fetch(self):
    return await self.app.model.http.message(self.id, self.channel)

  async def edit(self, content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING, view = MISSING, components = MISSING, flags = MISSING):
    if embed is not MISSING and embeds is not MISSING:
      raise ValueError('cannot edit both embed and embeds')
    if file is not MISSING and files is not MISSING:
      raise ValueError('cannot edit both file and files')
    if view is not MISSING and components is not MISSING:
      raise ValueError('cannot edit both view and components')

    body = edit_params(content, embed = embed, embeds = embeds, file = file,
      files = files, view = view, components = components, flags = flags)
    if view not in (MISSING, None):
      self.app.add_views(view)
    if components is not MISSING and components:
      self.app.add_components(*components)
    data = await self.app.http.edit_message(self.channel.id, self.id, body)
    return self.app.model.message(data, channel = self.channel, guild = self.channel.guild)

class Message(PartialMessage):
  def __init__(self, app, payload, *, channel = None, guild = None):
    message_id = payload['id']
    channel_id = payload['channel_id']
    guild_id = payload.get('guild_id')

    if guild is None and guild_id:
      guild = app.model.partial_guild(guild_id)

    if channel is None:
      channel = app.model.partial_channel(channel_id, guild)

    super().__init__(app, message_id, channel)
    self.data = payload
    self.guild = guild
    self.content = payload.get('content', '')
    self.flags = MessageFlags(payload.get('flags', 0))

    # for DMs, .guild is None, and .author is User instead of Member
    user = payload['author']
    member = payload.get('member')
    if guild and member:
      self.author = app.model.member(member, user = user, guild = guild)
    else:
      self.author = app.model.user(user)
