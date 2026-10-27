import copy
import types
import inspect

class BaseHandler:
  def __init__(self, callback = None, name = None):
    if callback:
      self.callback = callback
    self.name = (
      name # as init param
      or getattr(callback, '__name__', None) # as function/method name
      or getattr(self, 'name', None) # as class attribute
    )

  def bind(self, instance):
    handler = copy.copy(self)
    if not inspect.ismethod(self.callback): # cog's @deco goes here, ignore for subclass
      handler.callback = types.MethodType(self.callback, instance)
    return handler

class Handler(BaseHandler):
  async def callback(self, *args, **kwargs):
    raise NotImplementedError(f'{type(self).__name__} is missing a callback!')

  async def __call__(self, *args, **kwargs):
    return await self.callback(*args, **kwargs)
