from typing import Any
from collections.abc import Callable
from typing import Concatenate
from collections.abc import Coroutine
from ..abc import PartialModel

class BaseWebhook(PartialModel):
  """
  TODO

  Attributes:
    token: TODO
    http: TODO
  """

  def __init__(self, webhook_id, token = ..., app = ..., http = ...) -> None: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      token: TODO
      app: TODO
      http: TODO
    """

  def require_token(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def fetch_message(self, message_id, *, thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      message_id: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def edit_message(self, message_id, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      message_id: TODO
      content: TODO
      embed: TODO
      embeds: TODO
      file: TODO
      files: TODO
      view: TODO
      components: TODO
      flags: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  async def delete_message(self, message_id, *, thread_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      message_id: TODO
      thread_id: TODO

    Returns:
      TODO
    """

  token: Any # TODO
  http: Any # TODO

class PartialWebhook(BaseWebhook):
  """
  TODO
  """

  async def fetch(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  async def send(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., username = ..., avatar_url = ..., thread_id = ..., wait = ...) -> Any: # TODO
    """
    TODO

    Args:
      content: TODO
      embed: TODO
      embeds: TODO
      file: TODO
      files: TODO
      view: TODO
      components: TODO
      flags: TODO
      username: TODO
      avatar_url: TODO
      thread_id: TODO
      wait: TODO

    Returns:
      TODO
    """

  async def edit(self, *, name = ..., avatar = ..., channel_id = ...) -> Any: # TODO
    """
    TODO

    Args:
      name: TODO
      avatar: TODO
      channel_id: TODO

    Returns:
      TODO
    """

  async def delete(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  @classmethod
  def from_url(cls, url, *, app = ...) -> Any: # TODO
    """
    TODO

    Args:
      url: TODO
      app: TODO

    Returns:
      TODO
    """

class Webhook(PartialWebhook):
  """
  TODO

  Attributes:
    data: TODO
    type: TODO
    name: TODO
    avatar: TODO
    application_id: TODO
    guild_id: TODO
    channel_id: TODO
    guild: TODO
    channel: TODO
    user: TODO
  """

  def __init__(self, app, payload) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      payload: TODO
    """

  data: Any # TODO
  type: Any # TODO
  name: Any # TODO
  avatar: Any # TODO
  application_id: Any # TODO
  guild_id: Any # TODO
  channel_id: Any # TODO
  guild: Any # TODO
  channel: Any # TODO
  user: Any # TODO

class FollowupWebhook(BaseWebhook):
  """
  TODO
  """

  def __init__(self, app, application_id, token) -> None: # TODO
    """
    TODO

    Args:
      app: TODO
      application_id: TODO
      token: TODO
    """

  async def send(self, content = ..., *, embed = ..., embeds = ..., file = ..., files = ..., view = ..., components = ..., flags = ..., ephemeral = ..., thread_id = ..., wait = ...) -> Any: # TODO
    """
    TODO

    Args:
      content: TODO
      embed: TODO
      embeds: TODO
      file: TODO
      files: TODO
      view: TODO
      components: TODO
      flags: TODO
      ephemeral: TODO
      thread_id: TODO
      wait: TODO

    Returns:
      TODO
    """

type Method[**P, R] = Callable[Concatenate[Any, P], R]

def wrap_sync[**P, R](method: Method[P, Coroutine[Any, Any, R]]) -> Method[P, R]: ...

class SyncWebhook:
  """
  TODO

  Attributes:
    send: TODO
    fetch: TODO
    edit: TODO
    delete: TODO
    fetch_message: TODO
    edit_message: TODO
    delete_message: TODO
    webhook: TODO
    id: TODO
    token: TODO
  """

  def __init__(self, webhook_id, token = ...) -> None: # TODO
    """
    TODO

    Args:
      webhook_id: TODO
      token: TODO
    """

  send: Any # TODO
  fetch: Any # TODO
  edit: Any # TODO
  delete: Any # TODO
  fetch_message: Any # TODO
  edit_message: Any # TODO
  delete_message: Any # TODO

  @classmethod
  def from_url(cls, url) -> Any: # TODO
    """
    TODO

    Args:
      url: TODO

    Returns:
      TODO
    """

  webhook: PartialWebhook
  id: Any # TODO
  token: Any # TODO
