from ..enums import InteractionType, ResponseType
from ..interaction import Interaction

async def handler(app, payload):
  kind = payload['type']

  if kind == InteractionType.PING:
    return {'type': ResponseType.PONG}

  if kind == InteractionType.APPLICATION_COMMAND:
    name = payload['data']['name']
    command = app.registry.get(name)

    if command is None:
      raise ValueError(f'unknown command: {name}')

    interaction = Interaction(payload)
    await command(interaction)
    return interaction.response # or {'type': ResponseType.DEFERRED_MESSAGE/etc}

  raise ValueError(f'unsupported interaction type: {kind}')
