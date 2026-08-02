# Getting started

> **TL;DR** Run `pwsh ./setup.ps1` once (installs Git, Node for the Claude CLI, uv+Python,
> just, GitHub CLI), reopen PowerShell, then `just lab` for the notebooks or `just serve`
> for the Flask app — both on `http://127.0.0.1:8124`. First run downloads packages into
> the uv cache; expect a wait once.

## Prerequisites

Only PowerShell + winget (stock Windows 10/11). Everything else is installed by the setup
script:

| Tool | Why | Installed by |
| --- | --- | --- |
| Git | version control | `setup.ps1` |
| Node.js LTS | required by the Claude Code CLI | `setup.ps1` |
| uv (+ Python) | runs everything Python — no global pip/venv needed | `setup.ps1` |
| just | task runner (all day-2 commands) | `setup.ps1` |
| GitHub CLI | used by `/commit` and `/create-pr` skills | `setup.ps1` |
| Claude Code CLI | optional, AI-assisted dev | `setup.ps1` |

## Steps

1. Clone and enter the repo:

   ```powershell
   git clone https://github.com/dxiiren/python-bootcamp-projects.git
   cd python-bootcamp-projects
   ```

2. Run the one-time setup (idempotent — safe to re-run any time):

   ```powershell
   pwsh ./setup.ps1
   ```

   Every line should end `[OK]`. The script also seeds a git-ignored `.mcp.json` from
   `.mcp.json.stub` for Claude Code MCP servers.

3. **Close and reopen PowerShell** so PATH updates land.

4. Start either entry point (they share port 8124 — one at a time):

   ```powershell
   just lab     # Jupyter Lab for the notebooks
   just serve   # the Flask web app
   ```

5. Open `http://127.0.0.1:8124`. Stop with Ctrl+C in that terminal, or `just stop` from
   another one.

## What "working" looks like

| Check | Expected |
| --- | --- |
| `just serve` then GET `/` | 200, home page titled "Welcome to Akmal's Web App Project" |
| `/random_joke` | 200 with a joke (JokeAPI is live) |
| `/country` search | 200 with a country table — the API's fixed sample country (Canada) under the bundled demo key; real results need `RESTCOUNTRIES_API_KEY` (see troubleshooting) |
| `just lab` | Jupyter Lab answers on 8124 (the root URL 302-redirects to `/lab`) |

## Related docs

| Doc | Why |
| --- | --- |
| [../03-development/workflow.md](../03-development/workflow.md) | The day-2 loop after setup |
| [../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md) | If a step above didn't match |
| [../05-reference/commands.md](../05-reference/commands.md) | Every recipe, one table |
