from typing import Any

def parse_arguments(parameters, text, name) -> Any: ...

class Context:
  """
  TODO

  Attributes:
    app: TODO
    message: TODO
    arguments: TODO
    author: TODO
    channel: TODO
    guild: TODO
  """

  app: Any # TODO
  message: Any # TODO
  arguments: Any # TODO
  author: Any # TODO
  channel: Any # TODO
  guild: Any # TODO

  def __init__(self, app, message, arguments = ...) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      message: TODO
      arguments: TODO
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
