import discord

class LifespanCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.lifespan
  async def lifespan(self):
    print('cog lifespan enter')
    yield
    print('cog lifespan exit')

async def setup(bot):
  await bot.add_cogs(LifespanCog)
