---
name: plan-survives-clear
description: Recover agent plans from disk after /clear or compaction; never trust memory over task_plan.md and progress.md.
---

# Plan survives /clear

Plans on disk outlive chat context. Treat markdown planning files as the source of truth after any wipe.

## Before `/clear` or compaction

1. Write the current phase and decisions into `task_plan.md` and `progress.md` (and `findings.md` when relevant).
2. Prefer an explicit plan under `.planning/<id>/` when using gated / named plans; pin with `PLAN_ID` when needed.
3. Do not leave critical state only in conversation memory.

## After `/clear` or compaction

1. Read the planning files first — never invent progress from memory.
2. Re-derive the next step from phase status in `task_plan.md` / `progress.md`.
3. Run `check-complete.sh` (advisory) or `check-complete.sh --gate` (opt-in block JSON) to observe completion from files alone.
4. Resume work only after file state matches what you intend to do next.

## Ritual (crash-proof loop)

```text
init-session → work + phase-status → /clear → read files → check-complete → continue
```

Memory is disposable. Files are not.
