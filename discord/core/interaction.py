from .. import MISSING
from .enums import ResponseType
from ..models.params import Payload, edit_params, send_params
from ..models.enums import MessageFlags, RESPONSE_MESSAGE_FLAGS

class InteractionResponse:
  def __init__(self, interaction):
    self.interaction = interaction
    self.app = interaction.app
    self.body = None # returned to discord when the interaction came from http
    self.responded = False

  async def create(self, type, data = None): # data is a Payload, json or None
    if self.responded:
      raise ValueError('interaction was already responded to')
    body = {'type': type}
    files = ()
    if isinstance(data, Payload):
      body['data'] = data.body
      files = data.files
    elif data is not None:
      body['data'] = data
    payload = Payload(body, files)
    self.responded = True
    if self.interaction.is_from_http:
      self.body = payload # hook so server.handler for HTTP bots can reach it
    else:
      await self.app.http.create_interaction_response(self.interaction.id, self.interaction.token, payload)

class MessageMixin(InteractionResponse):
  async def send(self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None):
    data = send_params(content, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags, allowed = RESPONSE_MESSAGE_FLAGS)
    if view is not None:
      self.app.add_views(view)
    if components:
      self.app.add_components(*components)
    await self.create(ResponseType.MESSAGE, data)

  async def defer(self, *, ephemeral = False):
    data = {'flags': int(MessageFlags.EPHEMERAL)} if ephemeral else None
    await self.create(ResponseType.DEFERRED_MESSAGE, data)

  async def premium_required(self): # deprecated
    await self.create(ResponseType.PREMIUM_REQUIRED)

  async def launch_activity(self):
    await self.create(ResponseType.LAUNCH_ACTIVITY)

class ModalMixin(InteractionResponse):
  async def send_modal(self, modal):
    self.app.add_modals(modal)
    await self.create(ResponseType.MODAL, modal.to_json())

class UpdateMixin(InteractionResponse):
  async def update(self, content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING, view = MISSING, components = MISSING, flags = MISSING):
    data = edit_params(content, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags)
    if view not in (MISSING, None):
      self.app.add_views(view)
    if components is not MISSING and components:
      self.app.add_components(*components)
    await self.create(ResponseType.UPDATE_MESSAGE, data)

  async def defer_update(self):
    await self.create(ResponseType.DEFERRED_UPDATE_MESSAGE)

class CommandResponse(MessageMixin, ModalMixin):
  pass
class ComponentResponse(MessageMixin, ModalMixin, UpdateMixin):
  pass
class ModalResponse(MessageMixin, UpdateMixin):
  pass

class AutocompleteResponse(InteractionResponse):
  async def send_choices(self, choices): ... # TODO

class Interaction:
  def __init__(self, data, app, is_from_http):
    self.data = data
    self.app = app
    self.is_from_http = is_from_http
    self.id = data['id']
    self.token = data['token']
    self.type = data['type']
    self.guild_id = data.get('guild_id')
    self.original_message = ... # TODO
    self.followup = ... # TODO

class CommandInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = CommandResponse(self)

class SlashInteraction(CommandInteraction):
  pass # TODO: add other slash cmd attributes

class UserInteraction(CommandInteraction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    command = data['data']
    resolved = command['resolved']
    user = resolved['users'][command['target_id']]
    member = resolved.get('members', {}).get(command['target_id'])
    guild = app.model.partial_guild(self.guild_id) if self.guild_id else None
    if guild and member:
      self.user = app.model.member(member, user = user, guild = guild)
    else:
      self.user = app.model.user(user)

class MessageInteraction(CommandInteraction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    command = data['data']
    message = command['resolved']['messages'][command['target_id']]
    guild = app.model.partial_guild(self.guild_id) if self.guild_id else None
    self.message = app.model.message(message, guild = guild)

class ComponentInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = ComponentResponse(self)

class ModalInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = ModalResponse(self)

class AutocompleteInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = AutocompleteResponse(self)
