"""M08 executor bridge: real subprocess execution, exit codes, stale SHA, blocked."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from agl.errors import AglError, ErrorCode
from agl.execution import (
    BLOCKED_EXECUTOR,
    ERROR,
    FAIL,
    PASS,
    STALE_TEST,
    TIMEOUT,
    BlockedRunner,
    ExecutorBridge,
    LocalSubprocessRunner,
)


@pytest.fixture
def worktree(tmp_path: Path) -> tuple[Path, str]:
    path = tmp_path / "wt"
    subprocess.run(["git", "init", "-q", str(path)], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.email", "t@t.t"], check=True)
    subprocess.run(["git", "-C", str(path), "config", "user.name", "t"], check=True)
    (path / "sample.py").write_text("print('hello from sample')\n", encoding="utf-8")
    subprocess.run(["git", "-C", str(path), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(path), "commit", "-qm", "init"], check=True)
    sha = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return path, sha


def _request(bridge, sha, command, timeout=30):
    request, _ = bridge.submit_request(task_id="TASK-1", command=command, commit_sha=sha,
                                       timeout_s=timeout)
    return request


def test_pass_has_real_exit_code_and_log(worktree, storage, ledger, tmp_path):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-1", worktree=path)
    request = _request(bridge, sha, [sys.executable, "-c", "print('ok-line')"])
    result = bridge.execute(request)
    assert result.status == PASS
    assert result.exit_code == 0
    assert result.commit_sha_tested == sha
    assert Path(result.stdout_path).read_text(encoding="utf-8").strip() == "ok-line"
    assert result.business_acceptance == "PENDING_CORE"


def test_failure_propagates_exit_code(worktree, storage, ledger):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-2", worktree=path)
    request = _request(bridge, sha, [sys.executable, "-c", "import sys; sys.exit(3)"])
    result = bridge.execute(request)
    assert result.status == FAIL
    assert result.exit_code == 3


def test_stale_commit_is_refused(worktree, storage, ledger):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-3", worktree=path)
    request = _request(bridge, "0" * 40, [sys.executable, "-c", "print('should not run')"])
    result = bridge.execute(request)
    assert result.status == STALE_TEST
    assert result.exit_code is None
    assert result.error_code == ErrorCode.STALE_TEST.value
    assert result.stdout_path is None


def test_timeout_preserves_partial_logs(worktree, storage, ledger):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-4", worktree=path)
    request = _request(bridge, sha, [sys.executable, "-c", "import time; time.sleep(3)"], timeout=1)
    result = bridge.execute(request)
    assert result.status == TIMEOUT
    assert "timed out" in " ".join(result.notes)


def test_missing_command_is_error(worktree, storage, ledger):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-5", worktree=path)
    request = _request(bridge, sha, ["definitely-not-a-real-binary-xyz"])
    result = bridge.execute(request)
    assert result.status == ERROR


def test_no_runner_returns_blocked_executor(storage, ledger):
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-6", worktree=None)
    assert bridge.availability()["available"] is False
    request, _ = bridge.submit_request(task_id="TASK-1", command=["true"], commit_sha="a" * 40)
    result = bridge.execute(request)
    assert result.status == BLOCKED_EXECUTOR
    assert result.error_code == ErrorCode.BLOCKED_EXECUTOR.value
    assert result.exit_code is None


def test_blocked_result_is_persisted_without_fake_pass(storage, ledger):
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-7", worktree=None)
    request, _ = bridge.submit_request(task_id="TASK-1", command=["true"], commit_sha="b" * 40)
    bridge.execute(request)
    snap = storage.read_file(
        f"factory/projects/AGL-SHADOW-001/06_evidence/TASK-1/RUN-T-7/"
        f"TEST_RESULT_{request.request_id}.json"
    )
    assert snap.exists
    payload = json.loads(snap.text)
    assert payload["status"] == BLOCKED_EXECUTOR
    assert payload["business_acceptance"] == "PENDING_CORE"


def test_pass_cannot_be_promoted_without_core(storage, ledger, worktree):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-8", worktree=path)
    request = _request(bridge, sha, [sys.executable, "-c", "print(1)"])
    assert bridge.execute(request).status == PASS
    with pytest.raises(AglError) as exc:
        bridge.ensure_business_acceptance()
    assert exc.value.code is ErrorCode.CONTROLLER_UNAVAILABLE


def test_result_and_ack_are_written_to_git(storage, ledger, worktree):
    path, sha = worktree
    bridge = ExecutorBridge(storage, ledger, runtime_root="factory/projects/AGL-SHADOW-001",
                            agent_id="WORKBUDDY_01", run_id="RUN-T-9", worktree=path)
    request = _request(bridge, sha, [sys.executable, "-c", "print('persisted')"])
    result = bridge.execute(request)

    base = f"factory/projects/AGL-SHADOW-001/06_evidence/TASK-1/RUN-T-9"
    assert storage.read_file(f"{base}/TEST_REQUEST_{request.request_id}.json").exists
    assert storage.read_file(f"{base}/TEST_RESULT_{request.request_id}.json").exists
    stdout_snap = storage.read_file(f"{base}/stdout_{request.request_id}.log")
    assert stdout_snap.exists
    from agl.storage.github import sha256_hex
    assert sha256_hex(stdout_snap.content) == result.stdout_sha256

    ack = ledger.read_receipt("WORKBUDDY_01", f"TEST-{request.request_id}")
    assert ack is not None and ack["result"] == PASS


def test_blocked_runner_reports_unavailable():
    runner = BlockedRunner()
    assert runner.available()[0] is False


def test_local_runner_accepts_subdirectory(worktree):
    path, _ = worktree
    sub = path / "sub"
    sub.mkdir()
    ok, detail = LocalSubprocessRunner(sub).available()
    assert ok is True
    assert "toplevel" in detail


def test_local_runner_rejects_non_worktree(tmp_path):
    runner = LocalSubprocessRunner(tmp_path)
    ok, detail = runner.available()
    assert ok is False
    assert "not inside a git worktree" in detail
