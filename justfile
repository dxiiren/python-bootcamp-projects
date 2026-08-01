# Python Bootcamp Projects justfile — development recipes

set shell := ["powershell.exe", "-NoProfile", "-Command"]

port := env_var_or_default('PORT', '8124')

# List available recipes
default:
    @just --list

# ─── Guards ───────────────────────────────────────────────

# uv — installed by setup.ps1; provides Python + Jupyter on demand (nothing global).
[private]
_require-uv:
    @if (-not (Get-Command uv -ErrorAction SilentlyContinue)) { Write-Error "uv not found on PATH.`n  -> Run setup.ps1 first:  pwsh ./setup.ps1"; exit 1 }

# ─── Notebooks ───────────────────────────────────────────

# Open Jupyter Lab on http://127.0.0.1:{{port}} (foreground, Ctrl+C to stop).
lab: _require-uv
    uv run --with jupyter jupyter lab --no-browser --port {{port}} --notebook-dir '{{justfile_directory()}}'

# The --with list carries every library the committed notebooks import (requests,
# pandas/matplotlib/seaborn/wordcloud) so execution never dies on a missing import.
# NOTE: all three committed notebooks are interactive / API-bound — see
# .docs/06-troubleshooting/common-issues.md before expecting exit 0.
# Execute one notebook headlessly (checks it still runs end to end).
# Example: just execute 'WebApp/Country API.ipynb'
execute nb: _require-uv
    uv run --with jupyter,nbclient,requests,pandas,matplotlib,seaborn,wordcloud jupyter nbconvert --to notebook --execute '{{nb}}' --output-dir $env:TEMP

# ─── Flask web app ───────────────────────────────────────

# Shares port {{port}} with `just lab` — run one at a time. The absolute --app path is
# deliberate: it puts the repo path on the process command line so `just stop` can match it.
# Serve the Flask web app (WebApp/script.py) on http://127.0.0.1:{{port}} (foreground, Ctrl+C to stop).
serve: _require-uv
    uv run --with flask,requests flask --app '{{justfile_directory()}}\WebApp\script.py' run --port {{port}}

# ─── Housekeeping ────────────────────────────────────────

# Stop only THIS project's Jupyter/Flask server (matches by repo path on the command line).
stop:
    $procs = @(Get-CimInstance Win32_Process -Filter "Name = 'python.exe'" | Where-Object { $_.CommandLine -like '*{{justfile_directory()}}*' }); $procs | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }; Write-Host "Stopped $($procs.Count) project python.exe process(es)"

# ─── Tools ───────────────────────────────────────────────

# Launch Claude Code with all permissions — Sonnet (latest)
claudex:
    claude --dangerously-skip-permissions --model sonnet

# Launch Claude Code with all permissions — Opus (latest)
claudeo:
    claude --dangerously-skip-permissions --model opus

# Launch Claude Code with all permissions — Haiku (latest)
claudeh:
    claude --dangerously-skip-permissions --model haiku
