import discord

class Events(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.event
  async def on_message_create(self):
    print('Message event 1')

  @discord.event(name = 'message_create')
  async def random_name(self, message):
    print('Message event 2:', message.content[:50])

async def setup(bot):
  await bot.add_cogs(Events)
