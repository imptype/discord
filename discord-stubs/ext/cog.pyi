from typing import Any

SETUP: str
TEARDOWN: str
RELOAD_INTERVAL: int

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
  def __init__(self, registrars, reload = ...) -> None: ...

  async def run_registrars(self, handlers, remove = ...) -> Any: ...

  async def add_cogs(self, *cogs) -> Any: ...

  async def remove_cogs(self, *cogs) -> Any: ...

  async def load_extensions(self, *names) -> Any: ...

  async def import_extensions(self, *names) -> Any: ...

  async def unload_extensions(self, *names) -> Any: ...

  async def watch_extensions(self) -> Any: ...

  registrars: Any
  reload: Any
  cogs: Any
  cog_handlers: Any
  extensions: Any
  extension_files: Any
  reload_task: Any
