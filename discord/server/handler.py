import asyncio
import logging
from ..core import HTTPStatus, InteractionType, ResponseType

log = logging.getLogger(__name__)

async def handler(app, payload, response_ack_future):
  match kind := payload['type']:
    case InteractionType.PING:
      return HTTPStatus.OK_200, {'type': ResponseType.PONG}
    case InteractionType.APPLICATION_COMMAND:
      coro = app.run_command
    case InteractionType.MESSAGE_COMPONENT:
      coro = app.run_component
    case InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE:
      coro = app.run_autocomplete
    case InteractionType.MODAL_SUBMIT:
      coro = app.run_modal
    case _:
      raise ValueError(f'unsupported interaction type: {kind}')

  interaction_id = int(payload['id'])
  response_future = app.loop.create_future()
  app.pending_interactions[interaction_id] = (response_future, response_ack_future)
  task = app.loop.create_task(coro(payload, is_from_http = True))
  app.tasks.add(task)
  task.add_done_callback(app.tasks.discard)
  try:
    await asyncio.wait({response_future, task}, return_when = asyncio.FIRST_COMPLETED)
  finally:
    app.pending_interactions.pop(interaction_id, None)
  if response_future.done():
    result = response_future.result()
    if result:
      return HTTPStatus.OK_200, result
    return HTTPStatus.ACCEPTED_202, None

  error = task.exception()
  data = payload['data']
  name = data.get('name') or data.get('custom_id')
  if error:
    log.error(f'{name!r} errored before it could respond to the interaction', exc_info = error)
  else:
    log.warning(f'{name!r} completed but forgot to respond to the interaction')
  return HTTPStatus.INTERNAL_SERVER_ERROR_500, {'error': 'interaction failed'}
