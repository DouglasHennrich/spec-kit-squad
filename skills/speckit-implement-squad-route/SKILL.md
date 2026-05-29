---
name: speckit-implement-squad-route
confidence: high
description: >
  Override for speckit.implement — routes speckit tasks through the Squad coordinator
  instead of executing them sequentially. The coordinator fans out tasks to specialist
  agents in parallel based on →AgentName annotations in tasks.md, then triggers the
  tasks-auditor ceremony.
---

# Speckit Implement → Squad Route

## When to Use

Apply this skill whenever **any** of the following is detected:

- User says "speckit implement", "run speckit implement", "implement the tasks", "implement the speckit tasks"
- The `speckit.implement` agent is about to be spawned
- A batch of tasks from `tasks.md` needs to be executed

**Do NOT execute tasks sequentially.** Always use this skill instead.

## Pre-condition

Tasks in `tasks.md` must already have `→AgentName` annotations added by `/speckit.squad.route`.

**If any unchecked task (`- [ ]`) lacks a `→AgentName` tag, stop immediately and tell the user:**

> "Tasks are not yet routed. Please run `/speckit.squad.route` before implementing."

## Step 1 — Resolve Tasks

1. Read `.specify/feature.json` → parse `feature_directory`
2. Load `{feature_directory}/tasks.md`
3. Load `{feature_directory}/plan.md` and `{feature_directory}/spec.md` for context
4. Read `agent_model` from `.specify/extensions/squad/squad-config.yml` → fallback to `claude-sonnet-4.6`

## Step 2 — Group Tasks by Agent

Parse every unchecked task (`- [ ]`) from `tasks.md`. Each task already carries a `→AgentName` annotation written by `/speckit.squad.route`. Group tasks by agent name.

Example annotation format:

```
- [ ] T018 [US1] →Simon Add unit tests for the care-assignment service
- [ ] T012 [P]   →Kaylee Extend the care-assignment entity with new fields
```

A task may belong to only one agent (the primary owner). Tasks with `co-owners` are still assigned to the primary owner.

## Step 3 — Respect Phase Dependencies

Tasks.md is organized in phases. **Phase N must be complete before Phase N+1 begins.**

- Spawn all agents for **Phase 1** in parallel (background mode)
- After all Phase 1 agents complete → spawn all agents for **Phase 2** in parallel
- Continue phase by phase until all tasks are complete

Within a phase, tasks assigned to different agents run in parallel. Tasks assigned to the same agent run sequentially inside that agent's spawn.

## Step 4 — Spawn Agents

For each agent with tasks in the current phase, spawn using the standard Squad template:

```
agent_type: "general-purpose"
model: "{agent_model}"
mode: "background"
name: "{agent-name}"
description: "{emoji} {AgentName}: Implementing Phase {N} tasks — {task-ids}"
prompt: |
  You are {AgentName}, the {Role} on this project.

  YOUR CHARTER:
  {paste contents of .squad/agents/{name}/charter.md}

  TEAM ROOT: {team_root}
  CURRENT_DATETIME: {current_datetime}

  Read .squad/agents/{name}/history.md
  Read .squad/decisions.md

  SPECKIT CONTEXT:
  - Spec: {feature_directory}/spec.md
  - Plan: {feature_directory}/plan.md
  - Tasks: {feature_directory}/tasks.md

  YOUR TASKS FOR THIS PHASE:
  {list of task IDs and full task descriptions assigned to this agent}

  INSTRUCTIONS:
  - Mark each task complete in tasks.md by changing `- [ ]` to `- [x]`
  - Do NOT implement tasks assigned to other agents
  - Write a decision inbox entry for any architectural choice made

  AFTER all your tasks:
  1. Append learnings to .squad/agents/{name}/history.md
  2. Write drop file to .squad/decisions/inbox/{name}-phase{N}-complete.md
  ⚠️ RESPONSE ORDER: plain text summary AFTER all tool calls.
```

## Step 5 — After Each Phase

After all agents in a phase complete:

1. Show compact results: `{emoji} {AgentName} — Phase {N}: {N} tasks done`
2. Spawn Scribe (background) to merge decisions and log the phase
3. Immediately start the next phase without waiting for user input

## Step 6 — After All Phases Complete

When all phases are done, **automatically trigger the Speckit Tasks Audit ceremony**:

- Spawn `tasks-auditor` (sync) to audit the full tasks.md
- If the report contains non-`✅ done` tasks, re-route failing tasks to the responsible agent
- Loop until all tasks pass or escalate to user after 3 retry cycles

## Coordinator Announcement

When this skill activates, say:

```
📋 speckit-implement-squad-route — distributing tasks.md across team agents.

Phase {N}: {X} tasks → {A} agents in parallel
  {emoji} {AgentName} — {task-ids}
  {emoji} {AgentName} — {task-ids}
```

## Rules

- NEVER execute tasks inline in the coordinator
- NEVER spawn a single agent to do all tasks
- ALWAYS respect phase boundaries
- ALWAYS trigger tasks-auditor after the last phase
