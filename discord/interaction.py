from .enums import ResponseType

class Interaction:
  def __init__(self, payload):
    self.payload = payload
    self.response = None

  async def respond(self, content):
    # if self is app, set response, or if bot do http
    self.response = {'type': ResponseType.MESSAGE, 'data': {'content': content}}
