import discord

class Count(discord.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.count = 0

  @discord.command(name = 'count')
  async def count_command(self, context):
    self.count += 1
    await context.send(self.count)

async def setup(bot):
  await bot.add_cogs(Count)
