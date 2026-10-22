from ..models.params import send_params
from .enums import InteractionType, ResponseType
from ..models.enums import RESPONSE_MESSAGE_FLAGS

class InteractionResponse:
  def __init__(self, interaction):
    self.interaction = interaction
    self.app = interaction.app
    self.body = None # returned to discord when the interaction came from http
    self.responded = False

  async def create(self, type, data):
    if self.responded:
      raise ValueError('interaction was already responded to')
    self.responded = True
    body = {'type': type, 'data': data}
    if self.interaction.is_from_http:
      self.body = body
    else:
      await self.app.http.create_interaction_response(self.interaction.id, self.interaction.token, body)

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

  async def send_modal(self, modal):
    if self.interaction.type in (InteractionType.PING, InteractionType.MODAL_SUBMIT):
      raise ValueError('cannot send a modal in response to this interaction type')
    self.app.add_modals(modal)
    await self.create(ResponseType.MODAL, modal.to_json())

class Interaction:
  def __init__(self, data, app, is_from_http):
    self.data = data
    self.app = app
    self.is_from_http = is_from_http
    self.id = data['id']
    self.token = data['token']
    self.type = data['type']
    self.response = InteractionResponse(self)
