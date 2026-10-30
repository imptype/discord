from .enums import ComponentType
from ..abc import Component, clean

class ContentComponent(Component):
  def __init__(self, *, id = None):
    self.id = id

class TextDisplay(ContentComponent):
  def __init__(self, content, *, id = None):
    super().__init__(id = id)
    self.content = content

  def to_json(self):
    return clean({'type': ComponentType.TEXT_DISPLAY, 'id': self.id, 'content': self.content})

class Thumbnail(ContentComponent):
  def __init__(self, url, *, description = None, spoiler = False, id = None):
    super().__init__(id = id)
    self.url = url
    self.description = description
    self.spoiler = spoiler

  def to_json(self):
    return clean({
      'type': ComponentType.THUMBNAIL,
      'id': self.id,
      'media': {'url': self.url},
      'description': self.description,
      'spoiler': self.spoiler
    })

class MediaGalleryItem:
  def __init__(self, url, *, description = None, spoiler = False):
    self.url = url
    self.description = description
    self.spoiler = spoiler

  def to_json(self):
    return clean({'media': {'url': self.url}, 'description': self.description, 'spoiler': self.spoiler})

class MediaGallery(ContentComponent):
  def __init__(self, *items, id = None):
    super().__init__(id = id)
    self.items = [item if isinstance(item, MediaGalleryItem) else MediaGalleryItem(item) for item in items]

  def to_json(self):
    return clean({
      'type': ComponentType.MEDIA_GALLERY,
      'id': self.id,
      'items': [item.to_json() for item in self.items]
    })

class FileComponent(ContentComponent):
  def __init__(self, url, *, spoiler = False, id = None):
    super().__init__(id = id)
    self.url = url
    self.spoiler = spoiler

  def to_json(self):
    return clean({
      'type': ComponentType.FILE,
      'id': self.id,
      'file': {'url': self.url},
      'spoiler': self.spoiler
    })
