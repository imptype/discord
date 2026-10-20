from .abc import MISSING, PartialModel, make_form

class PartialMessage(PartialModel):
  def __init__(self, app, message_id, channel):
    super().__init__(app, message_id)
    self.channel = channel

  async def fetch(self):
    return await self.app.model.http.message(self.id, self.channel)

  async def edit(self, content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING):
    if embed is not MISSING and embeds is not MISSING:
      raise ValueError('cannot edit both embed and embeds')
    if file is not MISSING and files is not MISSING:
      raise ValueError('cannot edit both file and files')

    body = {}
    if content is not MISSING:
      body['content'] = content
    if embed is not MISSING:
      if embed is None:
        embeds = None
      else:
        embeds = [embed]
    if embeds is not MISSING:
      if embeds is None: # pass embed/s = None to clear embeds (sends [])
        body['embeds'] = []
      else:
        body['embeds'] = [embed.to_json() for embed in embeds]
    if file is not MISSING:
      if file is None:
        files = None
      else:
        files = [file]
    if files is not MISSING:
      if files:
        body = make_form(body, files)
      else:
        body['attachments'] = [] # pass none to clear files (sends [])

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

    # for DMs, .guild is None, and .author is User instead of Member
    user = payload['author']
    member = payload.get('member')
    if guild and member:
      self.author = app.model.member(member, user = user, guild = guild)
    else:
      self.author = app.model.user(user)