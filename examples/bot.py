import os
from funcs import another_message_command, on_message_create as func_event, ping_command
import discord

discord.enable_logs(truncate_after = 100)
bot = discord.Bot(token = os.environ['TOKEN'], intents = discord.Intents.all())

@bot.event
async def on_message_create(data):
  print('got a message')

@bot.event(name = 'on_message_create')
async def another_event_func(data):
  print('got a message2')

bot.add_event(func_event)

@bot.event
async def on_ready(data):
  print('bot is ready', data)

bot.add_command(ping_command)

@bot.command
async def foo(data):
  print('did !foo')

bot.add_command(another_message_command)

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
