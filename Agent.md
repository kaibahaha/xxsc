# Agent.md

## P1 relay authority

This file is the authoritative execution contract for the P1 relay on branch `exp/p1-relay-dualwrite-20261023`.

- Repository: `kaibahaha/xxsc`
- Source of truth for A task identity: WorkBuddy's A order under `workbuddy/a_orders/`.
- Source of truth for C/D task identity: WorkBuddy's C/D order under `workbuddy/c_orders/` or `workbuddy/d_orders/`.
- Preserve `TASK_ID`, `SCHEDULE_ID`, `GLOBAL_SEQ`, `QUESTION_NO`, `INPUT_COMMIT`, source identity, and result identity exactly as dispatched.
- Do not invent or renumber question numbers.
- Read completed Markdown from the authorized delivery folder; copy bytes/content without rewriting, summarizing, solving, or reconstructing.
- A/C/D results mirror to `results/chatgpt-a/`, `results/chatgpt-c/`, and `results/chatgpt-d/`.
- C/D also retain the existing Drive delivery and Google Docs recovery flow.
- Every write requires a real commit SHA and independent read-back equality verification.
- Missing source, missing identity, incomplete result, permission failure, or mismatch is BLOCKED/REWORK; preserve source and retry next run.
- Never delete source or target files and never accept exit code, directory existence, registration, or historical audit alone as success.

The detailed gate is defined by `docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md`.
