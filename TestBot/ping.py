import discord

@discord.command.slash()
async def ping(interaction):
  await interaction.respond('pong')
