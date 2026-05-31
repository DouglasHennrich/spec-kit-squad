---
description: "Initialize a Squad team from the current Speckit spec"
---

# Squad Bridge: Init

Read the current project spec and bootstrap a Squad team tailored to its
technology domains, roles, and work types. Run this once after your initial
`/speckit.specify` to get a squad that mirrors your project's shape.

## Prerequisites

Verify Squad CLI is available:

```bash
squad --version
```

If that fails, install it first:

```bash
npm install -g @bradygaster/squad-cli
```

## User Input

$ARGUMENTS

## Steps

1. **Read the spec** from the active spec directory under `specs/` (e.g.,
   `specs/001-<name>/spec.md`). If no spec directory exists, tell the user
   to run `/speckit.specify` first and stop.

2. **Read tasks** from `specs/<id>/tasks.md` if it exists (used to infer work
   types and routing signals).

3. **Load bridge config** from `.specify/extensions/squad/squad-config.yml`
   if it exists, otherwise use extension defaults.

4. **Analyze the spec** to extract:
   - Technology domains (e.g., React, Node.js, PostgreSQL, Python, Go, iOS)
   - Architectural concerns (e.g., API design, database schema, DevOps/CI)
   - Cross-cutting concerns (e.g., auth, testing, documentation)
   - Any explicit roles or team structure mentioned in the spec

5. **Initialize Squad** if `.squad/` does not already exist:

   ```bash
   squad init
   ```

6. **Generate agent definitions** — for each identified domain/concern,
   create a Squad agent with:
   - A descriptive `name` (e.g., `backend-engineer`, `frontend-engineer`)
   - A `role` derived from the domain
   - `capabilities` array (name + level: expert/proficient/basic) inferred
     from how prominently the domain features in the spec
   - `model` set to the tier from config that matches the agent's complexity
   - `status: active`

   Squad's format. Update `.squad/team.md` and `.squad/routing.md` to reflect
   the current roster, routing rules, and model tier assignments. In
   markdown-first mode, no root `squad.config.ts` file is required.

7. **Generate routing rules** in `.squad/routing.md` that map task keywords
   and domain patterns to the agents created above. Examples:
   - `/\bAPI|endpoint|REST|GraphQL\b/i` → backend-engineer
   - `/\bReact|component|UI|frontend\b/i` → frontend-engineer
   - `/\btest|spec|coverage|QA\b/i` → qa-engineer

8. **Install Squad skills** — for each skill below, check if the target file
   already exists. If it does **not** exist, create the directory and copy the
   file from the extension's installed path. If it already exists, print an
   info message and skip.

   | Skill | Source | Target |
   |-------|--------|--------|
   | `speckit-implement-squad-route` | `.specify/extensions/squad/skills/speckit-implement-squad-route/SKILL.md` | `.github/skills/speckit-implement-squad-route/SKILL.md` |

   **`speckit-implement-squad-route`:** copy from the extension bundle if target does not exist; skip silently if already present.

   **`grill-with-docs`:** this skill is fetched from its official repository at install
   time so the project always receives the latest version. If the target directory
   does not already exist:

   1. Create `.github/skills/grill-with-docs/`.
   2. For each file below, attempt to download with `curl -fsSL <url> -o <target>`.
      If `curl` fails (no network, rate-limit, etc.), copy the bundled fallback
      from `.specify/extensions/squad/skills/grill-with-docs/<file>` instead.

   | File | Official URL |
   |------|--------------|
   | `SKILL.md` | `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/SKILL.md` |
   | `CONTEXT-FORMAT.md` | `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/CONTEXT-FORMAT.md` |
   | `ADR-FORMAT.md` | `https://raw.githubusercontent.com/mattpocock/skills/main/skills/engineering/grill-with-docs/ADR-FORMAT.md` |

   If the target directory already exists, skip the entire `grill-with-docs` block
   (same idempotency rule as all other skills).

   For each skill:
   - If installed from GitHub: `✅ Skill installed (latest): {target}`
   - If installed from bundle fallback: `✅ Skill installed (bundled): {target}`
   - If already present: `ℹ️  Skill already present — skipping: {target}`

9. **Install `list-hooks.sh`** — copy
   `.specify/extensions/squad/scripts/bash/list-hooks.sh` to
   `.specify/scripts/bash/list-hooks.sh` and make it executable (`chmod +x`).
   Overwrite if it already exists (always keep the latest version from the
   extension bundle).

   Print: `✅ Script installed: .specify/scripts/bash/list-hooks.sh`

