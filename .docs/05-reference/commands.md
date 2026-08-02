# Commands reference

> **TL;DR** Everything is a `just` recipe; run `just` with no arguments to list them.
> `just lab` (notebooks) and `just serve` (Flask) share port 8124 — one at a time;
> `just stop` kills only this repo's servers.

## Daily recipes

| Command | What it does | Notes |
| --- | --- | --- |
| `just` | List all recipes | |
| `just lab` | Jupyter Lab on `http://127.0.0.1:8124` | Foreground; Ctrl+C or `just stop`. Root URL 302-redirects to `/lab` |
| `just execute <nb>` | Run one notebook headlessly via nbconvert | Executed copy goes to `%TEMP%` — never commit it. Quote paths with spaces: `just execute 'WebApp/Country API.ipynb'`. All three committed notebooks currently fail for documented reasons |
| `just serve` | Flask app on `http://127.0.0.1:8124` | Foreground. Passes the absolute `--app` path so `just stop` can match the process |
| `just test` | pytest suite (`tests/test_app.py`) via `uv run --with flask,requests,pytest` | Offline — external HTTP is monkeypatched; no server/port needed, safe alongside `just serve` |
| `just stop` | Kill this repo's `python.exe` processes | Project-scoped: matches the repo path on the command line; never touches other projects |
| `just claudex` | Claude Code, Sonnet, all permissions | Also `just claudeo` (Opus), `just claudeh` (Haiku) |

## One-time / occasional

| Command | What it does |
| --- | --- |
| `pwsh ./setup.ps1` | Install/verify the toolchain (idempotent) and seed `.mcp.json` |
| `uv run --no-project python -m py_compile WebApp/script.py` | Syntax gate for the app |
| `uv run --with jupyter jupyter --version` | Prove the Jupyter toolchain resolves |

## Environment knobs

| Variable | Effect | Default |
| --- | --- | --- |
| `PORT` | Overrides the serve/lab port | `8124` |

## Related docs

| Doc | Why |
| --- | --- |
| [project-layout.md](project-layout.md) | What file lives where |
| [../03-development/workflow.md](../03-development/workflow.md) | When to run which gate |
| [../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md) | Why `just execute` fails on the committed notebooks |
