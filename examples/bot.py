import os
import datetime
from pathlib import Path
from funcs import another_message_command, on_message_create as func_event
import discord
import asyncio

discord.enable_logs(truncate_after = 100)
bot = discord.Bot(token = os.environ['TOKEN'], intents = discord.Intents.all())

@bot.command
async def echo(context):
  message = await context.send('text')
  await asyncio.sleep(1)

  iurl = 'https://www.python.org/static/img/python-logo.png'
  embed = discord.Embed(
    title = 'titlea',
    description = 'descrip',
    url = 'https://python.org',
    color = 0x123123,
    timestamp = datetime.datetime.now()
  )
  embed.add_field('f1', 'v1', True)
  embed.add_field('f2', 'v2', True)
  embed.add_field('f3', 'v3', True)
  embed.set_author(name = 'authorname', url = iurl, icon_url = iurl)
  embed.set_image(url = iurl)
  embed.set_thumbnail(url = iurl)
  embed.set_footer(text = 'footer text', icon_url = iurl)
  embed2 = discord.Embed(title = 'second title')

  await message.edit(embed = embed)
  await asyncio.sleep(1)
  await message.edit('many', embeds = [embed, embed2])
  await asyncio.sleep(1)

  data = (Path(__file__).parent / 'image.png').read_bytes()
  file = discord.File(data, 'image.png')

  await message.edit('image, embeds gone', embeds = None, file = file)
  await asyncio.sleep(1)
  await message.edit('same file idk', file = file)
  await asyncio.sleep(1)

  embed3 = discord.Embed(title = 'files + embed')
  embed3.set_image(url = 'attachment://image.png')

  await message.edit(content = None, embed = embed3, files = [file, file])
  await asyncio.sleep(1)
  await message.edit('files gone.', files = None)

@bot.event
async def on_message_create(data):
  print('got a message')

@bot.event(name = 'on_message_create')
async def another_event_func(data):
  print('got a message2')

bot.add_events(func_event)

@bot.event
async def on_ready(data):
  print('bot is ready', data)

@bot.command
async def loadcog(data):
  print('loaded math cog')
  await bot.load_extensions('cogs.utils')

@bot.command
async def unloadcog(data):
  print('unloaded math cog')
  await bot.unload_extensions('cogs.utils')

bot.add_commands(another_message_command)

@bot.command.slash()
async def hello(interaction):
  await interaction.respond('hi')

@bot.lifespan
async def lifespan():
  print('startup')
  print(bot.registry)
  # print(await app.sync())
  yield
  print('shutdown')

bot.run()
