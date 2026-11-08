from typing import Any

class BaseHandler:
  callback: Any # TODO
  name: Any # TODO

  def __init__(self, callback = ..., name = ...) -> None: ...

  def bind(self, cog_instance) -> Any: ...

class Handler(BaseHandler):
  async def callback(self, *args, **kwargs) -> Any: ...

  async def __call__(self, *args, **kwargs) -> Any: ...
