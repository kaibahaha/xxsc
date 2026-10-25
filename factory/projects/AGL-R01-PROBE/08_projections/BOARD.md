# BOARD (adapter projection)

project_id: AGL-R01-PROBE
repo: kaibahaha/xxsc
ref: dev/agl-v4.2-workbuddy-adapters
events: 1
events_digest: 64acb2e3cb1c55b8f52e5b262fe4afeebc4594d8573d28df60a996366d7d2e0e

> This file is a deterministic projection over immutable events. The
> authoritative board is produced by the Controller (M09); this copy is
> for audit and must not be used to grant leases.

## Agents

| agent | provider | state | capabilities |
| --- | --- | --- | --- |
| CHATGPT_01 | chatgpt | ADMITTED_ACTIVE | research,requirements,review,code_draft |
| CHATGPT_02 | chatgpt | ADMITTED_ACTIVE | research,requirements,review,code_draft |
| CHATGPT_03 | chatgpt | ADMITTED_ACTIVE | research,requirements,review,code_draft |
| CODEX_01 | codex | ADMITTED_ACTIVE | architecture,complex_coding,review |
| WORKBUDDY_01 | workbuddy | ADMITTED_ACTIVE | code_execution,test_run,git_write |
| WORKBUDDY_02 | workbuddy | ADMITTED_ACTIVE | code_execution,test_run,git_write |

## Events

| date/event | kind | task | producer | targets |
| --- | --- | --- | --- | --- |
| 20261025/EV-R01-COLLIDE-1 | FACT_PUBLISHED | TASK-R01-PROBE | WORKBUDDY_01 | WORKBUDDY_01 |
