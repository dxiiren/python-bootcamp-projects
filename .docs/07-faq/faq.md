# FAQ

> **TL;DR** Short answers to the questions the rest of the docs raise: why no
> requirements.txt, why one port, why the notebooks don't run headless, and what is
> deliberately left broken.

## Why is there no `requirements.txt` or `pyproject.toml`?

The repo is a preserved 2023 bootcamp snapshot that never had one. Rather than
retrofitting packaging, the `justfile` injects each entry point's dependencies at run time
(`uv run --with flask,requests ...`). uv caches them, so only the first run pays the
download. If you add an import, add the package to the matching `--with` list.

## Why do `just lab` and `just serve` share one port?

Every repo in this workspace gets exactly one assigned port (this one: **8124**) so
projects never collide. Since you develop either the notebooks or the web app at a given
moment, the two entry points share it — run one at a time.

## Why can't I `just execute` any of the committed notebooks?

Each has a real blocker: an `input()` menu (Joke), a hardcoded uncommitted CSV plus a
markdown-in-code-cell `SyntaxError` (Data Analyst), and a retired upstream API (Country).
Full detail in
[../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md). Use
`just lab` and run cells interactively.

## Is the `/country` feature supposed to work?

Yes — it was migrated to REST Countries **v5** after the keyless v1–v4 endpoints were
retired upstream. With no configuration it authenticates using the public demo key, so
every search returns the API's fixed sample country (Canada); export a free personal key
as `RESTCOUNTRIES_API_KEY` for real lookups. The Country **notebook** still carries the
old v3.1 client and remains broken by design (notebooks are preserved as submitted).

## Why does `just execute` write to `%TEMP%`?

`nbconvert --execute` produces an executed copy of the notebook (outputs baked in).
Writing it to `%TEMP%` keeps executed outputs out of the repo — committed notebooks should
keep their sources clean, and executed copies must never be committed.

## Can I fix the bootcamp code's style (camelCase methods, tutorial comments)?

Only if a change explicitly targets it. The repo's value is as a preserved snapshot of
bootcamp work; drive-by modernisation destroys that. Bug fixes with minimal diffs are
fine.

## Where do Claude Code sessions get their rules?

`CLAUDE.md` (repo root) is the contract; `.claude/skills/` holds the playbooks
(`/commit`, `/create-pr`, `/lint-check`, ...); `.claude/memory/MEMORY.md` is the durable
fact index. MCP servers wire through `.mcp.json.stub` → git-ignored `.mcp.json`.

## Related docs

| Doc | Why |
| --- | --- |
| [../01-overview/project-overview.md](../01-overview/project-overview.md) | What the projects are |
| [../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md) | The failure details behind these answers |
