from typing import Any
from ..ext import CogMixin
from ..ext import TaskMixin
from ..ext import SignalMixin
from ..ext import LifespanMixin
from ..ext import SchedulerMixin
from .command import CommandMixin
from .factory import ModelFactory
from .component import ComponentMixin

class AppBase(CommandMixin, LifespanMixin, ComponentMixin, CogMixin, SignalMixin, TaskMixin, SchedulerMixin):
  model: ModelFactory

  def __init__(self, token = ..., application_id = ..., reload = ...) -> None: ...

  async def sync(self) -> Any: ...
