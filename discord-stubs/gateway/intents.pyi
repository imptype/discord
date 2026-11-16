from enum import IntFlag
from typing import Any

class Intents(IntFlag):
  """
  TODO
  """


  @classmethod
  def none(cls) -> Any: # TODO
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

  @classmethod
  def all(cls) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
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

  def __init__(self, value = ...) -> None: # TODO
    """
    TODO

    Args:
      value: TODO
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

  value: Any # TODO

class IntentFlag:
  bit: Any # TODO

  def __init__(self, bit) -> None: ...

  def __set_name__(self, owner, name) -> Any: ...

  def __get__(self, instance, owner) -> Any: ...

  def __set__(self, instance, value) -> Any: ...
