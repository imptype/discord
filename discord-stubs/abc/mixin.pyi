import asyncio
from typing import Any

class RegistrarMixin:
  """
  TODO

  Attributes:
    registrars: TODO
  """

  registrars: Any # TODO

  def __init__(self, **kwargs) -> None: ... # TODO

class LoopMixin:
  """
  TODO

  Attributes:
    loop: TODO
  """

  loop: asyncio.AbstractEventLoop

  def __init__(self, **kwargs) -> None: ... # TODO
