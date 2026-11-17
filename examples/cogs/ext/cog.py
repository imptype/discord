import discord

class AnotherCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def another(self, context):
    await context.send('did another command')

class CogCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def load2(self, context):
    await self.bot.add_cogs(AnotherCog)
    await context.send('Loaded another cog!')

  @discord.command
  async def unload2(self, context):
    await self.bot.remove_cogs(AnotherCog)
    await context.send('Unloaded another cog.')

async def setup(bot):
  await bot.add_cogs(CogCog)
