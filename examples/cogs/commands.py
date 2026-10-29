import discord

class Commands(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def echo(self, context, *, text = None):
    if not text:
      return await context.send('Missing arguments! Usage: `!echo <your text goes here>`')
    await context.send(text)

  @discord.command.message(name = 'Edited At')
  async def edited_at(self, interaction, message):
    if message.edited_at:
      stamp = int(message.edited_at.timestamp())
      text = f'This message was edited at: <t:{stamp}:F> (<t:{stamp}:R>)'
    else:
      text = 'This message has not been edited yet.'
    await interaction.response.send(text, ephemeral = True)

async def setup(bot):
  await bot.add_cogs(Commands)
