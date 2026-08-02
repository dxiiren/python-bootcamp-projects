# Architecture

> **TL;DR** One Flask file (`WebApp/script.py`) holds two API-client classes, a display
> model and four routes; a shared `base.html` layout plus six Jinja2 page templates
> (Tailwind CDN) render the pages; dependencies are injected
> per-run by `uv run --with ...` (there is deliberately no requirements.txt). The
> notebooks are standalone and share nothing with the app.

## The Flask app

```
Browser ──> Flask route (script.py) ──> JokeAPI / CountriesAPI (requests) ──> external API
                    │                                     │
                    └── render_template(...) <── formatted text / Country object / error dict
```

| Piece | Role | Key details |
| --- | --- | --- |
| `JokeAPI` | Joke fetching + formatting | `base_url = https://v2.jokeapi.dev/joke/`; `randomJoke()` and `specificJoke(**kwargs)` build query strings (blacklist flags, category, `amount`, `lang`); `displayJoke(url)` handles single/twopart and multi-joke responses |
| `CountriesAPI` | Country search URL builders + fetch | `searchByName/Currency/Language/CapitalCity` return URLs under `https://restcountries.com/v3.1`; `createCountry(url)` GETs, picks `response.json()[0]`, and builds a `Country` |
| `Country` | Display model | name, currencies, capital, region, subregion, languages, population, timezones + `printCountryData()` |
| Routes | Controller layer | `/`, `/random_joke`, `/specific_joke` (GET form / POST result), `/country` (GET form / POST result) |
| Templates | Views (`WebApp/templates/`) | `base` (shared shell: amber header, nav, footer) extended by `home`, `joke`, `specific_joke_form`, `country_form`, `country`, `error` — Tailwind CSS via CDN |

Error handling pattern: API classes return a `{"error": ...}` dict on failure; routes check
for it and render `error.html`. (The Country notebook prototype skips that check — which is
why it crashes now that the API is deprecated.)

## Dependency model (why there is no requirements.txt)

The repo predates any packaging setup and is preserved that way. The `justfile` recipes
inject what each entry point needs at run time:

| Recipe | Injected packages |
| --- | --- |
| `just serve` | `flask`, `requests` |
| `just lab` | `jupyter` |
| `just execute <nb>` | `jupyter`, `nbclient`, `requests`, `pandas`, `matplotlib`, `seaborn`, `wordcloud` |

uv resolves and caches these once; later runs start in seconds. If you add an import to the
code, add the package to the matching `--with` list in the `justfile`.

## Port plan

Everything serves on **8124** (this repo's assigned port): `just lab` and `just serve`
share it, so run one at a time. `just stop` kills only processes whose command line carries
this repo's path — the `serve` recipe passes the **absolute** script path for exactly that
reason.

## Related docs

| Doc | Why |
| --- | --- |
| [project-overview.md](project-overview.md) | What each project is |
| [../05-reference/commands.md](../05-reference/commands.md) | The full recipe table |
| [../03-development/workflow.md](../03-development/workflow.md) | Day-2 development loop |
