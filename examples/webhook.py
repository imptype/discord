import os
import asyncio
import discord

url = os.environ['WEBHOOK_URL']

async def main():
  webhook = discord.PartialWebhook.from_url(url)
  await webhook.send('aaaaa')

  def syncinasync():
    webhook = discord.SyncWebhook.from_url(url)
    webhook.send('bbbb')

  syncinasync()

asyncio.run(main())

webhook = discord.SyncWebhook.from_url(url)
webhook.send('ccc')