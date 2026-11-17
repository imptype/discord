import discord

class TaskCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.ticks = 0

  @discord.task(seconds = 5) # runs every 5 seconds on cog load
  async def tick(self):
    self.ticks += 1
    print('tick', self.ticks)

  @discord.task(seconds = 10, autostart = False) # does not auto start
  async def manual(self):
    print('manual task ran')

  @discord.command
  async def startmanual(self, context):
    if self.manual.runner:
      return await context.send('manual task is already running!')
    self.manual.start()
    await context.send('started manual task')

  @discord.command
  async def stopmanual(self, context):
    self.manual.stop() # does nothing if not running
    await context.send('stopped manual task')

async def setup(bot):
  await bot.add_cogs(TaskCog)
