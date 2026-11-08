from typing import Any
from ..abc import Handler
import asyncio

class SignalTimeoutError(TimeoutError): ...

class SignalCancelledError(asyncio.CancelledError): ...

class SignalHandler(Handler):
  """
  TODO

  Attributes:
    priority: TODO
    timeout: TODO
    max_runs: TODO
    runs: TODO
    app: TODO
  """

  def __init__(self, callback = ..., name = ..., priority = ..., timeout = ..., max_runs = ..., once = ...) -> None: # TODO
    """
    TODO

    Args:
      callback: TODO
      name: TODO
      priority: TODO
      timeout: TODO
      max_runs: TODO
      once: TODO
    """

  def cancel(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def __call__(self, *args) -> Any: # TODO
    """
    TODO

    Args:
      *args: TODO

    Returns:
      TODO
    """

  priority: Any # TODO
  timeout: Any # TODO
  max_runs: Any # TODO
  runs: Any # TODO
  app: Any # TODO

class SignalWaiter:
  """
  TODO

  Attributes:
    app: TODO
    name: TODO
    priority: TODO
    timeout: TODO
    waiter_future: TODO
    waiter_done_future: TODO
    sender_done_future: TODO
  """

  def __init__(self, app, name, priority = ..., timeout = ...) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      name: TODO
      priority: TODO
      timeout: TODO
    """

  def cancel(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def receive(self, is_async_with) -> Any: # TODO
    """
    TODO

    Args:
      is_async_with: TODO

    Returns:
      TODO
    """

  def __await__(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def __aenter__(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def __aexit__(self, *exception) -> Any: # TODO
    """
    TODO

    Args:
      *exception: TODO

    Returns:
      TODO
    """

  app: Any # TODO
  name: Any # TODO
  priority: Any # TODO
  timeout: Any # TODO
  waiter_future: Any # TODO
  waiter_done_future: Any # TODO
  sender_done_future: Any # TODO

class SignalModule:
  def __init__(self, app) -> None: ...

  def spawn(self, coro, eager = ...) -> Any: ...

  async def dispatch(self, name, args, *, each, wait) -> Any: ...

  async def fire(self, name, /, *args) -> Any: ...

  async def fire_each(self, name, /, *args) -> Any: ...

  async def send(self, name, /, *args) -> Any: ...

  async def send_each(self, name, /, *args) -> Any: ...

  async def defer(self, name, /, *args) -> Any: ...

  async def defer_each(self, name, /, *args) -> Any: ...

  def wait(self, name, priority = ..., timeout = ...) -> Any: ...

  def __call__(self, callback = ..., *, name = ..., priority = ..., timeout = ..., max_runs = ..., once = ...) -> Any: ...

  app: Any # TODO

def signal(callback = ..., *, name = ..., priority = ..., timeout = ..., max_runs = ..., once = ...) -> Any: # TODO
  """
  TODO

  Args:
    callback: TODO
    name: TODO
    priority: TODO
    timeout: TODO
    max_runs: TODO
    once: TODO

  Returns:
    TODO
  """

class SignalMixin:
  """
  TODO

  Attributes:
    signal_handlers: TODO
    signal_waiters: TODO
    signal: TODO
  """

  def __init__(self, registrars) -> None: # TODO
    """
    TODO

    Args:
      registrars: TODO
    """

  def add_signals(self, *signals) -> Any: # TODO
    """
    TODO

    Args:
      *signals: TODO

    Returns:
      TODO
    """

  def remove_signals(self, *signals) -> Any: # TODO
    """
    TODO

    Args:
      *signals: TODO

    Returns:
      TODO
    """

  signal_handlers: Any # TODO
  signal_waiters: Any # TODO
  signal: SignalModule
