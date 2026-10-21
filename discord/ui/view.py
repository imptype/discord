import copy
import uuid
import types
from .button import Button
from .layout import ActionRow
from .select import SelectMenu
from .abc import Component, Interactable, DEFAULT_TIMEOUT

MAX_BUTTONS_PER_ROW = 5

class BaseView:
  def __init__(self, *, timeout = DEFAULT_TIMEOUT):
    self.timeout = timeout

  def children(self):
    return []

  def walk(self):
    for child in self.children():
      yield from child.walk()

  def interactables(self):
    return [component for component in self.walk() if isinstance(component, Interactable)]

  def to_json(self):
    return [child.to_json() for child in self.children()]

class View(BaseView):
  def __init__(self, *components, timeout = DEFAULT_TIMEOUT):
    super().__init__(timeout = timeout)
    self.rows = []

    interactables: dict = { # allows for multiple same ids
      name: value
      for cls in reversed(type(self).__mro__)
      for name, value in vars(cls).items()
      if isinstance(value, Interactable)
    }
    copies = []
    for name, interactable in interactables.items():
      new = copy.copy(interactable)
      if not interactable.has_custom_id:
        new.custom_id = uuid.uuid4().hex
      new.callback = types.MethodType(interactable.callback, self)
      setattr(self, name, new) # diff for each view instance
      copies.append(new)

    self.add_interactables(*components, *copies)

  def children(self):
    return [row for row in self.rows if row.components] # skips empty rows

  def add_interactables(self, *components):
    for component in components:
      if isinstance(component, SelectMenu):
        self.add_select(component)
      else:
        self.add_buttons(component)

  def add_buttons(self, *buttons):
    for button in buttons:
      if button.row is None: # default to next with space if no index
        for row in self.rows:
          if not row.components or (isinstance(row.components[0], Button) and len(row.components) < MAX_BUTTONS_PER_ROW):
            break
        else:
          row = ActionRow()
          self.rows.append(row)
      else:
        while len(self.rows) <= button.row:
          self.rows.append(ActionRow())
        row = self.rows[button.row]
      row.components.append(button)

  def add_select(self, select):
    row = ActionRow(select) # a select takes a whole row
    self.rows.append(row)
    return row

class LayoutView(BaseView):
  def __init__(self, *components, timeout = DEFAULT_TIMEOUT):
    super().__init__(timeout = timeout)
    self.components = []
    if components:
      self.add_components(*components)

  def children(self):
    return self.components

  def add_components(self, *components):
    for component in components:
      if not isinstance(component, Component):
        raise ValueError(f'not a component: {component!r}')
      if isinstance(component, Interactable):
        raise ValueError(f'{component!r} must be inside an Layout component')
    self.components.extend(components)
    return self
