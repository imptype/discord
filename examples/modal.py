import discord

@discord.command
async def testform(context):

  @discord.modal(
    title = 'Quick form',
    components = [discord.Label(discord.TextInput(custom_id = 'answer'), label = 'what is 6 + 7')]
  )
  async def form_modal(modal, interaction):
    label = interaction.data['data']['components'][0]
    name = label['component']['value'] # labels wrap their component
    print(f'submitted! {name}')
    await interaction.response.send(f'submitted! your answer {name}')

  @discord.button('Open form')
  async def open_button(button, interaction):
    await interaction.response.send_modal(form_modal)

  # await context.send(view = discord.LayoutView(discord.ActionRow(open_button)))
  await context.send(components = [discord.ActionRow(open_button)]) # comp sets cv2 flag

async def show_modal(modal, interaction):
  lines = []
  for row in interaction.data['data']['components']:
    component = row.get('component', row) # labels wrap their component
    if 'custom_id' in component:
      lines.append(f'{component['custom_id']}: {component.get('values', component.get('value'))}')
  await interaction.response.send('\n'.join(lines) or 'no values')

class SelectsModal(discord.Modal):
  async def callback(self, interaction):
    await show_modal(self, interaction)

@discord.command
async def testmodal(context):
  # discord allows max 5 top-level components per modal, so this is split into 3 modals

  async def open_text(button, interaction): # TextDisplay, TextInput x2, RadioGroup, CheckboxGroup
    modal = discord.Modal(
      discord.TextDisplay('**Modal 1/3** - text + groups'),
      discord.Label(
        discord.TextInput(
          custom_id = 'short', style = discord.TextInputStyle.SHORT, min_length = 2, max_length = 20,
          required = True, value = 'prefilled', placeholder = 'short placeholder', id = 20
        ),
        label = 'Short TextInput', description = 'min 2, max 20 chars'
      ),
      discord.Label(
        discord.TextInput(
          custom_id = 'paragraph', style = discord.TextInputStyle.PARAGRAPH, required = False,
          placeholder = 'optional paragraph'
        ),
        label = 'Paragraph TextInput'
      ),
      discord.Label(
        discord.RadioGroup(
          'plain',
          discord.GroupOption('with extras', 'v2', description = 'desc', default = True),
          custom_id = 'radio'
        ),
        label = 'RadioGroup'
      ),
      discord.Label(
        discord.CheckboxGroup(
          'one',
          discord.GroupOption('two', 'v2', description = 'desc', default = True),
          'three',
          min_values = 1, max_values = 2, custom_id = 'checkboxes'
        ),
        label = 'CheckboxGroup', description = 'pick 1-2'
      ),
      title = 'Text modal',
      custom_id = 'modal:text', # persistent, timeout = None needs a custom_id
      timeout = None, # type: ignore # need to typehint timeout as None | int later
      callback = show_modal
    )
    await interaction.response.send_modal(modal)

  async def open_selects(button, interaction): # every select type, subclass style
    modal = SelectsModal(title = 'Selects modal').add_components(
      discord.Label(
        discord.StringSelect(
          'plain', discord.SelectOption('with extras', 'v2', description = 'desc', emoji = '🔥', default = True),
          custom_id = 'string', placeholder = 'string select', min_values = 0, max_values = 2, required = False
        ),
        label = 'StringSelect (optional)'
      ),
      discord.Label(
        discord.UserSelect(custom_id = 'user', default_values = [interaction.data['member']['user']['id']], max_values = 3),
        label = 'UserSelect'
      ),
      discord.Label(discord.RoleSelect(custom_id = 'role', max_values = 3), label = 'RoleSelect'),
      discord.Label(
        discord.MentionableSelect(custom_id = 'mentionable', default_users = [interaction.data['member']['user']['id']], max_values = 3),
        label = 'MentionableSelect'
      ),
      discord.Label(
        discord.ChannelSelect(
          custom_id = 'channel', channel_types = [discord.ChannelType.GUILD_TEXT, discord.ChannelType.GUILD_VOICE],
          default_values = [context.channel.id]
        ),
        label = 'ChannelSelect'
      )
    )
    await interaction.response.send_modal(modal)

  async def open_misc(button, interaction): # Checkbox, FileUpload, chained add_components
    modal = discord.Modal(title = 'Misc modal', callback = show_modal)
    modal.add_components(discord.TextDisplay('**Modal 3/3** - checkbox + file upload'))
    modal.add_components(
      discord.Label(discord.Checkbox(custom_id = 'checkbox', default = True), label = 'Checkbox', description = 'single toggle'),
      discord.Label(
        discord.FileUpload(
          custom_id = 'files', min_values = 1, max_values = 3, required = False, file_types = ['image', '.pdf']
        ),
        label = 'FileUpload (optional)', description = 'images or pdf, up to 3'
      )
    )
    await interaction.response.send_modal(modal)

  await context.send(view = discord.LayoutView(
    discord.TextDisplay('# Modal test'),
    discord.ActionRow(
      discord.Button('text + groups', callback = open_text),
      discord.Button('selects', callback = open_selects),
      discord.Button('checkbox + file', callback = open_misc)
    )
  ))
