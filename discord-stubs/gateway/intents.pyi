from typing import Any

class IntentFlag:
  bit: Any # TODO

  def __init__(self, bit) -> None: ...

  def __set_name__(self, owner, name) -> Any: ...

  def __get__(self, instance, owner) -> Any: ...

  def __set__(self, instance, value) -> Any: ...

class Intents:
  """
  TODO

  Attributes:
    guilds: TODO
    guild_members: TODO
    guild_moderation: TODO
    guild_expressions: TODO
    guild_integrations: TODO
    guild_webhooks: TODO
    guild_invites: TODO
    guild_voice_states: TODO
    guild_presences: TODO
    guild_messages: TODO
    guild_message_reactions: TODO
    guild_message_typing: TODO
    direct_messages: TODO
    direct_message_reactions: TODO
    direct_message_typing: TODO
    message_content: TODO
    guild_scheduled_events: TODO
    auto_moderation_configuration: TODO
    auto_moderation_execution: TODO
    guild_message_polls: TODO
    direct_message_polls: TODO
    value: TODO
  """

  guilds: IntentFlag
  guild_members: IntentFlag
  guild_moderation: IntentFlag
  guild_expressions: IntentFlag
  guild_integrations: IntentFlag
  guild_webhooks: IntentFlag
  guild_invites: IntentFlag
  guild_voice_states: IntentFlag
  guild_presences: IntentFlag
  guild_messages: IntentFlag
  guild_message_reactions: IntentFlag
  guild_message_typing: IntentFlag
  direct_messages: IntentFlag
  direct_message_reactions: IntentFlag
  direct_message_typing: IntentFlag
  message_content: IntentFlag
  guild_scheduled_events: IntentFlag
  auto_moderation_configuration: IntentFlag
  auto_moderation_execution: IntentFlag
  guild_message_polls: IntentFlag
  direct_message_polls: IntentFlag
  value: Any # TODO

  def __init__(self, value = ...) -> None: # TODO
    """
    TODO

    Args:
      value: TODO
    """

  @classmethod
  def none(cls) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  @classmethod
  def all(cls) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  @classmethod
  def default(cls) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def __int__(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  def __or__(self, other) -> Any: # TODO
    """
    TODO

    Args:
      other: TODO

    Returns:
      TODO
    """

  def __and__(self, other) -> Any: # TODO
    """
    TODO

    Args:
      other: TODO

    Returns:
      TODO
    """

  def __invert__(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """
