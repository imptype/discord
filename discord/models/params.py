import orjson
import aiohttp
from .. import MISSING
from ..ui import LayoutView
from .enums import MessageFlags, EDIT_MESSAGE_FLAGS, SEND_MESSAGE_FLAGS

def make_form(body, files):
  attachments = []
  for index, file in enumerate(files):
    attachment = {'id': index, 'filename': file.filename}
    if file.description:
      attachment['description'] = file.description
    attachments.append(attachment)

  payload = {**body, 'attachments': attachments}
  form = aiohttp.FormData()
  form.add_field('payload_json', orjson.dumps(payload).decode(), content_type = 'application/json')
  for index, file in enumerate(files):
    form.add_field(f'files[{index}]', file.data, filename = file.filename, content_type = file.content_type)
  return form

def check_flags(flags, allowed, action):
  if not isinstance(flags, MessageFlags):
    raise ValueError(f'flags must be MessageFlags, got: {type(flags)}')
  if extra := int(flags) & ~int(allowed):
    names = ' / '.join(flag.name for flag in allowed if flag.name)
    raise ValueError(f'cannot {action} with flags {MessageFlags(extra)!r}, allowed: {names}')
  return int(flags)

def view_params(body, view):
  body['components'] = view.to_json()
  if isinstance(view, LayoutView):
    body['flags'] = body.get('flags', 0) | int(MessageFlags.IS_COMPONENTS_V2)

def send_params(content = None, *, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None):
  body = {}
  if content is not None:
    body['content'] = content
  if flags is not None:
    body['flags'] = check_flags(flags, SEND_MESSAGE_FLAGS, 'send')
  if embed:
    embeds = [embed]
  if embeds:
    body['embeds'] = [embed.to_json() for embed in embeds]
  if view is not None:
    view_params(body, view)
  if components is not None:
    body['components'] = [component.to_json() for component in components]
    if components:
      body['flags'] = body.get('flags', 0) | int(MessageFlags.IS_COMPONENTS_V2)
  if file:
    files = [file]
  if files:
    return make_form(body, files)
  return body

def edit_params(content = MISSING, *, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING, view = MISSING, components = MISSING, flags = MISSING):
  body = {}
  if content is not MISSING:
    body['content'] = content
  if flags is not MISSING:
    body['flags'] = check_flags(flags, EDIT_MESSAGE_FLAGS, 'edit')
  if embed is not MISSING:
    embeds = None if embed is None else [embed]
  if embeds is not MISSING:
    if embeds is None: # pass embed/s = None to clear embeds (sends [])
      body['embeds'] = []
    else:
      body['embeds'] = [embed.to_json() for embed in embeds]
  if view is not MISSING:
    if view is None:
      body['components'] = []
    else:
      view_params(body, view)
  if components is not MISSING:
    if components is None:
      body['components'] = []
    else:
      body['components'] = [component.to_json() for component in components]
      if components:
        body['flags'] = body.get('flags', 0) | int(MessageFlags.IS_COMPONENTS_V2)
  if file is not MISSING:
    files = None if file is None else [file]
  if files is not MISSING:
    if files:
      return make_form(body, files)
    body['attachments'] = [] # pass none to clear files (sends [])
  return body
