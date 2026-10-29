import discord

@discord.event
async def on_message_create():
  print('Message from a file')

@discord.command(name = 'foo')
async def another_message_command(context):
  await context.send('Bar! (You said "!foo")')
