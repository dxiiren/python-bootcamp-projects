# Deployment

> **TL;DR** There is no deployment. This repo runs locally only — no CI/CD, no hosting
> target, no build artifact. "Shipping" means pushing to `main` on GitHub.

## Current state

| Aspect | Status |
| --- | --- |
| CI/CD | None — no workflow files, no pipelines |
| Hosting | None — the Flask app runs on `http://127.0.0.1:8124` via `just serve` only |
| Build artifact | None — Python is run from source; notebooks are opened in place |
| Release process | Push to `main` on `github.com/dxiiren/python-bootcamp-projects` |

The Flask app as committed is not production-shaped anyway: it runs under the Flask dev
server and has almost no configuration layer (the one env knob is
`RESTCOUNTRIES_API_KEY` for the country feature).

## If you ever deploy it

Not planned, but the honest checklist would be: pin dependencies in a real manifest
(pyproject.toml), swap the dev server for a WSGI server, externalise the port/host
config, and provision a real REST Countries v5 API key (the committed default is the
public demo key, which only ever returns the API's sample country).

## Related docs

| Doc | Why |
| --- | --- |
| [../02-setup/getting-started.md](../02-setup/getting-started.md) | Running locally (the only "environment") |
| [../06-troubleshooting/common-issues.md](../06-troubleshooting/common-issues.md) | The deprecated-API detail |
