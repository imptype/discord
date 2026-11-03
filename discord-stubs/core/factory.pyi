from typing import Any

class ModelHTTP:
  def __init__(self, app, model) -> None: ...

  async def guild(self, guild_id) -> Any: ...

  async def channel(self, channel_id, guild = ...) -> Any: ...

  async def user(self, user_id) -> Any: ...

  async def member(self, user_id, guild) -> Any: ...

  async def message(self, message_id, channel) -> Any: ...

  async def webhook(self, webhook_id, token = ...) -> Any: ...

  app: Any
  model: Any

class ModelFactory:
  def __init__(self, app) -> None: ...

  http: ModelHTTP
  partial_guild: Any
  partial_channel: Any
  partial_user: Any
  partial_member: Any
  partial_message: Any
  partial_webhook: Any
  followup_webhook: Any
  guild: Any
  channel: Any
  user: Any
  member: Any
  message: Any
  webhook: Any
  context: Any
