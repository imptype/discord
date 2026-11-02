import asyncio
import discord

# This simulates a message send (because we'll hit ratelimits)
async def send(count):
  print(count)
  await asyncio.sleep(0.1)
  if count % 2:
    print(count, 'mid')
    await asyncio.sleep(0.1)
  print(count, 'finish')

class SignalCog(discord.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.count = 0
    self.with_waiters = []

  @discord.command
  async def hold(self, context):
    self.count += 1
    count = self.count
    print(count, 'is waiting')
    await self.bot.signal.wait('foo')
    await send(count)

  @discord.command
  async def release(self, context):
    await context.send(f'firing {self.count}...')
    print('release start')

    # Comment out to see the differnet ways to fire, "send()" and "defer()" are probably the only useful ones.
    # You can also pass args, kwargs when triggering a signal, see discord/ext/signal.py for examples

    await self.bot.signal.fire('foo')       # runs concurrently and exits when all yield
    # await self.bot.signal.fire_each('foo')  # runs sequentially and exits when last one yields
    # await self.bot.signal.send('foo')       # runs concurrently and waits for each to finish
    # await self.bot.signal.send_each('foo')  # runs sequentially and waits for each to finish
    # await self.bot.signal.defer('foo')      # exits immediately, and runs concurrently
    # await self.bot.signal.defer_each('foo') # exits immediately, and runs sequentially

    print('release done')
    self.count = 0

  @discord.command
  async def whold(self, context):
    self.count += 1
    count = self.count
    print(count, 'is waiting (with block)')
    waiter = self.bot.signal.wait('foo')
    self.with_waiters.append(waiter)
    async with waiter:
      print(count, 'whold enter')
      await asyncio.sleep(0.1)
      await send(count)
      await asyncio.sleep(0.4)
      print(count, 'whold exit')
    self.with_waiters.remove(waiter)
    print(count, 'whold outside')

  @discord.command
  async def wcancel(self, context):
    await context.send(f'cancelling {len(self.with_waiters)} waiters')
    while self.with_waiters:
      self.with_waiters.pop().cancel()
      self.count -= 1

  @discord.command
  async def rhold(self, context):
    self.count += 1
    count = self.count

    # a "Roblox"-like :Once signal, keep in mind cog reloads can't reach handlers inside
    # so make a self.list and unregister yourself via cog_unload or always pair it with a timeout
    @self.bot.signal(once = True, timeout = 10)
    async def foo():
      print(count, 'foo once')
    print(count, 'foo once handler is waiting')

  @discord.signal(name = 'bar', max_runs = 5)
  async def bar(self, a, b, c, d):
    print(self.bar.runs, 'bar', a, b, c, d)

  @discord.command
  async def firebar(self, context):
    await context.send('firing bar...')
    await self.bot.signal.fire('bar', 1, 2, 3, 4) # arg count must match

async def setup(bot):
  await bot.add_cogs(SignalCog)
