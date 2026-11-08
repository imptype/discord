import logging
from typing import Any

def ansi(hex_color) -> Any: ...

class Formatter(logging.Formatter):
  def format(self, record) -> Any: ...

class LogSettings:
  """
  TODO

  Attributes:
    JSON_INDENT: TODO
    TRUNCATE_AFTER: TODO
  """

  JSON_INDENT: Any # TODO
  TRUNCATE_AFTER: Any # TODO

  @classmethod
  def enable(cls, level = ..., json_indent = ..., truncate_after = ...) -> Any: # TODO
    """
    TODO

    Args:
      level: TODO
      json_indent: TODO
      truncate_after: TODO

    Returns:
      TODO
    """

  @classmethod
  def truncate(cls, text) -> Any: # TODO
    """
    TODO

    Args:
      text: TODO

    Returns:
      TODO
    """

  @classmethod
  def expand_json_strings(cls, value) -> Any: # TODO
    """
    TODO

    Args:
      value: TODO

    Returns:
      TODO
    """

  @classmethod
  def format_json(cls, data, redact = ...) -> Any: # TODO
    """
    TODO

    Args:
      data: TODO
      redact: TODO

    Returns:
      TODO
    """

enable_logs = LogSettings.enable
format_json = LogSettings.format_json
