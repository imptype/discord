from .abc import Component
from .enums import ComponentType

class LayoutComponent(Component): ...

class ActionRow(LayoutComponent):
  def __init__(self, *components):
    self.components = list(components)

  def children(self):
    return self.components

  def to_json(self):
    return {
      'type': ComponentType.ACTION_ROW,
      'components': [component.to_json() for component in self.components]
    }

class Section(LayoutComponent): ...
class Container(LayoutComponent): ...
class Separator(LayoutComponent): ...
