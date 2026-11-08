from typing import Any
from ..ext import CogMixin
from ..ext import SignalMixin
from ..ext import LifespanMixin
from .command import CommandMixin
from .factory import ModelFactory
from .component import ComponentMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin, SignalMixin):
  model: ModelFactory
  tasks: Any # TODO

  def __init__(self, token = ..., application_id = ..., reload = ...) -> None: ...

  async def sync(self) -> Any: ...
