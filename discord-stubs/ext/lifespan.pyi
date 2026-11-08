from typing import Any
from contextlib import AsyncExitStack
from ..abc import BaseHandler
import asyncio
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

class LifespanMixin:
  """
  TODO

  Attributes:
    http: The app's HTTPClient.
    stack: TODO
    lifespan_handlers: TODO
    loop: TODO
    started_at: TODO
  """

  http: HTTPClient
  stack: AsyncExitStack
  lifespan_handlers: Any # TODO
  loop: asyncio.AbstractEventLoop
  started_at: Any # TODO

  def __init__(self, registrars, http) -> None: # TODO
    """
    TODO

    Args:
      registrars: TODO
      http: TODO
    """

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

  async def startup_lifespans(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def shutdown_lifespans(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """
