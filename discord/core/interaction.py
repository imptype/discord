from .. import MISSING
from .enums import ResponseType
from ..models.params import edit_params, send_params
from ..models.enums import MessageFlags, RESPONSE_MESSAGE_FLAGS

class InteractionResponse:
  def __init__(self, interaction):
    self.interaction = interaction
    self.app = interaction.app
    self.body = None # returned to discord when the interaction came from http
    self.responded = False

  async def create(self, type, data = None):
    if self.responded:
      raise ValueError('interaction was already responded to')
    self.responded = True
    body = {'type': type} if data is None else {'type': type, 'data': data}
    if self.interaction.is_from_http:
      self.body = body
    else:
      await self.app.http.create_interaction_response(self.interaction.id, self.interaction.token, body)

class MessageMixin(InteractionResponse):
  async def send(self, content = None, *, embed = None, embeds = None, view = None, components = None, flags = None):
    if embed is not None and embeds is not None:
      raise ValueError('cannot send both embed and embeds')
    if view is not None and components is not None:
      raise ValueError('cannot send both view and components')

    data = send_params(content, embed = embed, embeds = embeds, view = view,
      components = components, flags = flags, allowed = RESPONSE_MESSAGE_FLAGS)
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
  async def update(self, content = MISSING, *, embed = MISSING, embeds = MISSING, view = MISSING, components = MISSING, flags = MISSING):
    if embed is not MISSING and embeds is not MISSING:
      raise ValueError('cannot update both embed and embeds')
    if view is not MISSING and components is not MISSING:
      raise ValueError('cannot update both view and components')

    data = edit_params(content, embed = embed, embeds = embeds, view = view,
      components = components, flags = flags)
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
    self.original_message = ... # TODO
    self.followup = ... # TODO

class CommandInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = CommandResponse(self)

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
