from typing import Any
from .enums import OptionType
from .response import AutocompleteResponse, CommandResponse, ComponentResponse, ModalResponse

def resolve_user(interaction, user_id):
  model = interaction.app.model
  resolved = interaction.data['data']['resolved']
  user = resolved['users'][user_id]
  member = resolved.get('members', {}).get(user_id)
  if interaction.guild_id and member:
    guild = model.partial_guild(interaction.guild_id)
    return model.member(member, user = user, guild = guild)
  return model.user(user)

def resolve_option(interaction, option):
  value = option['value']
  model = interaction.app.model
  resolved = interaction.data['data'].get('resolved', {})
  match option['type']:
    case OptionType.USER:
      return resolve_user(interaction, value)
    case OptionType.CHANNEL:
      guild = model.partial_guild(interaction.guild_id) if interaction.guild_id else None
      return model.channel(resolved['channels'][value], guild)
    case OptionType.ROLE:
      return resolved['roles'][value]
    case OptionType.MENTIONABLE:
      if value in resolved.get('roles', {}):
        return resolved['roles'][value]
      return resolve_user(interaction, value)
    case OptionType.ATTACHMENT:
      return resolved['attachments'][value]
  return value

def parse_options(interaction, is_autocomplete = False) -> Any:
  data = interaction.data['data']
  names = [data['name']]
  options = data.get('options', [])
  while options and options[0]['type'] in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP):
    names.append(options[0]['name'])
    options = options[0].get('options', [])
  values = {}
  focused = None
  for option in options:
    if is_autocomplete and option.get('focused'):
      focused = (option['name'], option['value'])
    else:
      values[option['name']] = resolve_option(interaction, option)
  if is_autocomplete:
    return names, values, focused
  return names, values

class Interaction:
  def __init__(self, data, app, is_from_http):
    self.data = data
    self.app = app
    self.is_from_http = is_from_http
    self.id = data['id']
    self.token = data['token']
    self.type = data['type']
    self.guild_id = data.get('guild_id')
    self.original_message = ... # TODO
    self.followup = ... # TODO

class CommandInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = CommandResponse(self)

class SlashInteraction(CommandInteraction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.names, self.options = parse_options(self)

class UserInteraction(CommandInteraction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.user = resolve_user(self, data['data']['target_id'])

class MessageInteraction(CommandInteraction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    command = data['data']
    message = command['resolved']['messages'][command['target_id']]
    guild = app.model.partial_guild(self.guild_id) if self.guild_id else None
    self.message = app.model.message(message, guild = guild)

class ComponentInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = ComponentResponse(self)

class ModalInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = ModalResponse(self)

class AutocompleteInteraction(Interaction):
  def __init__(self, data, app, is_from_http):
    super().__init__(data, app, is_from_http)
    self.response = AutocompleteResponse(self)
    self.names, self.options, self.focused = parse_options(self, is_autocomplete = True)
