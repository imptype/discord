from typing import Any
from .response import AutocompleteResponse
from .response import CommandResponse
from .response import ComponentResponse
from .response import ModalResponse
from .modal import ModalResult
from ..abc import Snowflake

def resolve_user(interaction, user_id) -> Any: ...

def resolve_option(interaction, option) -> Any: ...

def parse_options(interaction, is_autocomplete = ...) -> Any: ...

class OriginalInteractionMessage:
  interaction: Any # TODO
  app: Any # TODO

  def __init__(self, interaction) -> None: ...

  async def fetch(self) -> Any: ...

  async def edit(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ...) -> Any: ...

  async def delete(self) -> Any: ...

class Interaction(Snowflake):
  """
  TODO

  Attributes:
    data: TODO
    app: TODO
    is_from_http: TODO
    token: TODO
    application_id: TODO
    type: TODO
    guild_id: TODO
    followup: TODO
    original_message: TODO
    author: TODO
  """

  data: Any # TODO
  app: Any # TODO
  is_from_http: Any # TODO
  token: Any # TODO
  application_id: Any # TODO
  type: Any # TODO
  guild_id: Any # TODO
  followup: Any # TODO
  original_message: OriginalInteractionMessage
  author: Any # TODO

  def __init__(self, data, app, is_from_http) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
    """

class CommandInteraction(Interaction):
  """
  TODO

  Attributes:
    response: TODO
  """

  response: CommandResponse

  def __init__(self, data, app, is_from_http) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
    """

class SlashInteraction(CommandInteraction):
  """
  TODO
  """

  def __init__(self, data, app, is_from_http) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
    """

class UserInteraction(CommandInteraction):
  """
  TODO

  Attributes:
    user: TODO
  """

  user: Any # TODO

  def __init__(self, data, app, is_from_http) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
    """

class MessageInteraction(CommandInteraction):
  """
  TODO

  Attributes:
    message: TODO
  """

  message: Any # TODO

  def __init__(self, data, app, is_from_http) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
    """

class ComponentInteraction(Interaction):
  """
  TODO

  Attributes:
    response: TODO
    component: TODO
  """

  response: ComponentResponse
  component: Any # TODO

  def __init__(self, data, app, is_from_http, component) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
      component: TODO
    """

class SelectInteraction(ComponentInteraction):
  values: Any # TODO

  def __init__(self, data, app, is_from_http, select) -> None: ...

class ModalInteraction(Interaction):
  """
  TODO

  Attributes:
    response: TODO
    modal: TODO
    result: TODO
  """

  response: ModalResponse
  modal: Any # TODO
  result: ModalResult

  def __init__(self, data, app, is_from_http, modal) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
      modal: TODO
    """

class AutocompleteInteraction(Interaction):
  """
  TODO

  Attributes:
    response: TODO
  """

  response: AutocompleteResponse

  def __init__(self, data, app, is_from_http) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
      app: TODO
      is_from_http: TODO
    """
