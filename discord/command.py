from .enums import CommandType

class Command:
  def __init__(self, func, name = None, description = None):
    self.func = func
    self.name = name or func.__name__
    self.description = description or self.name

  def to_json(self):
    return {'name': self.name, 'type': CommandType.CHAT_INPUT, 'description': self.description}

  async def __call__(self, interaction):
    return await self.func(interaction)

def slash(func = None, *, name = None, description = None):
  def wrap(f):
    return Command(f, name, description)
  return wrap(func) if func else wrap
