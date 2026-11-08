from typing import Any

DEFAULT_TIMEOUT: int

def describe(component) -> Any: ...

def is_class_in_cog(instance) -> Any: ...

def resolve_timeout(component, view = ...) -> Any: ...

def validate_timeout(component, view = ...) -> Any: ...

class ComponentMixin:
  """
  TODO

  Attributes:
    component_cache: TODO
    component_timers: TODO
    modal_cache: TODO
    modal_timers: TODO
    loop: TODO
  """

  component_cache: Any # TODO
  component_timers: Any # TODO
  modal_cache: Any # TODO
  modal_timers: Any # TODO
  loop: Any # TODO

  def __init__(self, registrars, loop) -> None: # TODO
    """
    TODO

    Args:
      registrars: TODO
      loop: TODO
    """

  def add_views(self, *views) -> Any: # TODO
    """
    TODO

    Args:
      *views: TODO

    Returns:
      TODO
    """

  def remove_views(self, *views) -> Any: # TODO
    """
    TODO

    Args:
      *views: TODO

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

  def remove_components(self, *components) -> Any: # TODO
    """
    TODO

    Args:
      *components: TODO

    Returns:
      TODO
    """

  def add_interactables(self, *interactables, view = ...) -> Any: # TODO
    """
    TODO

    Args:
      *interactables: TODO
      view: TODO

    Returns:
      TODO
    """

  def remove_interactables(self, *interactables) -> Any: # TODO
    """
    TODO

    Args:
      *interactables: TODO

    Returns:
      TODO
    """

  def add_modals(self, *modals) -> Any: # TODO
    """
    TODO

    Args:
      *modals: TODO

    Returns:
      TODO
    """

  def remove_modals(self, *modals) -> Any: # TODO
    """
    TODO

    Args:
      *modals: TODO

    Returns:
      TODO
    """

  async def run_component(self, payload, is_from_http) -> Any: # TODO
    """
    TODO

    Args:
      payload: TODO
      is_from_http: TODO

    Returns:
      TODO
    """

  async def run_modal(self, payload, is_from_http) -> Any: # TODO
    """
    TODO

    Args:
      payload: TODO
      is_from_http: TODO

    Returns:
      TODO
    """
