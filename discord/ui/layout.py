from .abc import Component, clean
from .enums import ComponentType, SeparatorSpacing

class LayoutComponent(Component):
  def __init__(self, *, id = None):
    self.id = id

class ActionRow(LayoutComponent):
  def __init__(self, *components, id = None):
    super().__init__(id = id)
    self.components = list(components)

  def children(self):
    return self.components

  def to_json(self):
    return clean({
      'type': ComponentType.ACTION_ROW,
      'id': self.id,
      'components': [component.to_json() for component in self.components]
    })

class Section(LayoutComponent):
  def __init__(self, *components, accessory, id = None):
    super().__init__(id = id)
    self.components = list(components)
    self.accessory = accessory # Thumbnail or Button

  def children(self):
    return [*self.components, self.accessory]

  def to_json(self):
    return clean({
      'type': ComponentType.SECTION,
      'id': self.id,
      'components': [component.to_json() for component in self.components],
      'accessory': self.accessory.to_json()
    })

class Separator(LayoutComponent):
  def __init__(self, *, divider = True, spacing = SeparatorSpacing.SMALL, id = None):
    super().__init__(id = id)
    self.divider = divider
    self.spacing = SeparatorSpacing(spacing)

  def to_json(self):
    return clean({
      'type': ComponentType.SEPARATOR,
      'id': self.id,
      'divider': self.divider,
      'spacing': self.spacing
    })

class Container(LayoutComponent):
  def __init__(self, *components, accent_color = None, spoiler = False, id = None):
    super().__init__(id = id)
    self.components = list(components)
    self.accent_color = accent_color # int, like 0x5865F2
    self.spoiler = spoiler

  def children(self):
    return self.components

  def to_json(self):
    return clean({
      'type': ComponentType.CONTAINER,
      'id': self.id,
      'components': [component.to_json() for component in self.components],
      'accent_color': self.accent_color,
      'spoiler': self.spoiler
    })

class Label(LayoutComponent):
  def __init__(self, component, *, label, description = None, id = None):
    super().__init__(id = id)
    self.component = component
    self.label = label
    self.description = description

  def children(self):
    return [self.component]

  def to_json(self):
    return clean({
      'type': ComponentType.LABEL,
      'id': self.id,
      'label': self.label,
      'description': self.description,
      'component': self.component.to_json()
    })
