# P1-ACD-GIT-RELAY-20261023 | WorkBuddy A/C/D Git Relay Dispatch

## Scope

WorkBuddy is responsible for discovering newly added complete Markdown results for ChatGPT A, C, and D, creating the corresponding concrete task orders in this directory, and executing the authorized Git relay on the experiment branch.

## Repository

- REPO: `kaibahaha/xxsc`
- BRANCH: `exp/p1-relay-dualwrite-20261023`
- DEADLINE_BEIJING: `2026-10-25T12:00:00+08:00`
- TARGETS:
  - A -> `results/chatgpt-a/`
  - C -> `results/chatgpt-c/`
  - D -> `results/chatgpt-d/`

## Required behavior

1. Read the current ChatGPT Library/Drive source inventory and identify only new, complete, not-yet-relayed Markdown.
2. For each A/C/D source, create a concrete child order under `workbuddy/a_orders/` using the existing TASK-P1-GIT-<LETTER> format.
3. Copy source Markdown bytes unchanged; do not rewrite, summarize, solve, or reconstruct content.
4. Create or update only the matching target result path. Never delete source or target files.
5. Obtain the real Git commit SHA and independently read the committed file back from this branch.
6. Verify filename, TASK_ID/RESULT_ID markers, byte/content equality, and result-block completion before marking success.
7. On failure, write an explicit failure/blocked ACK with the reason and leave the item pending for the next run.
8. Preserve the existing C/D Google Docs missing-submission recovery, A/C/D Drive mirror, and fixed audit-log responsibilities.
9. Do not claim success from a tool exit code, registration, or historical audit entry alone.

## Acceptance

The parent task is successful only when each child order has an independent read-back receipt containing source identity, target path, commit SHA, and equality status. Any mismatch is REWORK, not PASS.

## Ownership

WorkBuddy owns child-order creation, execution, ACKs, and audit updates. This parent file is dispatch configuration only and is not itself a result.
