# Changelog

## [2.1.0] - 2026-05-31

### Changed
- Squad definitions are now markdown-first and authoritative in `.squad/` artifacts (`agents/`, `team.md`, `routing.md`); a root `squad.config.ts` file is no longer required.

## [2.0.0] - 2026-05-29

### Added
- `/speckit.squad.api-contract` — detect API-impacting tasks and generate/update `API.md` contract with agent ownership
- `/speckit.squad.after-tasks` — orchestrator that runs `route` + `api-contract` in sequence; now used by the `after_tasks` hook
- `squad.config.ts` generation at project root via `defineSquad()` from `@bradygaster/squad-sdk`
- `speckit-implement-squad-route` skill auto-installed by `init` and `generate` into `.github/skills/`
- `grill-with-docs` skill bundled and installed by `generate`
- `list-hooks.sh` script installed and kept up-to-date by `init`/`generate`
- `.github/copilot-instructions.md` blocks managed by `init`/`generate` via HTML comment markers
- `ceremonies.md` Speckit Tasks Audit block appended by `init`/`generate`

### Changed
- `after_tasks` hook now runs `speckit.squad.after-tasks` (was `speckit.squad.route`)
- Both hooks (`after_specify`, `after_tasks`) are now non-optional — always prompt before executing
- Updated author to Douglas Hennrich; repository moved to `DouglasHennrich/spec-kit-squad`

### Fixed
- Task annotations in `tasks.md` now use `→AgentName` format (canonical per CONTEXT.md)

## [1.3.0] - 2026-01-01

Initial public release by jwill824.
