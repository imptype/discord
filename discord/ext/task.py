"""
task.py - for background task loops.

Defining:
  @discord.task(seconds = 5)
  async def anything():
    ...
  app.add_tasks(anything)

  or @app.task

Controlling:
  anything.start() - starts the loop (use if autostart is false)
  anything.stop()  - stops the loop

Params:
  seconds = seconds to wait before repeating a task after it ends
  autostart = whether to start on app add/cog load, otherwise you start it with .start()

Task loops will continue errors (waits again).
"""

import asyncio
import logging
from ..abc import Handler

log = logging.getLogger(__name__)

class Task(Handler):
  def __init__(self, callback = None, name = None, *, seconds, autostart = True):
    super().__init__(callback, name)
    self.seconds = seconds
    self.autostart = autostart
    self.app = None
    self.runner = None

  def start(self):
    if not self.app or not self.app.started_at:
      raise ValueError(f'task {self.name!r} cannot start until it is added to an app that has started')
    if self.runner:
      raise ValueError(f'task {self.name!r} is already running')
    self.runner = self.app.loop.create_task(self.run())

  def stop(self):
    if self.runner:
      self.runner.cancel()
      self.runner = None

  async def run(self):
    while True:
      try:
        await self.callback()
      except Exception:
        log.exception(f'task {self.name!r} errored')
      await asyncio.sleep(self.seconds)

def task(callback = None, *, name = None, seconds, autostart = True):
  def wrap(callback):
    return Task(callback, name, seconds = seconds, autostart = autostart)
  return wrap(callback) if callback else wrap

class TaskMixin:
  def __init__(self, registrars):
    registrars[Task] = (self.add_tasks, self.remove_tasks)
    self.task_handlers = {} # {Task: None}, ordered
    self.tasks_started = False # is true when enter lifespan, so new tasks start now

  def task(self, callback = None, *, name = None, seconds, autostart = True):
    def wrap(callback):
      handler = Task(callback, name, seconds = seconds, autostart = autostart)
      self.add_tasks(handler)
      return handler
    return wrap(callback) if callback else wrap

  def add_tasks(self, *tasks):
    for handler in tasks:
      if not isinstance(handler, Task):
        raise ValueError(f'not a task: {handler!r}')
      if handler in self.task_handlers:
        raise ValueError(f'task already added: {handler.name}')
    for handler in tasks:
      self.task_handlers[handler] = None
      handler.app = self
      if self.tasks_started and handler.autostart:
        handler.start()

  def remove_tasks(self, *tasks):
    for handler in tasks:
      if not isinstance(handler, Task):
        raise ValueError(f'not a task: {handler!r}')
    for handler in tasks:
      if handler in self.task_handlers: # may not be added yet e.g. cog failed to load
        handler.stop()
        handler.app = None
        del self.task_handlers[handler]

  async def task_lifespan(self):
    self.tasks_started = True
    for handler in list(self.task_handlers):
      if handler.autostart and not handler.runner:
        handler.start()
    yield
    self.tasks_started = False
    runners = [handler.runner for handler in self.task_handlers if handler.runner]
    for handler in self.task_handlers:
      handler.stop()
    if runners: # wait for cancels to finish
      await asyncio.gather(*runners, return_exceptions = True)
