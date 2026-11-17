"""
scheduler.py - wrapper for asyncio.Task

app.spawn(coro)    - starts coro in the background immediately
app.defer(coro)    - starts coro in the background on next on async loop
app.delay(x, coro) - starts it after x seconds
"""

import asyncio
import logging

log = logging.getLogger(__name__)

def schedule(tasks, coro, eager_start = False):
  task = asyncio.create_task(coro, eager_start = eager_start)
  tasks.add(task)

  def callback(task):
    tasks.discard(task)
    if not task.cancelled() and (error := task.exception()):
      log.error(f'spawned task {task.get_name()!r} errored', exc_info = error)

  task.add_done_callback(callback)
  return task

class SchedulerMixin:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.tasks = set() # holds running asyncio tasks

  def spawn(self, coro):
    return schedule(self.tasks, coro, True)

  def defer(self, coro):
    return schedule(self.tasks, coro)

  def delay(self, seconds, coro):
    async def runner():
      await asyncio.sleep(seconds)
      await coro
    task = self.spawn(runner())
    task.add_done_callback(lambda task: coro.close())
    return task
