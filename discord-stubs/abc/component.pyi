from typing import Any
from .handler import Handler

def clean(data) -> Any: ...

class Component:
  """
  TODO
  """

  def children(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def walk(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def interactables(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def to_json(self) -> Any:
    """
    TODO

    Returns:
      TODO
    """

class Interactable(Component, Handler):
  """
  TODO

  Attributes:
    has_custom_id: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    id: TODO
  """

  has_custom_id: Any # TODO
  custom_id: Any # TODO
  disabled: Any # TODO
  timeout: Any # TODO
  id: Any # TODO

  def __init__(self, *, custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """
