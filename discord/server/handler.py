from ..core import InteractionType, ResponseType

async def handler(app, payload):
  match kind := payload['type']:
    case InteractionType.PING:
      return {'type': ResponseType.PONG}
    case InteractionType.APPLICATION_COMMAND:
      interaction = await app.run_command(payload, is_from_http = True)
    case InteractionType.MESSAGE_COMPONENT:
      interaction = await app.run_component(payload, is_from_http = True)
    case InteractionType.MODAL_SUBMIT:
      interaction = await app.run_modal(payload, is_from_http = True)
    case _:
      raise ValueError(f'unsupported interaction type: {kind}')
  return interaction.response.body
