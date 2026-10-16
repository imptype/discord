import os
from funcs import on_message_create as func_event
import discord

discord.enable_logs(truncate_after = 100)
bot = discord.Bot(token = os.environ['TOKEN'])

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

bot.run()
