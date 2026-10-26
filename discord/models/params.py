import uuid
import orjson
from .. import MISSING
from ..ui import LayoutView
from .enums import MessageFlags, EDIT_MESSAGE_FLAGS, SEND_MESSAGE_FLAGS

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

def encode_part(boundary, name, data, filename = None, content_type = None):
  disposition = f'form-data; name="{name}"'
  if filename:
    safe = filename.replace('"', '%22').replace('\r', '').replace('\n', '')
    disposition += f'; filename="{safe}"'
  header = f'--{boundary}\r\nContent-Disposition: {disposition}\r\n'
  if content_type:
    header += f'Content-Type: {content_type}\r\n'
  return header.encode() + b'\r\n' + data + b'\r\n'

class Payload:
  def __init__(self, body, files = ()):
    self.body = body # final json to send
    self.files = files # list of files to build multipart if any

  def encode(self): # returns content_type, body (json or form bytes)
    payload = orjson.dumps(self.body)
    if not self.files:
      return 'application/json', payload
    boundary = uuid.uuid4().hex
    parts = [encode_part(boundary, 'payload_json', payload, content_type = 'application/json')]
    parts += [
      encode_part(boundary, f'files[{index}]', file.data, file.filename, file.content_type)
      for index, file in enumerate(self.files)
    ]
    parts.append(f'--{boundary}--\r\n'.encode())
    return f'multipart/form-data; boundary={boundary}', b''.join(parts)

def send_params(content = None, *, app = None, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None, ephemeral = False, allowed = SEND_MESSAGE_FLAGS):
  if embed is not None and embeds is not None:
    raise ValueError('cannot send both embed and embeds')
  if file is not None and files is not None:
    raise ValueError('cannot send both file and files')
  if view is not None and components is not None:
    raise ValueError('cannot send both view and components')

  body = {}
  if content is not None:
    body['content'] = content
  if flags is not None:
    body['flags'] = check_flags(flags, allowed, 'send')
  if ephemeral:
    body['flags'] = body.get('flags', 0) | int(MessageFlags.EPHEMERAL)
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
  files = list(files or [])
  if files: # attachment metadata and index matches the files[index] multipart name
    body['attachments'] = [file.to_json(index) for index, file in enumerate(files)]

  if app:
    if view is not None:
      app.add_views(view)
    if components:
      app.add_components(*components)
  return Payload(body, files)

def edit_params(content = MISSING, *, app = None, embed = MISSING, embeds = MISSING, file = MISSING, files = MISSING, view = MISSING, components = MISSING, flags = MISSING):
  if embed is not MISSING and embeds is not MISSING:
    raise ValueError('cannot edit both embed and embeds')
  if file is not MISSING and files is not MISSING:
    raise ValueError('cannot edit both file and files')
  if view is not MISSING and components is not MISSING:
    raise ValueError('cannot edit both view and components')

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
  if files is MISSING:
    files = []
  else: # pass file/s = None to send attachments [] which clears them
    files = list(files or [])
    body['attachments'] = [file.to_json(index) for index, file in enumerate(files)]

  if app:
    if view not in (MISSING, None):
      app.add_views(view)
    if components is not MISSING and components:
      app.add_components(*components)
  return Payload(body, files)
