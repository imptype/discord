import os
import asyncio
import discord

url = os.environ['WEBHOOK_URL']

async def main():
  webhook = discord.PartialWebhook.from_url(url)
  await webhook.send('aaaaa')

  def sync_in_async():
    webhook = discord.SyncWebhook.from_url(url)
    webhook.send('bbbb')

  sync_in_async()

asyncio.run(main())

webhook = discord.SyncWebhook.from_url(url)
webhook.send('ccc')
