# Project layout

> **TL;DR** Two project folders (`WebApp/`, `Data Analyst/`) hold all the bootcamp code;
> everything else is the onboarding kit (justfile, setup.ps1, `.docs/`, `.claude/`).

## Tree

```
python-bootcamp-projects/
  Data Analyst/
    Data Analyst.ipynb         # Pandas/Matplotlib/Seaborn/WordCloud analysis of a Kaggle
                               #   anime dataset (CSV not committed; hardcoded local path)
  WebApp/
    script.py                  # The whole Flask app: JokeAPI, CountriesAPI, Country + 4 routes
    templates/
      home.html                # Landing page linking the three features
      joke.html                # Renders fetched joke text
      specific_joke_form.html  # Amount / language / category form
      country_form.html        # Search-type + term form
      country.html             # Country details table
      error.html               # Error page every failure funnels to
    Joke API - Web App.ipynb   # Console prototype of the joke client (input()-driven)
    Country API.ipynb          # Console prototype of the country client (hardcoded searches)
  .docs/                       # This documentation set (01-overview ... 07-faq + tldr)
  .claude/                     # Claude Code kit: skills, hooks/statusline, settings, memory
  .mcp.json.stub               # Committed MCP config template (real .mcp.json is git-ignored)
  CLAUDE.md                    # Agent contract for Claude Code sessions
  justfile                     # All day-2 commands (lab / execute / serve / stop / claude*)
  setup.ps1                    # One-time idempotent machine setup
  README.md                    # Front door: quick start + cheat sheet
```

## Notable absences (deliberate)

| Missing | Why |
| --- | --- |
| `requirements.txt` / `pyproject.toml` | Preserved repo; deps are injected per-run via `uv run --with ...` in the justfile |
| Tests, linter configs | Never existed; `/lint-check` runs the honest substitutes |
| `anime.csv` | The Kaggle dataset was never committed — download it yourself to run the analysis notebook |
| CI workflows | Local-only repo |

## Generated / ignored paths

| Path | Source | Git status |
| --- | --- | --- |
| `.ipynb_checkpoints/` | Jupyter autosave | ignored |
| `__pycache__/` | Python imports | ignored |
| `.mcp.json`, `.claude/settings.local.json`, `.claude/workspace/` | per-dev Claude config/scratch | ignored |
| `%TEMP%\<notebook>.ipynb` | `just execute` output | outside the repo by design |

## Related docs

| Doc | Why |
| --- | --- |
| [commands.md](commands.md) | The recipes that operate on this tree |
| [../01-overview/architecture.md](../01-overview/architecture.md) | How the WebApp pieces connect |
