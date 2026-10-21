from .enums import ResponseType

class Interaction:
  def __init__(self, payload, app, is_from_http):
    self.payload = payload
    self.app = app
    self.is_from_http = is_from_http
    self.id = payload['id']
    self.token = payload['token']
    self.response = None

  async def respond(self, content):
    data = {'type': ResponseType.MESSAGE, 'data': {'content': content}}
    if self.is_from_http:
      self.response = data
    else:
      await self.app.http.create_interaction_response(self.id, self.token, data)
