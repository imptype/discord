from typing import Any

class BaseHandler:
  """
  TODO

  Attributes:
    callback: TODO
    name: TODO
  """

  def __init__(self, callback = ..., name = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
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

class Handler(BaseHandler):
  """
  TODO
  """

  async def callback(self, *args, **kwargs) -> Any: # TODO
    """
    TODO

    Args:
      *args: TODO
      **kwargs: TODO

    Returns:
      TODO
    """

  async def __call__(self, *args, **kwargs) -> Any: # TODO
    """
    TODO

    Args:
      *args: TODO
      **kwargs: TODO

    Returns:
      TODO
    """
