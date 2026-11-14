from typing import Any
from nacl.signing import VerifyKey
from ..core import AppBase

class App(AppBase):
  verify_key: VerifyKey
  pending_interactions: Any # TODO

  def __init__(self, public_key, token = ..., application_id = ..., reload = ...) -> None: ...

  def run(self, host = ..., port = ...) -> Any: ...

  async def run_lifespan(self, receive, send) -> Any: ...

  async def respond(self, send, status, obj = ...) -> Any: ...

  async def __call__(self, scope, receive, send) -> Any: ...
