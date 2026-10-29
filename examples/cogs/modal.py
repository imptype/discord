import discord

class ModalCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command.slash(name = 'write', description = 'Open up a text input modal')
  async def write(self, interaction):
    components = [discord.Label(discord.TextInput(custom_id = 'text'), label = 'Type something here')]
    @discord.modal(title = 'Write something!', components = components)
    async def write_modal(interaction):
      await interaction.response.send(interaction.result['text'])
    await interaction.response.send_modal(write_modal)

  @discord.command.slash(name = 'upload', description = 'Opens up a file upload modal')
  async def upload(self, interaction):
    @discord.modal(title = 'Upload a file!') # alternate way to add components to modal
    async def upload_modal(interaction):
      attachment = interaction.result['file'][0]
      async with interaction.app.http.session.get(attachment['url']) as response:
        content = await response.read()
      await interaction.response.send(file = discord.File(content, attachment['filename']))
    upload_modal.add_components(discord.Label(discord.FileUpload(max_values = 1, custom_id = 'file'), label = 'Choose a file'))
    await interaction.response.send_modal(upload_modal)

  @discord.modal(title = 'Persistent write!', custom_id = 'modalcog:persistent', timeout = None,
    components = [discord.Label(discord.TextInput(id = 1), label = 'Type something here')])
  async def persistent_modal(self, interaction):
    await interaction.response.send(interaction.result[1]) # can index with id (int) or custom_id (str)

  @discord.command.slash(name = 'persistentmodal', description = 'Opens a modal that can still submit after restarting')
  async def persistent_modal_command(self, interaction):
    await interaction.response.send_modal(self.persistent_modal)

  class PersistentModal(discord.Modal): # alt syntax if you prefer subclassing
    def __init__(self):
      super().__init__(title = 'Persistent write 2!', custom_id = 'modalcog:persistent2', timeout = None)
      self.add_components(discord.Label(discord.TextInput(id = 1), label = 'ALT Type something here')) # u can also add on super

    async def callback(self, interaction):
      await interaction.response.send(f'ALT {interaction.result[1]}')

  @discord.command.slash(name = 'persistentmodal2', description = 'ALT Opens a modal that can still submit after restarting')
  async def persistent_modal_command2(self, interaction):
    await interaction.response.send_modal(self.persistent_modal)

async def setup(bot):
  await bot.add_cogs(ModalCog)
