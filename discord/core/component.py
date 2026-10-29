import os
import asyncio
import logging
from .. import MISSING
from .modal import Modal
from .cog import Cog, CogMixin
from ..ui import BaseView, Interactable
from .interaction import ComponentInteraction, ModalInteraction

DEFAULT_TIMEOUT = 180 # if a class is in a Cog default is None (persistent)

log = logging.getLogger(__name__)

def describe(component): # Button MyView.on_click() in cogs/test.py:42
  callback = component.callback
  code = getattr(callback, '__code__', None)
  qualname = getattr(callback, '__qualname__', None)
  location = f'{os.path.relpath(code.co_filename)}:{code.co_firstlineno}' if code else None
  return f'{type(component).__name__} {qualname}() in {location}'

def is_class_in_cog(instance):
  return isinstance(getattr(instance, 'cog', None), Cog)

def resolve_timeout(component, view = None):
  has_component_timeout = component.timeout is not MISSING

  if is_class_in_cog(component):
    if has_component_timeout and component.timeout is not None:
      raise ValueError(f'{describe(component)} is a class in a cog, which is intended for persistence, move it out of the cog to set a timeout.')
    return None # component class in cog is persistent

  is_persistent_view = False
  if view:
    is_persistent_view = is_class_in_cog(view)
    if is_persistent_view and view.timeout not in (MISSING, None):
      raise ValueError(f'{type(view).__qualname__} is a View class in a cog, which is intended for persistence, move it out of the cog to set a timeout.')

  if has_component_timeout:
    return component.timeout # takes priority over view

  if is_persistent_view:
    return None # view in a cog is persistent

  if view and view.timeout is not MISSING:
    return view.timeout

  return DEFAULT_TIMEOUT

def validate_timeout(component, view = None):
  timeout = resolve_timeout(component, view)
  print('validate timeout:', describe(component), timeout)
  if timeout is None and not component.has_custom_id:
    raise ValueError(f'{describe(component)} must set a custom_id to be persistent')
  return timeout

class ComponentMixin(CogMixin):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.component_cache = {}
    self.component_timers = {}
    self.modal_cache = {}
    self.modal_timers = {}

  def registrars(self):
    return super().registrars() | {
      Modal: (self.add_modals, self.remove_modals),
      BaseView: (self.add_views, self.remove_views),
      Interactable: (self.add_components, self.remove_components)
    }

  def add_views(self, *views): # also used by send() and edit()
    for view in views:
      self.add_interactables(*view.interactables(), view = view)

  def remove_views(self, *views):
    self.remove_interactables(*[*view.interactables() for view in views])

  def add_components(self, *components): # does .interactables() walk for you
    self.add_interactables(*[*component.interactables() for component in components])

  def remove_components(self, *components):
    self.remove_interactables(*[*component.interactables() for component in components])

  def add_interactables(self, *interactables, view = None):
    timeouts = [(component, validate_timeout(component, view)) for component in interactables]
    for component, timeout in timeouts:
      if timer := self.component_timers.pop(component.custom_id, None):
        timer.cancel()
      self.component_cache[component.custom_id] = component
      if timeout is not None:
        loop = asyncio.get_running_loop()
        self.component_timers[component.custom_id] = loop.call_later(timeout, self.remove_interactables, component)

  def remove_interactables(self, *interactables):
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
