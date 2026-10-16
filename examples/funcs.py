import discord

@discord.command.slash(name = 'ping')
async def ping_command(interaction): # custom func name
  await interaction.respond('pong')

@discord.event
async def on_message_create(data):
  print('got message from file')
