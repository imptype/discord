from typing import Any
from .enums import InteractionType

class InteractionResult:
  data: Any # TODO
  interaction_id: Any # TODO
  interaction_type: InteractionType
  activity_instance_id: Any # TODO
  response_message_id: Any # TODO
  response_message_loading: Any # TODO
  response_message_ephemeral: Any # TODO
  resource_type: Any # TODO
  activity_instance: Any # TODO
  message: Any # TODO

  def __init__(self, app, data) -> None: ...

class InteractionResponse:
  """
  TODO

  Attributes:
    interaction: TODO
    app: TODO
    body: TODO
    responded: TODO
  """

  interaction: Any # TODO
  app: Any # TODO
  body: Any # TODO
  responded: Any # TODO

  def __init__(self, interaction) -> None: # TODO
    """
    TODO

    Args:
      interaction: TODO
    """

  async def create(self, type, data = ..., with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      type: TODO
      data: TODO
      with_response: TODO

    Returns:
      TODO
    """

class MessageMixin(InteractionResponse):
  """
  TODO
  """

  async def send(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., ephemeral = ..., with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      content: TODO
      embed: TODO
      embeds: TODO
      file: TODO
      files: TODO
      view: TODO
      components: TODO
      flags: TODO
      ephemeral: TODO
      with_response: TODO

    Returns:
      TODO
    """

  async def defer(self, *, ephemeral = ..., with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      ephemeral: TODO
      with_response: TODO

    Returns:
      TODO
    """

  async def premium_required(self, *, with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      with_response: TODO

    Returns:
      TODO
    """

  async def launch_activity(self, *, with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      with_response: TODO

    Returns:
      TODO
    """

class ModalMixin(InteractionResponse):
  """
  TODO
  """

  async def send_modal(self, modal, *, with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      modal: TODO
      with_response: TODO

    Returns:
      TODO
    """

class UpdateMixin(InteractionResponse):
  """
  TODO
  """

  async def update(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      content: TODO
      embed: TODO
      embeds: TODO
      file: TODO
      files: TODO
      view: TODO
      components: TODO
      flags: TODO
      with_response: TODO

    Returns:
      TODO
    """

  async def defer_update(self, *, with_response = ...) -> Any: # TODO
    """
    TODO

    Args:
      with_response: TODO

    Returns:
      TODO
    """

class CommandResponse(MessageMixin, ModalMixin):
  """
  TODO
  """

class ComponentResponse(MessageMixin, ModalMixin, UpdateMixin):
  """
  TODO
  """

class ModalResponse(MessageMixin, UpdateMixin):
  """
  TODO
  """

class AutocompleteResponse(InteractionResponse):
  """
  TODO
  """

  async def send_choices(self, choices = ...) -> Any: # TODO
    """
    TODO

    Args:
      choices: TODO

    Returns:
      TODO
    """
