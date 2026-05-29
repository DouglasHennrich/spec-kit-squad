# Squad Bridge — Context Map

Glossary of resolved terms and domain decisions for this extension.

---

## Terms

### Skill (Squad Bridge)

A Copilot agent customization file (`SKILL.md`) that overrides the default
`speckit.implement` behavior. The Squad Bridge ships one skill:
`speckit-implement-squad-route`, which routes tasks to specialist agents in
parallel instead of executing them sequentially.

**Canonical location in the extension repo:** `skills/speckit-implement-squad-route/SKILL.md`
**Canonical location in the user's project:** `.github/skills/speckit-implement-squad-route/SKILL.md`
**Dev-time location (extension authors only):** `.github/skills/speckit-implement-squad-route/SKILL.md`

The skill is **static and generic** — it reads `→AgentName` annotations already
written into `tasks.md` by `/speckit.squad.route`. It does not embed a routing
table and does not need regeneration when agents change.

### Skill Installation

The act of copying the skill from the extension's installed path
(`.specify/extensions/squad/skills/speckit-implement-squad-route/SKILL.md`)
into the project's `.github/skills/` directory. Performed by both
`speckit.squad.init` and `speckit.squad.generate`.

**Idempotency rule:** install only if the target file does not already exist.
Never overwrite an existing skill in the user's project.

### →AgentName Annotation

A tag appended to each task line in `tasks.md` by `/speckit.squad.route`.
Format: `→AgentName` (e.g., `→Kaylee`, `→Simon`). The skill reads these
annotations at runtime to group tasks by agent — no separate routing lookup
required at implement-time.

### extensions.yml Sentinel

The comment `# squad-managed: true` placed on the first line of
`.specify/extensions.yml` by the Squad extension on first write.

Detection rule used by `speckit.squad.init` and `speckit.squad.generate`:
- Sentinel **absent** → file is the speckit default → overwrite with squad template
- Sentinel **present** → Squad has already patched → skip silently

The sentinel is embedded in the `templates/extensions.yml` bundled in the
extension. After the first forced write the user owns the file and Squad will
never overwrite it again.

### list-hooks.sh

A bash script bundled in `scripts/bash/list-hooks.sh` (extension repo) that
reads `.specify/extensions.yml` and outputs enabled hooks for a given lifecycle
event, one per line in `COMMAND=… OPTIONAL=… PROMPT=…` format.

Installed to `.specify/scripts/bash/list-hooks.sh` on every `init`/`generate`
(always overwrite — the script is fully extension-owned).

Depends on `common.sh` (provided by speckit base installation).

---

## Decisions

| # | Decision | Rationale |
|---|----------|-----------|
| 1 | Skill installed by `init` and `generate`, not at `specify extension add` time | The spec-kit extension system has no native mechanism to copy assets to `.github/`. Commands are the only extension point for arbitrary file writes. |
| 2 | Skill source lives in `skills/` at the extension root | `.github/` is excluded by `.extensionignore` to avoid installing CI/workflows into user projects. A top-level `skills/` folder is included in the installed copy. |
| 3 | Skill content is static — no dynamic generation | The skill reads `→AgentName` annotations from `tasks.md` at runtime. The routing table is not embedded; the skill works for any Squad project without modification. |
| 4 | Idempotency: skip if file exists, no overwrite | Protects potential manual edits. `init` and `generate` both skip silently if the skill is already present (`init` prints an info message; `generate` skips silently). |
| 5 | `grill-with-docs` fetched from official repo at install time; bundled copy is fallback | The skill is owned by an external repo (`mattpocock/skills`). Fetching at install time ensures the project always receives the latest version. The bundled copy (`skills/grill-with-docs/`) ships as an offline/CI fallback. Files fetched: `SKILL.md`, `CONTEXT-FORMAT.md`, `ADR-FORMAT.md`. Idempotency: skip entire block if target directory already exists. |
| 6 | `extensions.yml` write-once via sentinel `# squad-managed: true` | speckit creates a default `.specify/extensions.yml` at base installation. Squad must overwrite it exactly once to add Squad hooks. Sentinel on line 1 signals "already patched"; absence means the file is the speckit default and safe to overwrite. After the first overwrite the user owns the file. |
| 7 | `list-hooks.sh` always overwritten | Unlike skills and extensions.yml, the hook-listing script is fully owned by the extension. It is copied fresh on every `init`/`generate` so updates ship automatically. |
| 8 | `.github/copilot-instructions.md` blocks are idempotent via HTML comment markers | Two blocks: `<!-- SQUAD OVERRIDES -->` and `<!-- SPECKIT HOOKS -->`. If a marker pair is found, the block is replaced in place. If absent, the block is appended. The file is created if it does not exist. |
| 9 | `.squad/ceremonies.md` Speckit Tasks Audit block is write-once, detected by heading | `init` and `generate` append the `## Speckit Tasks Audit` block from `templates/ceremonies-tasks-auditor.md` only if the heading is absent from the file. Content-based detection (no separate sentinel) — heading presence means Squad already patched it. File is created if missing. |
