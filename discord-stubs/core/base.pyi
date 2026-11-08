from typing import Any
from ..ext import CogMixin
from .command import CommandMixin
from .component import ComponentMixin
from ..ext import LifespanMixin
from .factory import ModelFactory
from ..ext import SignalMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin, SignalMixin):
  """
  TODO

  Attributes:
    model: TODO
    tasks: TODO
  """

  def __init__(self, token = ..., application_id = ..., reload = ...) -> None: # TODO
    """
    TODO

    Args:
      token: TODO
      application_id: TODO
      reload: TODO
    """

  async def sync(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  model: ModelFactory
  tasks: Any # TODO
