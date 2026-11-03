"""
signal.py - for custom events.

Receiving:
  1. As a decorator (handler):
  @app.signal(*, name, priority, timeout, max_runs, once)
  async def anything(a, b, c):

  2. In a coroutine (waiter):
  a, b, c = await app.signal.wait(name, priority, timeout) - raises SignalTimeoutError if timed out

  3. In a coro as a context manager (waiter), it's like "each" on an individual basis:
  async with app.signal.wait(...) as (a, b, c):
    ...

Cancel receive:
  1. For handler do `handler.cancel()`
  2. For coro, use `waiter = app.signal.wait(...)` then `await waiter` then `waiter.cancel()` to raise SignalCancelledError

Sending:
  await app.signal.fire(name, *a)       - Run handlers now, dispatch is concurrent, sender continues once all handlers yield or complete
  await app.signal.fire_each(name, *a)  - Run handlers now, dispatch is sequential, sender continues until last handler yields or completes
  await app.signal.send(name, *a)       - Run handlers now, dispatch is concurrent, sender continues once all handlers complete only
  await app.signal.send_each(name, *a)  - Run handlers now, dispatch is sequential, sender continues once all handlers complete only
  await app.signal.defer(name, *a)      - Schedule to run later, dispatch is concurrent, sender continues immediately
  await app.signal.defer_each(name, *a) - Schedule to run later, dispatch is sequential, sender continues immediately

Terms:
  concurrent = handlers run indepdendently, a yield in the handler can change completion order
  sequential = handlers run one at a time, a yield in one slows down the whole thing
  priority = lower number first, None last, handlers and waiters interleave but handler takes priority when same priority
  max_runs = handler automatically removes after hitting that amount of runs, default is None which is unlimited
  once = shortcut for max_runs = 1, raises ValueError if max_runs is also set
"""

import asyncio
import logging
from ..abc import Handler

DEFAULT_WAITER_TIMEOUT = 180
DEFAULT_HANDLER_TIMEOUT = None

log = logging.getLogger(__name__)

class SignalTimeoutError(TimeoutError):
  pass

class SignalCancelledError(asyncio.CancelledError):
  pass

class SignalHandler(Handler):
  def __init__(self, callback = None, name = None, priority = None, timeout = DEFAULT_HANDLER_TIMEOUT, max_runs = None, once = False):
    super().__init__(callback, name)
    if once and max_runs:
      raise ValueError('cannot set both once and max_runs')
    if max_runs is not None and max_runs < 1:
      raise ValueError(f'max_runs must be at least 1: {max_runs!r}')
    elif once:
      max_runs = 1
    self.priority = priority
    self.timeout = timeout
    self.max_runs = max_runs
    self.runs = 0
    self.app = None

  def cancel(self):
    if self.app:
      self.app.remove_signals(self)

  async def __call__(self, *args):
    timeout = asyncio.timeout(self.timeout)
    try:
      async with timeout:
        await self.callback(*args)
    except Exception:
      if timeout.expired():
        log.warning(f'signal handler {self.name!r} timed out after {self.timeout}s')
      else:
        log.exception(f'signal handler {self.name!r} errored')

