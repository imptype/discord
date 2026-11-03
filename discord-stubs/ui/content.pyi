from typing import Any
from ..abc import Component

class ContentComponent(Component):
  """
  TODO

  Attributes:
    id: TODO
  """

  def __init__(self, *, id = ...) -> None: # TODO
    """
    TODO

    Args:
      id: TODO
    """

  id: Any # TODO

class TextDisplay(ContentComponent):
  """
  TODO

  Attributes:
    content: TODO
  """

  def __init__(self, content, *, id = ...) -> None: # TODO
    """
    TODO

    Args:
      content: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  content: Any # TODO

class Thumbnail(ContentComponent):
  """
  TODO

  Attributes:
    url: TODO
    description: TODO
    spoiler: TODO
  """

  def __init__(self, url, *, description = ..., spoiler = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      url: TODO
      description: TODO
      spoiler: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  url: Any # TODO
  description: Any # TODO
  spoiler: Any # TODO

class MediaGalleryItem:
  """
  TODO

  Attributes:
    url: TODO
    description: TODO
    spoiler: TODO
  """

  def __init__(self, url, *, description = ..., spoiler = ...) -> None: # TODO
    """
    TODO

    Args:
      url: TODO
      description: TODO
      spoiler: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  url: Any # TODO
  description: Any # TODO
  spoiler: Any # TODO

class MediaGallery(ContentComponent):
  """
  TODO

  Attributes:
    items: TODO
  """

  def __init__(self, *items, id = ...) -> None: # TODO
    """
    TODO

    Args:
      *items: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  items: Any # TODO

class FileComponent(ContentComponent):
  """
  TODO

  Attributes:
    url: TODO
    spoiler: TODO
  """

  def __init__(self, url, *, spoiler = ..., id = ...) -> None: # TODO
    """
    TODO

    Args:
      url: TODO
      spoiler: TODO
      id: TODO
    """

  def to_json(self) -> Any: # TODO
    """
    TODO

    Returns:
      TODO
    """

  url: Any # TODO
  spoiler: Any # TODO
