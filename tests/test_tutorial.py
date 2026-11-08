import asyncio
from typing import assert_type
from unittest.mock import AsyncMock, MagicMock
import pytest
import discord

TEST_TOKEN = 'test-token'

TUTORIAL_SOURCE = """
import os
import discord

intents = discord.Intents.default() | discord.Intents.MESSAGE_CONTENT
bot = discord.Bot(token = os.environ['TOKEN'], intents = intents)

@bot.command
async def ping(context):
  await context.send('pong!')

bot.run()
"""

@pytest.fixture
def bot(monkeypatch):
  monkeypatch.setenv('TOKEN', TEST_TOKEN)
  monkeypatch.setattr(discord.Bot, 'run', MagicMock())
  namespace = {}
  exec(TUTORIAL_SOURCE, namespace)
  bot = namespace['bot']
  bot.http.create_message = AsyncMock(return_value = {
    'id': '101',
    'channel_id': '200',
    'content': 'pong!',
    'author': {'id': '1', 'username': 'bot'}
  })
  return bot

def test_privileged_message_content_is_not_default():
  assert not discord.Intents.default() & discord.Intents.MESSAGE_CONTENT

def test_bot_intents_are_default_plus_message_content(bot):
  assert bot.intents == discord.Intents.default() | discord.Intents.MESSAGE_CONTENT

def test_token_is_set_on_http_client(bot):
  assert bot.http.token == TEST_TOKEN

def test_ping_command_registered(bot):
  assert bot.command_handlers['ping'].name == 'ping'

def test_stub_types(bot: discord.Bot):
  assert_type(bot.http.token, str | None)
  assert_type(bot.intents, discord.Intents)
  assert_type(bot.prefix, str)

@pytest.mark.asyncio
async def test_ping_reply(bot):
  bot.loop = asyncio.get_running_loop()
  await bot.on_event('MESSAGE_CREATE', {
    'id': '100',
    'channel_id': '200',
    'content': '!ping',
    'author': {'id': '300', 'username': 'tester'}
  })
  await asyncio.gather(*bot.tasks)
  channel_id, payload = bot.http.create_message.await_args.args
  assert channel_id == 200
  assert payload.body == {'content': 'pong!'}
