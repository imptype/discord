"""
intents.py

You can define intents in 2 ways:
  intents = Intents.default() | Intents.message_content
or:
  intents = Intents.default()
  intents.message_content = True
"""

class IntentFlag:
  def __init__(self, bit):
    self.bit = bit

  def __set_name__(self, owner, name):
    self.name = name

  def __get__(self, instance, owner):
    if instance is None:
      return owner(self.bit) # Intents.guilds (class) vs intents.guilds (instance)
    return bool(instance.value & self.bit)

  def __set__(self, instance, value):
    if value:
      instance.value |= self.bit
    else:
      instance.value &= ~self.bit

class Intents:
  guilds = IntentFlag(1 << 0)
  guild_members = IntentFlag(1 << 1)
  guild_moderation = IntentFlag(1 << 2)
  guild_expressions = IntentFlag(1 << 3)
  guild_integrations = IntentFlag(1 << 4)
  guild_webhooks = IntentFlag(1 << 5)
  guild_invites = IntentFlag(1 << 6)
  guild_voice_states = IntentFlag(1 << 7)
  guild_presences = IntentFlag(1 << 8)
  guild_messages = IntentFlag(1 << 9)
  guild_message_reactions = IntentFlag(1 << 10)
  guild_message_typing = IntentFlag(1 << 11)
  direct_messages = IntentFlag(1 << 12)
  direct_message_reactions = IntentFlag(1 << 13)
  direct_message_typing = IntentFlag(1 << 14)
  message_content = IntentFlag(1 << 15)
  guild_scheduled_events = IntentFlag(1 << 16)
  auto_moderation_configuration = IntentFlag(1 << 20)
  auto_moderation_execution = IntentFlag(1 << 21)
  guild_message_polls = IntentFlag(1 << 24)
  direct_message_polls = IntentFlag(1 << 25)

  def __init__(self, value = 0):
    self.value = int(value)

  @classmethod
  def none(cls):
    return cls(0)

  @classmethod
  def all(cls):
    return cls(sum(flag.bit for flag in FLAGS))

  @classmethod
  def default(cls):
    return cls.all() & ~PRIVILEGED

  def __int__(self):
    return self.value

  def __or__(self, other):
    return Intents(self.value | int(other))

  def __and__(self, other):
    return Intents(self.value & int(other))

  def __invert__(self):
    return Intents(~self.value)

  def __str__(self):
    privileged = [flag.name for flag in FLAGS if flag.bit & self.value & PRIVILEGED.value]
    text = f'{len(privileged)} privileged'
    if privileged:
      text += ': ' + ', '.join(privileged)
    return f'intents={self.value} {self.value.bit_count()}/{len(FLAGS)} enabled ({text})'

FLAGS = tuple(flag for flag in vars(Intents).values() if isinstance(flag, IntentFlag))
PRIVILEGED = Intents.guild_members | Intents.guild_presences | Intents.message_content
