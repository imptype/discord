"""
context.py - a custom object for message commands, to access things quickly.
"""

class Context:
  def __init__(self, app, message):
    self.app = app
    self.message = message
    self.author = message.author
    self.channel = message.channel
    self.guild = message.guild

  async def send(self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None):
    return await self.channel.send(
      content, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags
    )
