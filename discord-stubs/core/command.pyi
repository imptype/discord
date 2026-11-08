from typing import Any
from ..abc import Handler

class BaseCommand(Handler):
  """
  TODO
  """

class PrefixCommand(BaseCommand):
  """
  TODO

  Attributes:
    name: TODO
  """

  def __init__(self, callback = ..., name = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
    """

  @property
  def parameters(self) -> Any: # TODO
    """
    TODO
    """

  async def __call__(self, context) -> Any: # TODO
    """
    TODO

    Args:
      context: TODO

    Returns:
      TODO
    """

  name: Any # TODO

class InteractionCommand(BaseCommand):
  """
  TODO

  Attributes:
    type: TODO
    key: TODO
  """

  def __init__(self, callback = ..., name = ..., type = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      type: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  type: Any # TODO
  key: Any # TODO

class SlashNode:
  """
  TODO

  Attributes:
    callback: TODO
    name: TODO
    description: TODO
    options: TODO
    level: TODO
    subcommands: TODO
    autocomplete: TODO
  """

  def __init__(self, callback = ..., name = ..., description = ..., options = ..., level = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      description: TODO
      options: TODO
      level: TODO
    """

  def subcommand(self, callback = ..., *, name = ..., description = ..., options = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      description: TODO
      options: TODO

    Returns:
      TODO
    """

  def on_autocomplete(self, callback = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO

    Returns:
      TODO
    """

  def find(self, names) -> Any: # TODO
    """
    TODO

    Args:
      names: TODO

    Returns:
      TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def bind(self, cog_instance) -> Any: # TODO
    """
    TODO

    Args:
      cog_instance: TODO

    Returns:
      TODO
    """

  callback: Any # TODO
  name: Any # TODO
  description: Any # TODO
  options: Any # TODO
  level: Any # TODO
  subcommands: Any # TODO
  autocomplete: Any

class SubCommand(SlashNode):
  """
  TODO
  """

class SlashCommand(SlashNode, InteractionCommand):
  """
  TODO
  """

  def __init__(self, callback = ..., name = ..., description = ..., options = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      description: TODO
      options: TODO
    """

  async def __call__(self, interaction) -> Any: # TODO
    """
    TODO

    Args:
      interaction: TODO

    Returns:
      TODO
    """

class UserCommand(InteractionCommand):
  """
  TODO
  """

  def __init__(self, callback = ..., name = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
    """

  async def __call__(self, interaction) -> Any: # TODO
    """
    TODO

    Args:
      interaction: TODO

    Returns:
      TODO
    """

class MessageCommand(InteractionCommand):
  """
  TODO
  """

  def __init__(self, callback = ..., name = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
    """

  async def __call__(self, interaction) -> Any: # TODO
    """
    TODO

    Args:
      interaction: TODO

    Returns:
      TODO
    """

class CommandNamespace:
  """
  TODO
  """

  @staticmethod
  def slash(callback = ..., *, name = ..., description = ..., options = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      description: TODO
      options: TODO

    Returns:
      TODO
    """

  @staticmethod
  def user(callback = ..., *, name = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO

    Returns:
      TODO
    """

  @staticmethod
  def message(callback = ..., *, name = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO

    Returns:
      TODO
    """

  def __call__(self, callback = ..., *, name = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO

    Returns:
      TODO
    """

command_namespace: CommandNamespace

class CommandProxy:
  def __init__(self, app, target) -> None: ...

  def __getattr__(self, name) -> Any: ...

  app: Any # TODO
  target: Any # TODO

class CommandMixin:
  """
  TODO

  Attributes:
    registry: TODO
    command: TODO
  """

  def __init__(self, registrars) -> None: # TODO
    """
    TODO

    Args:
      registrars: TODO
    """

  def set_proxy(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def add_commands(self, *commands) -> Any: # TODO
    """
    TODO

    Args:
      *commands: TODO

    Returns:
      TODO
    """

  def remove_commands(self, *commands) -> Any: # TODO
    """
    TODO

    Args:
      *commands: TODO

    Returns:
      TODO
    """

  async def run_command(self, payload, is_from_http) -> Any: # TODO
    """
    TODO

    Args:
      payload: TODO
      is_from_http: TODO

    Returns:
      TODO
    """

  async def run_autocomplete(self, payload, is_from_http) -> Any: # TODO
    """
    TODO

    Args:
      payload: TODO
      is_from_http: TODO

    Returns:
      TODO
    """

  registry: Any # TODO
  command: CommandNamespace
