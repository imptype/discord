from ..enums import InteractionType, ResponseType

async def handler(app, payload):
  kind = payload['type']

  if kind == InteractionType.PING:
    return {'type': ResponseType.PONG}

  if kind == InteractionType.APPLICATION_COMMAND:
    interaction = await app.run_command(payload, is_from_http = True)
    return interaction.response # or {'type': ResponseType.DEFERRED_MESSAGE/etc}

  raise ValueError(f'unsupported interaction type: {kind}')
