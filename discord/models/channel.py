import orjson
import aiohttp
from .abc import PartialModel

class PartialChannel(PartialModel):
  def __init__(self, app, channel_id, guild = None):
    super().__init__(app, channel_id)
    self.guild = guild

  async def fetch(self):
    return await self.app.model.http.channel(self.id, self.guild)

  async def send(self, content = None, *, embed = None, embeds = None, file = None, files = None):
    if embed is not None and embeds is not None:
      raise ValueError('cannot send both embed and embeds')
    if file is not None and files is not None:
      raise ValueError('cannot send both file and files')

    body = {}
    if content is not None:
      body['content'] = content
    if embed:
      embeds = [embed]
    if embeds:
      body['embeds'] = [embed.to_json() for embed in embeds]
    if file:
      files = [file]
    if files:
      body['attachments'] = []
      for index, file in enumerate(files):
        attachment = {'id': index, 'filename': file.filename}
        if file.description:
          attachment['description'] = file.description
        body['attachments'].append(attachment)
      form = aiohttp.FormData()
      form.add_field('payload_json', orjson.dumps(body).decode(), content_type = 'application/json')
      for index, file in enumerate(files):
        form.add_field(f'files[{index}]', file.data, filename = file.filename, content_type = file.content_type)
      body = form

    data = await self.app.http.create_message(self.id, body)
    return self.app.model.message(data)

class Channel(PartialChannel):
  def __init__(self, app, payload, guild = None):
    channel_id = payload['id']
    guild_id = payload.get('guild_id')

    if guild is None and guild_id:
      guild = app.model.partial_guild(guild_id)

    super().__init__(app, channel_id, guild)
    self.data = payload
    self.name = payload.get('name') # none for DMs
