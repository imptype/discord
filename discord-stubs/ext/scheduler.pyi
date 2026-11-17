from typing import Any

def schedule(tasks, coro, eager_start = ...) -> Any: # TODO
  """
  TODO

  Args:
    tasks: TODO
    coro: TODO
    eager_start: TODO

  Returns:
    TODO
  """

class SchedulerMixin:
  """
  TODO

  Attributes:
    tasks: TODO
  """

  tasks: Any # TODO

  def __init__(self, **kwargs) -> None: ... # TODO

  def spawn(self, coro) -> Any: # TODO
    """
    TODO

    Args:
      coro: TODO

    Returns:
      TODO
    """

  def defer(self, coro) -> Any: # TODO
    """
    TODO

    Args:
      coro: TODO

    Returns:
      TODO
    """

  def delay(self, seconds, coro) -> Any: # TODO
    """
    TODO

    Args:
      seconds: TODO
      coro: TODO

    Returns:
      TODO
    """
