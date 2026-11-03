from typing import Any
from .member import Member
from .enums import MessageFlags
from ..abc import PartialModel

class PartialMessage(PartialModel):
  """
  TODO

  Attributes:
    channel: TODO
  """

  def __init__(self, app, message_id, channel) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      message_id: TODO
      channel: TODO
    """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def edit(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ...) -> Any: # TODO
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

    Returns:
      TODO
    """

  channel: Any # TODO

class Message(PartialMessage):
  """
  TODO

  Attributes:
    data: TODO
    guild: TODO
    content: TODO
    flags: TODO
    edited_at: TODO
    author: TODO
  """

  def __init__(self, app, payload, *, channel = ..., guild = ...) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      payload: TODO
      channel: TODO
      guild: TODO
    """

  data: Any # TODO
  guild: Any # TODO
  content: Any # TODO
  flags: MessageFlags
  edited_at: Any # TODO
  author: Member
