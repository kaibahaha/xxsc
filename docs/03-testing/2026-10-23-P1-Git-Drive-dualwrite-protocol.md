# P1 Git/Drive Dual-Write Protocol V1.2

VERSION=V1.2
REPOSITORY=kaibahaha/xxsc
BRANCH=exp/p1-relay-dualwrite-20261023
DEADLINE_BEIJING=2026-10-25T12:00:00+08:00

## Authority and source

1. WorkBuddy task orders are authoritative for task identity and question numbering.
2. A reads the A order from `workbuddy/a_orders/`; C and D read their orders from `workbuddy/c_orders/` and `workbuddy/d_orders/`.
3. The completed Markdown in the authorized delivery folder is the payload source. Do not use a historical audit entry or an original Drive task as a substitute payload.

## Required mirrors

- A/C/D delivery-folder Markdown -> Git:
  - A: `results/chatgpt-a/`
  - C: `results/chatgpt-c/`
  - D: `results/chatgpt-d/`
- C/D delivery-folder Markdown -> the existing Drive destination.
- Preserve the existing C/D Google Docs missing-submission recovery, A/C/D Drive mirror, and audit-log duties.

## Identity and numbering

Copy `TASK_ID`, `SCHEDULE_ID`, `GLOBAL_SEQ`, `QUESTION_NO`, `INPUT_COMMIT`, source identity, and result identity exactly from the WorkBuddy order and completed result. Do not renumber, infer, or repair missing identifiers.

## Git acceptance gate

For each file:

1. Confirm the source is complete and not previously successfully mirrored.
2. Copy the Markdown content unchanged to the matching target directory.
3. Record the real commit SHA and target blob SHA.
4. Read the committed file back from this exact branch.
5. Compare source and read-back content byte-for-byte where the source bytes are available; otherwise compare the complete UTF-8 content and record the comparison method.
6. Confirm identity fields, completion marker, and result block are present.
7. Record PASS only after all checks pass.

Any missing authority file, permission error, incomplete source, identity mismatch, or read-back mismatch is BLOCKED/REWORK. Preserve all files and retry next run. Never delete, overwrite unrelated paths, or claim success from an exit code, registration, directory listing, or historical audit alone.
