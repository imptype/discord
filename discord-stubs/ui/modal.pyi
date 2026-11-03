from typing import Any
from ..abc import Component
from .enums import TextInputStyle

class ModalInput(Component):
  """
  TODO

  Attributes:
    custom_id: TODO
    id: TODO
  """

  def __init__(self, *, custom_id = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      custom_id: TODO
      id: TODO
    """

  custom_id: Any # TODO
  id: Any # TODO

class TextInput(ModalInput):
  """
  TODO

  Attributes:
    style: TODO
    min_length: TODO
    max_length: TODO
    required: TODO
    value: TODO
    placeholder: TODO
  """

  def __init__(self, *, style = ..., min_length = ..., max_length = ..., required = ..., value = ..., placeholder = ..., custom_id = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      style: TODO
      min_length: TODO
      max_length: TODO
      required: TODO
      value: TODO
      placeholder: TODO
      custom_id: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  style: TextInputStyle
  min_length: Any # TODO
  max_length: Any # TODO
  required: Any # TODO
  value: Any # TODO
  placeholder: Any # TODO

class GroupOption:
  """
  TODO

  Attributes:
    label: TODO
    value: TODO
    description: TODO
    default: TODO
  """

  def __init__(self, label, value = ..., *, description = ..., default = ...) -> None: # TODO
    """
    TODO

    Args:
      label: TODO
      value: TODO
      description: TODO
      default: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  label: Any # TODO
  value: Any # TODO
  description: Any # TODO
  default: Any # TODO

class RadioGroup(ModalInput):
  """
  TODO

  Attributes:
    options: TODO
    required: TODO
  """

  def __init__(self, *options, required = ..., custom_id = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      *options: TODO
      required: TODO
      custom_id: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  options: Any # TODO
  required: Any # TODO

class CheckboxGroup(ModalInput):
  """
  TODO

  Attributes:
    options: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
  """

  def __init__(self, *options, min_values = ..., max_values = ..., required = ..., custom_id = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      *options: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  options: Any # TODO
  min_values: Any # TODO
  max_values: Any # TODO
  required: Any # TODO

class Checkbox(ModalInput):
  """
  TODO

  Attributes:
    default: TODO
  """

  def __init__(self, *, default = ..., custom_id = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      default: TODO
      custom_id: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  default: Any # TODO

class FileUpload(ModalInput):
  """
  TODO

  Attributes:
    min_values: TODO
    max_values: TODO
    required: TODO
    file_types: TODO
  """

  def __init__(self, *, min_values = ..., max_values = ..., required = ..., file_types = ..., custom_id = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      min_values: TODO
      max_values: TODO
      required: TODO
      file_types: TODO
      custom_id: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  min_values: Any # TODO
  max_values: Any # TODO
  required: Any # TODO
  file_types: Any # TODO
