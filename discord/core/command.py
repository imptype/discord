import copy
import types
import inspect
from typing import Any, cast
from functools import cached_property
from ..ui.abc import clean
from .enums import CommandType, OptionType
from ..models.context import parse_arguments
from .interaction import AutocompleteInteraction, MessageInteraction, SlashInteraction, UserInteraction

class Handler:
  def __init__(self, func, name = None):
    self.func = func
    self.name = name or func.__name__

  def bind(self, instance):
    handler = copy.copy(self)
    handler.func = types.MethodType(self.func, instance)
    return handler

class BaseCommand(Handler):
  async def __call__(self, data):
    return await self.func(data)

class PrefixCommand(BaseCommand):
  def __init__(self, func, name = None):
    super().__init__(func, name)
    self.name = self.name.lower()

  @cached_property
  def parameters(self):
    return list(inspect.signature(self.func).parameters.values())[1:]

  async def __call__(self, ctx):
    args, kwargs = parse_arguments(self.parameters, ctx.arguments, self.name)
    return await self.func(ctx, *args, **kwargs)

class InteractionCommand(BaseCommand):
  def __init__(self, func, name = None, type = None):
    super().__init__(func, name)
    self.type = type
    self.key = (type, self.name)

  def to_json(self):
    return {'name': self.name, 'type': self.type}

class SlashNode:
  def __init__(self, func, name = None, description = None, options = (), level = 1):
    self.func = func
    self.name = name or func.__name__
    self.description = description or self.name
    self.options = options
    self.level = level
    self.subcommands = {}
    self.autocomplete: Any = None

  def subcommand(self, func = None, *, name = None, description = None, options = ()):
    if self.level >= 2:
      raise ValueError(f'cannot add a subcommand to {self.name!r}, command > group > subcommand is the maximum depth')
    def wrap(f):
      subcommand = SubCommand(f, name, description, options, self.level + 1)
      self.subcommands[subcommand.name] = subcommand
      return subcommand
    return wrap(func) if func else wrap

  def on_autocomplete(self, func = None):
    def wrap(f):
      self.autocomplete = f
      return f
    return wrap(func) if func else wrap

  def find(self, names):
    node = self
    for name in names:
      if (node := node.subcommands.get(name)) is None:
        raise ValueError(f'unknown subcommand: {name}')
    return node

  def to_json(self):
    if self.subcommands and self.options:
      raise ValueError(f'{self.name!r} cannot have both options and subcommands')
    if self.level == 0:
      type = CommandType.CHAT_INPUT
    elif self.subcommands:
      type = OptionType.SUB_COMMAND_GROUP
    else:
      type = OptionType.SUB_COMMAND
    children = self.subcommands.values() if self.subcommands else self.options
    return clean({
      'name': self.name,
      'type': type,
      'description': self.description,
      'options': [child.to_json() for child in children] or None
    })

  def bind(self, instance):
    node = copy.copy(self)
    node.func = types.MethodType(self.func, instance)
    node.subcommands = {name: subcommand.bind(instance) for name, subcommand in self.subcommands.items()}
    if self.autocomplete:
      node.autocomplete = types.MethodType(self.autocomplete, instance)
    return node

class SubCommand(SlashNode): # an alias for now
  pass

class SlashCommand(SlashNode, InteractionCommand):
  def __init__(self, func, name = None, description = None, options = ()):
    SlashNode.__init__(self, func, name, description, options, 0)
    InteractionCommand.__init__(self, func, name, CommandType.CHAT_INPUT)

  async def __call__(self, interaction):
    node = self.find(interaction.names[1:])
    return await node.func(interaction, **interaction.options)

class UserCommand(InteractionCommand):
  def __init__(self, func, name = None):
    super().__init__(func, name, CommandType.USER)

  async def __call__(self, interaction):
    return await self.func(interaction, interaction.user)

class MessageCommand(InteractionCommand):
  def __init__(self, func, name = None):
    super().__init__(func, name, CommandType.MESSAGE)

  async def __call__(self, interaction):
    return await self.func(interaction, interaction.message)

class CommandNamespace:
  def __call__(self, func = None, *, name = None):
    def wrap(f):
      return PrefixCommand(f, name)
    return wrap(func) if func else wrap

  @staticmethod
  def slash(func = None, *, name = None, description = None, options = ()):
    def wrap(f):
      return SlashCommand(f, name, description, options)
    return wrap(func) if func else wrap

  @staticmethod
  def user(func = None, *, name = None):
    def wrap(f):
      return UserCommand(f, name)
    return wrap(func) if func else wrap

  @staticmethod
  def message(func = None, *, name = None):
    def wrap(f):
      return MessageCommand(f, name)
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
    self.registry = {} # {(kind, name): InteractionCommand}
    self.set_proxy()

  def set_proxy(self):
    self.command = cast(CommandNamespace, CommandProxy(self, command_namespace))

  def add_commands(self, *commands):
    for command in commands: # noqa: F402
      if not isinstance(command, InteractionCommand):
        raise ValueError(f'not an interaction command: {command!r}')
    for command in commands:
      self.registry[command.key] = command

  def remove_commands(self, *commands):
    for command in commands: # noqa: F402
      if not isinstance(command, InteractionCommand):
        raise ValueError(f'not an interaction command: {command!r}')
    for command in commands:
      if self.registry.get(command.key) is command:
        del self.registry[command.key]

  async def run_command(self, payload, is_from_http):
    data = payload['data']
    kind = CommandType(data['type'])
    name = data['name']
    if (command := self.registry.get((kind, name))) is None:
      raise ValueError(f'unknown {kind.name} command: {name}')
    match kind:
      case CommandType.CHAT_INPUT:
        interaction = SlashInteraction(payload, self, is_from_http)
      case CommandType.USER:
        interaction = UserInteraction(payload, self, is_from_http)
      case CommandType.MESSAGE:
        interaction = MessageInteraction(payload, self, is_from_http)
      case _:
        raise ValueError(f'unsupported command type: {kind.name}')
    await command(interaction)
    return interaction

  async def run_autocomplete(self, payload, is_from_http):
    name = payload['data']['name']
    if (command := self.registry.get((CommandType.CHAT_INPUT, name))) is None:
      raise ValueError(f'unknown command: {name}')
    interaction = AutocompleteInteraction(payload, self, is_from_http)
    node = command.find(interaction.names[1:])
    if node.autocomplete is None:
      raise ValueError(f'no autocomplete handler for: {node.name}')
    name, value = interaction.focused
    await node.autocomplete(interaction, name, value, options = interaction.options)
    return interaction
