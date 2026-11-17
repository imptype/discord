import asyncio
from typing import Any

class RegistrarMixin:
  """
  TODO

  Attributes:
    registrars: TODO
  """

  registrars: Any # TODO

  def __init__(self, **kwargs) -> None: # TODO
    """
    TODO

    Args:
      **kwargs: TODO
    """

class LoopMixin:
  loop: asyncio.AbstractEventLoop

  def __init__(self, **kwargs) -> None: ...
