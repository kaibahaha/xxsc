# factory/agl -- Agensh-Lite V4.2 adapter plane (WorkBuddy scope)

Implementation of modules **M02 / M06 / M08 / M10** for workorder
`AGL-WB-ADAPTERS-R01`. Codex owns M01/M03/M04/M05/M07/M09; nothing here
re-implements a Controller, lease, event state machine or schema registry.

```
agl/
  errors.py             typed error taxonomy (NO_PERMISSION/CONFLICT/UNKNOWN_WRITE/...)
  storage/
    transports.py       RestTransport (GitHub API) + LocalGitTransport (real git plumbing)
    github.py           M02  immutable writes, independent readback, CAS projections
    ledger.py           per-(event_id,target) events, receipts, monotonic cursors
  adapters/
    types.py            capability probe value objects (SUPPORTED/UNSUPPORTED/UNKNOWN/BLOCKED)
    base.py             AgentAdapter protocol
    github_mailbox.py   Git-file mailbox transport shared by all providers
    providers.py        chatgpt / workbuddy / codex / custom adapters
    registry_view.py    adapter-side config preflight, admission gate, quota view
  poll.py               M06  per-provider scheduling + one wake-up cycle
  execution.py          M08  TEST_REQUEST -> Runner -> TEST_RESULT -> ACK
  cli.py                M10  command line
  support/poolgen.py    N-agent pool fixture generator
config/                 valid N=6 pool (honest PENDING_PROBE) + admitted test fixture
tests/                  adapter unit tests + integration over a real bare repo
```

## Install / test

```bash
cd factory
python3.11 -m pip install -e .          # optional; tests also run with PYTHONPATH=.
PYTHONPATH=. python3.11 -m pytest tests -q
```

No third-party runtime dependency: the REST client is stdlib `urllib`.

## CLI

Every command is read-only by default. Writes need `--apply` **plus** explicit
`--repo`, `--branch`, `--project` that match the config, and a path inside the
whitelist. `main`/`master` are refused at both config and adapter level.

```bash
agl validate-config --config config/pool_n6.valid.json
agl gen-pool --n 20 --mix chatgpt=8,workbuddy=8,codex=4 --out /tmp/n20.json
agl plan-schedules --config config/pool_n6.valid.json --json
agl offsets --k 5
agl probe --agent WORKBUDDY_DEV_01 --config ...            # dry-run: no write probe
agl probe --agent WORKBUDDY_DEV_01 --config ... --apply --repo ... --branch ... --project ...
agl poll --agent WORKBUDDY_DEV_01 --run-id RUN-... --config ...
agl submit-event --event ev.json --config ...              # dry-run prints sha256
agl reconcile --event-id EV-... --config ...
agl rebuild-board --deterministic --config ...
agl audit --config ...
agl run-sample-test --task TASK-1 --commit <sha> --worktree ../.. --command "python -m pytest -q" --apply ...
agl verify-roundtrip --config ... --apply --repo ... --branch ... --project ...
```

Exit codes: `0` ok, `2` config/guard, `3` blocked (admission/executor/provider),
`4` test failed, `5` stale SHA, `6` conflict/collision.

## Local transport for tests

`--transport local --local-remote /path/to/bare.git` swaps the GitHub API for
real `git` plumbing (`git hash-object`, `commit-tree`, `update-ref <new> <old>`).
Commit and blob SHAs are genuine; CAS is enforced by git itself. This is the
harness the integration tests use; it is **not** evidence of a GitHub connection.

## What is deliberately absent

* no Controller, lease, fencing, event replay (Codex M01/M03/M04/M05/M07/M09);
  `poll` emits `CLAIM_PROPOSED` and reports `CONTROLLER_UNAVAILABLE`
* no platform schedule creation; `plan-schedules` only proposes a manifest
* no webhook: cross-provider hand-off is Git mailbox + each platform's cadence
* no `QA_GREEN`: a passing test is `PASS` with `business_acceptance=PENDING_CORE`
  until the Controller accepts it
