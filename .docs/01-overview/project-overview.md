# Project overview

> **TL;DR** Two beginner Python projects from the Exelerate Asia / K-Youth Python bootcamp
> (2023), preserved as-is: a Flask web app that serves jokes (JokeAPI) and country lookups
> (REST Countries), and a Pandas/Matplotlib/Seaborn analysis of a Kaggle anime dataset,
> plus two console-prototype notebooks. No manifest, no CI — everything runs through
> `uv` + `just`; an offline pytest suite (`just test`) guards the Flask app.

## What this repo is

A portfolio snapshot of work produced during the Python bootcamp with **Exelerate Asia**
and **K-Youth**. The code demonstrates two domains:

| Project | Where | What it shows |
| --- | --- | --- |
| Flask web app | `WebApp/` | Basic web development: routes, forms, Jinja2 templates, calling external REST APIs with `requests` |
| Data analysis | `Data Analyst/` | Pandas data manipulation, Matplotlib/Seaborn/WordCloud visualisation of an anime dataset |

The code is **preserved bootcamp work** — treat it as a historical artifact. Fix bugs when
asked, but do not restyle or modernise it uninvited.

## The Flask web app (`WebApp/`)

`WebApp/script.py` defines the whole app: three classes and four routes.

| Route | Methods | What it does |
| --- | --- | --- |
| `/` | GET | Home page (`home.html`) linking to the three features |
| `/random_joke` | GET | Fetches one random joke from JokeAPI and renders `joke.html` |
| `/specific_joke` | GET, POST | Form (`specific_joke_form.html`) for amount/language/category, then renders the jokes |
| `/country` | GET, POST | Form (`country_form.html`) to search by name/currency/language/capital, then renders `country.html` |

Classes: `JokeAPI` (URL building + response formatting for
[JokeAPI v2](https://jokeapi.dev/)), `CountriesAPI` (search-URL builders for
[REST Countries](https://restcountries.com/) **v5** with bearer-key auth), `Country` (a
display model built from one API response). Errors funnel to `error.html`.

**Note on the country API:** REST Countries retired its keyless v1–v4 endpoints; the
Flask app was migrated to v5 and works. It ships the public demo key (every search then
returns the API's fixed sample country) — export `RESTCOUNTRIES_API_KEY` with a free
personal key for real data. The Country **notebook** still carries the old v3.1 client
and crashes (notebooks are preserved as submitted).
Details in [`../06-troubleshooting/common-issues.md`](../06-troubleshooting/common-issues.md).

## The notebooks

| Notebook | What it contains | Headless (`just execute`)? |
| --- | --- | --- |
| `Data Analyst/Data Analyst.ipynb` | Pandas analysis + Matplotlib/Seaborn/WordCloud visualisations of the [Kaggle anime dataset (2022)](https://www.kaggle.com/datasets/vishalmane10/anime-dataset-2022/) | No — reads a hardcoded `C:\Users\Admin\Downloads\anime.csv` (not committed) and has raw markdown in a code cell (SyntaxError) |
| `WebApp/Joke API - Web App.ipynb` | Console prototype of the joke client, driven by an `input()` menu | No — `input()` has no stdin in a headless kernel |
| `WebApp/Country API.ipynb` | Console prototype of the country client (hardcoded searches) | No — it still carries the old v3.1 client: the retired API returns an error dict, and the notebook calls `.printCountryData()` on it |

Run them interactively instead: `just lab` opens Jupyter Lab on
`http://127.0.0.1:8124`.

## Historical note (from the original README)

The original README described the layout as `flask-web-app/` and `pandas-data-analyst/`
folders; the actual committed folders have always been `WebApp/` and `Data Analyst/`. The
project descriptions, API links and dataset link above are carried over from that README —
the folder names are corrected here.

## Related docs

| Doc | Why |
| --- | --- |
| [architecture.md](architecture.md) | How the Flask app's pieces fit together |
| [../02-setup/getting-started.md](../02-setup/getting-started.md) | Get it running on a fresh machine |
| [../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md) | The deprecated-API and notebook failure details |
