#!/usr/bin/env bash
# Reproducible local evidence run (no network, no credentials).
#
#   bash factory/tools/local_evidence.sh
#
# Creates a throw-away bare repository from the current checkout, runs the CLI
# against it with --transport local, and prints every command plus its exit code.
# Commit/blob SHAs are computed by git itself; only the network hop is absent.
set -uo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK="$(mktemp -d /tmp/agl-evidence-XXXXXX)"
BARE="$WORK/remote.git"
CFG="$WORK/pool.json"
export PYTHONPATH="$REPO_ROOT/factory"
PY=python3.11

say() { printf '\n### %s\n' "$*"; }
run() {
  printf '$ %s\n' "$*"
  "$@"
  local rc=$?
  printf '[exit=%s]\n' "$rc"
  return 0
}

say "environment"
run $PY -c "import sys, platform; print(sys.version.split()[0], platform.platform())"
run git --version
printf 'workdir=%s\n' "$WORK"

say "prepare bare remote from current checkout"
git clone -q --bare "$REPO_ROOT" "$BARE"
git -C "$BARE" branch -f exp/test HEAD >/dev/null
run git -C "$BARE" rev-parse refs/heads/exp/test

say "generate N=6 pool bound to the local ref"
$PY - "$CFG" <<'PYEOF'
import json, sys
from pathlib import Path
from agl.support.poolgen import build_pool
cfg = build_pool(6, mix={"chatgpt": 3, "workbuddy": 2, "codex": 1},
                 admission="ADMITTED_ACTIVE", project_id="AGL-EVIDENCE-006",
                 ref="exp/test", runtime_root="factory/projects/AGL-EVIDENCE-006")
Path(sys.argv[1]).write_text(json.dumps(cfg, indent=2), encoding="utf-8")
print("config written", sys.argv[1])
PYEOF

run $PY -m agl.cli validate-config --config "$CFG"

say "pool sizes 2/3/5/6/10/20"
for n in 2 3 5 6 10 20; do
  run $PY -m agl.cli gen-pool --n "$n" --out "$WORK/n$n.json" --project "AGL-N$n"
  run $PY -m agl.cli validate-config --config "$WORK/n$n.json"
done

say "offset tables K=1..6"
for k in 1 2 3 4 5 6; do run $PY -m agl.cli offsets --k "$k"; done

say "schedule manifest (per provider)"
run $PY -m agl.cli plan-schedules --config "$CFG" --json

say "capability probes (read-only, local git)"
for a in CHATGPT_01 WORKBUDDY_01 CODEX_01; do
  run $PY -m agl.cli probe --agent "$a" --config "$CFG" \
      --transport local --local-remote "$BARE"
done

say "write probe (real immutable write + independent readback)"
run $PY -m agl.cli probe --agent WORKBUDDY_01 --config "$CFG" \
    --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006 --json

say "roundtrip: write + independent readback"
run $PY -m agl.cli verify-roundtrip --config "$CFG" \
    --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006 --json

say "event submit -> reconcile -> audit"
$PY - "$WORK/ev.json" <<'PYEOF'
import json, sys
from pathlib import Path
ev = {
  "schema_version": "1.0", "event_id": "EV-EVIDENCE-0001", "project_id": "AGL-EVIDENCE-006",
  "task_id": "TASK-DEMO", "producer": "WORKBUDDY_01",
  "target_agents": ["CHATGPT_01", "WORKBUDDY_01", "CODEX_01"],
  "kind": "FACT_PUBLISHED", "source": "github", "observed_at": "2026-10-25T16:00:00Z",
  "summary": "evidence event", "raw_ref": "kaibahaha/xxsc@exp/test:factory/agl/cli.py",
  "spec_hash": "c" * 64, "run_id": "RUN-EVIDENCE"
}
Path(sys.argv[1]).write_text(json.dumps(ev), encoding="utf-8")
print("event written")
PYEOF
run $PY -m agl.cli submit-event --event "$WORK/ev.json" --config "$CFG"
run $PY -m agl.cli submit-event --event "$WORK/ev.json" --config "$CFG" \
    --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006
run $PY -m agl.cli submit-event --event "$WORK/ev.json" --config "$CFG" \
    --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006
run $PY -m agl.cli reconcile --event-id EV-EVIDENCE-0001 --config "$CFG" \
    --transport local --local-remote "$BARE" --json
run $PY -m agl.cli audit --config "$CFG" --transport local --local-remote "$BARE" --json
run $PY -m agl.cli rebuild-board --config "$CFG" --transport local --local-remote "$BARE" \
    --deterministic

say "seed a READY task into the isolated repo"
$PY - "$BARE" <<'PYEOF'
import sys
from agl.storage.github import GitHubStorage, open_storage
from agl.storage.transports import LocalGitTransport
storage = GitHubStorage(LocalGitTransport(sys.argv[1]), "kaibahaha/xxsc", "exp/test",
                        allowed_prefixes=("factory",))
body = ("# Demo task for evidence run\n"
        "STATUS: READY\n"
        "CAPABILITIES: code_execution, git_write\n"
        "PRIORITY: P1\n"
        "SPEC_HASH: " + "d" * 64 + "\n")
receipt = storage.write_immutable("factory/projects/AGL-EVIDENCE-006/01_tasks/TASK-DEMO/TASK.md",
                                  body.encode(), idempotency_key="seed-task-demo")
print("seeded", receipt.status, receipt.commit_sha[:12], receipt.blob_sha[:12])
PYEOF

say "publish board projection (needed before polling)"
run $PY -m agl.cli rebuild-board --config "$CFG" --transport local --local-remote "$BARE" \
    --apply --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006 --deterministic

say "poll (dry-run then apply)"
run $PY -m agl.cli poll --agent WORKBUDDY_01 --run-id RUN-EV-1 --config "$CFG" \
    --transport local --local-remote "$BARE"
run $PY -m agl.cli poll --agent WORKBUDDY_01 --run-id RUN-EV-1 --config "$CFG" \
    --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006

say "run-sample-test (real pytest inside the checkout)"
COMMIT="$(git -C "$REPO_ROOT" rev-parse HEAD)"   # worktree must be at the tested commit
run $PY -m agl.cli run-sample-test --task TASK-DEMO --commit "$COMMIT" \
    --worktree "$REPO_ROOT/factory" --command "$PY -m pytest tests/adapters/test_offsets.py -q -p no:cacheprovider" \
    --config "$CFG" --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006

say "run-sample-test with a stale SHA (must be STALE_TEST)"
run $PY -m agl.cli run-sample-test --task TASK-DEMO --commit 0000000000000000000000000000000000000000 \
    --worktree "$REPO_ROOT/factory" --command "true" --config "$CFG" \
    --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006

say "run-sample-test with no executor (must be BLOCKED_EXECUTOR)"
run $PY -m agl.cli run-sample-test --task TASK-DEMO --commit "$COMMIT" \
    --command "true" --config "$CFG" --transport local --local-remote "$BARE" --apply \
    --repo kaibahaha/xxsc --branch exp/test --project AGL-EVIDENCE-006

say "apply guard: missing --repo/--branch/--project"
run $PY -m agl.cli poll --agent WORKBUDDY_01 --config "$CFG" \
    --transport local --local-remote "$BARE" --apply

say "final ref state"
run git -C "$BARE" log --oneline -5 refs/heads/exp/test

printf '\nworkdir kept at %s\n' "$WORK"
