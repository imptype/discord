from typing import Any
from ..abc import Handler

class ModalResult:
  """
  TODO

  Attributes:
    fields: TODO
  """

  def __init__(self, data) -> None: # TODO
    """
    TODO

    Args:
      data: TODO
    """

  def __getitem__(self, key) -> Any: # TODO
    """
    TODO

    Args:
      key: TODO

    Returns:
      TODO
    """

  fields: Any # TODO

class Modal(Handler):
  """
  TODO

  Attributes:
    title: TODO
    has_custom_id: TODO
    custom_id: TODO
    timeout: TODO
    components: TODO
  """

  def __init__(self, *components, title, custom_id = ..., timeout = ..., callback = ...) -> None: # TODO
    """
    TODO

    Args:
      *components: TODO
      title: TODO
      custom_id: TODO
      timeout: TODO
      callback: TODO
    """

  def bind(self, cog_instance) -> Any: # TODO
    """
    TODO

    Args:
      cog_instance: TODO

    Returns:
      TODO
    """

  def add_components(self, *components) -> Any: # TODO
    """
    TODO

    Args:
      *components: TODO

    Returns:
      TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  title: Any # TODO
  has_custom_id: Any # TODO
  custom_id: Any # TODO
  timeout: Any # TODO
  components: Any # TODO

def modal(callback = ..., *, title = ..., components = ..., custom_id = ..., timeout = ...) -> Any: # TODO
  """
  TODO

  Args:
    callback: TODO
    title: TODO
    components: TODO
    custom_id: TODO
    timeout: TODO

  Returns:
    TODO
  """
