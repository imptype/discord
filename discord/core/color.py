from enum import IntEnum

def convert(hex_color: str):
  return int(hex_color.removeprefix('#'), 16)

class Color(IntEnum):

  # Discord brand palette
  blurple = convert('#5865f2')
  green = convert('#57f287')
  yellow = convert('#fee75c')
  fuchsia = convert('#eb459e')
  red = convert('#ed4245')
  white = convert('#ffffff')
  black = convert('#000000')

  # Discord legacy brand palette
  og_blurple = convert('#7289da')
  greyple = convert('#99aab5')
  dark_but_not_black = convert('#2c2f33')
  not_quite_black = convert('#23272a')

  # Discord status colors
  online = convert('#23a55a')
  idle = convert('#f0b232')
  dnd = convert('#f23f43')
  offline = convert('#80848e')
  streaming = convert('#593695')

  # Discord button colors
  primary = blurple
  secondary = convert('#3e3f45')
  success = convert('#008545')
  danger = convert('#d22d39')

  # Color wheel (24 hues 15 deg, 100% saturation, 50% lightness)
  # red      = convert('#ff0000')
  vermilion = convert('#ff4000')
  amber = convert('#ff8000')
  orange = convert('#ffbf00')
  # yellow   = convert('#ffff00')
  chartreuse = convert('#bfff00')
  lime = convert('#80ff00')
  leaf = convert('#40ff00')
  # green    = convert('#00ff00')
  emerald = convert('#00ff40')
  spring = convert('#00ff80')
  aquamarine = convert('#00ffbf')
  cyan = convert('#00ffff')
  sky = convert('#00bfff')
  azure = convert('#007fff')
  cobalt = convert('#0040ff')
  blue = convert('#0000ff')
  indigo = convert('#4000ff')
  violet = convert('#7f00ff')
  purple = convert('#bf00ff')
  magenta = convert('#ff00ff')
  # fuchsia  = convert('#ff00bf')
  pink = convert('#ff0080')
  rose = convert('#ff0040')

  # Color wheel variants (10-90% lightness, 100% saturation)
  # Red
  pale_red = convert('#ffcccc')
  pastel_red = convert('#ff9999')
  light_red = convert('#ff6666')
  bright_red = convert('#ff3333')
  medium_red = convert('#ff0000')
  dim_red = convert('#cc0000')
  dark_red = convert('#990000')
  night_red = convert('#660000')
  ink_red = convert('#330000')

  # Vermilion
  pale_vermilion = convert('#ffd9cc')
  pastel_vermilion = convert('#ffb399')
  light_vermilion = convert('#ff8c66')
  bright_vermilion = convert('#ff6633')
  medium_vermilion = convert('#ff4000')
  dim_vermilion = convert('#cc3300')
  dark_vermilion = convert('#992600')
  night_vermilion = convert('#661a00')
  ink_vermilion = convert('#330d00')

  # Amber
  pale_amber = convert('#ffe6cc')
  pastel_amber = convert('#ffcc99')
  light_amber = convert('#ffb266')
  bright_amber = convert('#ff9933')
  medium_amber = convert('#ff8000')
  dim_amber = convert('#cc6600')
  dark_amber = convert('#994c00')
  night_amber = convert('#663300')
  ink_amber = convert('#331a00')

  # Orange
  pale_orange = convert('#fff2cc')
  pastel_orange = convert('#ffe699')
  light_orange = convert('#ffd966')
  bright_orange = convert('#ffcc33')
  medium_orange = convert('#ffbf00')
  dim_orange = convert('#cc9900')
  dark_orange = convert('#997300')
  night_orange = convert('#664d00')
  ink_orange = convert('#332600')

  # Yellow
  pale_yellow = convert('#ffffcc')
  pastel_yellow = convert('#ffff99')
  light_yellow = convert('#ffff66')
  bright_yellow = convert('#ffff33')
  medium_yellow = convert('#ffff00')
  dim_yellow = convert('#cccc00')
  dark_yellow = convert('#999900')
  night_yellow = convert('#666600')
  ink_yellow = convert('#333300')

  # Chartreuse
  pale_chartreuse = convert('#f2ffcc')
  pastel_chartreuse = convert('#e6ff99')
  light_chartreuse = convert('#d9ff66')
  bright_chartreuse = convert('#ccff33')
  medium_chartreuse = convert('#bfff00')
  dim_chartreuse = convert('#99cc00')
  dark_chartreuse = convert('#739900')
  night_chartreuse = convert('#4d6600')
  ink_chartreuse = convert('#263300')

  # Lime
  pale_lime = convert('#e6ffcc')
  pastel_lime = convert('#ccff99')
  light_lime = convert('#b3ff66')
  bright_lime = convert('#99ff33')
  medium_lime = convert('#80ff00')
  dim_lime = convert('#66cc00')
  dark_lime = convert('#4d9900')
  night_lime = convert('#336600')
  ink_lime = convert('#1a3300')

  # Leaf
  pale_leaf = convert('#d9ffcc')
  pastel_leaf = convert('#b2ff99')
  light_leaf = convert('#8cff66')
  bright_leaf = convert('#66ff33')
  medium_leaf = convert('#40ff00')
  dim_leaf = convert('#33cc00')
  dark_leaf = convert('#269900')
  night_leaf = convert('#196600')
  ink_leaf = convert('#0d3300')

  # Green
  pale_green = convert('#ccffcc')
  pastel_green = convert('#99ff99')
  light_green = convert('#66ff66')
  bright_green = convert('#33ff33')
  medium_green = convert('#00ff00')
  dim_green = convert('#00cc00')
  dark_green = convert('#009900')
  night_green = convert('#006600')
  ink_green = convert('#003300')

  # Emerald
  pale_emerald = convert('#ccffd9')
  pastel_emerald = convert('#99ffb3')
  light_emerald = convert('#66ff8c')
  bright_emerald = convert('#33ff66')
  medium_emerald = convert('#00ff40')
  dim_emerald = convert('#00cc33')
  dark_emerald = convert('#009926')
  night_emerald = convert('#00661a')
  ink_emerald = convert('#00330d')

  # Spring
  pale_spring = convert('#ccffe6')
  pastel_spring = convert('#99ffcc')
  light_spring = convert('#66ffb3')
  bright_spring = convert('#33ff99')
  medium_spring = convert('#00ff80')
  dim_spring = convert('#00cc66')
  dark_spring = convert('#00994d')
  night_spring = convert('#006633')
  ink_spring = convert('#00331a')

  # Aquamarine
  pale_aquamarine = convert('#ccfff2')
  pastel_aquamarine = convert('#99ffe6')
  light_aquamarine = convert('#66ffd9')
  bright_aquamarine = convert('#33ffcc')
  medium_aquamarine = convert('#00ffbf')
  dim_aquamarine = convert('#00cc99')
  dark_aquamarine = convert('#009973')
  night_aquamarine = convert('#00664d')
  ink_aquamarine = convert('#003326')

  # Cyan
  pale_cyan = convert('#ccffff')
  pastel_cyan = convert('#99ffff')
  light_cyan = convert('#66ffff')
  bright_cyan = convert('#33ffff')
  medium_cyan = convert('#00ffff')
  dim_cyan = convert('#00cccc')
  dark_cyan = convert('#009999')
  night_cyan = convert('#006666')
  ink_cyan = convert('#003333')

  # Sky
  pale_sky = convert('#ccf2ff')
  pastel_sky = convert('#99e6ff')
  light_sky = convert('#66d9ff')
  bright_sky = convert('#33ccff')
  medium_sky = convert('#00bfff')
  dim_sky = convert('#0099cc')
  dark_sky = convert('#007399')
  night_sky = convert('#004d66')
  ink_sky = convert('#002633')

  # Azure
  pale_azure = convert('#cce5ff')
  pastel_azure = convert('#99ccff')
  light_azure = convert('#66b2ff')
  bright_azure = convert('#3399ff')
  medium_azure = convert('#007fff')
  dim_azure = convert('#0066cc')
  dark_azure = convert('#004c99')
  night_azure = convert('#003366')
  ink_azure = convert('#001933')

  # Cobalt
  pale_cobalt = convert('#ccd9ff')
  pastel_cobalt = convert('#99b2ff')
  light_cobalt = convert('#668cff')
  bright_cobalt = convert('#3366ff')
  medium_cobalt = convert('#0040ff')
  dim_cobalt = convert('#0033cc')
  dark_cobalt = convert('#002699')
  night_cobalt = convert('#001966')
  ink_cobalt = convert('#000d33')

  # Blue
  pale_blue = convert('#ccccff')
  pastel_blue = convert('#9999ff')
  light_blue = convert('#6666ff')
  bright_blue = convert('#3333ff')
  medium_blue = convert('#0000ff')
  dim_blue = convert('#0000cc')
  dark_blue = convert('#000099')
  night_blue = convert('#000066')
  ink_blue = convert('#000033')

  # Indigo
  pale_indigo = convert('#d9ccff')
  pastel_indigo = convert('#b399ff')
  light_indigo = convert('#8c66ff')
  bright_indigo = convert('#6633ff')
  medium_indigo = convert('#4000ff')
  dim_indigo = convert('#3300cc')
  dark_indigo = convert('#260099')
  night_indigo = convert('#1a0066')
  ink_indigo = convert('#0d0033')

  # Violet
  pale_violet = convert('#e5ccff')
  pastel_violet = convert('#cc99ff')
  light_violet = convert('#b266ff')
  bright_violet = convert('#9933ff')
  medium_violet = convert('#7f00ff')
  dim_violet = convert('#6600cc')
  dark_violet = convert('#4c0099')
  night_violet = convert('#330066')
  ink_violet = convert('#190033')

  # Purple
  pale_purple = convert('#f2ccff')
  pastel_purple = convert('#e699ff')
  light_purple = convert('#d966ff')
  bright_purple = convert('#cc33ff')
  medium_purple = convert('#bf00ff')
  dim_purple = convert('#9900cc')
  dark_purple = convert('#730099')
  night_purple = convert('#4d0066')
  ink_purple = convert('#260033')

  # Magenta
  pale_magenta = convert('#ffccff')
  pastel_magenta = convert('#ff99ff')
  light_magenta = convert('#ff66ff')
  bright_magenta = convert('#ff33ff')
  medium_magenta = convert('#ff00ff')
  dim_magenta = convert('#cc00cc')
  dark_magenta = convert('#990099')
  night_magenta = convert('#660066')
  ink_magenta = convert('#330033')

  # Fuchsia
  pale_fuchsia = convert('#ffccf2')
  pastel_fuchsia = convert('#ff99e5')
  light_fuchsia = convert('#ff66d9')
  bright_fuchsia = convert('#ff33cc')
  medium_fuchsia = convert('#ff00bf')
  dim_fuchsia = convert('#cc0099')
  dark_fuchsia = convert('#990073')
  night_fuchsia = convert('#66004c')
  ink_fuchsia = convert('#330026')

  # Pink
  pale_pink = convert('#ffcce6')
  pastel_pink = convert('#ff99cc')
  light_pink = convert('#ff66b3')
  bright_pink = convert('#ff3399')
  medium_pink = convert('#ff0080')
  dim_pink = convert('#cc0066')
  dark_pink = convert('#99004d')
  night_pink = convert('#660033')
  ink_pink = convert('#33001a')

  # Rose
  pale_rose = convert('#ffccd9')
  pastel_rose = convert('#ff99b2')
  light_rose = convert('#ff668c')
  bright_rose = convert('#ff3366')
  medium_rose = convert('#ff0040')
  dim_rose = convert('#cc0033')
  dark_rose = convert('#990026')
  night_rose = convert('#660019')
  ink_rose = convert('#33000d')

  @classmethod
  def _missing_(cls, value): # color('#ff8800')
    member = int.__new__(cls, convert(str(value)))
    member._name_ = str(value)
    member._value_ = int(member)
    return member

color = Color
colour = Color # alias
