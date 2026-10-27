import uuid
from typing import Any
from .. import MISSING

DEFAULT_TIMEOUT = 180

def clean(data):
  return {key: value for key, value in data.items() if value is not None}

class Component:
  def children(self):
    return []

  def walk(self):
    yield self
    for child in self.children():
      yield from child.walk()

  def interactables(self):
    return [component for component in self.walk() if isinstance(component, Interactable)]

  def to_json(self) -> Any:
    pass

class Interactable(Component):
  def __init__(self, *, custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    self.has_custom_id = bool(custom_id) # helps debug if it needs to be persistent
    self.custom_id = custom_id or uuid.uuid4().hex
    self.disabled = disabled
    self.timeout = timeout
    if callback is not None: # skipped for None so the class-level callback() isn't shadowed
      self.callback = callback
    self.id = id

  async def callback(self, interaction):
    raise NotImplementedError(f'{type(self).__name__} is missing a callback!')

  async def __call__(self, interaction):
    return await self.callback(interaction)
