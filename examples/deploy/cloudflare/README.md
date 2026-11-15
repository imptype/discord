# Cloudflare Example

To deploy, you need these files:
- `pyproject.toml` - your bot's project defintion.
- `main.py` - your bot's source code.
- `wrangler.jsonc` - cloudflare's wrangler config.
- `cloudflare.py` - wraps cloudflare's entry point.

Because Cloudflare Workers isn't ready yet, you need these files too:
- `discord.py` - a stripped down Python 3.14 version of our library.
- `crypto.py` - an ed25519 verify key implementation to replace PyNaCl.

The other files `uv.lock`, `pylock.toml`, `example.env`, `.gitignore`, `.env`, `.venv/`, `.venv-workers/`, `.wrangler/`, `python_modules/` are for local testing so they can be skipped if you're just deploying.

## Testing locally
To run locally (for syncing commands), run this command:
```sh
uv run --env-file .env python discord.py main:app
```
To test cloudflare workers, run this command:
```sh
uv run pywrangler dev --log-level info
```

## Deploying
Deploy via dashboard, or run these commands:
```sh
uv run pywrangler secret bulk .env # create worker project with envs
uv run pywrangler deploy # deploys
```
The **Interactions Endpoint URL** to set should look like this:
```
https://<project>.<name>.workers.dev/interactions
```

## Note on Cloudflare Workers

Cloudflare Workers is <u>not</u> ready yet. This example is just a proof of concept, but here are the 2 issues that are blocking us:

1. **Only Python 3.14 is supported on Cloudflare workers.** Our library requires 3.15+ and Cloudflare has scheduled to support 3.15 in April 2027, so until then, this cloudflare example will use a stripped down `discord.py` file to represent the library.

2. **PyNaCl import errors.** PyNaCl uses libsodium, which uses `EM_ASM`, which does `eval`, which `workerd` (Cloudflare's runtime) does not allow. So a `crypto.py` file is required to replace the PyNaCl dependency. They will either fix it by 2027 or we'll remove our PyNaCl dep for our `asgi.app` too.
