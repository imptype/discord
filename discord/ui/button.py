from .. import MISSING
from .abc import Interactable, clean
from .enums import ButtonStyle, ComponentType

class Button(Interactable):
  def __init__(self, label, *, style = ButtonStyle.PRIMARY, custom_id = None, disabled = False, timeout = MISSING, callback = None, row = None, id = None):
    if not label:
      raise ValueError('button label is required')
    super().__init__(custom_id = custom_id, disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.label = label
    self.style = ButtonStyle(style)
    self.row = row # action row index using regular View

  def to_json(self):
    return clean({
      'type': ComponentType.BUTTON,
      'id': self.id,
      'style': self.style,
      'label': self.label,
      'custom_id': self.custom_id,
      'disabled': self.disabled
    })

def button(label, *, style = ButtonStyle.PRIMARY, custom_id = None, disabled = False, timeout = MISSING, callback = None, row = None, id = None):
  def wrap(func):
    return Button(label, style = style, custom_id = custom_id, disabled = disabled, timeout = timeout, callback = func, row = row, id = id)
  return wrap(callback) if callback is not None else wrap
