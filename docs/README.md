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

```
Spec Kit artifacts          Squad artifacts
──────────────────          ───────────────
specs/<id>/spec.md  ──────► .squad/agents/{name}/charter.md
specs/<id>/tasks.md ──────► .squad/routing.md
                            .squad/team.md
                            squad.config.ts
```

Each command file in `commands/` is a Markdown prompt executed by the Spec Kit
runtime inside Claude Code. The commands shell out to the `squad` CLI for
operations that require Squad's agent management.

## Repository Layout

```
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
```

> `.extensionignore` excludes `docs/` and `.github/` so neither folder is
> installed when a user runs `specify extension add squad`.

## CI Workflows

### `release.yml` — Semantic Release

Triggers on every push to `main` (and `workflow_dispatch`). Uses
[`semantic-release`](https://semantic-release.gitbook.io/) with the following
plugin pipeline:

1. **`commit-analyzer`** — determines version bump from conventional commits
2. **`release-notes-generator`** — generates release notes
3. **`changelog`** — writes/updates `docs/CHANGELOG.md`
4. **`exec`** — updates `version:` in `extension.yml`
5. **`git`** — commits `docs/CHANGELOG.md` + `extension.yml` back with `[skip ci]`
6. **`github`** — creates the GitHub Release

Config: `.releaserc.json`

> **Requires** a `GH_TOKEN` repository secret (Personal Access Token with
> `repo` scope) — `GITHUB_TOKEN` cannot push back to the branch.

### `lint.yml` — YAML + Markdown Linting

Triggers on every push and on pull requests to `main`. Lints all `.yml` files
with `yamllint` and all `.md` files with `markdownlint-cli2`. Configuration:

- `.yamllint.yml` — relaxed line length, truthy disabled
- `.markdownlint.json` — MD013 (line length) and MD033 (inline HTML) disabled
