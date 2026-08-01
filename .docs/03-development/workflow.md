# Development workflow

> **TL;DR** Branch off `main`, edit, verify with the same commands every time
> (`py_compile` for the app, `just serve` + a browser/curl check, `just lab` for
> notebooks), commit with Conventional Commits via `/commit`, PR via `/create-pr`.
> Everything day-2 is a `just` recipe — run `just` to list them.

## The loop

1. **Branch** — `git checkout -b feat/...` (or `fix/`, `docs/`). Never work directly on
   `main` for anything you intend to PR.
2. **Edit** — the app lives in `WebApp/script.py` + `WebApp/templates/`; notebooks are
   edited in Jupyter Lab (`just lab`).
3. **Verify** — pick the gate that matches what you touched:

   | You touched | Gate |
   | --- | --- |
   | `WebApp/script.py` / templates | `uv run --no-project python -m py_compile WebApp/script.py` exits 0, then `just serve` and check the touched route on `http://127.0.0.1:8124` |
   | A notebook | Re-run its cells top-to-bottom in `just lab`; `just execute '<nb>'` only works for notebooks free of `input()`/missing-data/dead-API blockers (currently: none of the committed three — see troubleshooting) |
   | `justfile` / `setup.ps1` | Run the recipe / re-run `pwsh ./setup.ps1` (must stay idempotent, all `[OK]`) |

4. **Stop servers** — `just stop` kills only THIS repo's `python.exe` processes (matched by
   the repo path on the command line). `just lab` and `just serve` share port 8124.
5. **Commit** — follow the [`/commit` skill](../../.claude/skills/commit/SKILL.md):
   Conventional Commits (`feat(webapp): ...`, `docs: ...`), no attribution footers.
6. **PR** — `/create-pr` pushes the branch and opens a GitHub PR into `main` with a
   Summary/Changes/Testing body. Optionally run `/pre-pr-review` first.

## Rules of the house

- **Preserved code**: don't restyle the bootcamp code (camelCase methods, tutorial
  comments) unless the change is the point of the branch.
- **Dependencies**: there is no requirements.txt on purpose. A new import goes into the
  matching `--with` list in the `justfile`, same commit.
- **Notebook hygiene**: `just execute` writes executed copies to `%TEMP%` — never commit
  them; `.ipynb_checkpoints/` and `__pycache__/` are git-ignored.
- **Port**: everything serves on 8124 only. Don't hardcode another port.
- **Quality suite**: `/lint-check` runs the honest layers this repo has (py_compile,
  serve smoke, placeholder + leftover greps). There is no linter/formatter/test runner to
  invoke.

## Working with Claude Code

`CLAUDE.md` is the agent contract. Skills live in `.claude/skills/` (see
[the catalog](../../.claude/skills/README.md)); MCP servers are wired via
`.mcp.json.stub` → git-ignored `.mcp.json` (seeded by `setup.ps1`). `just claudex`
launches Claude with permissions pre-granted.

## Related docs

| Doc | Why |
| --- | --- |
| [../05-reference/commands.md](../05-reference/commands.md) | Every recipe, one table |
| [../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md) | When a gate fails |
| [../01-overview/architecture.md](../01-overview/architecture.md) | Where each piece lives |
