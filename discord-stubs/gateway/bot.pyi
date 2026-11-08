from typing import Any
from ..core import AppBase
from ..core import CommandProxy
from .intents import Intents
from .connection import Connection

class BotCommandProxy(CommandProxy):
  def __call__(self, *args, **kwargs) -> Any: ...

class Bot(AppBase):
  """
  TODO

  Attributes:
    intents: The bot's gateway intents.
    prefix: The prefix for gateway message commands.
    connection: TODO
    event_handlers: TODO
    command_handlers: TODO
    ready_at: TODO
  """

  intents: Intents
  prefix: str
  connection: Connection
  event_handlers: Any # TODO
  command_handlers: Any # TODO
  ready_at: Any # TODO

  def __init__(self, token, application_id = ..., intents = ..., prefix = ..., reload = ...) -> None: # TODO
    """
    TODO

    Args:
      token: TODO
      application_id: TODO
      intents: TODO
      prefix: TODO
      reload: TODO
    """

  def set_proxy(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def run(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def start(self) -> Any: # TODO
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

  def event(self, callback = ..., *, name = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO

    Returns:
      TODO
    """

  def add_events(self, *events) -> Any: # TODO
    """
    TODO

    Args:
      *events: TODO

    Returns:
      TODO
    """

  def remove_events(self, *events) -> Any: # TODO
    """
    TODO

    Args:
      *events: TODO

    Returns:
      TODO
    """

  def spawn(self, coro) -> Any: # TODO
    """
    TODO

    Args:
      coro: TODO

    Returns:
      TODO
    """

  def handle_gateway_command(self, message) -> Any: # TODO
    """
    TODO

    Args:
      message: TODO

    Returns:
      TODO
    """

  async def on_event(self, name, data) -> Any: # TODO
    """
    TODO

    Args:
      name: TODO
      data: TODO

    Returns:
      TODO
    """
