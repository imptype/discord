from typing import Any
from .user import PartialUser

class PartialMember(PartialUser):
  """
  TODO

  Attributes:
    guild: TODO
  """

  guild: Any # TODO

  def __init__(self, app, user_id, guild) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      user_id: TODO
      guild: TODO
    """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

class Member(PartialMember):
  """
  TODO

  Attributes:
    data: TODO
    username: TODO
    joined_at: TODO
  """

  data: Any # TODO
  username: Any # TODO
  joined_at: Any # TODO

  def __init__(self, app, payload, *, user = ..., guild = ...) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      payload: TODO
      user: TODO
      guild: TODO
    """
