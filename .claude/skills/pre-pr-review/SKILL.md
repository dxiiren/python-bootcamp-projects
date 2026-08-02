---
name: pre-pr-review
description: Use when the developer says 'pre-pr review', 'review my branch', 'audit my work', or 'self review' — self-reviews the current branch's diff against a Flask + notebooks checklist (route/template sync, API error paths, notebook hygiene, docs sync) before opening a PR, then saves a report to .claude/workspace/reports/pr/.
model: opus
---

# Pre-PR Review (Self-Audit)

Self-review your feature-branch diff **before** opening a PR. This is a preserved bootcamp
repo — a small Flask app (`WebApp/script.py` + 6 Jinja2 templates) and three Jupyter
notebooks, with an offline pytest suite (`just test`) but no dependency manifest — the
goal is to catch correctness,
error-path, and sync problems early, not to restyle preserved bootcamp code.

## Trigger

- `"pre-pr review"` / `"self review"`
- `"review my branch"` / `"review my work"` / `"review my code"`
- `"audit my work"` / `"audit my branch"`

## Do NOT flag

- The app's existing tutorial-style comments and naming (`createCountry`, `displayJoke`
  camelCase) — that IS the preserved bootcamp code; only flag conventions in NEW code.
- Pre-existing patterns the developer copied from the codebase — not this branch's problem.
- Style-only rewrites of untouched code unless the branch touches those lines anyway.
- The `/country` route failing against the live API — REST Countries v3.1 is deprecated
  upstream (documented known issue), unless the branch claims to fix it.

## Step 1 — Branch & base

```bash
git branch --show-current
```

If on `main`: **STOP** — "You're on `main`; switch to your feature branch first."

```bash
git fetch origin main
git diff origin/main...HEAD --name-only
```

If no files changed: **STOP** — "No changes vs `main`."

Scope the review to reviewable source: `WebApp/**` (`*.py`, `templates/*.html`), `*.ipynb`,
`justfile`, `setup.ps1`. **Exclude** `.claude/` and generated artifacts. If only excluded
files changed: **STOP** — "No reviewable source changed."

Report: "Branch `{name}` changed {N} source files. Running review."

## Step 2 — Fetch the diff

```bash
git diff origin/main...HEAD -- WebApp '*.ipynb' justfile setup.ps1
```

For context-dependent checks (route/template variable sync, API URL building), read the
**full file**, not just the hunk. For notebooks, read the JSON `source` arrays — a raw
`.ipynb` diff is noisy; focus on code-cell content and whether `outputs` were committed.

## Step 3 — Run the checklist

Verify each finding against the actual code before reporting it.

| #   | Check                        | Label      | What to look for                                                                                                                                                 |
| --- | ---------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1   | **Compiles clean**           | issue      | `uv run --no-project python -m py_compile WebApp/script.py` exits 0. Run it — a PR with a SyntaxError is dead on arrival.                                        |
| 2   | **Boots end-to-end**         | issue      | `just serve` boots and GET `/` returns 200 (see Step 4). A traceback on boot is blocking.                                                                        |
| 3   | **Route/template sync**      | issue      | Every variable a template uses (`joke`, `name`, `currencies`, ...) is passed by its route, and form field names (`amount`, `search_type`, ...) match `request.form` reads. |
| 4   | **API error paths**          | issue      | External calls (`requests.get`) keep their status-code check + `try/except`; error dicts still funnel to `error.html` instead of crashing the route.             |
| 5   | **Input robustness**         | suggestion | `int(request.form['amount'])`-style raw casts — does bad input produce the error page or an unhandled `ValueError`/`KeyError`? Flag regressions, don't demand rewrites. |
| 6   | **URL building**             | issue      | Query-string assembly in `specificJoke`/`searchBy*` stays well-formed (`?` vs `&`, lowercase paths); a referenced-but-undefined attribute (e.g. `self.joke_type`) in a NEW path. |
| 7   | **Notebook hygiene**         | issue      | Committed notebooks keep outputs stripped of secrets/PII; no `just execute` output copies (from `%TEMP%`) or `.ipynb_checkpoints/` sneak into the diff.          |
| 8   | **No debug leftovers**       | issue      | `print("here")`-style debugging, `breakpoint()`, commented-out dead blocks, `TODO` without follow-up — in NEW code.                                              |
| 9   | **Naming & structure**       | suggestion | New code follows Python conventions (snake_case, logic on the class that owns the data) even though the preserved code predates them.                            |
| 10  | **Docs sync**                | suggestion | Behavior changes reflected in `README.md` / `.docs/` (especially routes, commands, and troubleshooting).                                                          |

## Step 4 — Syntax & boot gate

If `WebApp/script.py`, any template, `justfile`, or `setup.ps1` changed:

```bash
uv run --no-project python -m py_compile WebApp/script.py
just serve          # then: curl.exe -s -o NUL -w "%{http_code}" http://127.0.0.1:8124/
just stop
```

`py_compile` must exit 0 and GET `/` must return 200. Paste the http code (and the first
traceback line on failure) as evidence. A failure is an **issue** (blocking). If only
notebooks changed, `just execute '<nb>'` is the equivalent gate — but a failure that matches
a documented known issue (input() menu, missing CSV, deprecated API) is NOT a finding.

## Step 5 — Finding labels & caps

- **issue** (blocking) — fix before opening the PR.
- **suggestion** (non-blocking) — recommended.
- **nitpick** (non-blocking) — minor/optional.

Every finding must carry: the label, the `file:line`, and **WHY** it matters (not just what).
Issues: uncapped. Suggestions + nitpicks: cap at 15 total; note "{X} more non-blocking
findings omitted" if over.

## Step 6 — Present

```
## Pre-PR Review: {branch}
Branch: {branch} -> main   |   Files: {N}
Syntax/boot gate: {pass/fail — exit code + http code}

### Issues (fix before PR)
1. [path:line] Finding — why it matters

### Suggestions
2. [path:line] Finding

### Nitpicks
3. [path:line] Finding

---
{Total} findings: {issues} issues, {suggestions} suggestions, {nitpicks} nitpicks
```

Zero findings → "No issues found — branch looks clean. Ready to open the PR."

## Step 7 — Save the report

Path: `.claude/workspace/reports/pr/{branch}-{YYYY-MM-DD}.md` (replace `/` in the branch name
with `-`; overwrite on a same-day re-run). Frontmatter then the same body as the terminal
output:

```yaml
---
branch: { branch }
base: main
date: { YYYY-MM-DD }
files_changed: { N }
issues: { count }
suggestions: { count }
nitpicks: { count }
---
```

Confirm: "Report saved to `{path}`".

## Tone

Self-improvement, not a verdict from a lead. "Consider extracting…", not "You must fix…".
Never directive, never judgmental.
