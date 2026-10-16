"""
proxy.py - allows for "@app/bot.command.slash" syntax.
"""

from . import command

class CommandProxy:
  def __init__(self, app, module):
    self.app = app
    self.module = module

  def __getattr__(self, name):
    attr = getattr(self.module, name)
    if not callable(attr):
      return attr

    def wrapper(*args, **kwargs):
      result = attr(*args, **kwargs)

      if isinstance(result, command.Command):
        self.app.add_command(result)
        return result

      if callable(result):
        def decorator(func):
          command = result(func)
          self.app.add_command(command)
          return command
        return decorator

      return result
    return wrapper
