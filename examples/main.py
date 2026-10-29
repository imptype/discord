import os
import discord

app = discord.App(
  public_key = os.environ['PUBLIC_KEY'],
  token = os.environ['TOKEN'],
  application_id = os.environ['APPLICATION_ID']
)

@app.command.slash()
async def ping(interaction):
  await interaction.response.send('pong')

@app.lifespan
async def lifespan():
  print('This runs when the HTTP server starts.')
  print('Uncomment to sync your interaction commands once:', app.registry)
  # print(result := await bot.sync())
  # print(f'Synced {len(result)} commands!')
  await app.load_extensions(
    'cogs.modal' # examples are the same as bot.py, remember gateway stuff won't work
  )
  yield
  print('This runs when the HTTP server stops.')
