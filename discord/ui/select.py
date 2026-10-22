from .. import MISSING
from .enums import ComponentType
from .abc import Interactable, clean

def format_defaults(kind, ids):
  return [{'id': str(id), 'type': kind} for id in ids] or None

class SelectOption:
  def __init__(self, label, value = None, *, description = None, emoji = None, default = False):
    self.label = label
    self.value = label if value is None else value
    self.description = description
    self.emoji = emoji # unicode str or {'name', 'id', 'animated'} dict (until Emoji implemented)
    self.default = default

  def to_json(self):
    emoji = {'name': self.emoji} if isinstance(self.emoji, str) else self.emoji
    return clean({
      'label': self.label,
      'value': self.value,
      'description': self.description,
      'emoji': emoji,
      'default': self.default
    })

class BaseSelect(Interactable):
  def __init__(self, type, *, placeholder = None, min_values = 1, max_values = 1, required = True,
    custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    super().__init__(custom_id = custom_id, disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.type = ComponentType(type)
    self.placeholder = placeholder
    self.min_values = min_values
    self.max_values = max_values
    self.required = required # modals only, ignored in messages

  def to_json(self):
    return clean({
      'type': self.type,
      'id': self.id,
      'custom_id': self.custom_id,
      'placeholder': self.placeholder,
      'min_values': self.min_values,
      'max_values': self.max_values,
      'required': self.required,
      'disabled': self.disabled or None # modals error on disabled
    })

class StringSelect(BaseSelect):
  def __init__(self, *options, placeholder = None, min_values = 1, max_values = 1, required = True,
    custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    super().__init__(ComponentType.STRING_SELECT, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.options = [option if isinstance(option, SelectOption) else SelectOption(option) for option in options]

  def to_json(self):
    return {**super().to_json(), 'options': [option.to_json() for option in self.options]}

class UserSelect(BaseSelect):
  def __init__(self, *, default_values = (), placeholder = None, min_values = 1, max_values = 1, required = True,
    custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    super().__init__(ComponentType.USER_SELECT, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.default_values = default_values

  def to_json(self):
    return clean({**super().to_json(), 'default_values': format_defaults('user', self.default_values)})

class RoleSelect(BaseSelect):
  def __init__(self, *, default_values = (), placeholder = None, min_values = 1, max_values = 1, required = True,
    custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    super().__init__(ComponentType.ROLE_SELECT, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.default_values = default_values

  def to_json(self):
    return clean({**super().to_json(), 'default_values': format_defaults('role', self.default_values)})

class MentionableSelect(BaseSelect):
  def __init__(self, *, default_users = (), default_roles = (), placeholder = None, min_values = 1,
    max_values = 1, required = True, custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    super().__init__(ComponentType.MENTIONABLE_SELECT, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.default_users = default_users
    self.default_roles = default_roles

  def to_json(self):
    values = [
      *(format_defaults('user', self.default_users) or []),
      *(format_defaults('role', self.default_roles) or [])
    ]
    return clean({**super().to_json(), 'default_values': values or None})

class ChannelSelect(BaseSelect):
  def __init__(self, *, channel_types = None, default_values = (), placeholder = None, min_values = 1,
    max_values = 1, required = True, custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
    super().__init__(ComponentType.CHANNEL_SELECT, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = callback, id = id)
    self.channel_types = channel_types
    self.default_values = default_values

  def to_json(self):
    return clean({
      **super().to_json(),
      'channel_types': self.channel_types,
      'default_values': format_defaults('channel', self.default_values)
    })

def string_select(*options, placeholder = None, min_values = 1, max_values = 1, required = True,
  custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
  def wrap(func):
    return StringSelect(*options, placeholder = placeholder, min_values = min_values, max_values = max_values,
      required = required, custom_id = custom_id, disabled = disabled, timeout = timeout, callback = func, id = id)
  return wrap(callback) if callback is not None else wrap

def user_select(*, default_values = (), placeholder = None, min_values = 1, max_values = 1, required = True,
  custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
  def wrap(func):
    return UserSelect(default_values = default_values, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = func, id = id)
  return wrap(callback) if callback is not None else wrap

def role_select(*, default_values = (), placeholder = None, min_values = 1, max_values = 1, required = True,
  custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
  def wrap(func):
    return RoleSelect(default_values = default_values, placeholder = placeholder,
      min_values = min_values, max_values = max_values, required = required, custom_id = custom_id,
      disabled = disabled, timeout = timeout, callback = func, id = id)
  return wrap(callback) if callback is not None else wrap

def mentionable_select(*, default_users = (), default_roles = (), placeholder = None, min_values = 1,
  max_values = 1, required = True, custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
  def wrap(func):
    return MentionableSelect(default_users = default_users, default_roles = default_roles,
      placeholder = placeholder, min_values = min_values, max_values = max_values, required = required,
      custom_id = custom_id, disabled = disabled, timeout = timeout, callback = func, id = id)
  return wrap(callback) if callback is not None else wrap

def channel_select(*, channel_types = None, default_values = (), placeholder = None, min_values = 1,
  max_values = 1, required = True, custom_id = None, disabled = False, timeout = MISSING, callback = None, id = None):
  def wrap(func):
    return ChannelSelect(channel_types = channel_types, default_values = default_values,
      placeholder = placeholder, min_values = min_values, max_values = max_values, required = required,
      custom_id = custom_id, disabled = disabled, timeout = timeout, callback = func, id = id)
  return wrap(callback) if callback is not None else wrap
