from typing import Any
from .enums import OptionType

class Choice:
  """
  TODO

  Attributes:
    name: TODO
    value: TODO
  """

  def __init__(self, name, value = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      value: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  name: Any # TODO
  value: Any # TODO

def format_choices(choices) -> Any: ...

class Option:
  """
  TODO

  Attributes:
    type: TODO
    name: TODO
    description: TODO
    required: TODO
  """

  def __init__(self, type, name, description = ..., *, required = ...) -> None: # TODO
    """
    TODO

    Args:
      type: TODO
      name: TODO
      description: TODO
      required: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  type: OptionType
  name: Any # TODO
  description: Any # TODO
  required: Any # TODO

class StringOption(Option):
  """
  TODO

  Attributes:
    choices: TODO
    min_length: TODO
    max_length: TODO
    autocomplete: TODO
  """

  def __init__(self, name, description = ..., *, required = ..., choices = ..., min_length = ..., max_length = ..., autocomplete = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
      choices: TODO
      min_length: TODO
      max_length: TODO
      autocomplete: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  choices: Any # TODO
  min_length: Any # TODO
  max_length: Any # TODO
  autocomplete: Any # TODO

class IntegerOption(Option):
  """
  TODO

  Attributes:
    choices: TODO
    min_value: TODO
    max_value: TODO
    autocomplete: TODO
  """

  def __init__(self, name, description = ..., *, required = ..., choices = ..., min_value = ..., max_value = ..., autocomplete = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
      choices: TODO
      min_value: TODO
      max_value: TODO
      autocomplete: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  choices: Any # TODO
  min_value: Any # TODO
  max_value: Any # TODO
  autocomplete: Any # TODO

class NumberOption(IntegerOption):
  """
  TODO

  Attributes:
    type: TODO
  """

  def __init__(self, name, description = ..., *, required = ..., choices = ..., min_value = ..., max_value = ..., autocomplete = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
      choices: TODO
      min_value: TODO
      max_value: TODO
      autocomplete: TODO
    """

  type: Any # TODO

class BooleanOption(Option):
  """
  TODO
  """

  def __init__(self, name, description = ..., *, required = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
    """

class UserOption(Option):
  """
  TODO
  """

  def __init__(self, name, description = ..., *, required = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
    """

class ChannelOption(Option):
  """
  TODO

  Attributes:
    channel_types: TODO
  """

  def __init__(self, name, description = ..., *, required = ..., channel_types = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
      channel_types: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  channel_types: Any # TODO

class RoleOption(Option):
  """
  TODO
  """

  def __init__(self, name, description = ..., *, required = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
    """

class MentionableOption(Option):
  """
  TODO
  """

  def __init__(self, name, description = ..., *, required = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
    """

class AttachmentOption(Option):
  """
  TODO
  """

  def __init__(self, name, description = ..., *, required = ...) -> None: # TODO
    """
    TODO

    Args:
      name: TODO
      description: TODO
      required: TODO
    """
