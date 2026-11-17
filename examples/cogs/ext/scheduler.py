import discord

class SchedulerCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def schedulespawn(self, context):

    async def callback():
      print('spawn coro') # runs before 'done'
    
    print('start')
    self.bot.spawn(callback())
    print('done')

  @discord.command
  async def scheduledefer(self, context):

    async def callback():
      print('defer coro') # runs after 'done'
    
    print('start')
    self.bot.defer(callback())
    print('done')

  @discord.command
  async def scheduledelay(self, context):

    async def callback():
      print('delay coro') # runs 5 seconds after 'done'
    
    print('start')
    self.bot.delay(5, callback())
    print('done')

async def setup(bot):
  await bot.add_cogs(SchedulerCog)
