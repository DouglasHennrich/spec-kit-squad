---
description: "Orchestrate after_tasks flow by routing tasks and preparing API contract docs when needed"
---

# Squad Bridge: After Tasks Orchestrator

Run the complete Squad post-task flow in order:

1. Route tasks to Squad agents
2. Detect API-impacting tasks and prepare API contract documentation only when needed

This command should be used by the `after_tasks` hook.

## User Input

$ARGUMENTS

## Steps

1. Execute `/speckit.squad.route` with the same `$ARGUMENTS`.
2. Execute `/speckit.squad.api-contract` with the same `$ARGUMENTS`.
3. Print a combined summary with:
   - tasks routed
   - API-impacting tasks found
   - API.md destination (if generated)
   - manual assignment warnings (if any)

## Notes

- Keep step order: routing must run first so API ownership can reuse assignments.
- If routing fails, stop and report the error.
- If routing succeeds but no API impact is found, finish successfully without creating API.md.
