"""
log.py - use the "enable_logs()" function to enable debug logs.
"""

import json
import logging
import orjson

COLORS = {
  logging.DEBUG: '\033[90m',
  logging.INFO: '\033[36m',
  logging.WARNING: '\033[33m',
  logging.ERROR: '\033[91m',
  logging.CRITICAL: '\033[31m'
}
RESET = '\033[0m'

class Formatter(logging.Formatter):
  def format(self, record):
    return f'{COLORS.get(record.levelno, "")}{super().format(record)}{RESET}'

log = logging.getLogger('discord')
handler = logging.StreamHandler()
handler.setFormatter(Formatter(
  '[%(asctime)s][%(levelname)s][%(name)s] %(message)s',
  datefmt = '%H:%M:%S'
))
log.addHandler(handler)
log.propagate = False
log.setLevel(logging.INFO)

class LogSettings:
  JSON_INDENT = None
  TRUNCATE_AFTER = None

  @classmethod
  def enable(cls, level = logging.DEBUG, json_indent = None, truncate_after = None):
    cls.JSON_INDENT = json_indent
    cls.TRUNCATE_AFTER = truncate_after
    log.setLevel(level)

  @classmethod
  def truncate(cls, text):
    limit = cls.TRUNCATE_AFTER
    if limit is not None and len(text) > limit:
      return f'{text[:limit]}... (truncated, {len(text)} chars total)'
    return text

  @classmethod
  def expand_json_strings(cls, value):
    if isinstance(value, dict):
      return {key: cls.expand_json_strings(item) for key, item in value.items()}
    if isinstance(value, list):
      return [cls.expand_json_strings(item) for item in value]
    if isinstance(value, str) and value[:1] in ('[', '{'):
      try:
        return cls.expand_json_strings(orjson.loads(value))
      except orjson.JSONDecodeError:
        pass
    return value

  @classmethod
  def format_json(cls, data, redact = None):
    text = json.dumps(
      cls.expand_json_strings(data),
      ensure_ascii = False,
      indent = cls.JSON_INDENT
    )
    if redact:
      for old, new in redact.items():
        text = text.replace(old, new)
    return cls.truncate(text)

enable_logs = LogSettings.enable
format_json = LogSettings.format_json
