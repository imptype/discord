import os
import discord

bot = discord.Bot(token = os.environ['TOKEN'], intents = discord.Intents.all())

@bot.command
async def ping(context):
  await context.send('Pong! (You said "!ping")')

@bot.command.slash
async def hello(interaction):
  await interaction.response.send('Hi! (You did `/hello`)')

@bot.event
async def on_first_ready():
  print('This runs on the first READY event, after `bot.http.application_id` is set.')
  print('Uncomment to sync your interaction commands once:', bot.registry)
  # print(result := await bot.sync())
  # print(f'Synced {len(result)} commands!')

@bot.lifespan
async def lifespan():
  print('This runs when bot enters async loop, before websocket connection is made.')

  await bot.load_extensions(
    'cogs.commands', # example of prefix commands with args and an interaction message command
    'cogs.events',   # example of gateway events
    'cogs.embeds',   # example of embed and cv2 messages
    'cogs.buttons',  # example of messages with buttons and interactive components
    'cogs.modal',    # example of modal with file upload and persistence
    'cogs.loader'    # example of reloading a command without restarting the bot
    # 'cogs.count',  # loaded by !loadcog command from 'cogs.loader'
  )

  # You can also import and add stuff directly (add_events/commands/lifespans/components/views etc.)
  from other.funcs import on_message_create, another_message_command
  bot.add_events(on_message_create)
  bot.add_commands(another_message_command)

  yield
  print('This runs after websocket conection exits, before exiting the async loop.')

bot.run()
