from ..abc import PartialModel

class PartialUser(PartialModel):
  async def fetch(self):
    return await self.app.model.http.user(self.id)

  async def create_dm(self):
    data = {'recipient_id': self.id}
    return self.app.model.channel(await self.app.http.create_dm(data))

class User(PartialUser):
  def __init__(self, app, payload):
    user_id = payload['id']

    super().__init__(app, user_id)
    self.data = payload
    self.username = payload['username']
