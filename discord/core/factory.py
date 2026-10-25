from functools import partial
from .webhook import FollowupWebhook, PartialWebhook, Webhook
from ..models import (
  Channel, Context, Guild, Member, Message, PartialChannel, PartialGuild,
  PartialMember, PartialMessage, PartialUser, User
)

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

  async def webhook(self, webhook_id, token = None):
    if token:
      data = await self.app.http.get_webhook_by_token(webhook_id, token)
    else:
      data = await self.app.http.get_webhook(webhook_id)
    return self.model.webhook(data)

class ModelFactory:
  def __init__(self, app):
    self.http = ModelHTTP(app, self)
    self.partial_guild = partial(PartialGuild, app)
    self.partial_channel = partial(PartialChannel, app)
    self.partial_user = partial(PartialUser, app)
    self.partial_member = partial(PartialMember, app)
    self.partial_message = partial(PartialMessage, app)
    self.partial_webhook = partial(PartialWebhook, app = app)
    self.followup_webhook = partial(FollowupWebhook, app)
    self.guild = partial(Guild, app)
    self.channel = partial(Channel, app)
    self.user = partial(User, app)
    self.member = partial(Member, app)
    self.message = partial(Message, app)
    self.webhook = partial(Webhook, app)
    self.context = partial(Context, app)
