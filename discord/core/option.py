from ..abc import clean
from .enums import OptionType

class Choice:
  def __init__(self, name, value = None):
    self.name = name
    self.value = name if value is None else value

  def to_json(self):
    return {'name': str(self.name), 'value': self.value}

def format_choices(choices):
  return [choice if isinstance(choice, Choice) else Choice(choice) for choice in choices]

class Option:
  def __init__(self, type, name, description = None, *, required = True):
    self.type = OptionType(type)
    self.name = name
    self.description = description or name
    self.required = required

  def to_json(self):
    return clean({
      'type': self.type,
      'name': self.name,
      'description': self.description,
      'required': self.required
    })

class StringOption(Option):
  def __init__(self, name, description = None, *, required = True, choices = (),
    min_length = None, max_length = None, autocomplete = False):
    super().__init__(OptionType.STRING, name, description, required = required)
    self.choices = format_choices(choices)
    self.min_length = min_length
    self.max_length = max_length
    self.autocomplete = autocomplete

  def to_json(self):
    return clean({
      **super().to_json(),
      'choices': [choice.to_json() for choice in self.choices] or None,
      'min_length': self.min_length,
      'max_length': self.max_length,
      'autocomplete': self.autocomplete or None
    })

class IntegerOption(Option):
  def __init__(self, name, description = None, *, required = True, choices = (),
    min_value = None, max_value = None, autocomplete = False):
    super().__init__(OptionType.INTEGER, name, description, required = required)
    self.choices = format_choices(choices)
    self.min_value = min_value
    self.max_value = max_value
    self.autocomplete = autocomplete

  def to_json(self):
    return clean({
      **super().to_json(),
      'choices': [choice.to_json() for choice in self.choices] or None,
      'min_value': self.min_value,
      'max_value': self.max_value,
      'autocomplete': self.autocomplete or None
    })

class NumberOption(IntegerOption):
  def __init__(self, name, description = None, *, required = True, choices = (),
    min_value = None, max_value = None, autocomplete = False):
    super().__init__(name, description, required = required, choices = choices,
      min_value = min_value, max_value = max_value, autocomplete = autocomplete)
    self.type = OptionType.NUMBER

class BooleanOption(Option):
  def __init__(self, name, description = None, *, required = True):
    super().__init__(OptionType.BOOLEAN, name, description, required = required)

class UserOption(Option):
  def __init__(self, name, description = None, *, required = True):
    super().__init__(OptionType.USER, name, description, required = required)

class ChannelOption(Option):
  def __init__(self, name, description = None, *, required = True, channel_types = None):
    super().__init__(OptionType.CHANNEL, name, description, required = required)
    self.channel_types = channel_types

  def to_json(self):
    return clean({**super().to_json(), 'channel_types': self.channel_types})

class RoleOption(Option):
  def __init__(self, name, description = None, *, required = True):
    super().__init__(OptionType.ROLE, name, description, required = required)

class MentionableOption(Option):
  def __init__(self, name, description = None, *, required = True):
    super().__init__(OptionType.MENTIONABLE, name, description, required = required)

class AttachmentOption(Option):
  def __init__(self, name, description = None, *, required = True):
    super().__init__(OptionType.ATTACHMENT, name, description, required = required)