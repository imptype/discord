"""
events.py - lets you prefix a function name with on_ so MESSAGE_CREATE is on_message_create too.
"""

from enum import Enum, StrEnum
from inspect import Parameter, signature
from functools import cached_property
from ..abc import Handler
from .intents import Intents

class CustomEvent(StrEnum): # not sent by the gateway
  ANY_EVENT = 'ANY_EVENT'
  FIRST_READY = 'FIRST_READY'

class EventIntents(Enum):
  READY = None
  RESUMED = None
  USER_UPDATE = None
  INTERACTION_CREATE = None
  APPLICATION_COMMAND_PERMISSIONS_UPDATE = None
  VOICE_SERVER_UPDATE = None

  ENTITLEMENT_CREATE = None
  ENTITLEMENT_UPDATE = None
  ENTITLEMENT_DELETE = None

  SUBSCRIPTION_CREATE = None
  SUBSCRIPTION_UPDATE = None
  SUBSCRIPTION_DELETE = None

  GUILD_CREATE = Intents.guilds
  GUILD_UPDATE = Intents.guilds
  GUILD_DELETE = Intents.guilds
  GUILD_ROLE_CREATE = Intents.guilds
  GUILD_ROLE_UPDATE = Intents.guilds
  GUILD_ROLE_DELETE = Intents.guilds

  CHANNEL_CREATE = Intents.guilds
  CHANNEL_UPDATE = Intents.guilds
  CHANNEL_DELETE = Intents.guilds
  CHANNEL_PINS_UPDATE = Intents.guilds | Intents.direct_messages

  THREAD_CREATE = Intents.guilds
  THREAD_UPDATE = Intents.guilds
  THREAD_DELETE = Intents.guilds
  THREAD_LIST_SYNC = Intents.guilds
  THREAD_MEMBER_UPDATE = Intents.guilds
  THREAD_MEMBERS_UPDATE = Intents.guilds | Intents.guild_members

  STAGE_INSTANCE_CREATE = Intents.guilds
  STAGE_INSTANCE_UPDATE = Intents.guilds
  STAGE_INSTANCE_DELETE = Intents.guilds

  GUILD_MEMBER_ADD = Intents.guild_members
  GUILD_MEMBER_UPDATE = Intents.guild_members
  GUILD_MEMBER_REMOVE = Intents.guild_members

  GUILD_AUDIT_LOG_ENTRY_CREATE = Intents.guild_moderation
  GUILD_BAN_ADD = Intents.guild_moderation
  GUILD_BAN_REMOVE = Intents.guild_moderation

  GUILD_EMOJIS_UPDATE = Intents.guild_expressions
  GUILD_STICKERS_UPDATE = Intents.guild_expressions
  GUILD_SOUNDBOARD_SOUND_CREATE = Intents.guild_expressions
  GUILD_SOUNDBOARD_SOUND_UPDATE = Intents.guild_expressions
  GUILD_SOUNDBOARD_SOUND_DELETE = Intents.guild_expressions
  GUILD_SOUNDBOARD_SOUNDS_UPDATE = Intents.guild_expressions

  GUILD_INTEGRATIONS_UPDATE = Intents.guild_integrations
  INTEGRATION_CREATE = Intents.guild_integrations
  INTEGRATION_UPDATE = Intents.guild_integrations
  INTEGRATION_DELETE = Intents.guild_integrations

  WEBHOOKS_UPDATE = Intents.guild_webhooks

  INVITE_CREATE = Intents.guild_invites
  INVITE_DELETE = Intents.guild_invites

  VOICE_CHANNEL_EFFECT_SEND = Intents.guild_voice_states
  VOICE_STATE_UPDATE = Intents.guild_voice_states

  PRESENCE_UPDATE = Intents.guild_presences

  MESSAGE_CREATE = Intents.guild_messages | Intents.direct_messages
  MESSAGE_UPDATE = Intents.guild_messages | Intents.direct_messages
  MESSAGE_DELETE = Intents.guild_messages | Intents.direct_messages
  MESSAGE_DELETE_BULK = Intents.guild_messages

  MESSAGE_REACTION_ADD = Intents.guild_message_reactions | Intents.direct_message_reactions
  MESSAGE_REACTION_REMOVE = Intents.guild_message_reactions | Intents.direct_message_reactions
  MESSAGE_REACTION_REMOVE_ALL = Intents.guild_message_reactions | Intents.direct_message_reactions
  MESSAGE_REACTION_REMOVE_EMOJI = Intents.guild_message_reactions | Intents.direct_message_reactions

  TYPING_START = Intents.guild_message_typing | Intents.direct_message_typing

  GUILD_SCHEDULED_EVENT_CREATE = Intents.guild_scheduled_events
  GUILD_SCHEDULED_EVENT_UPDATE = Intents.guild_scheduled_events
  GUILD_SCHEDULED_EVENT_DELETE = Intents.guild_scheduled_events
  GUILD_SCHEDULED_EVENT_USER_ADD = Intents.guild_scheduled_events
  GUILD_SCHEDULED_EVENT_USER_REMOVE = Intents.guild_scheduled_events

  AUTO_MODERATION_RULE_CREATE = Intents.auto_moderation_configuration
  AUTO_MODERATION_RULE_UPDATE = Intents.auto_moderation_configuration
  AUTO_MODERATION_RULE_DELETE = Intents.auto_moderation_configuration
  AUTO_MODERATION_ACTION_EXECUTION = Intents.auto_moderation_execution

  MESSAGE_POLL_VOTE_ADD = Intents.guild_message_polls | Intents.direct_message_polls
  MESSAGE_POLL_VOTE_REMOVE = Intents.guild_message_polls | Intents.direct_message_polls

class Event(Handler):
  def __init__(self, callback = None, name: str | None = None):
    super().__init__(callback, name)
    event_name = self.name
    is_from_function = callback and not name and event_name and event_name == getattr(callback, '__name__', None)
    if is_from_function:
      if not event_name.startswith('on_'):
        raise ValueError(f'event function name must start with on_: {event_name}')
      event_name = event_name.removeprefix('on_')
    self.gateway_name = event_name and event_name.upper()

  @cached_property
  def count(self): # allows for optional args
    kinds = [parameter.kind for parameter in signature(self.callback).parameters.values()]
    if Parameter.VAR_POSITIONAL in kinds:
      return None
    return sum(kind < Parameter.VAR_POSITIONAL for kind in kinds)

  async def __call__(self, *args):
    return await self.callback(*args[:self.count])

def event(callback = None, *, name = None):
  def wrap(callback):
    return Event(callback, name)
  return wrap(callback) if callback else wrap
