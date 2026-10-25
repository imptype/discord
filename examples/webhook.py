import os
import asyncio
import discord

url = os.environ['WEBHOOK_URL']

async def main():
  webhook = discord.PartialWebhook.from_url(url)
  await webhook.send('aaaaa')

asyncio.run(main())
