from pathlib import Path
import discord

wikipedia_tree = (
  'In botany, a tree is a perennial plant with an elongated stem, or trunk, '
  'usually supporting branches and leaves. In some usages, the definition of '
  'a tree may be narrower, e.g., including only woody plants with secondary growth, '
  'only plants that are usable for timber, or only plants above a specified height. '
  'Wider definitions include taller palms, tree ferns, bananas, and bamboos.'
)

image_path = Path(__file__).parent / '../other/image.png'

class Embeds(discord.Cog):
  def __init__(self, bot):
    self.bot = bot

  @discord.command
  async def embed(self, context):
    embed = discord.Embed(
      title = 'What is a tree?',
      description = wikipedia_tree,
      color = discord.color.blurple
    )
    await context.send(embed = embed)

  @discord.command
  async def image(self, context):
    file = discord.File(image_path.read_bytes(), image_path.name)
    await context.send('Here is image.png:', file = file)

  @discord.command
  async def embedimage(self, context):
    file = discord.File(image_path.read_bytes(), image_path.name)
    embed = discord.Embed(title = 'Image')
    embed.set_image('attachment://image.png')
    await context.send('Here is image.png in an embed:', embed = embed, file = file)

  @discord.command
  async def components(self, context):
    components = [
      discord.Container(
        discord.TextDisplay('## What is a tree?'),
        discord.TextDisplay(wikipedia_tree),
        accent_color = discord.color.blurple
      )
    ]
    await context.send(components = components)

  @discord.command
  async def layoutview(self, context):
    view = discord.LayoutView(
      discord.Container(
        discord.TextDisplay('## What is a tree? (using view = param)'),
        discord.TextDisplay(wikipedia_tree),
        accent_color = discord.color.blurple
      )
    )
    await context.send(view = view)

async def setup(bot):
  await bot.add_cogs(Embeds)
