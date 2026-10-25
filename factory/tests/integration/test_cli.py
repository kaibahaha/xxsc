"""CLI behaviour: dry-run defaults, apply guards, exit codes, determinism."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agl.cli import (
    EXIT_BLOCKED,
    EXIT_CONFIG,
    EXIT_CONFLICT,
    EXIT_OK,
    EXIT_STALE,
    EXIT_TEST_FAILED,
    build_board,
    main,
)
from agl.adapters.registry_view import RegistryView
from agl.storage.ledger import EventLedger

from helpers import make_event

ROOT = "factory/projects/AGL-SHADOW-001"


def test_validate_config_ok(pool_config, capsys):
    assert main(["validate-config", "--config", str(pool_config)]) == EXIT_OK
    out = capsys.readouterr().out
    assert "PASS" in out and "pool size N : 6" in out


def test_validate_config_rejects_duplicate_ids(tmp_path, capsys):
    from agl.support.poolgen import build_pool

    cfg = build_pool(4, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["agents"].append(dict(cfg["agents"][0]))
    cfg["pool"]["active_agent_ids"] = [a["agent_id"] for a in cfg["agents"]]
    path = tmp_path / "bad.json"
    path.write_text(json.dumps(cfg), encoding="utf-8")
    assert main(["validate-config", "--config", str(path), "--json"]) == EXIT_CONFIG
    payload = json.loads(capsys.readouterr().out)
    assert any(e["code"] == "DUPLICATE_AGENT_ID" for e in payload["errors"])


def test_gen_pool_writes_valid_config(tmp_path, capsys):
    out = tmp_path / "n20.json"
    assert main(["gen-pool", "--n", "20", "--out", str(out),
                 "--mix", "chatgpt=8,workbuddy=8,codex=4"]) == EXIT_OK
    cfg = json.loads(out.read_text())
    assert len(cfg["agents"]) == 20
    assert main(["validate-config", "--config", str(out)]) == EXIT_OK


def test_plan_schedules_json_shows_per_provider_offsets(cli_argv, capsys):
    assert main(cli_argv("plan-schedules", "--json")) == EXIT_OK
    manifest = json.loads(capsys.readouterr().out)
    chat = manifest["providers"]["chatgpt"]["slots"]
    assert [s["minute_in_hour"] for s in chat] == [0, 20, 40]
    wb = manifest["providers"]["workbuddy"]["slots"]
    assert all(s["cadence_minutes"] == 20 for s in wb)
    assert manifest["verified"] is False


def test_offsets_command(capsys):
    assert main(["offsets", "--k", "5"]) == EXIT_OK
    assert json.loads(capsys.readouterr().out)["offsets"] == [0, 12, 24, 36, 48]


def test_probe_dry_run_reports_no_write(cli_argv, capsys):
    assert main(cli_argv("probe", "--agent", "WORKBUDDY_01")) == EXIT_OK
    out = capsys.readouterr().out
    assert "SUPPORTED" in out and "UNSUPPORTED" in out
    assert "write probe skipped" in out


def test_probe_apply_performs_real_write_and_readback(cli_argv, capsys):
    assert main(cli_argv("probe", "--agent", "WORKBUDDY_01", "--json", apply=True)) == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    items = payload[0]["items"]
    assert items["write"]["state"] == "SUPPORTED"
    assert items["reread"]["state"] == "SUPPORTED"


def test_submit_event_dry_run_writes_nothing(cli_argv, tmp_path, capsys, bare_remote):
    event_file = tmp_path / "ev.json"
    event_file.write_text(json.dumps(make_event()), encoding="utf-8")
    before = subprocess.run(["git", "rev-parse", "exp/test"], cwd=str(bare_remote),
                            capture_output=True, text=True).stdout.strip()
    assert main(cli_argv("submit-event", "--event", str(event_file))) == EXIT_OK
    after = subprocess.run(["git", "rev-parse", "exp/test"], cwd=str(bare_remote),
                           capture_output=True, text=True).stdout.strip()
    assert before == after
    assert "dry-run" in capsys.readouterr().out


def test_submit_event_apply_then_reconcile(cli_argv, tmp_path, capsys):
    event_file = tmp_path / "ev.json"
    event_file.write_text(json.dumps(make_event()), encoding="utf-8")
    assert main(cli_argv("submit-event", "--event", str(event_file), apply=True)) == EXIT_OK
    capsys.readouterr()

    assert main(cli_argv("reconcile", "--event-id", "EV-0001", "--json")) == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["manifest"]["payload_sha256"]
    assert payload["targets"][0]["event_present"] is True
    assert payload["targets"][0]["ack_present"] is False


def test_submit_event_collision_returns_conflict(cli_argv, tmp_path, capsys):
    path = tmp_path / "ev.json"
    path.write_text(json.dumps(make_event(summary="first")), encoding="utf-8")
    assert main(cli_argv("submit-event", "--event", str(path), apply=True)) == EXIT_OK
    path.write_text(json.dumps(make_event(summary="second")), encoding="utf-8")
    assert main(cli_argv("submit-event", "--event", str(path), apply=True)) == EXIT_CONFLICT
    assert "COLLISION" in capsys.readouterr().out.upper()


def test_apply_requires_explicit_repo_branch_project(pool_config, bare_remote, capsys):
    rc = main(["poll", "--agent", "WORKBUDDY_01", "--config", str(pool_config),
               "--transport", "local", "--local-remote", str(bare_remote), "--apply"])
    assert rc == EXIT_CONFIG
    assert "--apply requires explicit" in capsys.readouterr().err


def test_rebuild_board_is_deterministic(pool_config, storage, ledger):
    from agl.storage.ledger import normalize_event

    ledger.put_event(normalize_event(make_event()), "CHATGPT_01")
    registry = RegistryView.load(pool_config)
    first = build_board(registry, ledger, generated_at=None)
    second = build_board(registry, ledger, generated_at=None)
    assert first == second
    assert "events_digest" in first
    assert "authoritative board" in first


def test_audit_reports_integrity(cli_argv, bare_remote, tmp_path, capsys):
    event_file = tmp_path / "ev.json"
    event_file.write_text(json.dumps(make_event()), encoding="utf-8")
    main(cli_argv("submit-event", "--event", str(event_file), apply=True))
    capsys.readouterr()
    assert main(cli_argv("audit", "--json")) == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["events"] == 1 and payload["problems"] == []


@pytest.fixture
def worktree(tmp_path: Path):
    path = tmp_path / "wt"
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t.t"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"], check=True)
    (path / "a.txt").write_text("a\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "init"], check=True)
    sha = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return path, sha


def test_run_sample_test_pass(cli_argv, worktree, capsys):
    path, sha = worktree
    argv = cli_argv("run-sample-test", "--task", "TASK-1", "--commit", sha,
                    "--worktree", str(path), "--command", f"{sys.executable} -c print(42)", apply=True)
    assert main(argv) == EXIT_OK
    out = capsys.readouterr().out
    assert "status     : PASS" in out


def test_run_sample_test_failure_exit_code(cli_argv, worktree):
    path, sha = worktree
    argv = cli_argv("run-sample-test", "--task", "TASK-1", "--commit", sha,
                    "--worktree", str(path), "--command", f"{sys.executable} -c import sys;sys.exit(2)",
                    apply=True)
    assert main(argv) == EXIT_TEST_FAILED


def test_run_sample_test_stale_sha(cli_argv, worktree):
    path, _ = worktree
    argv = cli_argv("run-sample-test", "--task", "TASK-1", "--commit", "0" * 40,
                    "--worktree", str(path), "--command", "true", apply=True)
    assert main(argv) == EXIT_STALE


def test_run_sample_test_without_worktree_is_blocked(cli_argv, capsys):
    argv = cli_argv("run-sample-test", "--task", "TASK-1", "--commit", "a" * 40, apply=True)
    assert main(argv) == EXIT_BLOCKED
    assert "BLOCKED_EXECUTOR" in capsys.readouterr().out


def test_verify_roundtrip_apply(cli_argv, capsys):
    assert main(cli_argv("verify-roundtrip", "--json", apply=True)) == EXIT_OK
    payload = json.loads(capsys.readouterr().out)
    assert payload["matches"] is True
    assert len(payload["commit_sha"]) == 40
    assert payload["content_sha256"] == payload["readback_sha256"]


def test_verify_roundtrip_is_idempotent_for_same_run_id(cli_argv, capsys, bare_remote):
    """Same --run-id twice: second call replays, no new commit."""
    first = main(cli_argv("verify-roundtrip", "--run-id", "RUN-RT-IDEM", "--json", apply=True))
    assert first == EXIT_OK
    out1 = json.loads(capsys.readouterr().out)
    second = main(cli_argv("verify-roundtrip", "--run-id", "RUN-RT-IDEM", "--json", apply=True))
    assert second == EXIT_OK
    out2 = json.loads(capsys.readouterr().out)
    assert out1["commit_sha"] == out2["commit_sha"]


def test_verify_roundtrip_dry_run(cli_argv, capsys):
    assert main(cli_argv("verify-roundtrip")) == EXIT_OK
    assert "dry-run" in capsys.readouterr().out


def test_poll_cli_applies_claim(cli_argv, capsys):
    assert main(cli_argv("poll", "--agent", "WORKBUDDY_01", "--run-id", "RUN-CLI-1", apply=True)) == EXIT_OK
    out = capsys.readouterr().out
    assert "CLAIM_PROPOSED" in out
    assert "CONTROLLER_UNAVAILABLE" in out


def test_real_subprocess_entrypoint(pool_config, capsys):
    """One test through a real process to capture a genuine exit code."""
    proc = subprocess.run(
        [sys.executable, "-m", "agl.cli", "validate-config", "--config", str(pool_config)],
        capture_output=True, text=True,
        env={"PYTHONPATH": str(Path(__file__).resolve().parents[2]), "PATH": "/usr/bin:/bin:/usr/local/bin"},
    )
    assert proc.returncode == 0, proc.stderr
    assert "PASS" in proc.stdout
