"""
modal.py - currently holds modal exclusive components.
"""

import uuid
from .abc import Component, clean
from .enums import ComponentType, TextInputStyle

class ModalInput(Component):
  def __init__(self, *, custom_id = None, id = None):
    self.custom_id = custom_id or uuid.uuid4().hex
    self.id = id

class TextInput(ModalInput):
  def __init__(
    self, *, style = TextInputStyle.SHORT, min_length = None, max_length = None, required = True,
    value = None, placeholder = None, custom_id = None, id = None
  ):
    super().__init__(custom_id = custom_id, id = id)
    self.style = TextInputStyle(style)
    self.min_length = min_length
    self.max_length = max_length
    self.required = required
    self.value = value
    self.placeholder = placeholder

  def to_json(self):
    return clean({
      'type': ComponentType.TEXT_INPUT,
      'id': self.id,
      'custom_id': self.custom_id,
      'style': self.style,
      'min_length': self.min_length,
      'max_length': self.max_length,
      'required': self.required,
      'value': self.value,
      'placeholder': self.placeholder
    })

class GroupOption:
  def __init__(self, label, value = None, *, description = None, default = False):
    self.label = label
    self.value = label if value is None else value
    self.description = description
    self.default = default

  def to_json(self):
    return clean({
      'label': self.label,
      'value': self.value,
      'description': self.description,
      'default': self.default
    })

class RadioGroup(ModalInput):
  def __init__(self, *options, required = True, custom_id = None, id = None):
    super().__init__(custom_id = custom_id, id = id)
    self.options = [option if isinstance(option, GroupOption) else GroupOption(option) for option in options]
    self.required = required

  def to_json(self):
    return clean({
      'type': ComponentType.RADIO_GROUP,
      'id': self.id,
      'custom_id': self.custom_id,
      'options': [option.to_json() for option in self.options],
      'required': self.required
    })

class CheckboxGroup(ModalInput):
  def __init__(self, *options, min_values = None, max_values = None, required = True, custom_id = None, id = None):
    super().__init__(custom_id = custom_id, id = id)
    self.options = [option if isinstance(option, GroupOption) else GroupOption(option) for option in options]
    self.min_values = min_values
    self.max_values = max_values
    self.required = required

  def to_json(self):
    return clean({
      'type': ComponentType.CHECKBOX_GROUP,
      'id': self.id,
      'custom_id': self.custom_id,
      'options': [option.to_json() for option in self.options],
      'min_values': self.min_values,
      'max_values': self.max_values,
      'required': self.required
    })

class Checkbox(ModalInput):
  def __init__(self, *, default = False, custom_id = None, id = None):
    super().__init__(custom_id = custom_id, id = id)
    self.default = default

  def to_json(self):
    return clean({
      'type': ComponentType.CHECKBOX,
      'id': self.id,
      'custom_id': self.custom_id,
      'default': self.default
    })

class FileUpload(ModalInput):
  def __init__(self, *, min_values = None, max_values = None, required = True, file_types = None, custom_id = None, id = None):
    super().__init__(custom_id = custom_id, id = id)
    self.min_values = min_values
    self.max_values = max_values
    self.required = required
    self.file_types = file_types # "image", "video", "audio" or extensions like ".pdf"

  def to_json(self):
    return clean({
      'type': ComponentType.FILE_UPLOAD,
      'id': self.id,
      'custom_id': self.custom_id,
      'min_values': self.min_values,
      'max_values': self.max_values,
      'required': self.required,
      'file_types': self.file_types
    })
