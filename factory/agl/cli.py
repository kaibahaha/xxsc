"""M10 -- command line entry points.

Every command is read-only unless ``--apply`` is given, and ``--apply`` itself
requires explicit ``--repo``, ``--branch`` and ``--project`` that match the
loaded config, plus a path whitelist check. Nothing here creates platform
schedules, deployments or paid services.

Commands
--------
validate-config   adapter-side preflight of a pool config
gen-pool          write a valid N-agent pool config (test/ops fixture)
plan-schedules    per-provider cadence + offsets + registration manifest
probe             capability probe for one agent (write probe only with --apply)
poll              one wake-up cycle for one agent (claim only with --apply)
submit-event      write one immutable UEM event per target
reconcile         read an event's manifest, per-target files and ACKs
rebuild-board     deterministic board projection from immutable events
audit             integrity checks over events/receipts/cursors
run-sample-test   execute a TEST_REQUEST and persist TEST_RESULT + logs
verify-roundtrip  write + independent readback of an isolated probe file
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from . import __version__
from .adapters.github_mailbox import AdapterContext
from .adapters.providers import build_adapter
from .adapters.registry_view import RegistryView, validate_config
from .adapters.types import OPS
from .errors import AglError, ErrorCode
from .execution import (
    BLOCKED_EXECUTOR,
    FAIL,
    PASS,
    STALE_TEST,
    TIMEOUT,
    ExecutorBridge,
)
from .poll import PollPlanner, compute_offsets
from .storage.github import canonical_json_bytes, open_storage, sha256_hex, utc_now
from .storage.ledger import EventLedger, normalize_event

EXIT_OK = 0
EXIT_INTERNAL = 1
EXIT_CONFIG = 2
EXIT_BLOCKED = 3
EXIT_TEST_FAILED = 4
EXIT_STALE = 5
EXIT_CONFLICT = 6

DEFAULT_CONFIG = "factory/config/pool_n6.valid.json"
WRITE_PREFIXES = (
    "factory",
    "frameworks/agensh-lite-v4.2/deliveries/WORKBUDDY_ADAPTERS_R01",
)
PROTECTED = {"main", "master"}


# --------------------------------------------------------------------------- #
# plumbing
# --------------------------------------------------------------------------- #


@dataclass
class Ctx:
    args: argparse.Namespace
    registry: RegistryView
    storage: Any
    ledger: EventLedger


def _die(code: int, message: str, as_json: bool, payload: dict[str, Any] | None = None) -> int:
    if as_json:
        print(json.dumps({"ok": False, "error": message, **(payload or {})}, ensure_ascii=False, indent=2))
    else:
        print(f"ERROR: {message}", file=sys.stderr)
    return code


def _require_apply_guards(args: argparse.Namespace, registry: RegistryView) -> str | None:
    """Return an error string when an --apply invocation is not fully explicit."""
    if not args.apply:
        return None
    missing = [name for name in ("repo", "branch", "project") if not getattr(args, name)]
    if missing:
        return f"--apply requires explicit {', '.join('--' + m for m in missing)}"
    if args.branch in PROTECTED:
        return f"refusing to write to protected branch {args.branch}"
    if args.repo != registry.repo:
        return f"--repo {args.repo} does not match config repo {registry.repo}"
    if args.branch != registry.ref:
        return f"--branch {args.branch} does not match config ref {registry.ref}"
    if args.project != registry.project_id:
        return f"--project {args.project} does not match config project_id {registry.project_id}"
    return None


def _ctx(args: argparse.Namespace, *, need_storage: bool = True) -> tuple[Ctx | int]:
    cfg_path = Path(args.config)
    if not cfg_path.exists():
        return _die(EXIT_CONFIG, f"config not found: {cfg_path}", args.json)
    try:
        raw = json.loads(cfg_path.read_text(encoding="utf-8"))
        registry = RegistryView.from_config(raw)
    except AglError as exc:
        return _die(EXIT_CONFIG, f"{exc.code.value}: {exc.message}", args.json, exc.to_dict())
    except json.JSONDecodeError as exc:
        return _die(EXIT_CONFIG, f"invalid JSON: {exc}", args.json)

    guard = _require_apply_guards(args, registry)
    if guard:
        return _die(EXIT_CONFIG, guard, args.json)

    storage = ledger = None
    if need_storage:
        try:
            storage = open_storage(
                args.repo or registry.repo,
                args.branch or registry.ref,
                transport=args.transport,
                token=(os.environ.get(args.token_env) if args.token_env else None),
                local_remote=args.local_remote,
                allowed_prefixes=WRITE_PREFIXES + (registry.runtime_root,),
            )
            ledger = EventLedger(storage, registry.runtime_root)
        except AglError as exc:
            return _die(EXIT_BLOCKED, f"{exc.code.value}: {exc.message}", args.json, exc.to_dict())
    return Ctx(args, registry, storage, ledger)


# --------------------------------------------------------------------------- #
# commands
# --------------------------------------------------------------------------- #


def cmd_validate_config(args: argparse.Namespace) -> int:
    path = Path(args.config)
    if not path.exists():
        return _die(EXIT_CONFIG, f"config not found: {path}", args.json)
    raw = json.loads(path.read_text(encoding="utf-8"))
    report = validate_config(raw)
    if args.json:
        print(json.dumps(report.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"config      : {path}")
        print(f"result      : {'PASS' if report.ok else 'FAIL'}")
        print(f"pool size N : {report.pool_size}")
        print(f"providers   : {report.providers}")
        for issue in report.issues:
            mark = "ERROR  " if issue.severity == "error" else "warning"
            print(f"  [{mark}] {issue.code}: {issue.message}")
    return EXIT_OK if report.ok else EXIT_CONFIG


def cmd_gen_pool(args: argparse.Namespace) -> int:
    from .support.poolgen import build_pool

    mix = None
    if args.mix:
        mix = {}
        for part in args.mix.split(","):
            name, _, count = part.partition("=")
            mix[name.strip()] = int(count)
    cfg = build_pool(args.n, mix=mix, project_id=args.project or "AGL-TEST-POOL")
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {out} with N={args.n}")
    return EXIT_OK


def cmd_plan_schedules(args: argparse.Namespace) -> int:
    built = _ctx(args, need_storage=False)
    if isinstance(built, int):
        return built
    ctx = built
    planner = PollPlanner(ctx.registry, None, None, run_id="PLAN", now_fn=None)  # type: ignore[arg-type]
    manifest = planner.schedule_manifest()
    if args.json:
        print(json.dumps(manifest, ensure_ascii=False, indent=2))
        return EXIT_OK
    print(f"project      : {manifest['project_id']}")
    print(f"global N     : {manifest['global_pool_size']}")
    print(f"verified     : {manifest['verified']}  (proposal only; no schedule created)")
    for provider, block in manifest["providers"].items():
        print(f"\n[{provider}] cadence={block['cadence_minutes']} "
              f"account={block['account_scope']}")
        for slot in block["slots"]:
            minute = slot["minute_in_hour"]
            when = f":{minute:02d}" if minute is not None else "native/unknown"
            print(f"  {slot['agent_id']:<18} offset={slot['offset_minutes']!s:<5} {when:<8} "
                  f"next={slot['planned_next_utc']}  {slot['source']}")
    print("\nregister these in each platform UI; then record the real schedule_id.")
    return EXIT_OK


def cmd_probe(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    ids = [args.agent] if args.agent else [a.agent_id for a in ctx.registry.enabled_agents()]
    probes = []
    for agent_id in ids:
        rec = ctx.registry.agents.get(agent_id)
        if rec is None:
            return _die(EXIT_CONFIG, f"unknown agent {agent_id}", args.json)
        adapter = build_adapter(rec, AdapterContext(
            storage=ctx.storage, ledger=ctx.ledger, runtime_root=ctx.registry.runtime_root,
            run_id=args.run_id or f"RUN-{uuid.uuid4().hex[:8]}",
            token_present=bool(args.token_env and os.environ.get(args.token_env)),
            write_probe=args.apply,
        ))
        probes.append(adapter.probe())

    if args.json:
        print(json.dumps([p.as_dict() for p in probes], ensure_ascii=False, indent=2))
        return EXIT_OK

    header = f"{'agent':<20}{'provider':<12}" + "".join(f"{op:<12}" for op in OPS)
    print(header)
    print("-" * len(header))
    for p in probes:
        row = f"{p.agent_id:<20}{p.provider_id:<12}" + "".join(
            f"{p.items[op].state.value:<12}" for op in OPS
        )
        print(row)
        for op in OPS:
            item = p.items[op]
            print(f"    {op:<9} {item.state.value:<11} [{item.method}] {item.detail}")
    print("\nwrite probe executed" if args.apply else "\nwrite probe skipped (dry-run): write/reread are not SUPPORTED until --apply runs a real write")
    return EXIT_OK


def cmd_poll(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    if not args.agent:
        return _die(EXIT_CONFIG, "--agent is required", args.json)
    run_id = args.run_id or f"RUN-{utc_now().replace(':', '').replace('-', '')}-{uuid.uuid4().hex[:6]}"
    planner = PollPlanner(
        ctx.registry, ctx.storage, ctx.ledger, run_id=run_id,
        runner_available=bool(args.worktree), token_present=bool(
            args.token_env and os.environ.get(args.token_env)
        ),
    )
    outcome = planner.poll_once(args.agent, allow_write=args.apply)
    if args.json:
        print(json.dumps(outcome.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"run_id     : {outcome.run_id}")
        print(f"agent      : {outcome.agent_id} ({outcome.provider_id})")
        print(f"status     : {outcome.status}")
        print(f"planned_at : {outcome.planned_at}")
        print(f"actual_at  : {outcome.actual_at}")
        print(f"task       : {outcome.task_id or '-'}")
        print(f"event      : {outcome.event_id or '-'}")
        print(f"controller : {outcome.controller_state}")
        for note in outcome.notes:
            print(f"note       : {note}")
    if outcome.status in ("CLAIM_PROPOSED", "CLAIM_PENDING_WRITE", "DRY_RUN",
                          "NO_ELIGIBLE_TASK", "RESUME_TASK"):
        return EXIT_OK
    return EXIT_BLOCKED


def cmd_submit_event(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    event = json.loads(Path(args.event).read_text(encoding="utf-8"))
    try:
        event = normalize_event(event)
    except AglError as exc:
        return _die(EXIT_CONFIG, f"{exc.code.value}: {exc.message}", args.json, exc.to_dict())
    targets = args.agent.split(",") if args.agent else list(event["target_agents"])
    body = canonical_json_bytes(event)
    if not args.apply:
        print(f"dry-run: event {event['event_id']} sha256={event['payload_sha256']}")
        print(f"         targets={targets} bytes={len(body)}")
        print("         re-run with --apply --repo --branch --project to write")
        return EXIT_OK
    results = []
    for target in targets:
        try:
            write = ctx.ledger.put_event(event, target)
            results.append({"target": target, "status": write.status, "path": write.path,
                            "commit_sha": write.receipt.commit_sha, "blob_sha": write.receipt.blob_sha})
        except AglError as exc:
            results.append({"target": target, "status": exc.code.value, "message": exc.message})
    if args.json:
        print(json.dumps({"event_id": event["event_id"], "results": results}, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['target']:<20}{item['status']:<20}{item.get('path', '')}")
    if any(r["status"] == ErrorCode.COLLISION.value for r in results):
        return EXIT_CONFLICT
    return EXIT_OK


def cmd_reconcile(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    if not args.event_id:
        return _die(EXIT_CONFIG, "--event-id is required", args.json)
    found = None
    for date in ctx.ledger.list_event_dates():
        for event_id in ctx.ledger.list_event_ids(date):
            if event_id == args.event_id:
                found = (date, event_id)
                break
        if found:
            break
    if not found:
        return _die(EXIT_BLOCKED, f"event not found: {args.event_id}", args.json)
    date, event_id = found
    manifest = ctx.ledger.read_manifest(date, event_id) or {}
    targets = manifest.get("target_agents", [])
    rows = []
    for target in targets:
        event = ctx.ledger.read_event(date, event_id, target)
        receipt = ctx.ledger.read_receipt(target, event_id)
        rows.append({
            "target": target,
            "event_present": event is not None,
            "event_sha256": sha256_hex(canonical_json_bytes(event)) if event else None,
            "ack_present": receipt is not None,
            "ack_result": (receipt or {}).get("result"),
            "ack_commit": (receipt or {}).get("commit_sha"),
        })
    payload = {"date": date, "manifest": manifest, "targets": rows}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"event      : {event_id}  date={date}")
        print(f"producer   : {manifest.get('producer')}  task={manifest.get('task_id')}")
        print(f"payload    : {manifest.get('payload_sha256')}")
        for row in rows:
            ack = "ACK" if row["ack_present"] else "no-ack"
            print(f"  {row['target']:<20} delivered={row['event_present']} {ack}"
                  f" {row['ack_result'] or ''}")
    missing = [r for r in rows if not r["event_present"]]
    return EXIT_BLOCKED if missing else EXIT_OK


def cmd_rebuild_board(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    text = build_board(ctx.registry, ctx.ledger, generated_at=None if args.deterministic else utc_now())
    path = f"{ctx.registry.runtime_root}/08_projections/BOARD.md"
    if not args.apply:
        print(text)
        print(f"\n(dry-run) would CAS-publish to {path}")
        return EXIT_OK
    current = ctx.storage.read_file(path)
    try:
        receipt = ctx.storage.cas_publish_projection(
            path, text.encode("utf-8"), current.blob_sha if current.exists else None,
            message=f"board projection ({ctx.registry.project_id})",
        )
    except AglError as exc:
        return _die(EXIT_CONFLICT, f"{exc.code.value}: {exc.message}", args.json, exc.to_dict())
    print(f"published {path} commit={receipt.commit_sha} sha256={receipt.content_sha256}")
    return EXIT_OK


def cmd_audit(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    problems: list[str] = []
    events = 0
    receipts = 0
    for date in ctx.ledger.list_event_dates():
        for event_id in ctx.ledger.list_event_ids(date):
            events += 1
            manifest = ctx.ledger.read_manifest(date, event_id)
            if manifest is None:
                problems.append(f"{date}/{event_id}: missing manifest")
                continue
            for target in manifest.get("target_agents", []):
                event = ctx.ledger.read_event(date, event_id, target)
                if event is None:
                    problems.append(f"{date}/{event_id}: missing delivery for {target}")
                    continue
                from .storage.ledger import event_digest

                if event_digest(event) != manifest.get("payload_sha256"):
                    problems.append(f"{date}/{event_id}/{target}: payload digest mismatch")
                if ctx.ledger.read_receipt(target, event_id):
                    receipts += 1
    for rec in ctx.registry.agents.values():
        cursor = ctx.ledger.get_cursor(rec.agent_id)
        if cursor.get("cursor") is not None and not str(cursor["cursor"])[:4].isdigit():
            problems.append(f"cursor for {rec.agent_id} is not ISO-like: {cursor['cursor']}")
    payload = {"events": events, "receipts": receipts, "problems": problems}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(f"events     : {events}")
        print(f"receipts   : {receipts}")
        print(f"problems   : {len(problems)}")
        for p in problems:
            print(f"  - {p}")
    return EXIT_OK if not problems else EXIT_BLOCKED


def cmd_run_sample_test(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    command = args.command.split() if args.command else ["python3", "-m", "pytest", "-q"]
    bridge = ExecutorBridge(
        ctx.storage, ctx.ledger, runtime_root=ctx.registry.runtime_root,
        agent_id=args.agent or ctx.registry.enabled_agents()[0].agent_id,
        run_id=args.run_id or f"RUN-TEST-{uuid.uuid4().hex[:8]}",
        worktree=args.worktree,
    )
    availability = bridge.availability()
    if not args.apply:
        print(f"runner     : {availability['runner_id']} available={availability['available']}")
        print(f"command    : {' '.join(command)}")
        print("dry-run: pass --apply to execute and persist TEST_RESULT")
        return EXIT_OK
    if not availability["available"]:
        print(f"BLOCKED_EXECUTOR: {availability['detail']}")
        return EXIT_BLOCKED
    request, _ = bridge.submit_request(
        task_id=args.task or "TASK-ADHOC", command=command, commit_sha=args.commit,
        timeout_s=args.timeout,
    )
    result = bridge.execute(request)
    if args.json:
        print(json.dumps(result.as_dict(), ensure_ascii=False, indent=2))
    else:
        print(f"request    : {request.request_id}")
        print(f"status     : {result.status}")
        print(f"exit_code  : {result.exit_code}")
        print(f"commit     : {result.commit_sha_tested}")
        print(f"stdout     : {result.stdout_path} sha256={result.stdout_sha256}")
        print(f"stderr     : {result.stderr_path} sha256={result.stderr_sha256}")
        print(f"env        : {result.environment_id}")
        print(f"acceptance : {result.business_acceptance} (requires M04 Controller)")
        for note in result.notes:
            print(f"note       : {note}")
    return _test_exit(result.status)


def cmd_verify_roundtrip(args: argparse.Namespace) -> int:
    built = _ctx(args)
    if isinstance(built, int):
        return built
    ctx = built
    run_id = args.run_id or f"RUN-RT-{uuid.uuid4().hex[:8]}"
    path = f"{ctx.registry.runtime_root}/_probe/ROUNDTRIP_{run_id}.json"
    body = canonical_json_bytes({
        "run_id": run_id, "agent": "WORKBUDDY_ADAPTERS_R01", "at": utc_now(),
        "purpose": "GitHub roundtrip evidence",
    })
    if not args.apply:
        print(f"dry-run: would write {path} ({len(body)} bytes, sha256={sha256_hex(body)})")
        return EXIT_OK
    try:
        ref = ctx.storage.read_ref()
        receipt = ctx.storage.write_immutable(
            path, body, idempotency_key=f"roundtrip:{run_id}", message=f"roundtrip probe {run_id}"
        )
        rb = ctx.storage.readback(receipt)
    except AglError as exc:
        payload = {"ok": False, "code": exc.code.value, "message": exc.message, **exc.detail}
        if args.json:
            print(json.dumps(payload, ensure_ascii=False, indent=2))
        else:
            print(f"{exc.code.value}: {exc.message}")
        return EXIT_BLOCKED
    payload = {
        "ok": rb.matches,
        "repo": ref.repo,
        "ref": ref.ref,
        "ref_head_at_start": ref.commit_sha,
        "path": path,
        "commit_sha": receipt.commit_sha,
        "blob_sha": receipt.blob_sha,
        "content_sha256": receipt.content_sha256,
        "readback_sha256": rb.readback_sha256,
        "readback_blob_sha": rb.readback_blob_sha,
        "matches": rb.matches,
        "transport": rb.receipt.transport,
        "times": {"written_at": receipt.observed_at, "read_at": rb.verified_at},
        "run_id": run_id,
    }
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        for key in ("repo", "ref", "ref_head_at_start", "path", "commit_sha", "blob_sha",
                    "content_sha256", "readback_sha256", "matches", "transport"):
            print(f"{key:<20}: {payload[key]}")
    return EXIT_OK if rb.matches else EXIT_BLOCKED


def cmd_offsets(args: argparse.Namespace) -> int:
    offsets = compute_offsets(args.k, args.cadence)
    print(json.dumps({"k": args.k, "cadence": args.cadence, "offsets": offsets}))
    return EXIT_OK


def cmd_version(args: argparse.Namespace) -> int:
    print(json.dumps({"version": __version__, "python": sys.version.split()[0]}))
    return EXIT_OK


# --------------------------------------------------------------------------- #
# board projection
# --------------------------------------------------------------------------- #


def build_board(registry: RegistryView, ledger: EventLedger, generated_at: str | None = None) -> str:
    """Deterministic projection: same events -> same bytes (given same timestamp)."""
    events = list(ledger.iter_events())
    events.sort(key=lambda pair: (pair[1].get("created_at", ""), pair[0]))
    digest = sha256_hex("\n".join(f"{key}:{m.get('payload_sha256')}" for key, m in events).encode())
    lines = [
        "# BOARD (adapter projection)",
        "",
        f"project_id: {registry.project_id}",
        f"repo: {registry.repo}",
        f"ref: {registry.ref}",
        f"events: {len(events)}",
        f"events_digest: {digest}",
    ]
    if generated_at:
        lines.append(f"generated_at: {generated_at}")
    lines += [
        "",
        "> This file is a deterministic projection over immutable events. The",
        "> authoritative board is produced by the Controller (M09); this copy is",
        "> for audit and must not be used to grant leases.",
        "",
        "## Agents",
        "",
        "| agent | provider | state | capabilities |",
        "| --- | --- | --- | --- |",
    ]
    for rec in sorted(registry.agents.values(), key=lambda r: r.agent_id):
        lines.append(f"| {rec.agent_id} | {rec.provider_id} | {rec.state} | {','.join(rec.capabilities)} |")
    lines += ["", "## Events", "", "| date/event | kind | task | producer | targets |", "| --- | --- | --- | --- | --- |"]
    for key, manifest in events:
        lines.append(
            f"| {key} | {manifest.get('kind')} | {manifest.get('task_id')} | "
            f"{manifest.get('producer')} | {','.join(manifest.get('target_agents', []))} |"
        )
    lines.append("")
    return "\n".join(lines)


def _preferred_executor(registry: RegistryView) -> str:
    """Runner identity defaults to a write-capable provider, never ChatGPT."""
    for rec in registry.enabled_agents():
        if rec.provider_id == "workbuddy":
            return rec.agent_id
    for rec in registry.enabled_agents():
        if rec.provider_id not in ("chatgpt",):
            return rec.agent_id
    raise AglError(ErrorCode.BLOCKED_PROVIDER, "no write-capable agent in pool for execution")


def _test_exit(status: str) -> int:
    if status == PASS:
        return EXIT_OK
    if status == FAIL:
        return EXIT_TEST_FAILED
    if status == STALE_TEST:
        return EXIT_STALE
    if status in (BLOCKED_EXECUTOR, TIMEOUT):
        return EXIT_BLOCKED
    return EXIT_INTERNAL


# --------------------------------------------------------------------------- #
# parser
# --------------------------------------------------------------------------- #


def _common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--config", default=DEFAULT_CONFIG)
    parser.add_argument("--repo", default=None, help="owner/name (required with --apply)")
    parser.add_argument("--branch", "--ref", dest="branch", default=None)
    parser.add_argument("--project", default=None)
    parser.add_argument("--transport", choices=("auto", "api", "local"), default="auto")
    parser.add_argument("--local-remote", default=None, help="path to a bare repo for transport=local")
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--worktree", default=None)
    parser.add_argument("--apply", action="store_true", help="perform writes (default: dry-run)")
    parser.add_argument("--json", action="store_true")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="agl", description="Agensh-Lite V4.2 adapter CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("validate-config", help="preflight a pool config")
    _common(p)
    p.set_defaults(func=cmd_validate_config)

    p = sub.add_parser("gen-pool", help="generate a valid N-agent config")
    p.add_argument("--n", type=int, required=True)
    p.add_argument("--mix", default=None, help="e.g. chatgpt=3,workbuddy=2,codex=1")
    p.add_argument("--out", required=True)
    p.add_argument("--project", default=None)
    p.set_defaults(func=cmd_gen_pool)

    p = sub.add_parser("plan-schedules", help="per-provider cadence and offsets")
    _common(p)
    p.set_defaults(func=cmd_plan_schedules)

    p = sub.add_parser("probe", help="capability probe")
    _common(p)
    p.add_argument("--agent", default=None)
    p.set_defaults(func=cmd_probe)

    p = sub.add_parser("poll", help="one wake-up cycle")
    _common(p)
    p.add_argument("--agent", required=True)
    p.set_defaults(func=cmd_poll)

    p = sub.add_parser("submit-event", help="write an immutable UEM event")
    _common(p)
    p.add_argument("--event", required=True, help="path to event JSON")
    p.add_argument("--agent", default=None, help="comma separated targets")
    p.set_defaults(func=cmd_submit_event)

    p = sub.add_parser("reconcile", help="inspect delivery/ACK state of an event")
    _common(p)
    p.add_argument("--event-id", required=True)
    p.set_defaults(func=cmd_reconcile)

    p = sub.add_parser("rebuild-board", help="deterministic projection")
    _common(p)
    p.add_argument("--deterministic", action="store_true", help="omit wall-clock line")
    p.set_defaults(func=cmd_rebuild_board)

    p = sub.add_parser("audit", help="integrity checks")
    _common(p)
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("run-sample-test", help="execute a TEST_REQUEST")
    _common(p)
    p.add_argument("--task", default=None)
    p.add_argument("--commit", required=True)
    p.add_argument("--command", default=None)
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--agent", default=None)
    p.set_defaults(func=cmd_run_sample_test)

    p = sub.add_parser("verify-roundtrip", help="write + independent readback")
    _common(p)
    p.set_defaults(func=cmd_verify_roundtrip)

    p = sub.add_parser("offsets", help="compute offset table for K slots")
    p.add_argument("--k", type=int, required=True)
    p.add_argument("--cadence", type=int, default=60)
    p.set_defaults(func=cmd_offsets)

    p = sub.add_parser("version")
    p.set_defaults(func=cmd_version)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except AglError as exc:
        return _die(EXIT_BLOCKED, f"{exc.code.value}: {exc.message}", getattr(args, "json", False), exc.to_dict())
    except KeyboardInterrupt:
        return EXIT_INTERNAL
    except Exception as exc:  # pragma: no cover - defensive
        return _die(EXIT_INTERNAL, f"internal error: {type(exc).__name__}: {exc}", getattr(args, "json", False))


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
