from typing import Any
from ..abc import PartialModel

class PartialChannel(PartialModel):
  """
  TODO

  Attributes:
    guild: TODO
  """

  def __init__(self, app, channel_id, guild = ...) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      channel_id: TODO
      guild: TODO
    """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def send(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ...) -> Any: # TODO
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

  guild: Any # TODO

class Channel(PartialChannel):
  """
  TODO

  Attributes:
    data: TODO
    name: TODO
  """

  def __init__(self, app, payload, guild = ...) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      payload: TODO
      guild: TODO
    """

  data: Any # TODO
  name: Any # TODO
