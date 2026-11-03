from typing import Any
from .enums import ComponentType
from ..abc import Interactable

def format_defaults(kind, ids) -> Any: ...

class SelectOption:
  """
  TODO

  Attributes:
    label: TODO
    value: TODO
    description: TODO
    emoji: TODO
    default: TODO
  """

  def __init__(self, label, value = ..., *, description = ..., emoji = ..., default = ...) -> None: # TODO
    """
    TODO

    Args:
      label: TODO
      value: TODO
      description: TODO
      emoji: TODO
      default: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  label: Any # TODO
  value: Any # TODO
  description: Any # TODO
  emoji: Any # TODO
  default: Any # TODO

class BaseSelect(Interactable):
  """
  TODO

  Attributes:
    type: TODO
    placeholder: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
  """

  def __init__(self, type, *, placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      type: TODO
      placeholder: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  type: ComponentType
  placeholder: Any # TODO
  min_values: Any # TODO
  max_values: Any # TODO
  required: Any # TODO

class StringSelect(BaseSelect):
  """
  TODO

  Attributes:
    options: TODO
  """

  def __init__(self, *options, placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      *options: TODO
      placeholder: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  options: Any # TODO

class UserSelect(BaseSelect):
  """
  TODO

  Attributes:
    default_values: TODO
  """

  def __init__(self, *, default_values = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      default_values: TODO
      placeholder: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  default_values: Any # TODO

class RoleSelect(BaseSelect):
  """
  TODO

  Attributes:
    default_values: TODO
  """

  def __init__(self, *, default_values = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      default_values: TODO
      placeholder: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  default_values: Any # TODO

class MentionableSelect(BaseSelect):
  """
  TODO

  Attributes:
    default_users: TODO
    default_roles: TODO
  """

  def __init__(self, *, default_users = ..., default_roles = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      default_users: TODO
      default_roles: TODO
      placeholder: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  default_users: Any # TODO
  default_roles: Any # TODO

class ChannelSelect(BaseSelect):
  """
  TODO

  Attributes:
    channel_types: TODO
    default_values: TODO
  """

  def __init__(self, *, channel_types = ..., default_values = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      channel_types: TODO
      default_values: TODO
      placeholder: TODO
      min_values: TODO
      max_values: TODO
      required: TODO
      custom_id: TODO
      disabled: TODO
      timeout: TODO
      callback: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  channel_types: Any # TODO
  default_values: Any # TODO

def string_select(*options, placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> Any: # TODO
  """
  TODO

  Args:
    *options: TODO
    placeholder: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    callback: TODO
    id: TODO

  Returns:
    TODO
  """

def user_select(*, default_values = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> Any: # TODO
  """
  TODO

  Args:
    default_values: TODO
    placeholder: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    callback: TODO
    id: TODO

  Returns:
    TODO
  """

def role_select(*, default_values = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> Any: # TODO
  """
  TODO

  Args:
    default_values: TODO
    placeholder: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    callback: TODO
    id: TODO

  Returns:
    TODO
  """

def mentionable_select(*, default_users = ..., default_roles = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> Any: # TODO
  """
  TODO

  Args:
    default_users: TODO
    default_roles: TODO
    placeholder: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    callback: TODO
    id: TODO

  Returns:
    TODO
  """

def channel_select(*, channel_types = ..., default_values = ..., placeholder = ..., min_values = ..., max_values = ..., required = ..., custom_id = ..., disabled = ..., timeout = ..., callback = ..., id = ...) -> Any: # TODO
  """
  TODO

  Args:
    channel_types: TODO
    default_values: TODO
    placeholder: TODO
    min_values: TODO
    max_values: TODO
    required: TODO
    custom_id: TODO
    disabled: TODO
    timeout: TODO
    callback: TODO
    id: TODO

  Returns:
    TODO
  """
