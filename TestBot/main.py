import os
from ping import ping
import discord

app = discord.App(
  public_key = os.environ['PUBLIC_KEY'],
  token = os.environ['TOKEN'],
  application_id = os.environ['APPLICATION_ID']
)

app.add_command(ping)

@app.command.slash()
async def hello(interaction):
  await interaction.respond('hi')

@app.lifespan
async def lifespan():
  print('startup')
  print(app.registry)
  # print(await app.sync())
  yield
  print('shutdown')