# Python Bootcamp Projects — documentation

Developer documentation for `python-bootcamp-projects`: a preserved 2023 bootcamp repo
holding a Flask joke/country web app and Jupyter data-analysis notebooks, run through
`uv` + `just`.

> **New here? Start with [`tldr.md`](tldr.md)** — every doc below summarised in 30 seconds
> each.

## Who is this for?

| Reader | Start here |
| --- | --- |
| New developer setting up the repo | [02-setup/getting-started.md](02-setup/getting-started.md) |
| Someone asking "what even is this?" | [01-overview/project-overview.md](01-overview/project-overview.md) |
| Day-2 contributor | [03-development/workflow.md](03-development/workflow.md) |
| "Why doesn't X work?" | [06-troubleshooting/common-issues.md](06-troubleshooting/common-issues.md) |
| Command lookup | [05-reference/commands.md](05-reference/commands.md) |

## Recommended reading order

1. [tldr.md](tldr.md)
2. [01-overview/project-overview.md](01-overview/project-overview.md)
3. [02-setup/getting-started.md](02-setup/getting-started.md)
4. [03-development/workflow.md](03-development/workflow.md)
5. [05-reference/commands.md](05-reference/commands.md)
6. [06-troubleshooting/common-issues.md](06-troubleshooting/common-issues.md) (when needed)

## 01-overview

| Document | What it covers |
| --- | --- |
| [project-overview.md](01-overview/project-overview.md) | The two bootcamp projects, routes, notebooks, known upstream-API issue, original-README history |
| [architecture.md](01-overview/architecture.md) | How the Flask app's classes/routes/templates fit; the uv per-run dependency model; the port plan |

## 02-setup

| Document | What it covers |
| --- | --- |
| [getting-started.md](02-setup/getting-started.md) | Fresh-machine setup via `setup.ps1`, first boot of `just lab` / `just serve`, what "working" looks like |

## 03-development

| Document | What it covers |
| --- | --- |
| [workflow.md](03-development/workflow.md) | Branch → edit → verify → commit → PR loop, per-change verification gates, house rules |

## 04-deployment

| Document | What it covers |
| --- | --- |
| [deployment.md](04-deployment/deployment.md) | Honest status: no CI/CD, no hosting — local-only, and what deploying would actually require |

## 05-reference

| Document | What it covers |
| --- | --- |
| [commands.md](05-reference/commands.md) | Every `just` recipe + occasional commands + env knobs |
| [project-layout.md](05-reference/project-layout.md) | Annotated tree, deliberate absences, generated/ignored paths |

## 06-troubleshooting

| Document | What it covers |
| --- | --- |
| [common-issues.md](06-troubleshooting/common-issues.md) | Real symptoms hit during verification: notebook execute failures, the v5 country API + demo key, slow first runs, port/stop quirks |

## 07-faq

| Document | What it covers |
| --- | --- |
| [faq.md](07-faq/faq.md) | Design-decision questions: no manifest, shared port, preserved style, %TEMP% outputs |
