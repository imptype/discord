from datetime import datetime
from .. import MISSING
from .user import User
from .member import Member
from ..abc import PartialModel
from .enums import MessageFlags
from .guild import PartialGuild
from .params import edit_params
from .channel import PartialChannel

class PartialMessage(PartialModel):
  def __init__(self, app, message_id, channel):
    super().__init__(app, message_id)
    self.channel = channel

  async def fetch(self):
    return await self.app.model.http.message(self.id, self.channel)

  async def edit(self, content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING, view = MISSING, components = MISSING, flags = MISSING):
    body = edit_params(content, app = self.app, embed = embed, embeds = embeds, file = file,
      files = files, view = view, components = components, flags = flags)
    data = await self.app.http.edit_message(self.channel.id, self.id, body)
    return self.app.model.message(data, channel = self.channel, guild = self.channel.guild)

class Message(PartialMessage): # app can be done for partial webhook messages
  def __init__(self, app, payload, *, channel = None, guild = None):
    message_id = payload['id']
    channel_id = payload['channel_id']
    guild_id = payload.get('guild_id')

    if not guild and guild_id:
      guild = PartialGuild(app, guild_id)

    if not channel:
      channel = PartialChannel(app, channel_id, guild)

    super().__init__(app, message_id, channel)
    self.data = payload
    self.guild = guild
    self.content = payload.get('content', '')
    self.flags = MessageFlags(payload.get('flags', 0))
    self.edited_at = None

    if edited_timestamp := payload.get('edited_timestamp'):
      self.edited_at = datetime.fromisoformat(edited_timestamp)

    # for DMs, .guild is None, and .author is User instead of Member
    user = payload['author']
    member = payload.get('member')
    if guild and member:
      self.author = Member(app, member, user = user, guild = guild)
    else:
      self.author = User(app, user)
