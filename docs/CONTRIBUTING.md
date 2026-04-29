# Contributing to spec-kit-squad

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/spec-kit-squad.git`
3. Create a feature branch: `git checkout -b feat/my-change`

## Development

Install spec-kit and test the extension locally:

```bash
# In a spec-kit project
specify extension add squad --dev /path/to/spec-kit-squad

# Verify it's installed
specify extension list

# Test a command (in Claude Code)
# /speckit.squad.status
```

## Commit Convention

This repository uses [Conventional Commits](https://www.conventionalcommits.org/)
for automated versioning. The CI action reads commit messages to determine the
next semantic version:

| Prefix | Version bump | Example |
|--------|-------------|---------|
| `feat:` | minor | `feat: add domain filtering to generate` |
| `fix:` | patch | `fix: handle missing tasks.md gracefully` |
| `docs:` | patch | `docs: improve route command examples` |
| `BREAKING CHANGE:` (footer) | major | Any commit with this in the footer |

## File Structure

```
spec-kit-squad/
├── extension.yml                  # Extension manifest — source of truth
├── squad-config.template.yml      # Config template installed with the extension
├── commands/
│   ├── init.md                    # /speckit.squad.init
│   ├── generate.md                # /speckit.squad.generate
│   ├── route.md                   # /speckit.squad.route
│   └── status.md                  # /speckit.squad.status
├── docs/                          # Developer docs (not installed with extension)
│   ├── README.md                  # Developer architecture reference
│   ├── CONTRIBUTING.md            # ← this file
│   └── CHANGELOG.md               # Version history
├── .github/workflows/             # CI (not installed with extension)
├── README.md                      # User-facing docs
└── LICENSE
```

## Submitting Changes

1. Ensure `extension.yml` is valid YAML:
   ```bash
   yq eval '.' extension.yml
   ```
2. Verify all command files listed in `extension.yml` exist:
   ```bash
   grep 'file:' extension.yml | awk '{print $2}' | xargs -I{} test -f {} && echo "OK"
   ```
3. Commit with a conventional commit message
4. Open a Pull Request against `main`

## Release Process

Releases are automated. When a PR is merged to `main` that changes
`commands/**`, `extension.yml`, or `squad-config.template.yml`, the CI
action automatically:

1. Determines the next version from commit messages
2. Creates a git tag (e.g., `v0.1.0`)
3. Updates the version in `extension.yml`
4. Creates a GitHub Release with auto-generated notes
