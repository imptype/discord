# discord

A minimal **Python 3.15** library for **Discord's API**.

## Requirements
- Python 3.15
- Recommended to use VSCode, `uv`, and other stuff.

## Installation
Install this library from **PyPI** using the `uv` package manager:
```sh
uv add idiscord
```

## Quick Example
Example of a `main.py` and `.env` files:
```py
import os
import discord

intents = discord.Intents.default()
intents.message_content = True
bot = discord.bot(os.environ['TOKEN'], intents = intents)

@bot.command
async def ping(context):
  await context.send('pong!')

bot.run()
```
```
TOKEN=abc
```
Run with `python main.py`, `CTRL+C` to stop.
 
This runs a bot with a text `!ping` command (message content intent must be enabled in the Developer Portal).  
More code examples are found in the  `/examples` folder, and check the docs for tutorials and the API reference.

## Links
- **PyPI:** https://pypi.org/project/idiscord
- **GitHub:** https://github.com/imptype/discord
- **Documentation:** https://imptype.github.io/discord/
- **Development Server:** https://discord.gg/8jrGWh9dPt
- **Discord API Docs:** https://docs.discord.com/developers
- **Discord Developer Portal:** https://discord.com/developers/applications
