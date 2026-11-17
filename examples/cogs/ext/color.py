import discord

class ColorCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def color(self, context, color = '000000'):
    embed = discord.Embed(
      title = f'custom color: `#{color}`',
      color = discord.color(color) # currently this only accepts hex, we'll have more modes in the future
    )
    url = f'https://singlecolorimage.com/get/{color}/100x100'
    embed.set_thumbnail(url = url)
    await context.send(embed = embed)

async def setup(bot):
  await bot.add_cogs(ColorCog)
