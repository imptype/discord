from typing import Any
from ..ext import CogMixin
from .command import CommandMixin
from .component import ComponentMixin
from ..ext import LifespanMixin
from .factory import ModelFactory
from ..ext import SignalMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin, SignalMixin):
  model: ModelFactory
  tasks: Any # TODO

  def __init__(self, token = ..., application_id = ..., reload = ...) -> None: ...

  async def sync(self) -> Any: ...
