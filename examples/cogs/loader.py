import discord

class Loader(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def loadcount(self, ctx):
    await self.bot.load_extensions('cogs.count')
    await ctx.send('Loaded count cog!')

  @discord.command
  async def unloadcount(self, ctx):
    await self.bot.unload_extensions('cogs.count')
    await ctx.send('Unloaded count cog.')

async def setup(bot):
  await bot.add_cogs(Loader)
