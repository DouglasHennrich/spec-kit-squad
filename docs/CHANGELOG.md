# Changelog

All notable changes to the Squad Bridge extension will be documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1] - 2026-04-29

### Added

- `speckit.squad.init` command — bootstrap a Squad team from the current spec
- `speckit.squad.generate` command — re-generate agent definitions as the spec evolves
- `speckit.squad.route` command — route open Speckit tasks to Squad agents
- `speckit.squad.status` command — unified view of spec, tasks, and squad alignment
- `after_specify` hook — optionally regenerate agents when the spec changes
- `after_tasks` hook — optionally route new tasks to agents after task generation
- `squad-config.template.yml` — configurable model tiers, routing strategy, and squad root
