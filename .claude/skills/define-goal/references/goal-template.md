# Goal file template - the exact shape of every `{topic}-goal.md`

Every file `define-goal` writes uses this structure, in this order. Consistency is the point: a
reader (human or the `/goal` evaluator) always finds the STOP CONDITION at the top and the work-list
in the middle. Fill **every** section; if one truly doesn't apply, keep the heading and write one
line saying why (e.g. "No environment bootstrap - pure-analysis goal") rather than deleting it.

## Contents

- [The template](#the-template)
- [Field guidance](#field-guidance)
- [Worked example (compact)](#worked-example-compact)
- [The handoff block to print after writing](#the-handoff-block-to-print-after-writing)

## The template

Copy this verbatim, then fill each `{placeholder}` and resolve each `<!-- note -->`. The template is
markdown, so it drops straight into a `.md` file.

````markdown
# GOAL - {Title Case mission name}

> Read this whole file before starting. Execute the Work List top to bottom. After EVERY item:
> set its status + append one Run Log line. This file - not your memory - is the source of truth.

## STOP CONDITION - read before ending ANY turn (the /goal evaluator checks THIS file)

**This goal is NOT complete - and you MUST NOT stop, summarize, or hand back - until EVERY row in
the Work List has a TERMINAL status.**

- **Terminal (a row may end here):** `DONE` - `GAP` (not implemented / out of scope - cite the code
  fact) - `BLOCKED` (proven impossible in code or a hard infra failure you cannot fix - cite
  `file:line` or the exact error).
- **Non-terminal (work remains - keep going):** `TODO` - `IN-PROGRESS` - `PARTIAL`. The words
  **"deferred" / "next session" / "focused session" / "later" are BANNED as a status.** Large or
  messy is not a reason to defer - slice it, timebox it, annotate honestly, mark it `DONE`/`PARTIAL`
  with a concrete note, and move to the next row.
- **Do NOT write a completion summary while any row is non-terminal.** A "Summary"/"final status"
  written early makes this file read as _met_ and lets you quit with work undone. Write the closing
  summary ONLY when the Work List has zero `TODO`/`IN-PROGRESS`/`PARTIAL` rows.
- **On every Stop attempt:** re-read this section, scan the Work List, pick the topmost non-terminal
  row, and execute it. Repeat until none remain.

## Mission

{1-2 sentences: the single objective and what "success" concretely delivers.}

## Locked decisions (do not re-litigate)

- {Decision already made - the agent must NOT reopen it. One bullet each. Delete the list only if
  there are genuinely none.}

## Environment bootstrap

<!-- Idempotent; re-verify every run. Delete/deactivate this section only for a pure-analysis goal. -->

- {Step to bring the world up + how to check it's up + what to do if it's down. e.g.
  `pwsh ./setup.ps1` if `uv` is missing; sanity gate:
  `uv run --no-project python -m py_compile WebApp/script.py` exits 0, and `just serve` answers
  GET `http://127.0.0.1:8124/` with 200 (then `just stop`). Reference the exact command.}

## Hard prohibitions / guardrails

- {git commit? push? staging? - state explicitly, e.g. "NEVER git commit/push/stage; all work stays
  in the working tree."}
- {External posts - GitHub PR/issue / email / any service: allowed or forbidden?}
- {Destructive ops, files/dirs that are off-limits, "touch only X".}
- {Any project house-rule that applies, e.g. "keep every template's variables in sync with what
  its route passes" or "never commit executed-notebook output copies".}

## What counts as a REAL blocker

- **Real (may mark `BLOCKED`):** {code facts - a missing class/method at `file:line`, an input the
  app cannot receive, an upstream API retired (like REST Countries v3.1 here); or a hard infra
  failure you tried once to fix and couldn't.}
- **NOT a blocker (keep working):** "it's late", "it's complex", "needs a focused session", missing
  fixture data (-> create it, e.g. a small stand-in CSV), a slow first `uv run` (-> it's a one-time
  package download; wait, continue).

## Definition of Done

Per item - an item is `DONE` only when:

- [ ] {check 1}
- [ ] {check 2}
- [ ] {evidence recorded - the concrete proof line, e.g. pasted `just run` exit code + output
      excerpt, a report path}

Global goals:

- **G1** {checkable outcome}
- **G2** {checkable outcome}

<!-- add G3.. as needed; each must be verifiable, not aspirational -->

## Work List

<!-- CHOOSE ONE of the two forms below and delete the other. -->

<!-- FORM 1 - KNOWN, enumerable list: one row per unit of work. -->

| #   | Item   | Status |
| --- | ------ | ------ |
| 1   | {item} | `TODO` |
| 2   | {item} | `TODO` |
| ... | ...    | `TODO` |

<!-- FORM 2 - UNKNOWN size: a discovery sweep enumerates the list first, then a Task Template. -->

### Goal 0 - Discovery sweep - `TODO`

Enumerate every unit of work into the table below BEFORE executing any of them. {How to discover:
grep/glob over the sources.} Append one row per item found; set each to `TODO`.

| #                       | Item | Status |
| ----------------------- | ---- | ------ |
| _(populated by Goal 0)_ |      |        |

### Task Template (copy for each row when you start it)

```text
### {id} - {item name} - `TODO`
- [ ] {DoD check 1}
- [ ] {DoD check 2}
- [ ] Evidence: {proof}
```

## Resume protocol

- Statuses in this file are the single source of truth - not conversation memory.
- On every (re)start, crash, or context compaction: re-read STOP CONDITION -> Work List -> continue
  from the first non-terminal row.
- Set a row to `IN-PROGRESS` the moment you start it, so a resumed run knows where you died.
- After EVERY item (not in batches): set its status + append one Run Log line.

## Run Log (append-only - one timestamped line per item)

<!-- format: "- {YYYY-MM-DD HH:MM} | {item id} | {what happened + evidence}" -->

- {first line goes here}
````

## Field guidance

- **STOP CONDITION** - keep it verbatim; only adjust the terminal-status _names_ if this goal needs
  a different vocabulary. It must stay checkable by re-reading the file.
- **Mission** - success must be stateable as something observable. If the answer was fuzzy in
  interrogation, it isn't ready to write.
- **Environment bootstrap** - only for goals that touch a running system. For an unattended run,
  make each step idempotent and give the up/down check + the recovery action inline.
- **Work List** - Form 1 when the developer handed you a finite list; Form 2 when the count is
  unknown or must be derived. Never leave the count implicit - Goal 0 makes it explicit before work
  starts, which is what makes "EVERY row terminal" a real bar.
- **Definition of Done** - the per-item checklist is what stops "looks done" from passing. Always
  include an **evidence** line (a pasted result / a report path), never just a checkbox.
- **Guardrails** - for an unattended run, default to the safe side: no commit/push, no external
  posts, unless the developer explicitly authorized them in interrogation.

## Worked example (compact)

A finite, attended-ish goal - harden the three form-input weak spots in the Flask app:

```markdown
# GOAL - Harden the three known form-input weak spots in WebApp/script.py

## STOP CONDITION - read before ending ANY turn (the /goal evaluator checks THIS file)

**NOT complete until EVERY row in the Work List has a TERMINAL status (`DONE`/`GAP`/`BLOCKED`).**
... (standard block) ...

## Mission

Make the `/specific_joke` and `/country` form handlers survive malformed input with the app's
`error.html` page instead of a raw 500. Success = GET `/` and `/random_joke` still return 200,
and each malformed-POST case renders the error page instead of crashing.

## Locked decisions (do not re-litigate)

- Keep the existing template wording and route URLs byte-for-byte for well-formed input.
- No new dependencies - Flask + requests via `uv run --with` stays; no requirements.txt.

## Environment bootstrap

- Sanity gate before starting: `uv run --no-project python -m py_compile WebApp/script.py`
  exits 0, and `just serve` answers GET `http://127.0.0.1:8124/` with 200 (then `just stop`).

## Hard prohibitions / guardrails

- NEVER git commit/push/stage - leave changes in the working tree for review.
- No GitHub PR/issue posts.
- Touch only `WebApp/script.py` (+ a template only if an error message must render).

## What counts as a REAL blocker

- Real: a case that cannot be guarded without restructuring the route/API-class contract - cite
  the `file:line` and describe the restructure needed.
- Not a blocker: "the form handling is messy" - slice the cases and harden them one at a time.

## Definition of Done

Per item - `DONE` only when:

- [ ] The malformed case renders `error.html` (shown by a `curl.exe -X POST` transcript excerpt)
- [ ] GET `/` and `/random_joke` still return 200 with unchanged happy-path behavior
- [ ] Evidence pasted into the Run Log (http codes + transcript lines)

Global: **G1** all three weak spots hardened. **G2** `py_compile` + the `just serve` smoke green
at the end.

## Work List

| #   | Item                                                          | Status |
| --- | ------------------------------------------------------------- | ------ |
| 1   | `/specific_joke` amount field (`int()` on non-numeric)        | `TODO` |
| 2   | Missing form keys (`request.form['...']` KeyError paths)      | `TODO` |
| 3   | `/country` error-dict path (deprecated API / empty responses) | `TODO` |

## Resume protocol

... (standard block) ...

## Run Log (append-only - one timestamped line per item)

- {first line goes here}
```

## The handoff block to print after writing

```text
Wrote .claude/checklist/{topic}/{topic}-goal.md
Run it in a fresh instance (Fable):
  /goal Work through @.claude/checklist/{topic}/{topic}-goal.md until the STOP CONDITION at the
  top is met. Follow every rule in it; update statuses + Run Log after each item.
```
