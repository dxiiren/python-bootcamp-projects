# TL;DR — every doc in 30 seconds

One paragraph per document. Read this page, then dive into whichever doc you actually
need.

## [01-overview/project-overview.md](01-overview/project-overview.md)

Two beginner projects from the 2023 Exelerate Asia / K-Youth Python bootcamp, preserved
as-is. `WebApp/` is a Flask app with four routes serving jokes (JokeAPI — still works) and
country lookups (REST Countries v3.1 — deprecated upstream, so `/country` always errors).
`Data Analyst/` is a Pandas/Matplotlib/Seaborn notebook over a Kaggle anime dataset whose
CSV was never committed. Two more notebooks are console prototypes of the API clients.
Treat the code as a historical artifact — fix, don't restyle.

## [01-overview/architecture.md](01-overview/architecture.md)

One file (`WebApp/script.py`) holds everything: `JokeAPI` and `CountriesAPI` build URLs and
fetch with `requests`, `Country` is the display model, four routes render six Tailwind-
styled Jinja2 templates (all extending a shared `base.html` shell), and failures funnel to
`error.html` as `{"error": ...}` dicts. There is no
requirements.txt on purpose — each `just` recipe injects its own deps via
`uv run --with ...`. Everything serves on port 8124, one server at a time.

## [02-setup/getting-started.md](02-setup/getting-started.md)

`pwsh ./setup.ps1` once (Git, Node for the Claude CLI, uv+Python, just, gh — idempotent),
reopen PowerShell, then `just lab` for notebooks or `just serve` for the Flask app, both on
`http://127.0.0.1:8124`. First run downloads packages into the uv cache — minutes once,
seconds after. A working install shows the home page at `/`, a joke at `/random_joke`, and
(expectedly) the error page for `/country` searches.

## [03-development/workflow.md](03-development/workflow.md)

Branch off `main`, edit, then verify with the gate matching your change: `just test`
(offline pytest — external HTTP monkeypatched) + `just serve` + a route check for app
code, an interactive cell run in `just lab` for notebooks, a re-run for tooling.
`just stop` before switching servers. Commit via the `/commit` skill (Conventional
Commits, no attribution footers), PR via `/create-pr`. New imports go into the justfile's
`--with` list in the same commit.

## [04-deployment/deployment.md](04-deployment/deployment.md)

There is nothing to deploy: no CI/CD, no hosting, no build artifact — the repo runs
locally only, and "shipping" is a push to `main`. The doc also lists what a real
deployment would require (a manifest, a WSGI server, config, and migrating off the dead
country API) so nobody mistakes the dev server for a target.

## [05-reference/commands.md](05-reference/commands.md)

The recipe table: `just lab` / `just serve` (both :8124, one at a time), `just execute
'<nb>'` (headless nbconvert, output to `%TEMP%`), `just test` (offline pytest suite),
`just stop` (project-scoped kill), `just claudex/claudeo/claudeh` (Claude Code tiers),
plus the occasional commands (`setup.ps1`, the `py_compile` gate) and the `PORT` override.

## [05-reference/project-layout.md](05-reference/project-layout.md)

Annotated tree: the two project folders, the seven templates (shared base + six pages),
the pytest suite (`tests/`),
and the kit files — plus the deliberate absences (no manifest, no committed CSV) and which
paths are generated-and-ignored (`.ipynb_checkpoints/`, `__pycache__/`, `.pytest_cache/`,
`.mcp.json`).

## [06-troubleshooting/common-issues.md](06-troubleshooting/common-issues.md)

The real failures, with observed errors: all three notebooks fail `just execute`
(`input()` menu; hardcoded missing CSV + a markdown-in-code-cell SyntaxError; dead API →
`AttributeError` on the error dict), `/country` always errors (v3.1 deprecated), first runs
are slow (uv cache fill), port 8124 is shared, and `just stop` depends on the absolute
`--app` path staying absolute.

## [07-faq/faq.md](07-faq/faq.md)

Why there's no requirements.txt (preserved repo; uv injects per-run), why one shared port
(one port per repo in this workspace), why headless notebook runs fail (real blockers, not
config), why `/country` stays visibly broken (documented known issue vs silent patch), and
where Claude Code rules live (`CLAUDE.md` + `.claude/skills/`).
