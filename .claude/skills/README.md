# Skills Catalog — `python-bootcamp-projects`

Project development skills for this preserved Python bootcamp repo — a Flask web app
(`WebApp/script.py`) plus Jupyter notebooks, run through `uv` + `just` (GitHub, no CI/CD).
Each skill lives in its own directory with a `SKILL.md`. **Follow the relevant skill before
writing code.** Run `/audit-skills` to verify every skill here is registered and that
`CLAUDE.md` references only existing skills.

Model tiers: `sonnet` (floor) · `opus` (deep reasoning / generation).

## Git

| Skill                           | What it does                                                                                                                                                                              | Model  |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ------ |
| [commit](commit/SKILL.md)       | Conventional-Commits stage + message flow (stale-lock preflight, `git add -A` fast path, scoped stage-by-name). Never auto-commits, never pipes `git commit` in an `&&` chain, no attribution footer. | sonnet |
| [create-pr](create-pr/SKILL.md) | Push the current branch and open a **GitHub** PR into `main` via `gh` / GitHub MCP, with a clean Summary/Changes/Testing body and no attribution footer.                                  | opus   |

## Quality & Review

| Skill                                   | What it does                                                                                                                | Model  |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | ------ |
| [pre-pr-review](pre-pr-review/SKILL.md) | Self-review the branch diff against a Flask + notebooks checklist (routes/templates in sync, API error paths, notebook hygiene) + the syntax/boot gate; report to `workspace/reports/pr/`. | opus   |
| [lint-check](lint-check/SKILL.md)       | Run the honest quality layers this repo has: `py_compile` syntax gate, Flask boot smoke (`just serve` + GET `/`), placeholder/debug-leftover greps.                          | sonnet |

## MCP tooling

| Skill                                 | What it does                                                                                                  | Model  |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------- | ------ |
| [setup-mcp](setup-mcp/SKILL.md)       | Registry-driven MCP setup / onboarding (reads `setup-mcp/registry.json`; wires stub + secret + enable tiers). | opus   |
| [test-all-mcp](test-all-mcp/SKILL.md) | Live per-server smoke-test sweep → PASS/FAIL/SKIP table (prompts in `test-all-mcp/checks/`).                  | sonnet |

## Maintenance

| Skill                                 | What it does                                                                                                     | Model  |
| ------------------------------------- | ----------------------------------------------------------------------------------------------------------------- | ------ |
| [audit-skills](audit-skills/SKILL.md) | Verify every skill has a valid, registered `SKILL.md` (no BOM, valid model, no hardcoded secret) via `audit.py`. | sonnet |

## Planning & handoff

| Skill                                       | What it does                                                                                                        | Model  |
| ------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ------ |
| [define-goal](define-goal/SKILL.md)         | Interrogate until a goal is unambiguous, then write a stop-proof `{topic}-goal.md` for the built-in `/goal` runner. | opus   |
| [claude-transfer](claude-transfer/SKILL.md) | Pointer-based session-handoff brief to `workspace/reports/transfers/claude/`.                                       | sonnet |
| [llm-transfer](llm-transfer/SKILL.md)       | Self-contained master prompt for an external LLM → `workspace/reports/transfers/{tool}/`.                           | sonnet |

## Stack add-ons not present (and why)

| Skill                      | Skipped because                                                                 |
| -------------------------- | -------------------------------------------------------------------------------- |
| `fix-typecheck`            | No typecheck script or `tsconfig` — plain Python, no type-checking toolchain.    |
| `generate-playwright-tests`| No Playwright dependency or config in the repo.                                  |
| `fix-phpstan`              | No PHP / `composer.json` here.                                                   |
| `monitor-ci`               | No CI workflow files — the repo runs locally only.                               |
