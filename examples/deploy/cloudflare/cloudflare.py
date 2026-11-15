import os
from workers import asgi, env # ty: ignore[unresolved-import]

# Inject Cloudflare environment variables
os.environ['PUBLIC_KEY'] = env.PUBLIC_KEY
os.environ['TOKEN'] = env.TOKEN
os.environ['APPLICATION_ID'] = env.APPLICATION_ID

# Import only after injecting variables
from main import app

Default = asgi.entrypoint(app)
