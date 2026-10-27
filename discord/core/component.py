import os
import asyncio
from .. import MISSING
from .cog import CogMixin
from ..ui import BaseView, Component, Modal, DEFAULT_TIMEOUT
from .interaction import ComponentInteraction, ModalInteraction

def resolve_timeout(component, view = None):
  if component.timeout is not MISSING: # component timeout takes priority
    return component.timeout
  return DEFAULT_TIMEOUT if view is None else view.timeout

def describe(component): # Button MyView.on_click() in cogs/test.py:42
  callback = component.callback
  code = getattr(callback, '__code__', None)
  qualname = getattr(callback, '__qualname__', None)
  location = f'{os.path.relpath(code.co_filename)}:{code.co_firstlineno}' if code else None
  return f'{type(component).__name__} {qualname}() in {location}'

class ComponentMixin(CogMixin):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.component_cache = {}
    self.component_timers = {}
    self.modal_cache = {}
    self.modal_timers = {}

  def registrars(self):
    return super().registrars() | {Modal: (self.add_modals, self.remove_modals)}

  def add_views(self, *views): # also used by send() and edit()
    for view in views:
      if not isinstance(view, BaseView):
        raise ValueError(f'not a view: {view!r}')
      self.check_persistent(view.interactables(), view)
    for view in views:
      self.add_interactables(view.interactables(), view)

  def remove_views(self, *views):
    for view in views:
      if not isinstance(view, BaseView):
        raise ValueError(f'not a view: {view!r}')
    for view in views:
      self.remove_interactables(view.interactables())

  def add_components(self, *components): # filters out for interactables
    for component in components:
      if not isinstance(component, Component):
        raise ValueError(f'not a component: {component!r}')
      self.check_persistent(component.interactables())
    for component in components:
      self.add_interactables(component.interactables())

  def remove_components(self, *components):
    for component in components:
      if not isinstance(component, Component):
        raise ValueError(f'not a component: {component!r}')
    for component in components:
      self.remove_interactables(component.interactables())

  def add_interactables(self, interactables, view = None):
    for component in interactables:
      if timer := self.component_timers.pop(component.custom_id, None):
        timer.cancel()
      self.component_cache[component.custom_id] = component
      timeout = resolve_timeout(component, view)
      if timeout is not None:
        loop = asyncio.get_running_loop()
        self.component_timers[component.custom_id] = loop.call_later(timeout, self.remove_interactables, [component])

  def remove_interactables(self, interactables):
    for component in interactables:
      if self.component_cache.get(component.custom_id) is not component:
        continue
      if timer := self.component_timers.pop(component.custom_id, None):
        timer.cancel()
      del self.component_cache[component.custom_id]

  def check_persistent(self, interactables, view = None):
    for component in interactables: # persistent (timeout = None) components must have a custom_id
      if resolve_timeout(component, view) is None and not component.has_custom_id:
        raise ValueError(f'{describe(component)} must set a custom_id to be persistent')

  def add_modals(self, *modals): # used by send_modal
    for modal in modals:
      if not isinstance(modal, Modal):
        raise ValueError(f'not a modal: {modal!r}')
      if modal.timeout is None and not modal.has_custom_id:
        raise ValueError(f'{type(modal).__name__} must set a custom_id to be persistent')
    for modal in modals:
      if timer := self.modal_timers.pop(modal.custom_id, None):
        timer.cancel()
      self.modal_cache[modal.custom_id] = modal
      if modal.timeout is not None:
        loop = asyncio.get_running_loop()
        self.modal_timers[modal.custom_id] = loop.call_later(modal.timeout, self.remove_modals, modal)

  def remove_modals(self, *modals):
    for modal in modals:
      if not isinstance(modal, Modal):
        raise ValueError(f'not a modal: {modal!r}')
    for modal in modals:
      if self.modal_cache.get(modal.custom_id) is not modal:
        continue
      if timer := self.modal_timers.pop(modal.custom_id, None):
        timer.cancel()
      del self.modal_cache[modal.custom_id]

  async def run_component(self, payload, is_from_http):
    custom_id = payload['data']['custom_id']
    if (component := self.component_cache.get(custom_id)) is None:
      raise ValueError(f'component not found: {custom_id}')
    interaction = ComponentInteraction(payload, self, is_from_http, component)
    await component(interaction)
    return interaction

  async def run_modal(self, payload, is_from_http):
    custom_id = payload['data']['custom_id']
    if (modal := self.modal_cache.get(custom_id)) is None:
      raise ValueError(f'modal not found: {custom_id}')
    interaction = ModalInteraction(payload, self, is_from_http, modal)
    await modal(interaction)
    return interaction
