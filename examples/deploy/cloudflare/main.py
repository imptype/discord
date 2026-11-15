import os
import uuid
from datetime import datetime, UTC
import discord

app = discord.App(
  public_key = os.environ['PUBLIC_KEY'],
  token = os.environ['TOKEN'],
  application_id = os.environ['APPLICATION_ID']
)

# @app.lifespan
# async def lifespan():
#   print(f'Synced {len(await app.sync())} commands!')
#   yield

instance_id = None
started_at = datetime.now(UTC)
request_count = 0
inflight_requests = 0

@app.command.slash()
async def cloudflare(interaction):

  # Cloudflare does not allow uuid usage at import time
  global instance_id
  if instance_id is None:
    instance_id = uuid.uuid4().hex[:8]

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

  try:
    await interaction.response.send(f'Hello from Cloudflare Workers! ```yml\n{debug}```')
  finally:
    inflight_requests -= 1