class SignalWaiter:
  def __init__(self, app, name, priority = None, timeout = DEFAULT_WAITER_TIMEOUT):
    self.app = app
    self.name = name
    self.priority = priority
    self.timeout = timeout
    self.waiter_future = None
    self.waiter_done_future = None
    self.sender_done_future = None

  def cancel(self):
    if self.waiter_future and not self.waiter_future.done():
      self.waiter_future.set_exception(SignalCancelledError(f'cancelled waiting for signal {self.name!r}'))

  async def receive(self, is_async_with):
    if self.waiter_future:
      raise ValueError(f'waiter is already waiting for signal {self.name!r}')

    # 1. Set
    current_name = self.name
    waiter_future = self.app.loop.create_future()
    self.waiter_future = waiter_future
    self.app.signal_waiters.setdefault(current_name, []).append(self)

    # 2. Wait
    timer = None
    if self.timeout is not None:
      def check_timed_out():
        if not waiter_future.done():
          waiter_future.set_exception(SignalTimeoutError(f'timed out waiting for signal {current_name!r}'))
      timer = self.app.loop.call_later(self.timeout, check_timed_out)
    is_enter_success = False # never becomes true if wait() errors, like timed out or cancelled
    try:
      args, waiter_done_future, sender_done_future, release = await waiter_future
      is_enter_success = True
      return args
    finally:

      # 3. Reset
      if timer:
        timer.cancel()
      waiters = self.app.signal_waiters.get(current_name)
      if waiters and self in waiters: # dispatch didn't pop yet (no signal or mid sequential)
        waiters.remove(self)
        if not waiters:
          del self.app.signal_waiters[current_name]
      self.waiter_future = None

      # 4. Mark waiter as finished, if "async with:" is being used, it sets on __aexit__ instead
      if waiter_future.done() and not waiter_future.cancelled() and waiter_future.exception() is None:
        args, waiter_done_future, sender_done_future, release = waiter_future.result()
        if is_async_with:
          if is_enter_success:
            self.waiter_done_future = waiter_done_future # set by __aexit__ when "async with:" ends
            self.sender_done_future = sender_done_future
          elif waiter_done_future:
            waiter_done_future.set_result(None) # did not enter with:, __aexit__ won't run
        elif waiter_done_future: # None unless the sender waits for completion (send, send_each, defer_each)
          current_task = asyncio.current_task()
          assert current_task # always exists
          def finish(task):
            waiter_done_future.set_result(None)
          current_task.add_done_callback(finish)
        release()

  def __await__(self):
    return self.receive(False).__await__()

  async def __aenter__(self):
    return await self.receive(True)

  async def __aexit__(self, *exception):
    waiter_done_future, self.waiter_done_future = self.waiter_done_future, None
    sender_done_future, self.sender_done_future = self.sender_done_future, None
    if sender_done_future: # set in __aenter__/recv
      if waiter_done_future: # None unless the sender is wait = true
        waiter_done_future.set_result(None)
      await sender_done_future # let the sender continue first, outside the "with" runs after

