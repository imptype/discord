from typing import Any

class BaseHandler:
  def __init__(self, callback = ..., name = ...) -> None: ...

  def bind(self, cog_instance) -> Any: ...

  callback: Any # TODO
  name: Any # TODO

class Handler(BaseHandler):
  async def callback(self, *args, **kwargs) -> Any: ...

  async def __call__(self, *args, **kwargs) -> Any: ...
