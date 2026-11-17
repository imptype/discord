from typing import Any

class RegistrarMixin:
  registrars: Any # TODO

  def __init__(self, **kwargs) -> None: ...

  def register(self, kind, add, remove) -> Any: ...

  async def run_registrars(self, handlers, remove = ...) -> Any: ...
