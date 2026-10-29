from .. import MISSING
from .enums import InteractionType, ResponseType
from ..models import MessageFlags, Payload, edit_params, send_params, RESPONSE_MESSAGE_FLAGS

class InteractionResult: # wraps InteractionCallbackResponse for with_response = True
  def __init__(self, app, data):
    interaction = data['interaction']
    resource = data.get('resource', {})
    message_id = interaction.get('response_message_id')
    self.data = data

    # Interaction Callback Object
    self.interaction_id = int(interaction['id'])
    self.interaction_type = InteractionType(interaction['type'])
    self.activity_instance_id = interaction.get('activity_instance_id')
    self.response_message_id = int(message_id) if message_id else None
    self.response_message_loading = interaction.get('response_message_loading')
    self.response_message_ephemeral = interaction.get('response_message_ephemeral')

    # Interaction Callback Resource Object
    self.resource_type = ResponseType(resource['type']) if resource else None
    self.activity_instance = resource.get('activity_instance')
    message = resource.get('message')
    self.message = app.model.message(message) if message else None

class InteractionResponse:
  def __init__(self, interaction):
    self.interaction = interaction
    self.app = interaction.app
    self.body = None # returned to discord when the interaction came from http
    self.responded = False

  async def create(self, type, data = None, with_response = False): # data is a Payload, json or None
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
      response_future, response_ack_future = self.app.pending_interactions.pop(self.interaction.id)
      if not with_response:
        self.body = payload
        response_future.set_result(payload)
        return None
      response_future.set_result(None)
      await response_ack_future # lets loop complete server/handler.py then does http request below

    result = await self.app.http.create_interaction_response(
      self.interaction.id, self.interaction.token, payload,
      with_response = True if with_response else None
    )

    if not with_response:
      return None

    return InteractionResult(self.app, result)

class MessageMixin(InteractionResponse):
  async def send(self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None, ephemeral = False, with_response = False):
    data = send_params(content, app = self.app, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags, ephemeral = ephemeral, allowed = RESPONSE_MESSAGE_FLAGS)
    return await self.create(ResponseType.MESSAGE, data, with_response = with_response)

  async def defer(self, *, ephemeral = False, with_response = False):
    data = {'flags': int(MessageFlags.EPHEMERAL)} if ephemeral else None
    return await self.create(ResponseType.DEFERRED_MESSAGE, data, with_response = with_response)

  async def premium_required(self, *, with_response = False): # deprecated
    return await self.create(ResponseType.PREMIUM_REQUIRED, with_response = with_response)

  async def launch_activity(self, *, with_response = False):
    return await self.create(ResponseType.LAUNCH_ACTIVITY, with_response = with_response)

class ModalMixin(InteractionResponse):
  async def send_modal(self, modal, *, with_response = False):
    self.app.add_modals(modal)
    return await self.create(ResponseType.MODAL, modal.to_json(), with_response = with_response)

class UpdateMixin(InteractionResponse):
  async def update(self, content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING, view = MISSING, components = MISSING, flags = MISSING, with_response = False):
    data = edit_params(content, app = self.app, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags)
    return await self.create(ResponseType.UPDATE_MESSAGE, data, with_response = with_response)

  async def defer_update(self, *, with_response = False):
    return await self.create(ResponseType.DEFERRED_UPDATE_MESSAGE, with_response = with_response)

class CommandResponse(MessageMixin, ModalMixin):
  pass
class ComponentResponse(MessageMixin, ModalMixin, UpdateMixin):
  pass
class ModalResponse(MessageMixin, UpdateMixin):
  pass

class AutocompleteResponse(InteractionResponse):
  async def send_choices(self, choices = None):
    await self.create(ResponseType.AUTOCOMPLETE_RESULT, {'choices': [choice.to_json() for choice in choices or []]})
