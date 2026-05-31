---
description: "Re-generate Squad agent definitions as your spec evolves"
---

# Squad Bridge: Generate

Re-read the current spec and regenerate Squad agent definitions, capabilities,
and routing rules to stay in sync with spec changes. Safe to run repeatedly —
existing agents are updated in place; agents no longer supported by the spec
are flagged (not deleted).

This command is also triggered by the `after_specify` hook.

## User Input

$ARGUMENTS

## Steps

1. **Verify `.squad/` exists** — if not, tell the user to run
   `/speckit.squad.init` first and stop.

2. **Read the spec** from the active spec directory under `specs/` (e.g.,
   `specs/001-<name>/spec.md`).

3. **Load bridge config** from `.specify/extensions/squad/squad-config.yml`
   if it exists, otherwise use extension defaults.

4. **Read existing agents** from `.squad/agents/` (each agent lives in
   `.squad/agents/{name}/charter.md`) so changes can be diffed rather than
   blindly overwritten.

5. **Analyze the spec** to extract technology domains, architectural concerns,
   and cross-cutting roles (same logic as `init`). If `$ARGUMENTS` names a
   specific domain, limit regeneration to that domain's agent.

6. **Diff against existing agents**:
   - **New domains** found in spec but no matching agent → create new agent
   - **Changed domains** (different prominence or tech stack) → update agent
     capabilities and model tier
   - **Removed domains** (in existing agents but absent from new spec) →
     set `status: inactive` and note in output (do NOT delete)

7. **Update `.squad/team.md` and `.squad/routing.md`** to reflect the new
   agent set, routing rules, and model tier assignments. In markdown-first mode,
   keep the root `.squad` artifacts authoritative and do not require a
   `squad.config.ts` file.

8. **Update `.squad/routing.md`** to add routing rules for any new agents and
   update patterns for changed agents.

9. **Install Squad skills if missing** — for each skill below, check if the
   target file already exists. If it does **not** exist, create the directory
   and copy the file from the extension's installed path. Skip silently if
   already present.

   | Skill | Source | Target |
   |-------|--------|--------|
   | `speckit-implement-squad-route` | `.specify/extensions/squad/skills/speckit-implement-squad-route/SKILL.md` | `.github/skills/speckit-implement-squad-route/SKILL.md` |

   **`speckit-implement-squad-route`:** copy from the extension bundle if target does not exist; skip silently if already present.

   **`grill-with-docs`:** fetched from the official repository so the project
   always receives the latest version. If the target directory does not already
   exist, create `.github/skills/grill-with-docs/` and download each file with
   `curl -fsSL <url> -o <target>`, falling back to the bundled copy in
   `.specify/extensions/squad/skills/grill-with-docs/<file>` if `curl` fails.

   | File | Official URL |
   |------|--------------|
   | `SKILL.md` | `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/SKILL.md` |
   | `CONTEXT-FORMAT.md` | `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md` |
   | `ADR-FORMAT.md` | `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/ADR-FORMAT.md` |

   If the target directory already exists, skip the entire block.

   Print `✅ Skill installed (latest): {target}` for each newly installed skill (or `✅ Skill installed (bundled): {target}` when curl fallback was used).

10. **Install `list-hooks.sh`** — copy
    `.specify/extensions/squad/scripts/bash/list-hooks.sh` to
    `.specify/scripts/bash/list-hooks.sh` and make it executable (`chmod +x`).
    Overwrite if it already exists (always keep the latest version from the
    extension bundle).

    Print: `✅ Script installed: .specify/scripts/bash/list-hooks.sh`

11. **Bootstrap `.specify/extensions.yml`** — open the file and check the first
    line for the sentinel `# squad-managed: true`.

    - **Sentinel absent** → overwrite the entire file with the contents of
      `.specify/extensions/squad/templates/extensions.yml`. Print:
      `✅ extensions.yml bootstrapped with Squad hooks`
    - **Sentinel present** → skip silently.

12. **Update `.github/copilot-instructions.md`** — create the file if it does
    not exist. Apply the two Squad blocks using their HTML comment markers as
    boundaries (replace if found, append if not):
    `<!-- SQUAD OVERRIDES -->` … `<!-- END SQUAD OVERRIDES -->` and
    `<!-- SPECKIT HOOKS -->` … `<!-- END SPECKIT HOOKS -->`.

    Use the same verbatim block contents as defined in `speckit.squad.init` step 12.

    Print: `✅ .github/copilot-instructions.md updated with Squad blocks`

13. **Bootstrap `.squad/ceremonies.md`** — open the file and check whether it
    already contains the heading `## Speckit Tasks Audit`.

    - **Heading absent** → append the contents of
      `.specify/extensions/squad/templates/ceremonies-tasks-auditor.md` to the
      end of the file. Print:
      `✅ ceremonies.md patched with Speckit Tasks Audit ceremony`
    - **Heading present** → skip silently. Print:
      `ℹ️  ceremonies.md already contains Speckit Tasks Audit — skipping`

    If `.squad/ceremonies.md` does not exist (e.g., user deleted it), create it
    and write the template content. Print:
    `✅ ceremonies.md created with Speckit Tasks Audit ceremony`

14. **Print a diff summary**:

   ```
   Squad agents updated
     ✅ Added   : data-engineer (PostgreSQL/migrations — proficient)
     ✏️  Updated : backend-engineer (added GraphQL capability)
     ⚠️  Inactive: mobile-engineer (no longer in spec — set to inactive)
   
   Routing rules updated: 8 total (2 added, 1 modified)
   ```

## Notes

- `inactive` agents remain in `.squad/` and can be reactivated manually with
  `squad` commands if needed.
- If the spec has not changed since the last run, this command reports
  "No changes detected" and exits cleanly.