class SignalModule:
  def __init__(self, app):
    self.app = app

  def spawn(self, coro, eager = False):
    task = asyncio.create_task(coro, eager_start = eager)
    self.app.tasks.add(task)
    task.add_done_callback(self.app.tasks.discard)
    return task

  async def dispatch(self, name, args, *, each, wait):
    """
    To explain the design of dispatch, there's basically 4 futures:
    1. waiter_future - when you do .wait(), the waiter waits on this.
    2. sender_future - the sender task waits for waiters in that step to at least yield before continuing the loop to the next step, helps with concurrency/seq logic
    3. waiter_done_future - the sender waits for the waiter to complete if dispatch(wait = True)
    4. sender_done_future - when you do "async with wait():", let sender continue first before you run outside the with
    """

    # This is segmented so "async with:" waiters don't continue outside until sender continues first
    sender_done_future = self.app.loop.create_future()
    handler_tasks = [] # spawned handler asyncio tasks
    finished_waiters = [] # holds waiters done futures

    try:

      # 1. Get handlers and waiters, handlers' run count incremented and waiters popped
      entries = []
      for handler in list(self.app.signal_handlers.get(name, ())): # make a list() copy because a cancel() changes list
        handler.runs += 1
        if handler.runs == handler.max_runs:
          handler.cancel()
        entries.append((handler.priority, handler))
      entries.extend((waiter.priority, waiter.waiter_future) for waiter in self.app.signal_waiters.pop(name, ()))
      entries.sort(key = lambda entry: (entry[0] is None, entry[0] or 0)) # sort by priority

      # 2. Organize into steps of a handler and waiters:
      # concurrent: [h1, [w1, w2], h2, [w3]]
      # sequential: [h1, [w1], [w2], h2, [w3]] (each)
      steps = []
      for priority, item in entries: # noqa: B007
        if isinstance(item, SignalHandler):
          steps.append(item)
        elif each or not steps or isinstance(steps[-1], SignalHandler):
          steps.append([item])
        else:
          steps[-1].append(item)

      # 3. Dispatch.
      for index, step in enumerate(steps):
        should_wait_to_finish = wait or (each and index < len(steps) - 1) # helps fire_each continue on last yield

        # 3.1. Run signal handler
        if isinstance(step, SignalHandler):
          if each and should_wait_to_finish:
            await step(*args)
          else:
            handler_tasks.append(self.spawn(step(*args), eager = True))

        # 3.2. Run signal waiter
        else:

          # 3.2.1. A waiter could've finished elsewhere if a previous task yielded/canceled/timed-out
          waiting_waiters = [waiter_future for waiter_future in step if not waiter_future.done()]
          if not waiting_waiters:
            continue

          # 3.2.2. We wait for the waiters to resume us when they're done
          sender_future = self.app.loop.create_future()
          remaining = len(waiting_waiters)
          def release():
            nonlocal remaining
            remaining -= 1
            if not remaining and not sender_future.done(): # a cancel will set it done # noqa: B023
              sender_future.set_result(None) # schedule sender_future to continue. # noqa: B023
          for waiter_future in waiting_waiters:
            waiter_done_future = None # create a waiter done future if we should wait
            if should_wait_to_finish:
              waiter_done_future = self.app.loop.create_future()
              finished_waiters.append(waiter_done_future)
            waiter_future.set_result((args, waiter_done_future, sender_done_future, release))
          await sender_future

          # 3.2.3. Wait for each waiter to finish in "each" mode
          if each and waiter_done_future and not waiter_done_future.done():
            await asyncio.wait({waiter_done_future})

      # 4. Wait for dispatch to finish in "wait" mode.
      if wait and (unfinished_callbacks := {item for item in (*handler_tasks, *finished_waiters) if not item.done()}):
        await asyncio.wait(unfinished_callbacks)

    # Make "async with:" waiters continue outside after we resume, even if cancelled
    finally:
      unfinished_handers = {task for task in handler_tasks if not task.done()}
      if unfinished_handers:
        def settle(task):
          unfinished_handers.discard(task)
          if not unfinished_handers:
            sender_done_future.set_result(None)
        for task in unfinished_handers.copy():
          task.add_done_callback(settle)
      else:
        sender_done_future.set_result(None) # set result schedules sender to continue

  async def fire(self, name, /, *args):
    await self.dispatch(name, args, each = False, wait = False)

  async def fire_each(self, name, /, *args):
    await self.dispatch(name, args, each = True, wait = False)

  async def send(self, name, /, *args):
    await self.dispatch(name, args, each = False, wait = True)

  async def send_each(self, name, /, *args):
    await self.dispatch(name, args, each = True, wait = True)

  async def defer(self, name, /, *args):
    self.spawn(self.dispatch(name, args, each = False, wait = False))

  async def defer_each(self, name, /, *args): # wait preferably keeps sender task alive til all done
    self.spawn(self.dispatch(name, args, each = True, wait = True))

  def wait(self, name, priority = None, timeout = DEFAULT_WAITER_TIMEOUT):
    return SignalWaiter(self.app, name, priority, timeout)

  def __call__(self, callback = None, *, name = None, priority = None, timeout = DEFAULT_HANDLER_TIMEOUT, max_runs = None, once = False):
    def wrap(callback):
      signal = SignalHandler(callback, name, priority, timeout, max_runs, once)
      self.app.add_signals(signal)
      return signal
    return wrap(callback) if callback else wrap

def signal(callback = None, *, name = None, priority = None, timeout = DEFAULT_HANDLER_TIMEOUT, max_runs = None, once = False):
  def wrap(callback):
    return SignalHandler(callback, name, priority, timeout, max_runs, once)
  return wrap(callback) if callback else wrap

class SignalMixin:
  def __init__(self, registrars):
    registrars[SignalHandler] = (self.add_signals, self.remove_signals)
    self.signal_handlers = {} # {name: [SignalHandler]}
    self.signal_waiters = {} # {name: [SignalWaiter]}
    self.signal = SignalModule(self)

  def add_signals(self, *signals):
    for signal in signals:
      if not isinstance(signal, SignalHandler):
        raise ValueError(f'not a signal handler: {signal!r}')
      if signal in self.signal_handlers.get(signal.name, ()):
        raise ValueError(f'signal handler already added: {signal.name}')
    for signal in signals:
      handlers = self.signal_handlers.setdefault(signal.name, [])
      handlers.append(signal)
      signal.app = self
      signal.runs = 0 # reset runs on re-register

  def remove_signals(self, *signals):
    for signal in signals:
      if not isinstance(signal, SignalHandler):
        raise ValueError(f'not a signal handler: {signal!r}')
    for signal in signals:
      handlers = self.signal_handlers.get(signal.name, ())
      if signal not in handlers:
        continue
      handlers.remove(signal)
      signal.app = None
      if not handlers:
        del self.signal_handlers[signal.name]
