from typing import Any
from .enums import InteractionType

class InteractionResult:
  def __init__(self, app, data) -> None: ...

  data: Any
  interaction_id: Any
  interaction_type: InteractionType
  activity_instance_id: Any
  response_message_id: Any
  response_message_loading: Any
  response_message_ephemeral: Any
  resource_type: Any
  activity_instance: Any
  message: Any

class InteractionResponse:
  """
  TODO

  Attributes:
    interaction: TODO
    app: TODO
    body: TODO
    responded: TODO
  """

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

  interaction: Any # TODO
  app: Any # TODO
  body: Any # TODO
  responded: Any # TODO

class MessageMixin(InteractionResponse):
  async def send(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., ephemeral = ..., with_response = ...) -> Any: ...

  async def defer(self, *, ephemeral = ..., with_response = ...) -> Any: ...

  async def premium_required(self, *, with_response = ...) -> Any: ...

  async def launch_activity(self, *, with_response = ...) -> Any: ...

class ModalMixin(InteractionResponse):
  async def send_modal(self, modal, *, with_response = ...) -> Any: ...

class UpdateMixin(InteractionResponse):
  async def update(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., with_response = ...) -> Any: ...

  async def defer_update(self, *, with_response = ...) -> Any: ...

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
