from typing import Any
from ..abc import Handler

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

class TaskMixin:
  task_handlers: Any # TODO
  tasks_started: Any # TODO

  def __init__(self, registrars) -> None: ...

  def task(self, callback = ..., *, name = ..., seconds, autostart = ...) -> Any: ...

  def add_tasks(self, *tasks) -> Any: ...

  def remove_tasks(self, *tasks) -> Any: ...

  async def task_lifespan(self) -> Any: ...
