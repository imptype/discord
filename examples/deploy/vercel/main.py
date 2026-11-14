import os
import uuid
from datetime import datetime, UTC
import discord

app = discord.App(
  public_key = os.environ['PUBLIC_KEY'],
  token = os.environ['TOKEN'],
  application_id = os.environ['APPLICATION_ID']
)

instance_id = uuid.uuid4().hex[:8]
started_at = datetime.now(UTC)
request_count = 0
inflight_requests = 0

@app.command.slash()
async def vercel(interaction):

  latency = (datetime.now(UTC) - interaction.created_at).total_seconds() * 1000

  global request_count
  request_count += 1

  global inflight_requests
  inflight_requests += 1

  debug = '\n'.join(
    f'{k}: {v}'
    for k, v in {
      'Ping': f'{latency:.2f} ms',
      'Request Count': request_count,
      'Is Cold Start': request_count == 1,
      'Instance ID': instance_id,
      'Inflight Requests': inflight_requests
    }.items()
  )

  await interaction.response.send(f'Hello from Vercel! ```yml\n{debug}```')

  inflight_requests -= 1
