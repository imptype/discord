"""
proxy.py - allows for "@app/bot.command.slash" syntax.
"""

from .command import BaseCommand

class CommandProxy:
  def __init__(self, app, target):
    self.app = app
    self.target = target

  # for namespace lookup app.command.slash or bot.command.slash
  def __getattr__(self, name):
    attr = getattr(self.target, name)

    def wrapper(*args, **kwargs):
      result = attr(*args, **kwargs)

      # decorator without brackets: @bot.command, @app/bot.command.slash
      if isinstance(result, BaseCommand):
        self.app.add_command(result)
        return result

      # decorator with brackets: @bot.command(...), @app/bot.command.slash(...)
      if callable(result):
        def decorator(func):
          command = result(func)
          self.app.add_command(command)
          return command
        return decorator

      return result
    return wrapper
