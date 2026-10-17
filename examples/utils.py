import discord

class Utils(discord.Cog):
  def __init__(self, bot):
    print('override init')
    self.bot = bot

  async def cog_load(self):
    print('run cog load')

    @self.bot.command
    async def idk(data):
      print('ran !idk command')

  @discord.command(name = 'math')
  async def a_cog_command(self, data):
    print('did !math command')

  @discord.command.slash(name = 'ping')
  async def ping_command(self, interaction): # custom func name
    await interaction.respond('pong')
