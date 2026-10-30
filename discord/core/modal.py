import uuid
from typing import Any
from .. import MISSING
from ..abc import Handler
from ..ui import ComponentType, Label, TextDisplay

class ModalResult:
  def __init__(self, data):
    attachments = data.get('resolved', {}).get('attachments', {})
    self.fields = [] # [(label id, input id, custom_id, value)]
    for row in data['components']:
      inner = row.get('component')
      if inner is None: # text displays have no input
        continue
      if 'values' in inner:
        value = inner['values']
        if inner['type'] == ComponentType.FILE_UPLOAD:
          value = [attachments[id] for id in value]
      else:
        value = inner.get('value')
      self.fields.append((row.get('id'), inner.get('id'), inner['custom_id'], value))

  def __getitem__(self, key): # result[1] id, result['text'] custom_id, result[component]
    key = getattr(key, 'custom_id', key) # allows component indexing too
    for label_id, input_id, custom_id, value in self.fields:
      if key == custom_id or (isinstance(key, int) and key in (label_id, input_id)):
        return value
    raise KeyError(key)

class Modal(Handler):
  def __init__(self, *components, title, custom_id = None, timeout = MISSING, callback = None):
    super().__init__(callback)
    self.title = title
    self.has_custom_id = bool(custom_id)
    self.custom_id = custom_id or uuid.uuid4().hex
    self.timeout = timeout
    self.components = []
    if components:
      self.add_components(*components)

  def bind(self, cog_instance):
    modal = super().bind(cog_instance)
    modal.components = list(self.components)
    return modal

  def add_components(self, *components):
    for component in components:
      if not isinstance(component, (Label, TextDisplay)):
        raise ValueError(f'not a label or text display: {component!r}')
    self.components.extend(components)
    return self

  def to_json(self):
    return {
      'custom_id': self.custom_id,
      'title': self.title,
      'components': [component.to_json() for component in self.components]
    }

def modal(callback = None, *, title = None, components = (), custom_id = None, timeout = MISSING) -> Any:
  def wrap(callback):
    return Modal(*components, title = title or callback.__name__, custom_id = custom_id, timeout = timeout, callback = callback)
  return wrap(callback) if callback else wrap