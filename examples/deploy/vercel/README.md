# Vercel Example
To deploy, you need these files:
- `pyproject.toml` - your bot's project defintion.
- `main.py` - your bot's source code.

Because Vercel doesn't have Python 3.15 built-in yet, you need this too:
- `Dockerfile.vercel` - vercel docker file.

The other files `uv.lock`, `example.env`, `.env`, `.env.local`, `.gitignore`, `.venv/`, `.vercel/` are for local testing so they can be skipped if you're just deploying.

## Testing locally
To run locally (for syncing commands), run this command:
```sh
uv run --env-file .env discord main:app
```
To test vercel, run this command:
```sh
vercel dev
```

## Deploying
Deploy via dashboard, or run this command:
```sh
vercel deploy --prod
```
The **Interactions Endpoint URL** to set should look like this:
```
https://<project-name>.vercel.app/interactions
```
