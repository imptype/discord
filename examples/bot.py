import os
import asyncio
import datetime
from pathlib import Path
from funcs import another_message_command, on_message_create as func_event
import discord

discord.enable_logs(truncate_after = 100)
bot = discord.Bot(token = os.environ['TOKEN'], intents = discord.Intents.all())

class TestView(discord.View):
  @discord.button('aaa')
  async def a_button(self, button, interaction):
    await interaction.respond('clicked a')

class PersistView(discord.View):
  @discord.button('persist', timeout = None, custom_id = 'persist:v1')
  async def persist_button(self, button, interaction):
    await interaction.respond('clicked persist')

@bot.command
async def selects(context):
  async def show(select, interaction):
    values = interaction.payload['data']['values']
    await interaction.respond(f'{type(select).__name__}: {values}')

  @discord.string_select(
    'plain string',
    discord.SelectOption('with extras', 'v2', description = 'desc', emoji = '🔥', default = True),
    discord.SelectOption('third', description = 'no emoji'),
    placeholder = 'string select', min_values = 1, max_values = 2, id = 10
  )
  async def string(select, interaction):
    await show(select, interaction)

  @discord.user_select(default_values = [context.author.id], placeholder = 'user select', max_values = 3)
  async def user(select, interaction):
    await show(select, interaction)

  @discord.role_select(placeholder = 'role select', max_values = 3)
  async def role(select, interaction):
    await show(select, interaction)

  @discord.mentionable_select(default_users = [context.author.id], placeholder = 'mentionable select', max_values = 3)
  async def mentionable(select, interaction):
    await show(select, interaction)

  @discord.channel_select(
    channel_types = [discord.ChannelType.GUILD_TEXT, discord.ChannelType.GUILD_VOICE],
    default_values = [context.channel.id],
    placeholder = 'channel select'
  )
  async def channel(select, interaction):
    await show(select, interaction)

  disabled = discord.StringSelect('a', 'b', placeholder = 'disabled select', disabled = True)

  await context.send(view = discord.LayoutView(
    discord.TextDisplay('# Select test'),
    discord.ActionRow(string),
    discord.ActionRow(user),
    discord.ActionRow(role),
    discord.ActionRow(mentionable),
    discord.ActionRow(channel),
    discord.ActionRow(disabled)
  ))

@bot.command
async def testlayout(context):
  iurl = 'https://www.python.org/static/img/python-logo.png'
  data = (Path(__file__).parent / 'image.png').read_bytes()
  file = discord.File(data, 'image.png')

  async def on_click(button, interaction):
    await interaction.respond(f'clicked {button.label}')

  view = discord.LayoutView(
    discord.TextDisplay('# LayoutView test', id = 1),
    discord.Container(
      discord.TextDisplay('**TextDisplay** inside a container'),
      discord.Separator(),
      discord.Section(
        discord.TextDisplay('Section with a Thumbnail accessory'),
        discord.TextDisplay('second line of text'),
        accessory = discord.Thumbnail(iurl, description = 'python logo')
      ),
      discord.Separator(divider = False, spacing = discord.SeparatorSpacing.LARGE),
      discord.Section(
        discord.TextDisplay('Section with a Button accessory'),
        accessory = discord.Button('section btn', callback = on_click)
      ),
      discord.Separator(),
      discord.MediaGallery(
        iurl,
        discord.MediaGalleryItem(iurl, description = 'with alt text'),
        discord.MediaGalleryItem('attachment://image.png', spoiler = True)
      ),
      discord.FileComponent('attachment://image.png'),
      discord.Separator(),
      discord.ActionRow(
        discord.Button('one', callback = on_click),
        discord.Button('two', style = discord.ButtonStyle.SECONDARY, callback = on_click),
        discord.Button('disabled', disabled = True)
      ),
      accent_color = 0x5865F2,
      id = 2
    ),
    discord.Container(
      discord.TextDisplay('spoilered container'),
      discord.FileComponent('attachment://image.png', spoiler = True),
      spoiler = True
    )
  )
  await context.send(view = view, file = file)

bot.add_views(PersistView())

@bot.command
async def button(context):
  await context.send(view = TestView())

@bot.command
async def pers(context):
  await context.send(view = PersistView())

@bot.command
async def echo(context):
  message = await context.send('text')
  await asyncio.sleep(1)

  iurl = 'https://www.python.org/static/img/python-logo.png'
  embed = discord.Embed(
    title = 'titlea',
    description = 'descrip',
    url = 'https://python.org',
    color = 0x123123,
    timestamp = datetime.datetime.now()
  )
  embed.add_field('f1', 'v1', True)
  embed.add_field('f2', 'v2', True)
  embed.add_field('f3', 'v3', True)
  embed.set_author(name = 'authorname', url = iurl, icon_url = iurl)
  embed.set_image(url = iurl)
  embed.set_thumbnail(url = iurl)
  embed.set_footer(text = 'footer text', icon_url = iurl)
  embed2 = discord.Embed(title = 'second title')

  await message.edit(embed = embed)
  await asyncio.sleep(1)
  await message.edit('many', embeds = [embed, embed2])
  await asyncio.sleep(1)

  data = (Path(__file__).parent / 'image.png').read_bytes()
  file = discord.File(data, 'image.png')

  await message.edit('image, embeds gone', embeds = None, file = file)
  await asyncio.sleep(1)
  await message.edit('same file idk', file = file)
  await asyncio.sleep(1)

  embed3 = discord.Embed(title = 'files + embed')
  embed3.set_image(url = 'attachment://image.png')

  await message.edit(content = None, embed = embed3, files = [file, file])
  await asyncio.sleep(1)
  await message.edit('files gone.', files = None)

@bot.event
async def on_message_create(data):
  print('got a message')

@bot.event(name = 'on_message_create')
async def another_event_func(data):
  print('got a message2')

bot.add_events(func_event)

@bot.event
async def on_ready(data):
  print('bot is ready', data)

@bot.command
async def loadcog(data):
  print('loaded math cog')
  await bot.load_extensions('cogs.utils')
  bot.add_commands(1)

@bot.command
async def unloadcog(data):
  print('unloaded math cog')
  await bot.unload_extensions('cogs.utils')

bot.add_commands(another_message_command)

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
