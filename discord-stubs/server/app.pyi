from typing import Any
from nacl.signing import VerifyKey
from ..core import AppBase

class App(AppBase):
  """
  TODO

  Attributes:
    verify_key: TODO
    pending_interactions: TODO
  """

  verify_key: VerifyKey
  pending_interactions: Any # TODO

  def __init__(self, public_key, token = ..., application_id = ..., reload = ...) -> None: # TODO
    """
    TODO

    Args:
      public_key: TODO
      token: TODO
      application_id: TODO
      reload: TODO
    """

  async def run_lifespan(self, receive, send) -> Any: # TODO
    """
    TODO

    Args:
      receive: TODO
      send: TODO

    Returns:
      TODO
    """

  async def respond(self, send, status, obj = ...) -> Any: # TODO
    """
    TODO

    Args:
      send: TODO
      status: TODO
      obj: TODO

    Returns:
      TODO
    """

  async def __call__(self, scope, receive, send) -> Any: # TODO
    """
    TODO

    Args:
      scope: TODO
      receive: TODO
      send: TODO

    Returns:
      TODO
    """