10. **Bootstrap `.specify/extensions.yml`** — open the file and check the first
    line for the sentinel `# squad-managed: true`.

    - **Sentinel absent** (file is the speckit default) → overwrite the entire
      file with the contents of
      `.specify/extensions/squad/templates/extensions.yml` (which begins with
      `# squad-managed: true`). Print:
      `✅ extensions.yml bootstrapped with Squad hooks`
    - **Sentinel present** (squad already patched it) → skip silently. Print:
      `ℹ️  extensions.yml already managed by Squad — skipping`

11. **Bootstrap `.squad/ceremonies.md`** — open the file and check whether it
    already contains the heading `## Speckit Tasks Audit`.

    - **Heading absent** → append the contents of
      `.specify/extensions/squad/templates/ceremonies-tasks-auditor.md` to the
      end of the file. Print:
      `✅ ceremonies.md patched with Speckit Tasks Audit ceremony`
    - **Heading present** → skip silently. Print:
      `ℹ️  ceremonies.md already contains Speckit Tasks Audit — skipping`

    If `.squad/ceremonies.md` does not exist (unexpected — `squad init` should
    create it), create it and write the template content. Print:
    `✅ ceremonies.md created with Speckit Tasks Audit ceremony`

12. **Update `.github/copilot-instructions.md`** — create the file if it does
    not exist. Then apply the two Squad blocks using their HTML comment markers
    as boundaries:

    - Search for `<!-- SQUAD OVERRIDES -->` … `<!-- END SQUAD OVERRIDES -->`.
      If found, replace the entire block. If not found, append the block at the
      end of the file.
    - Search for `<!-- SPECKIT HOOKS -->` … `<!-- END SPECKIT HOOKS -->`.
      If found, replace the entire block. If not found, append the block at the
      end of the file.

    Block contents to write (verbatim):

    ```
    <!-- SQUAD OVERRIDES -->

    ## speckit.implement → Squad Route

    **IMPORTANT:** `speckit.implement` is overridden in this project.
    Do NOT execute tasks sequentially. Instead:

    1. Read `.github/skills/speckit-implement-squad-route/SKILL.md`
    2. Follow the skill exactly — group tasks by agent, fan out in parallel per phase
    3. After all phases, trigger the Speckit Tasks Audit ceremony (tasks-auditor)

    This override applies whenever the user says "speckit implement", "implement the tasks",
    "implement speckit tasks", or the `speckit.implement` agent is invoked.

    <!-- END SQUAD OVERRIDES -->

    <!-- SPECKIT HOOKS -->

    ## Hook Execution — Mandatory Protocol

    After **every** speckit command completes, you MUST run ALL hooks for the corresponding event.

    **Never skip a hook because you already processed the first one.**

    ### How to do it

    1. Run the hook list script to get every hook for the event:

       ```
       bash .specify/scripts/bash/list-hooks.sh <event>
       ```

       Replace `<event>` with the event name (e.g., `after_tasks`, `after_specify`).

    2. The script outputs one line per enabled hook:

       ```
       COMMAND=speckit.squad.route OPTIONAL=false PROMPT=Routing tasks to Squad agents...
       ```

    3. Process **every line**:
       - `OPTIONAL=false` → execute immediately with `runSubagent("<COMMAND>")`
       - `OPTIONAL=true` → announce to the user and ask for confirmation before executing

    ### Event ↔ Command mapping

    | After completing...   | Event name            |
    | --------------------- | --------------------- |
    | speckit.specify       | `after_specify`       |
    | speckit.clarify       | `after_clarify`       |
    | speckit.plan          | `after_plan`          |
    | speckit.tasks         | `after_tasks`         |
    | speckit.implement     | `after_implement`     |
    | speckit.checklist     | `after_checklist`     |
    | speckit.analyze       | `after_analyze`       |
    | speckit.constitution  | `after_constitution`  |
    | speckit.taskstoissues | `after_taskstoissues` |

    Same pattern applies to `before_*` hooks (run the script with the before event name before invoking the command).

    <!-- END SPECKIT HOOKS -->
    ```

    Print: `✅ .github/copilot-instructions.md updated with Squad blocks`

13. **Print a summary**:

   ```
   ✅ Squad initialized
      Agents created : 3
        - backend-engineer   (Node.js/REST API — expert)
        - frontend-engineer  (React/TypeScript — expert)
        - qa-engineer        (Testing/QA — proficient)
      Routing rules  : 6
      Config         : markdown-first `.squad` artifacts
   
   Next steps:
     squad doctor          — verify your team
     /speckit.plan         — create your implementation plan
     /speckit.tasks        — generate tasks from the plan
     /speckit.squad.route  — route tasks to agents (after tasks exist)
   ```

## Notes

- Running this command more than once is safe — it will not overwrite existing
  agent files. Use `/speckit.squad.generate` to refresh agents as the spec
  evolves.
- If `$ARGUMENTS` contains a domain or role name, generate an agent for that
  domain in addition to those inferred from the spec.
