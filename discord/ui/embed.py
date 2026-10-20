from datetime import datetime

def clean(data):
  return {key: value for key, value in data.items() if value is not None}

class Embed:
  def __init__(self, title = None, description = None, url = None, color = None, timestamp = None):
    self.title = title
    self.description = description
    self.url = url
    self.color = color # int, like 0x5865F2
    self.timestamp = timestamp # datetime or iso string
    self.footer = None
    self.image = None
    self.thumbnail = None
    self.author = None
    self.fields = []

  def set_footer(self, text, icon_url = None):
    self.footer = clean({'text': text, 'icon_url': icon_url})

  def set_image(self, url):
    self.image = {'url': url}

  def set_thumbnail(self, url):
    self.thumbnail = {'url': url}

  def set_author(self, name, url = None, icon_url = None):
    self.author = clean({'name': name, 'url': url, 'icon_url': icon_url})

  def add_field(self, name, value, inline = False):
    self.fields.append({'name': name, 'value': value, 'inline': inline})

  def to_json(self):
    timestamp = self.timestamp
    if isinstance(timestamp, datetime):
      timestamp = timestamp.isoformat()
    return clean({
      'title': self.title,
      'description': self.description,
      'url': self.url,
      'color': self.color,
      'timestamp': timestamp,
      'footer': self.footer,
      'image': self.image,
      'thumbnail': self.thumbnail,
      'author': self.author,
      'fields': self.fields or None
    })
