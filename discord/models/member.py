from datetime import datetime
from .user import PartialUser

class PartialMember(PartialUser):
  def __init__(self, app, user_id, guild):
    super().__init__(app, user_id)
    self.guild = guild

  async def fetch(self):
    return await self.app.model.http.member(self.id, self.guild)

class Member(PartialMember):
  def __init__(self, app, payload, *, user = None, guild = None):
    if user is None:
      user = payload['user']

    user_id = user['id']
    guild_id = payload.get('guild_id')

    if guild is None and guild_id:
      guild = app.model.partial_guild(guild_id)

    super().__init__(app, user_id, guild)
    self.data = payload
    self.username = user['username']
    self.joined_at = None
    joined_at = payload.get('joined_at')

    if joined_at:
      self.joined_at = datetime.fromisoformat(joined_at)
