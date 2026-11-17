from typing import Any
from ..abc import Handler
from ..abc import RegistrarMixin

class Task(Handler):
  """
  TODO

  Attributes:
    seconds: TODO
    autostart: TODO
    app: TODO
    runner: TODO
  """

  seconds: Any # TODO
  autostart: Any # TODO
  app: Any # TODO
  runner: Any # TODO

  def __init__(self, callback = ..., name = ..., *, seconds, autostart = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      seconds: TODO
      autostart: TODO
    """

  def start(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def stop(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def run(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

def task(callback = ..., *, name = ..., seconds, autostart = ...) -> Any: # TODO
  """
  TODO

  Args:
    callback: TODO
    name: TODO
    seconds: TODO
    autostart: TODO

  Returns:
    TODO
  """

class TaskMixin(RegistrarMixin):
  """
  TODO

  Attributes:
    task_handlers: TODO
    tasks_started: TODO
  """

  task_handlers: Any # TODO
  tasks_started: bool

  def __init__(self, **kwargs) -> None: ... # TODO

  def task(self, callback = ..., *, name = ..., seconds, autostart = ...) -> Any: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      seconds: TODO
      autostart: TODO

    Returns:
      TODO
    """

  def add_tasks(self, *tasks) -> Any: # TODO
    """
    TODO

    Args:
      *tasks: TODO

    Returns:
      TODO
    """

  def remove_tasks(self, *tasks) -> Any: # TODO
    """
    TODO

    Args:
      *tasks: TODO

    Returns:
      TODO
    """

  async def task_lifespan(self) -> Any:
    """
    TODO

    Returns:
      TODO
    """
