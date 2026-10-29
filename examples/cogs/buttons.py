import random
import discord

class ButtonsCog(discord.Cog):
  # def __init__(self, bot): # init not required, internally sets self.app for u
  #   self.bot = bot

  @discord.command
  async def hibutton(self, context):
    @discord.button('Hi')
    async def hi_button(interaction):
      await interaction.response.send('Hi! You clicked a button.')
    view = discord.View(hi_button)
    await context.send(view = view)
    # await context.send(components = [discord.ActionRow(hi_button)]) # alt, but it makes it cv2 message

  @discord.command
  async def counter(self, context):
    count = 0
    @discord.button('Click me')
    async def counter_button(interaction):
      nonlocal count
      count += 1
      interaction.component.label = f'Clicked {count} times'
      await interaction.response.update(view = view)
    view = discord.View(counter_button)
    await context.send('Click the button to count!', view = view)

  @discord.command
  async def select(self, context):
    options = 'Red', 'Blue', discord.SelectOption('Green', description = 'Ay, the grass is green.')
    @discord.string_select(*options, placeholder = 'Pick a color')
    async def color_select(interaction):
      await interaction.response.send(f'You picked: {interaction.values[0]}', ephemeral = True)
    view = discord.View(color_select)
    await context.send('Here is a select menu:', view = view)

  @discord.command
  async def layoutbuttons(self, context):
    async def on_click(interaction): # callback = param, instead of using a decorator in a class
      await interaction.response.send(f'You clicked {interaction.component.label}!', ephemeral = True)
    view = discord.LayoutView(
      discord.Container(
        discord.TextDisplay('## Buttons in a LayoutView'),
        discord.Section(
          discord.TextDisplay('A section with a button accessory'),
          accessory = discord.Button('Section button', callback = on_click)
        ),
        discord.Separator(),
        discord.ActionRow(
          discord.Button('One', callback = on_click),
          discord.Button('Two', style = discord.ButtonStyle.Secondary, callback = on_click),
          discord.Button('Disabled', disabled = True)
        ),
        accent_color = discord.color.blurple
      )
    )
    await context.send(view = view)

  class DiceView(discord.View): # example of a persistent view, loads and unloads with the cog
    def __init__(self, loaded_by_cog = True):
      super().__init__()
      self.loaded_by_cog = loaded_by_cog

    @discord.button('Roll Dice', custom_id = 'DiceView:roll')
    async def roll_button(self, interaction):
      await interaction.response.send(f'You rolled: {random.randint(1, 6)}')

    @discord.button('Debug', custom_id = 'DiceView:debug')
    async def debug_button(self, interaction):
      text = 'This view was registered by the "!dice" command.'
      if self.loaded_by_cog:
        text = 'This view was registered on cog load.'
      await interaction.response.send(text)

  @discord.command
  async def dice(self, context):
    view = self.DiceView(loaded_by_cog = False)
    # print(self.instances['DiceView'].loaded_by_cog) # this is the instance loaded by the cog!
    await context.send('Roll the dice:', view = view)

async def setup(bot):
  await bot.add_cogs(ButtonsCog)
