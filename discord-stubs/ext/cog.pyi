from typing import Any

class Cog:
  """
  TODO

  Attributes:
    app: TODO
    instances: TODO
  """

  def __init__(self, app) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
    """

  async def cog_load(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def cog_unload(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  app: Any # TODO
  instances: Any # TODO

class CogMixin:
  """
  TODO

  Attributes:
    registrars: TODO
    reload: TODO
    cogs: TODO
    cog_handlers: TODO
    extensions: TODO
    extension_files: TODO
    reload_task: TODO
  """

  def __init__(self, registrars, reload = ...) -> None: # TODO
    """
    TODO

    Args:
      registrars: TODO
      reload: TODO
    """

  async def run_registrars(self, handlers, remove = ...) -> Any: # TODO
    """
    TODO

    Args:
      handlers: TODO
      remove: TODO

    Returns:
      TODO
    """

  async def add_cogs(self, *cogs) -> Any: # TODO
    """
    TODO

    Args:
      *cogs: TODO

    Returns:
      TODO
    """

  async def remove_cogs(self, *cogs) -> Any: # TODO
    """
    TODO

    Args:
      *cogs: TODO

    Returns:
      TODO
    """

  async def load_extensions(self, *names) -> Any: # TODO
    """
    TODO

    Args:
      *names: TODO

    Returns:
      TODO
    """

  async def import_extensions(self, *names) -> Any: # TODO
    """
    TODO

    Args:
      *names: TODO

    Returns:
      TODO
    """

  async def unload_extensions(self, *names) -> Any: # TODO
    """
    TODO

    Args:
      *names: TODO

    Returns:
      TODO
    """

  async def watch_extensions(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  registrars: Any # TODO
  reload: Any # TODO
  cogs: Any # TODO
  cog_handlers: Any # TODO
  extensions: Any # TODO
  extension_files: Any # TODO
  reload_task: Any # TODO
