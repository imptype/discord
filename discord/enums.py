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

class HTTPStatus(IntEnum):
  OK_200 = 200
  NO_CONTENT_204 = 204
  UNAUTHORIZED_401 = 401
  NOT_FOUND_404 = 404
