from typing import Any

class ModelHTTP:
  app: Any # TODO
  model: Any # TODO

  def __init__(self, app, model) -> None: ...

  async def guild(self, guild_id) -> Any: ...

  async def channel(self, channel_id, guild = ...) -> Any: ...

  async def user(self, user_id) -> Any: ...

  async def member(self, user_id, guild) -> Any: ...

  async def message(self, message_id, channel) -> Any: ...

  async def webhook(self, webhook_id, token = ...) -> Any: ...

class ModelFactory:
  http: ModelHTTP
  partial_guild: Any # TODO
  partial_channel: Any # TODO
  partial_user: Any # TODO
  partial_member: Any # TODO
  partial_message: Any # TODO
  partial_webhook: Any # TODO
  followup_webhook: Any # TODO
  guild: Any # TODO
  channel: Any # TODO
  user: Any # TODO
  member: Any # TODO
  message: Any # TODO
  webhook: Any # TODO
  context: Any # TODO

  def __init__(self, app) -> None: ...
