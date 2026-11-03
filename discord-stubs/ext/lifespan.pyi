from typing import Any
from contextlib import AsyncExitStack
from ..abc import BaseHandler
import asyncio

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
  def __init__(self, registrars, http) -> None: ...

  def lifespan(self, callback = ...) -> Any: ...

  async def enter_lifespan(self, handler) -> Any: ...

  async def add_lifespans(self, *handlers) -> Any: ...

  async def remove_lifespans(self, *handlers) -> Any: ...

  async def startup_lifespans(self) -> Any: ...

  async def shutdown_lifespans(self) -> Any: ...

  http: Any
  stack: AsyncExitStack
  lifespan_handlers: Any
  loop: asyncio.AbstractEventLoop
  started_at: Any
