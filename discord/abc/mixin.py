import asyncio
from typing import cast

class RegistrarMixin:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.registrars = {} # {kind: (add, remove)}, for CogMixin (cog loads)

class LoopMixin:
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.loop = cast(asyncio.AbstractEventLoop, None) # set by startup_lifespans
