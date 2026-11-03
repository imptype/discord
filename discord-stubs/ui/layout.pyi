from typing import Any
from ..abc import Component
from .enums import SeparatorSpacing

class LayoutComponent(Component):
  """
  TODO

  Attributes:
    id: TODO
  """

  def __init__(self, *, id = ...) -> None: # TODO
    """
    TODO

    Args:
      id: TODO
    """

  id: Any # TODO

class ActionRow(LayoutComponent):
  """
  TODO

  Attributes:
    components: TODO
  """

  def __init__(self, *components, id = ...) -> None: # TODO
    """
    TODO

    Args:
      *components: TODO
      id: TODO
    """

  def children(self) -> Any: # TODO
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

  components: Any # TODO

class Section(LayoutComponent):
  """
  TODO

  Attributes:
    components: TODO
    accessory: TODO
  """

  def __init__(self, *components, accessory, id = ...) -> None: # TODO
    """
    TODO

    Args:
      *components: TODO
      accessory: TODO
      id: TODO
    """

  def children(self) -> Any: # TODO
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

  components: Any # TODO
  accessory: Any # TODO

class Separator(LayoutComponent):
  """
  TODO

  Attributes:
    divider: TODO
    spacing: TODO
  """

  def __init__(self, *, divider = ..., spacing = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      divider: TODO
      spacing: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  divider: Any # TODO
  spacing: SeparatorSpacing

class Container(LayoutComponent):
  """
  TODO

  Attributes:
    components: TODO
    accent_color: TODO
    spoiler: TODO
  """

  def __init__(self, *components, accent_color = ..., spoiler = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      *components: TODO
      accent_color: TODO
      spoiler: TODO
      id: TODO
    """

  def children(self) -> Any: # TODO
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

  components: Any # TODO
  accent_color: Any # TODO
  spoiler: Any # TODO

class Label(LayoutComponent):
  """
  TODO

  Attributes:
    component: TODO
    label: TODO
    description: TODO
  """

  def __init__(self, component, *, label, description = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      component: TODO
      label: TODO
      description: TODO
      id: TODO
    """

  def children(self) -> Any: # TODO
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

  component: Any # TODO
  label: Any # TODO
  description: Any # TODO
