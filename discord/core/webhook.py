from typing import Any, Concatenate
from collections.abc import Callable, Coroutine
from .. import MISSING
from ..models import Message
from .http import HTTPClient
from ..models.abc import PartialModel
from ..models.enums import RESPONSE_MESSAGE_FLAGS
from ..models.params import edit_params, send_params

class BaseWebhook(PartialModel):
  def __init__(self, webhook_id, token = None, app = None, http = None):
    super().__init__(app, webhook_id)
    self.token = token
    self.http = http or (app.http if app else HTTPClient.implicit())

  def require_token(self):
    if not self.token:
      raise ValueError('webhook token is required for this action')
    return self.token

  async def fetch_message(self, message_id, *, thread_id = None):
    data = await self.http.get_webhook_message(self.id, self.require_token(), message_id, thread_id = thread_id)
    return Message(self.app, data)

  async def edit_message(
    self, message_id, content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING,
    files = MISSING, view = MISSING, components = MISSING, flags = MISSING, thread_id = None
  ):
    token = self.require_token()
    body = edit_params(content, embed = embed, embeds = embeds, file = file,
      files = files, view = view, components = components, flags = flags)
    if self.app:
      if view not in (MISSING, None):
        self.app.add_views(view)
      if components is not MISSING and components:
        self.app.add_components(*components)
    data = await self.http.update_webhook_message(
      self.id, token, message_id, body,
      thread_id = thread_id,
      with_components = True if 'components' in body.body else None
    )
    return Message(self.app, data)

  async def delete_message(self, message_id, *, thread_id = None):
    await self.http.delete_webhook_message(self.id, self.require_token(), message_id, thread_id = thread_id)

class PartialWebhook(BaseWebhook):
  async def fetch(self):
    if self.token:
      data = await self.http.get_webhook_by_token(self.id, self.token)
    else:
      data = await self.http.get_webhook(self.id)
    return self.app.model.webhook(data) if self.app else data

  async def send(
    self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None,
    components = None, flags = None, username = None, avatar_url = None, thread_id = None, wait = False
  ):
    token = self.require_token()
    body = send_params(content, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags)
    if username is not None:
      body.body['username'] = username
    if avatar_url is not None:
      body.body['avatar_url'] = avatar_url
    if self.app:
      if view is not None:
        self.app.add_views(view)
      if components:
        self.app.add_components(*components)
    data = await self.http.execute_webhook(
      self.id, token, body,
      wait = True if wait else None,
      thread_id = thread_id,
      with_components = True if 'components' in body.body else None
    )
    if wait:
      return Message(self.app, data)

  async def edit(self, *, name = MISSING, avatar = MISSING, channel_id = MISSING):
    fields = {'name': name, 'avatar': avatar, 'channel_id': channel_id}
    body = {key: value for key, value in fields.items() if value is not MISSING}
    if self.token:
      data = await self.http.update_webhook_by_token(self.id, self.token, body)
    else:
      data = await self.http.update_webhook(self.id, body)
    return self.app.model.webhook(data) if self.app else data

  async def delete(self):
    if self.token:
      await self.http.delete_webhook_by_token(self.id, self.token)
    else:
      await self.http.delete_webhook(self.id)

  @classmethod
  def from_url(cls, url, *, app = None):
    return cls(*url.split('/')[-2:], app = app)

class Webhook(PartialWebhook):
  def __init__(self, app, payload):
    super().__init__(payload['id'], payload.get('token'), app = app)
    self.data = payload
    self.type = payload.get('type')
    self.name = payload.get('name')
    self.avatar = payload.get('avatar')
    self.application_id = payload.get('application_id')
    self.guild_id = payload.get('guild_id')
    self.channel_id = payload.get('channel_id')
    self.guild = app.model.partial_guild(self.guild_id) if self.guild_id else None
    self.channel = app.model.partial_channel(self.channel_id, self.guild) if self.channel_id else None
    self.user = app.model.user(payload['user']) if payload.get('user') else None # creator, not sent with token

class FollowupWebhook(BaseWebhook):
  def __init__(self, app, application_id, token):
    super().__init__(application_id, token, app = app)

  async def send(
    self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None,
    components = None, flags = None, ephemeral = False, thread_id = None, wait = False
  ):
    body = send_params(content, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags, ephemeral = ephemeral, allowed = RESPONSE_MESSAGE_FLAGS)
    if view is not None:
      self.app.add_views(view)
    if components:
      self.app.add_components(*components)
    data = await self.http.execute_webhook(
      self.id, self.token, body,
      wait = True if wait else None,
      thread_id = thread_id,
      with_components = True if 'components' in body.body else None
    )
    if wait:
      return self.app.model.message(data)

type Method[**P, R] = Callable[Concatenate[Any, P], R]
def wrap_sync[**P, R](method: Method[P, Coroutine[Any, Any, R]]) -> Method[P, R]:
  def wrapper(self, *args, **kwargs):
    try:
      method(self.webhook, *args, **kwargs).send(None)
    except StopIteration as stop:
      return stop.value
    raise RuntimeError('coroutine tried to suspend')
  return wrapper

class SyncWebhook:
  def __init__(self, webhook_id, token = None):
    self.webhook = PartialWebhook(webhook_id, token, http = HTTPClient(use_sync = True))
    self.id = self.webhook.id
    self.token = token

  send = wrap_sync(PartialWebhook.send)
  fetch = wrap_sync(PartialWebhook.fetch)
  edit = wrap_sync(PartialWebhook.edit)
  delete = wrap_sync(PartialWebhook.delete)
  fetch_message = wrap_sync(PartialWebhook.fetch_message)
  edit_message = wrap_sync(PartialWebhook.edit_message)
  delete_message = wrap_sync(PartialWebhook.delete_message)

  @classmethod
  def from_url(cls, url):
    return cls(*url.split('/')[-2:])
