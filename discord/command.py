from .enums import CommandType

class Handler:
  def __init__(self, func, name = None):
    self.func = func
    self.name = name or func.__name__

class BaseCommand(Handler):
  async def __call__(self, data):
    return await self.func(data)

class InteractionCommand(BaseCommand):
  def __init__(self, func, name = None, description = None):
    super().__init__(func, name)
    self.description = description or self.name

  def to_json(self):
    return {'name': self.name, 'type': CommandType.CHAT_INPUT, 'description': self.description}

class MessageCommand(BaseCommand):
  def __init__(self, func, name = None):
    super().__init__(func, name)
    self.name = self.name.lower()

class CommandNamespace:
  def __call__(self, func = None, *, name = None):
    def wrap(f):
      return MessageCommand(f, name)
    return wrap(func) if func else wrap

  @staticmethod
  def slash(func = None, *, name = None, description = None):
    def wrap(f):
      return InteractionCommand(f, name, description)
    return wrap(func) if func else wrap

command = CommandNamespace()
