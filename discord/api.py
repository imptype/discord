from typing import Any

MAJOR_PARAMS = ('channel_id', 'guild_id', 'webhook_id', 'webhook_token')

class Route:
  def __init__(self, method, path, **params):
    self.method = method
    self.path = path.format(**params)
    self.key = f'{method} {path}' # TODO: key and major for ratelimit handling later
    self.major = '+'.join(params[key] for key in MAJOR_PARAMS if key in params)

class API:
  async def request(
    self,
    route: Route,
    *,
    body: Any = None,
    authorize: bool = False,
    reason: str | None = None,
    **params: Any
  ) -> Any:
    ...

  async def create_interaction_response(
    self,
    interaction_id: str,
    interaction_token: str,
    data: Any,
    with_response: bool = False
  ):
    return await self.request(
      Route(
        'POST',
        '/interactions/{interaction_id}/{interaction_token}/callback',
        interaction_id = interaction_id,
        interaction_token = interaction_token
      ),
      body = data,
      with_response = with_response
    )

  async def create_message(self, channel_id, data):
    return await self.request(
      Route(
        'POST',
        '/channels/{channel_id}/messages',
        channel_id = channel_id
      ),
      body = data,
      authorize = True
    )

  async def bulk_overwrite_global_commands(self, application_id, data):
    return await self.request(
      Route(
        'PUT',
        '/applications/{application_id}/commands',
        application_id = application_id
      ),
      body = data,
      authorize = True
    )
