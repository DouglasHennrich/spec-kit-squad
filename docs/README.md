# Squad Bridge — Documentation

## Contents

- [User Guide](../README.md) — Installation, commands, and configuration
- [Contributing](CONTRIBUTING.md) — How to contribute to this extension
- [Changelog](../CHANGELOG.md) — Version history

## Architecture

The extension is a thin bridge between two tools:

- **[Spec Kit](https://github.com/github/spec-kit)** provides the specification
  workflow (`/speckit.specify`, `/speckit.tasks`, etc.)
- **[Squad](https://bradygaster.github.io/squad/)** manages a team of AI agents
  with declared capabilities

The extension reads Spec Kit artifacts (`.specify/spec.md`, `.specify/tasks.md`)
and writes Squad artifacts (`.squad/agents/`, `.squad/routing.md`,
`squad.config.ts`).

## Command Reference

| Command | Trigger | Output |
|---------|---------|--------|
| `speckit.squad.init` | Manual, once | `.squad/agents/`, `.squad/routing.md`, `squad.config.ts` |
| `speckit.squad.generate` | Manual or `after_specify` hook | Updated agent definitions |
| `speckit.squad.route` | Manual or `after_tasks` hook | Routing table, optional tasks.md annotations |
| `speckit.squad.status` | Manual | Coverage + utilization report |

## Configuration Reference

Config file: `.specify/extensions/squad/squad-config.yml`  
Template: `.specify/extensions/squad/squad-config.template.yml` (created on install)

```yaml
squad:
  agent_model: "claude-sonnet-4"        # Model for agent generation
  routing_strategy: "capability-match"  # or "round-robin"
  squad_root: ".squad"                  # Squad directory path
  auto_generate: false                  # Auto-run generate on after_specify
  model_tiers:
    complex: "claude-opus-4"
    standard: "claude-sonnet-4"
    simple: "claude-haiku-3.5"
  default_capability_level: "proficient"
```

## Versioning

This extension follows [Semantic Versioning](https://semver.org/):

- **MAJOR** — breaking changes to command behavior or config schema
- **MINOR** — new commands or hooks
- **PATCH** — bug fixes, documentation updates

Versions are auto-bumped by CI when `commands/**` or `extension.yml` change.
Use conventional commits:

- `feat:` → minor bump
- `fix:` → patch bump
- `BREAKING CHANGE:` in footer → major bump
