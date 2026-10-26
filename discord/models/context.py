"""
context.py - a custom object for gateway commands, to access things quickly.
"""

def parse_arguments(parameters, text, name):
  args = []
  kwargs = {}
  for parameter in parameters:
    match parameter.kind:
      case parameter.POSITIONAL_ONLY | parameter.POSITIONAL_OR_KEYWORD:
        word, text = (text.split(maxsplit = 1) + ['', ''])[:2]
        if not word:
          if parameter.default is parameter.empty:
            raise ValueError(f'{name}: missing argument {parameter.name!r}')
          word = parameter.default
        args.append(word)
      case parameter.VAR_POSITIONAL:
        args.extend(text.split())
        text = ''
      case parameter.KEYWORD_ONLY:
        if text.strip():
          kwargs[parameter.name] = text.strip()
        elif parameter.default is parameter.empty:
          raise ValueError(f'{name}: missing argument {parameter.name!r}')
        text = ''
  return args, kwargs

class Context:
  def __init__(self, app, message, arguments = ''):
    self.app = app
    self.message = message
    self.arguments = arguments
    self.author = message.author
    self.channel = message.channel
    self.guild = message.guild

  async def send(self, content = None, *, embed = None, embeds = None, file = None, files = None, view = None, components = None, flags = None):
    return await self.channel.send(
      content, embed = embed, embeds = embeds, file = file, files = files,
      view = view, components = components, flags = flags
    )
