from typing import Any
from ..abc import PartialModel

class PartialUser(PartialModel):
  """
  TODO
  """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def create_dm(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

class User(PartialUser):
  """
  TODO

  Attributes:
    data: TODO
    username: TODO
  """

  def __init__(self, app, payload) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      payload: TODO
    """

  data: Any # TODO
  username: Any # TODO
