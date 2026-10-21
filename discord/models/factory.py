from functools import partial
from .context import Context
from .user import PartialUser, User
from .guild import Guild, PartialGuild
from .member import Member, PartialMember
from .channel import Channel, PartialChannel
from .message import Message, PartialMessage

class ModelHTTP:
  def __init__(self, app, model):
    self.app = app
    self.model = model

  async def guild(self, guild_id):
    return self.model.guild(await self.app.http.get_guild(guild_id))

  async def channel(self, channel_id, guild = None):
    return self.model.channel(await self.app.http.get_channel(channel_id), guild)

  async def user(self, user_id):
    return self.model.user(await self.app.http.get_user(user_id))

  async def member(self, user_id, guild):
    data = await self.app.http.get_guild_member(guild.id, user_id)
    return self.model.member(data, guild = guild)

  async def message(self, message_id, channel):
    data = await self.app.http.get_message(channel.id, message_id)
    return self.model.message(data, channel = channel, guild = channel.guild)

class ModelFactory:
  def __init__(self, app):
    self.http = ModelHTTP(app, self)
    self.partial_guild = partial(PartialGuild, app)
    self.partial_channel = partial(PartialChannel, app)
    self.partial_user = partial(PartialUser, app)
    self.partial_member = partial(PartialMember, app)
    self.partial_message = partial(PartialMessage, app)
    self.guild = partial(Guild, app)
    self.channel = partial(Channel, app)
    self.user = partial(User, app)
    self.member = partial(Member, app)
    self.message = partial(Message, app)
    self.context = partial(Context, app)
