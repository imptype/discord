from typing import Any
from ..abc import PartialModel

class PartialGuild(PartialModel):
  """
  TODO
  """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

class Guild(PartialGuild):
  """
  TODO

  Attributes:
    data: TODO
    name: TODO
  """

  def __init__(self, app, payload) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      payload: TODO
    """

  data: Any # TODO
  name: Any # TODO
