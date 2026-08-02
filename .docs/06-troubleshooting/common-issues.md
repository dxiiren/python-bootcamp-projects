# Common issues

> **TL;DR** Every symptom below was hit for real while verifying this kit. Headline items:
> all three committed notebooks fail `just execute` for real reasons; the `/country`
> feature runs on REST Countries **v5** (the app was migrated off the retired v3.1) and
> shows the API's fixed sample country until you export a personal key.

## `just execute` fails on every committed notebook

Expected — each has a genuine blocker, observed on 2026-08-02:

| Notebook | Failure | Root cause |
| --- | --- | --- |
| `WebApp/Joke API - Web App.ipynb` | `CellExecutionError` at the `input()` menu | Interactive-only: a headless kernel has no stdin |
| `Data Analyst/Data Analyst.ipynb` | `FileNotFoundError: C:\Users\Admin\Downloads\anime.csv` in cell 1 | The Kaggle CSV was never committed and the path is hardcoded to the original author's machine. Cell 2 would then fail anyway: it is a planning note written as raw markdown in a code cell (`- Best Anime for each year (top 1,2,3)` → `SyntaxError`) |
| `WebApp/Country API.ipynb` | `AttributeError: 'dict' object has no attribute 'printCountryData'` | The notebook still carries its own inline copy of the 2023 v3.1 client (notebooks are preserved as-submitted): the retired API returns a deprecation notice, `createCountry` returns its error dict, and the notebook calls a `Country` method on it. The Flask app's `CountriesAPI` was migrated to v5 and works |

Work interactively instead: `just lab`, open the notebook, run cells one by one. To make
the Data Analyst notebook run, download the
[Kaggle anime dataset](https://www.kaggle.com/datasets/vishalmane10/anime-dataset-2022/)
and fix the `file_path` in cell 1 to where you saved it.

## `/country` always shows the same country (Canada) — FIXED (was: always the error page)

Historical: REST Countries retired the keyless v1–v4 endpoints, so `/country` used to
error on every search. `WebApp/script.py` now targets **v5**
(`api.restcountries.com/countries/v5`, bearer-token auth, `data.objects` payloads —
verified live 2026-08-02). Out of the box it authenticates with the public no-account
demo key, which answers every query with the API's fixed sample country (Canada) — that
is the expected demo behavior, not a bug. For real results, export a free personal key
before serving:

```powershell
$env:RESTCOUNTRIES_API_KEY = "rc_live_..."   # https://restcountries.com/sign-up
just serve
```

If `/country` lands on the **error page**: a 401 means the key is missing/expired
upstream; "No country matched that search." means the (real-keyed) search found nothing.

## First `just lab` / `just execute` / `just serve` takes minutes

uv is downloading the injected packages (Jupyter is ~96 packages; `execute` adds
pandas/matplotlib/seaborn/wordcloud) into its cache on first use. Later runs reuse the
cache and start in seconds. A slow first run is not a hang.

## Port 8124 already in use

`just lab` and `just serve` share port 8124 — run one at a time. `just stop` kills
whichever this repo has running and never touches other projects' servers.

## `just stop` says "Stopped 0" but the server is still up

`stop` matches processes by this repo's absolute path on the command line. The `serve`
recipe deliberately passes `--app '<repo>\WebApp\script.py'` as an absolute path so the
match works — if you change it back to a relative path, Flask's processes become
invisible to `just stop` (this exact bug was hit and fixed during kit verification).
If you're ever stuck: find the PID with
`Get-CimInstance Win32_Process -Filter "Name = 'python.exe'"` and `Stop-Process -Id` it.

## Jupyter Lab "redirects" instead of serving `/`

Normal: GET `http://127.0.0.1:8124/` answers 302 to `/lab` (and may bounce via a token
login page on some setups). The server is healthy if anything answers on 8124.

## Related docs

| Doc | Why |
| --- | --- |
| [../07-faq/faq.md](../07-faq/faq.md) | Design-decision questions (why no requirements.txt, etc.) |
| [../05-reference/commands.md](../05-reference/commands.md) | The recipes referenced above |
