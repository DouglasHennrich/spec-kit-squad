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

```mermaid
flowchart LR
    subgraph sk["Spec Kit artifacts"]
        S1["specs/&lt;id&gt;/spec.md"]
        S2["specs/&lt;id&gt;/tasks.md"]
    end
    subgraph sq["Squad artifacts"]
        D1[".squad/agents/{name}/charter.md"]
        D2[".squad/routing.md"]
        D3[".squad/team.md"]
        D4["squad.config.ts"]
    end
    S1 --> D1
    S1 --> D3
    S1 --> D4
    S2 --> D2
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
├── .github/
│   ├── scripts/
│   │   └── build-catalog-submission.py  # Jinja2 renderer: extension.yml → issue body
│   ├── templates/
│   │   └── catalog-submission.md.j2     # Jinja2 template for spec-kit catalog issue
│   └── workflows/
│       ├── release.yml        # Auto-bump semver on changes to commands/ or extension.yml
│       ├── lint.yml           # Lint YAML and Markdown on non-main pushes + PRs to main
│       ├── test.yml           # Run extension smoke tests on non-main pushes + PRs to main
│       └── catalog-submit.yml # File catalog submission issue on github/spec-kit on release
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

```mermaid
flowchart TD
    A["Push to main"] --> B["commit-analyzer\ndetermine version bump"]
    B --> C["release-notes-generator"]
    C --> D["changelog\nwrite docs/CHANGELOG.md"]
    D --> E["exec\nupdate version in extension.yml"]
    E --> F["git\ncommit changelog + extension.yml"]
    F --> G["github\ncreate GitHub Release"]
    G --> H["catalog-submit.yml\nfile issue on github/spec-kit"]
```

1. **`commit-analyzer`** — determines version bump from conventional commits
2. **`release-notes-generator`** — generates release notes
3. **`changelog`** — writes/updates `docs/CHANGELOG.md`
4. **`exec`** — updates `version:` in `extension.yml`
5. **`git`** — commits `docs/CHANGELOG.md` + `extension.yml` back with `[skip ci]`
6. **`github`** — creates the GitHub Release

Config: `.releaserc.json`

> **Requires** a `GH_TOKEN` repository secret (fine-grained Personal Access Token
> with contents/metadata read and write access to this repo) — `GITHUB_TOKEN`
> cannot push back to the branch.

### `lint.yml` — YAML + Markdown Linting

Triggers on push to non-main branches and on pull requests targeting `main`.
Lints all `.yml` files with `yamllint` and all `.md` files with
`markdownlint-cli2`. Configuration:

- `.yamllint.yml` — relaxed line length, truthy disabled
- `.markdownlint.json` — MD013 (line length) and MD033 (inline HTML) disabled

### `test.yml` — Extension Smoke Tests

Triggers on push to non-main branches and on pull requests targeting `main`.
Validates that all command files referenced in `extension.yml` exist and that
`extension.yml` parses as valid YAML.

### `catalog-submit.yml` — Spec Kit Catalog Submission

Triggers on every release publish and on `workflow_dispatch` (with an optional
`tag` input for resubmission). On each run it:

```mermaid
flowchart TD
    A["Release published\nor workflow_dispatch"] --> B["Render catalog-submission.md.j2\nbuild-catalog-submission.py"]
    B --> C["Close any open stale\ncatalog submission issues"]
    C --> D["gh issue create\n--repo github/spec-kit"]
```

1. Renders `.github/templates/catalog-submission.md.j2` via
   `.github/scripts/build-catalog-submission.py` — all values sourced from
   `extension.yml`, nothing hardcoded
2. Closes any previously open catalog submission issues (to avoid stale entries)
3. Opens a new issue on `github/spec-kit` with the rendered body

> **Requires** a `PUBLIC_REPO_TOKEN` repository secret — a classic Personal
> Access Token with `public_repo` scope. Fine-grained PATs cannot create issues
> on third-party public repositories.
