from typing import Any

MAX_BUTTONS_PER_ROW: int

class BaseView:
  """
  TODO

  Attributes:
    timeout: TODO
  """

  def __init__(self, *, timeout = ...) -> None: # TODO
    """
    TODO

    Args:
      timeout: TODO
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

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  timeout: Any # TODO

class View(BaseView):
  """
  TODO

  Attributes:
    rows: TODO
  """

  def __init__(self, *components, timeout = ...) -> None: # TODO
    """
    TODO

    Args:
      *components: TODO
      timeout: TODO
    """

  def children(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def add_interactables(self, *components) -> Any: # TODO
    """
    TODO

    Args:
      *components: TODO

    Returns:
      TODO
    """

  def add_buttons(self, *buttons) -> Any: # TODO
    """
    TODO

    Args:
      *buttons: TODO

    Returns:
      TODO
    """

  def add_select(self, select) -> Any: # TODO
    """
    TODO

    Args:
      select: TODO

    Returns:
      TODO
    """

  rows: Any # TODO

class LayoutView(BaseView):
  """
  TODO

  Attributes:
    components: TODO
  """

  def __init__(self, *components, timeout = ...) -> None: # TODO
    """
    TODO

    Args:
      *components: TODO
      timeout: TODO
    """

  def children(self) -> Any: # TODO
    """
    TODO

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

  components: Any # TODO
