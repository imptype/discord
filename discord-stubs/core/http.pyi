from ..abc import API
from typing import Any
from ..abc import Route

USER_AGENT: str

class HTTPClient(API):
  """
  TODO

  Attributes:
    token: TODO
    application_id: TODO
    use_sync: TODO
    cleanup_task: TODO
  """

  def __init__(self, token = ..., application_id = ..., use_sync = ...) -> None: # TODO
    """
    TODO

    Args:
      token: TODO
      application_id: TODO
      use_sync: TODO
    """

  @classmethod
  def implicit(cls) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def request(self, route: Route, *, body: Any = ..., authorize: bool | str = ..., reason: str | None = ..., **params: Any) -> Any: # TODO
    """
    TODO

    Args:
      route: TODO
      body: TODO
      authorize: TODO
      reason: TODO
      **params: TODO

    Returns:
      TODO
    """

  async def __aenter__(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def __aexit__(self, *exc_info) -> Any: # TODO
    """
    TODO

    Args:
      *exc_info: TODO

    Returns:
      TODO
    """

  token: Any # TODO
  application_id: Any # TODO
  use_sync: Any # TODO
  cleanup_task: Any # TODO
