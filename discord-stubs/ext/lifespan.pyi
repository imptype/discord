from typing import Any
from contextlib import AsyncExitStack
from ..abc import LoopMixin
from ..abc import BaseHandler
from ..abc import RegistrarMixin
from ..core.http import HTTPClient

class Lifespan(BaseHandler):
  """
  TODO
  """

  def __init__(self, callback, name = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
    """

def lifespan(callback = ..., *, name = ...) -> Any: # TODO
  """
  TODO

  Args:
    callback: TODO
    name: TODO

  Returns:
    TODO
  """

class LifespanMixin(RegistrarMixin, LoopMixin):
  """
  TODO

  Attributes:
    http: The app's HTTPClient.
    stack: TODO
    lifespan_handlers: TODO
    started_at: TODO
  """

  http: HTTPClient
  stack: AsyncExitStack
  lifespan_handlers: Any # TODO
  started_at: Any # TODO

  def __init__(self, *, http, **kwargs) -> None: ... # TODO

  def lifespan(self, callback = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO

    Returns:
      TODO
    """

  async def enter_lifespan(self, handler) -> Any: # TODO
    """
    TODO

    Args:
      handler: TODO

    Returns:
      TODO
    """

  async def add_lifespans(self, *handlers) -> Any: # TODO
    """
    TODO

    Args:
      *handlers: TODO

    Returns:
      TODO
    """

  async def remove_lifespans(self, *handlers) -> Any: # TODO
    """
    TODO

    Args:
      *handlers: TODO

    Returns:
      TODO
    """

  async def startup_lifespans(self) -> Any:
    """
    TODO

    Returns:
      TODO
    """

  async def shutdown_lifespans(self) -> Any:
    """
    TODO

    Returns:
      TODO
    """
