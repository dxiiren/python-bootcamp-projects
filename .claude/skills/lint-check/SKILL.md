---
name: lint-check
description: Use when the developer says 'lint check', 'run lint', 'check lint', 'run the quality suite', or 'lint everything' — runs the quality checks available to this repo (pytest suite via just test, Python syntax gate via py_compile, Flask boot smoke on port 8124, placeholder + debug-leftover greps) and reports pass/fail per layer. No flake8/ruff here — the repo has no lint toolchain on purpose.
model: sonnet
---

# lint-check — Quality suite (pytest · py_compile · Flask boot smoke · greps)

This repo has **no linter and no formatter** — it is a preserved bootcamp project
with no dependency manifest (every run injects deps via `uv run --with ...`). The honest
quality layers are the offline pytest suite (`just test`), the Python compiler's syntax
check, a boot-to-200 smoke of the Flask app, and two greps. Run each independently so one
failure doesn't hide the others.

## Trigger

When the developer says any of: "lint check", "run lint", "check lint",
"run the quality suite", "lint everything".

---

## What to Do

### 0 — pytest suite (`just test`)

```powershell
just test
```

Pass = exit 0, `10 passed`. Fully offline (external HTTP is monkeypatched) — no server,
no port, safe to run any time. Note: `test_country_search_fails_against_deprecated_api`
asserts the CURRENT broken `/country` behavior (error page) on purpose — if it fails
after a `/country` migration, the test needs replacing, not the migration reverting.

### 1 — Python syntax gate (`py_compile`)

```powershell
uv run --no-project python -m py_compile 'WebApp/script.py'
```

Pass = exit 0, no output. A `SyntaxError` is a blocking finding — report file:line.
(The notebooks are NOT part of this gate — see Notes.)

### 2 — Flask boot smoke

```powershell
just serve      # in one terminal (foreground)
curl.exe -s -o NUL -w "%{http_code}" http://127.0.0.1:8124/
just stop
```

Pass = GET `/` returns **200** with the home page HTML. Poll with `curl.exe` (never the
PowerShell `curl` alias) every 2 s, max 60 s for the first boot (uv may download Flask).
`/random_joke` should also return 200 when JokeAPI is reachable. Do NOT treat a `/country`
error page as a failure — REST Countries v3.1 is deprecated upstream (known issue, see
`.docs/06-troubleshooting/common-issues.md`).

### 3 — Leftover template placeholders

The onboarding kit stamps files from templates whose fill-in tokens are delimited by
doubled at-signs. The `@[@]` character class below matches that delimiter in files
without this skill file matching its own check:

```bash
grep -rnI "@[@]" --exclude-dir=.git .
```

Pass = **zero hits** (grep exits 1). Any hit is an unfilled kit placeholder token —
fix it at the source. (`-I` skips binaries.)

### 4 — Debug / draft leftovers

```bash
grep -n "TODO\|FIXME\|XXX\|breakpoint()\|pdb.set_trace" WebApp/script.py
```

Pass = zero hits (grep exits 1). A hit is not automatically fatal — judge it: a
deliberate TODO with a follow-up is fine; a stray `breakpoint()` is not. Do not flag the
app's existing tutorial-style `#` comments — they are part of the preserved bootcamp code.

---

## Reporting back

Report a per-layer table, then an overall verdict:

```
LAYER         TOOL                              STATUS
tests         just test (pytest, offline)       PASS | FAIL (failing test names)
syntax        py_compile WebApp/script.py       PASS | FAIL (file:line)
smoke         just serve + GET / (:8124)        PASS | FAIL (http code / first traceback line)
placeholders  grep for doubled at-signs         PASS | FAIL (N hits)
leftovers     grep TODO/FIXME/breakpoint        PASS | FAIL (N hits)
OVERALL: PASS | FAIL
```

---

## Notes

- Run from the **repo root** — recipe paths (`WebApp/script.py`) are root-relative.
- Notebooks are excluded from the suite: all three committed notebooks are
  interactive-/data-bound and fail `just execute` for real, documented reasons
  (`input()` menu, missing Kaggle CSV, deprecated REST Countries API). Checking them
  headlessly would only re-report known issues.
- There is no auto-fix layer here — every fix is a source edit; re-run the layer after.
- Don't bolt on ruff/flake8 uninvited — this is a preserved bootcamp project;
  propose new tooling to the developer instead of adding it inside a lint run.
