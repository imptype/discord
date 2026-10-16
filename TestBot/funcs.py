import discord

@discord.command.slash()
async def ping_command(interaction):
  await interaction.respond('pong')

@discord.event
async def on_message_create(data):
  print('got message from file')
