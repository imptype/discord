from typing import Any
from .enums import ButtonStyle
from ..abc import Interactable

class Button(Interactable):
  """
  TODO

  Attributes:
    label: TODO
    style: TODO
    row: TODO
  """

  def __init__(self, label, *, style = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., row = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      label: TODO
      style: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      row: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  label: Any # TODO
  style: ButtonStyle
  row: Any # TODO

def button(label, *, style = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., row = ..., id = ...) -> Any: # TODO
  """
  TODO

  Args:
    label: TODO
    style: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    callback: TODO
    row: TODO
    id: TODO

  Returns:
    TODO
  """
