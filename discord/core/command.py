from typing import cast
from .enums import CommandType
from .interaction import Interaction

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

command_namespace = CommandNamespace()

# allows for "@app/bot.command.slash" syntax
class CommandProxy:
  def __init__(self, app, target):
    self.app = app
    self.target = target

  # for namespace lookup app.command.slash or bot.command.slash
  def __getattr__(self, name):
    attr = getattr(self.target, name)

    def wrapper(*args, **kwargs):
      result = attr(*args, **kwargs)

      # decorator without brackets: @bot.command, @app/bot.command.slash
      if isinstance(result, BaseCommand):
        self.app.add_commands(result)
        return result

      # decorator with brackets: @bot.command(...), @app/bot.command.slash(...)
      if callable(result):
        def decorator(func):
          command = result(func)
          self.app.add_commands(command)
          return command
        return decorator

      return result
    return wrapper

class CommandMixin:
  def __init__(self):
    super().__init__()
    self.registry = {}
    self.set_proxy()

  def set_proxy(self):
    self.command = cast(CommandNamespace, CommandProxy(self, command_namespace))

  def add_commands(self, *commands):
    for command in commands: # noqa: F402
      if not isinstance(command, InteractionCommand):
        raise ValueError(f'not an interaction command: {command!r}')
    for command in commands:
      self.registry[command.name] = command

  def remove_commands(self, *commands):
    for command in commands: # noqa: F402
      if not isinstance(command, InteractionCommand):
        raise ValueError(f'not an interaction command: {command!r}')
    for command in commands:
      if self.registry.get(command.name) is command:
        del self.registry[command.name]

  async def run_command(self, payload, is_from_http):
    name = payload['data']['name']
    if (command := self.registry.get(name)) is None:
      raise ValueError(f'unknown command: {name}')
    interaction = Interaction(payload, self, is_from_http)
    await command(interaction)
    return interaction
