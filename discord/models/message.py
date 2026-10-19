from .abc import PartialModel

class PartialMessage(PartialModel):
  def __init__(self, app, message_id, channel):
    super().__init__(app, message_id)
    self.channel = channel

  async def fetch(self):
    return await self.app.model.http.message(self.id, self.channel)

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

    # for DMs, .guild is None, and .author is User instead of Member
    user = payload['author']
    member = payload.get('member')
    if guild and member:
      self.author = app.model.member(member, user = user, guild = guild)
    else:
      self.author = app.model.user(user)
