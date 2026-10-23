import mimetypes
from io import BytesIO

class File:
  def __init__(self, data, filename, *, description = None):
    if isinstance(data, BytesIO):
      data = data.getvalue()
    if not isinstance(data, bytes):
      raise ValueError(f'file data must be bytes or BytesIO, got: {type(data)}')
    self.data = data
    self.filename = filename
    self.description = description # alt text
    self.content_type = mimetypes.guess_type(filename)[0] or 'application/octet-stream'

  def to_json(self, index):
    body = {'id': index, 'filename': self.filename}
    if self.description:
      body['description'] = self.description
    return body
