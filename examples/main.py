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
  # print(result := await app.sync())
  # print(f'Synced {len(result)} commands!')
  await app.load_extensions(
    'cogs.modal' # examples are the same as bot.py, remember gateway stuff won't work
  )
  yield
  print('This runs when the HTTP server stops.')

# Run with either:
# a) python main.py
# or b) discord main:app --host 127.0.0.1 --port 8000 (args default)

# If you want to use both, keep this if __name__ check in. When you use
# our CLI or another server like `uvicorn`, it won't run app.run()
if __name__ == '__main__':
  app.run()
