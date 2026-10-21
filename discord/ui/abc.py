import uuid
from .. import MISSING

DEFAULT_TIMEOUT = 180

class Component:
  def children(self):
    return []

  def walk(self):
    yield self
    for child in self.children():
      yield from child.walk()

  def interactables(self):
    return [component for component in self.walk() if isinstance(component, Interactable)]

  def to_json(self) -> dict: ...

class Interactable(Component):
  def __init__(self, *, custom_id = None, disabled = False, timeout = MISSING, callback = None):
    self.has_custom_id = bool(custom_id)
    self.custom_id = custom_id or uuid.uuid4().hex
    self.disabled = disabled
    self.timeout = timeout
    self.callback = callback

  async def __call__(self, interaction):
    if self.callback:
      return await self.callback(self, interaction)
