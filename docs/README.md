# Squad Bridge — Developer Docs

> **Looking for the user guide?** See the [root README](../README.md) for
> installation, commands, and configuration.

## Contents

- [Contributing](CONTRIBUTING.md) — Development setup, commit conventions, PR process
- [Changelog](CHANGELOG.md) — Version history

---

## Architecture

The extension is a thin bridge between two tools:

- **[Spec Kit](https://github.com/github/spec-kit)** provides the specification
  workflow (`/speckit.specify`, `/speckit.tasks`, etc.) and owns `.specify/`
- **[Squad](https://bradygaster.github.io/squad/)** manages a team of AI agents
  with declared capabilities and owns `.squad/`

```text
Spec Kit artifacts          Squad artifacts
──────────────────          ───────────────
.specify/spec.md    ──────► .squad/agents/*.md
.specify/tasks.md   ──────► .squad/routing.md
                            squad.config.ts
```text

Each command file in `commands/` is a Markdown prompt executed by the Spec Kit
runtime inside Claude Code. The commands shell out to the `squad` CLI for
operations that require Squad's agent management.

## Repository Layout

```text
spec-kit-squad/
├── extension.yml              # Manifest: commands, hooks, config, dependencies
├── squad-config.template.yml  # Installed to .specify/extensions/squad/ on add
├── commands/
│   ├── init.md                # /speckit.squad.init — first-time bootstrap
│   ├── generate.md            # /speckit.squad.generate — resync agents to spec
│   ├── route.md               # /speckit.squad.route — assign tasks to agents
│   └── status.md              # /speckit.squad.status — health check
├── docs/                      # Developer docs (excluded from installs)
│   ├── README.md              # ← you are here
│   ├── CONTRIBUTING.md        # How to contribute
│   └── CHANGELOG.md           # Version history
├── .github/workflows/
│   ├── release.yml            # Auto-bump semver on changes to commands/ or extension.yml
│   └── lint.yml               # Lint YAML and Markdown on every push
├── README.md                  # User-facing docs (installed with extension)
└── LICENSE
```text

> `.extensionignore` excludes `docs/` and `.github/` so neither folder is
> installed when a user runs `specify extension add squad`.

## CI Workflows

### `release.yml` — Semantic Versioning

Triggers on push to `main` when `commands/**`, `extension.yml`, or
`squad-config.template.yml` change. Uses
[`mathieudutour/github-tag-action`](https://github.com/mathieudutour/github-tag-action)
to parse conventional commits and bump the version:

| Commit prefix | Version bump |
|---------------|-------------|
| `feat:` | minor |
| `fix:`, `docs:`, `chore:` | patch |
| `BREAKING CHANGE:` in footer | major |

The action updates `extension.yml` `version:` field, creates a git tag, and
publishes a GitHub Release.

### `lint.yml` — YAML + Markdown Linting

Triggers on every push and on pull requests to `main`. Lints all `.yml` files
with `yamllint` and all `.md` files with `markdownlint-cli2`. Configuration:

- `.yamllint.yml` — relaxed line length, truthy disabled
- `.markdownlint.json` — MD013 (line length) and MD033 (inline HTML) disabled
