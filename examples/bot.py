import os
from funcs import another_message_command, on_message_create as func_event
import discord
import datetime

discord.enable_logs(truncate_after = 100)
bot = discord.Bot(token = os.environ['TOKEN'], intents = discord.Intents.all())

@bot.command
async def echo(context):
  await context.send('aa')
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
  embed2 = discord.Embed(title = 'second title')
  await context.send(embed = embed)
  await context.send('many', embeds = [embed, embed2])

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
