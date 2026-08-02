# CLAUDE.md — python-bootcamp-projects

> Human-facing developer docs live in [`.docs/`](./.docs/README.md) — start at
> [`.docs/tldr.md`](./.docs/tldr.md). Keep them in sync when changing behavior they document.

## Project: Python Bootcamp Projects

Two beginner Python projects from the Exelerate Asia / K-Youth Python bootcamp (2023),
preserved as-is: a Flask web app that serves random/custom jokes (JokeAPI) and country
lookups (REST Countries), plus Jupyter notebooks — console prototypes of both API clients
and a Pandas/Matplotlib/Seaborn analysis of a Kaggle anime dataset.

- **Repo:** GitHub — `github.com/dxiiren/python-bootcamp-projects`
- **Runs locally only** — no CI/CD, no deployment target. `just lab` (Jupyter Lab) and
  `just serve` (the Flask app) both serve on `http://127.0.0.1:8124` — one at a time.

### Tech Stack Quick Reference

| Layer | Technology | Key details |
| --- | --- | --- |
| Language | Python 3 (uv-managed) | No requirements.txt/pyproject — every recipe injects deps via `uv run --with ...` |
| Web app | Flask + requests (`WebApp/script.py`) | Routes `/`, `/random_joke`, `/specific_joke`, `/country`; classes `JokeAPI`, `CountriesAPI`, `Country`; Jinja2 templates in `WebApp/templates/` |
| External APIs | JokeAPI v2 · REST Countries v3.1 | JokeAPI works; REST Countries **v3.1 is deprecated upstream** — `/country` and the Country notebook fail against the live API |
| Notebooks | Jupyter (Lab via `just lab`) | `Data Analyst.ipynb` (Pandas/Matplotlib/Seaborn/WordCloud, Kaggle anime CSV not committed) + two WebApp console prototypes |
| Tests | pytest (`just test`) | `tests/test_app.py` — Flask `test_client`, all external HTTP monkeypatched (offline). The dead `/country` route has an honest current-behavior test (asserts the error page), not a fake pass |
| Task runner | just | wraps `uv run` — see `justfile` |

### Project Structure

```
python-bootcamp-projects/
  Data Analyst/
    Data Analyst.ipynb         # Pandas analysis of a Kaggle anime dataset (CSV not committed)
  WebApp/
    script.py                  # Flask app — joke + country lookup routes
    templates/                 # 6 Jinja2 templates (home, joke, country, forms, error)
    Joke API - Web App.ipynb   # console prototype of the joke client (input()-driven)
    Country API.ipynb          # console prototype of the country client
  tests/
    test_app.py                # pytest suite (offline — external HTTP monkeypatched)
  .docs/                       # numbered documentation set
  .claude/                     # skills, hooks, settings
  justfile, setup.ps1
```

## Git Commits

- **Conventional Commits** (`feat:`, `fix:`, `chore:`, `docs:` ...).
- **NEVER** add `Co-Authored-By` lines or "Generated with Claude Code" / session-link footers to
  **any** outward artifact — commit messages, PR descriptions, or issue comments.
- Commit author email for this repo is `mohdakmal875@gmail.com` (set repo-locally).
- Only stage and commit files relevant to the change. **Never auto-commit** after a fix — the
  developer says "commit" first.

## Local Development

- One-time machine setup: `pwsh ./setup.ps1` (idempotent — installs Git, Node (for the Claude
  CLI), uv/Python, just, the Claude Code CLI). Then `just lab` (notebooks) or `just serve`
  (Flask app).
- All day-2 commands are `just` recipes — run `just` to list them. Never invent an alternative
  command for something a recipe already covers.
- `just stop` kills only THIS repo's server processes (matched by repo path on the command
  line) — safe to run while other projects are serving.
- The `serve` recipe passes the **absolute** `--app` path on purpose: with a relative
  `WebApp/script.py` the Flask processes carry no repo path on their command line and
  `just stop` can't find them. Don't "simplify" it back to a relative path.
- No dependency manifest exists on purpose — `uv run --with ...` supplies everything per-run.
  The first `just lab` / `just execute` downloads packages (minutes once, cached after).
- `just lab` and `just serve` share port 8124 — run one at a time.
- Headless `just execute` currently fails on all three committed notebooks, each for a real
  reason: the Joke notebook drives an `input()` menu, `Data Analyst.ipynb` reads a hardcoded
  `C:\Users\Admin\Downloads\anime.csv` (dataset not committed) and has a planning cell with
  raw markdown in a code cell, and the Country notebook hits the deprecated REST Countries
  v3.1 API. Use `just lab` to run them interactively cell by cell.
- `just execute` writes the executed copy to `%TEMP%` — never commit executed notebook outputs.

## Project Skills

Development skills live in `.claude/skills/` — check `.claude/skills/README.md` for the catalog
and **follow the relevant skill before writing code**. Notables: `/commit`, `/create-pr`,
`/pre-pr-review`, `/lint-check`, `/claude-transfer`, `/llm-transfer`, `/define-goal`,
`/setup-mcp`, `/test-all-mcp`, `/audit-skills`.

## MCP Servers

Wired via the committed-stub + git-ignored-secret pattern: `.mcp.json.stub` (committed,
placeholders) → `.mcp.json` (git-ignored, real — seeded by `setup.ps1`). Turnkey: `context7`
(library docs — call `resolve-library-id` then `query-docs` instead of recalling APIs),
`playwright` (drive a real browser). Per-dev: `github` (fill the PAT in `.mcp.json`).
Health check: `/test-all-mcp`. Fall back to native tools silently if a server is unavailable.

## Memory

Lightweight, single-developer, file-based project memory at `.claude/memory/`:

- **`MEMORY.md`** is the index (one line per memory: `- [Title](file.md) — hook`), loaded each
  session.
- Each memory is **one fact in its own `*.md` file** with frontmatter (`name`, `description`,
  `metadata.type` = `reference` | `feedback` | `project`). Read the fact file on demand when its
  index hook is relevant.
- After writing a fact file, add its one-line pointer to `MEMORY.md`. Update rather than
  duplicate; delete a memory that turns out wrong. Don't store what the repo already records.
