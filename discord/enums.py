from enum import IntEnum

class InteractionType(IntEnum):
  PING = 1
  APPLICATION_COMMAND = 2

class ResponseType(IntEnum):
  PONG = 1
  MESSAGE = 4
  DEFERRED_MESSAGE = 5

class CommandType(IntEnum):
  CHAT_INPUT = 1
