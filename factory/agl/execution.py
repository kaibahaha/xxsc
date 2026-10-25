"""M08 -- Executor Bridge.

Protocol::

    TEST_REQUEST  (immutable JSON in 06_evidence/<task>/<run>/)
        -> Runner (real subprocess)
        -> stdout.log / stderr.log (raw bytes, hashed)
        -> TEST_RESULT (immutable JSON, binds commit_sha + log sha256 + exit_code)
        -> ACK (07_receipts/<agent>/TEST-<request_id>.json)

Hard rules encoded here:

* No runner -> ``BLOCKED_EXECUTOR``. Never a fabricated PASS.
* A result is only valid for the exact ``commit_sha`` that was executed; a
  worktree at another commit yields ``STALE_TEST``.
* ``PASS`` is a *test* verdict, not ``QA_GREEN``: promotion requires the
  Controller (Codex M04) to accept the evidence. This module reports
  ``business_acceptance = PENDING_CORE`` when the core is absent.
* Timeouts are reported as ``TIMEOUT`` with the partial logs preserved.
"""

from __future__ import annotations

import hashlib
import os
import platform
import shutil
import subprocess
import sys
import time
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Protocol

from .errors import AglError, ErrorCode, redact
from .storage.github import GitHubStorage, WriteReceipt, canonical_json_bytes, utc_now
from .storage.ledger import EventLedger

PASS = "PASS"
FAIL = "FAIL"
ERROR = "ERROR"
TIMEOUT = "TIMEOUT"
BLOCKED_EXECUTOR = "BLOCKED_EXECUTOR"
STALE_TEST = "STALE_TEST"


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


@dataclass(frozen=True)
class TestRequest:
    request_id: str
    task_id: str
    repo: str
    ref: str
    commit_sha: str
    spec_hash: str | None
    command: tuple[str, ...]
    timeout_s: int
    requested_by: str
    run_id: str
    created_at: str
    expected: str = "EXIT_0"

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "kind": "TEST_REQUEST",
            "request_id": self.request_id,
            "task_id": self.task_id,
            "repo": self.repo,
            "ref": self.ref,
            "commit_sha": self.commit_sha,
            "spec_hash": self.spec_hash,
            "command": list(self.command),
            "timeout_s": self.timeout_s,
            "expected": self.expected,
            "requested_by": self.requested_by,
            "run_id": self.run_id,
            "created_at": self.created_at,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "TestRequest":
        return cls(
            request_id=data["request_id"], task_id=data["task_id"], repo=data["repo"],
            ref=data["ref"], commit_sha=data["commit_sha"], spec_hash=data.get("spec_hash"),
            command=tuple(data["command"]), timeout_s=int(data.get("timeout_s", 300)),
            requested_by=data.get("requested_by", "unknown"), run_id=data.get("run_id", "RUN-?"),
            created_at=data.get("created_at", utc_now()), expected=data.get("expected", "EXIT_0"),
        )


@dataclass(frozen=True)
class TestResult:
    request_id: str
    task_id: str
    status: str
    exit_code: int | None
    started_at: str
    finished_at: str
    duration_ms: int
    environment_id: str
    commit_sha_tested: str | None
    runner_id: str
    stdout_sha256: str | None = None
    stderr_sha256: str | None = None
    stdout_path: str | None = None
    stderr_path: str | None = None
    error_code: str | None = None
    notes: list[str] = field(default_factory=list)
    business_acceptance: str = "PENDING_CORE"

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "kind": "TEST_RESULT",
            "request_id": self.request_id,
            "task_id": self.task_id,
            "status": self.status,
            "exit_code": self.exit_code,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "duration_ms": self.duration_ms,
            "environment_id": self.environment_id,
            "commit_sha_tested": self.commit_sha_tested,
            "runner_id": self.runner_id,
            "stdout_sha256": self.stdout_sha256,
            "stderr_sha256": self.stderr_sha256,
            "stdout_path": self.stdout_path,
            "stderr_path": self.stderr_path,
            "error_code": self.error_code,
            "notes": list(self.notes),
            "business_acceptance": self.business_acceptance,
        }


class Runner(Protocol):
    runner_id: str

    def available(self) -> tuple[bool, str]: ...

    def run(self, request: TestRequest, worktree: Path, evidence_dir: Path) -> TestResult: ...


class BlockedRunner:
    """No execution environment: every request is explicitly BLOCKED_EXECUTOR."""

    runner_id = "blocked"

    def available(self) -> tuple[bool, str]:
        return False, "no runner configured"

    def run(self, request: TestRequest, worktree: Path, evidence_dir: Path) -> TestResult:
        now = utc_now()
        return TestResult(
            request.request_id, request.task_id, BLOCKED_EXECUTOR, None, now, now, 0,
            environment_id="none", commit_sha_tested=None, runner_id=self.runner_id,
            error_code=ErrorCode.BLOCKED_EXECUTOR.value,
            notes=["cloud/local executor unavailable; nothing was executed"],
        )


class LocalSubprocessRunner:
    """Real execution in a real worktree; captures raw stdout/stderr bytes."""

    runner_id = "local-subprocess"

    def __init__(self, worktree: str | Path, env: dict[str, str] | None = None) -> None:
        self.worktree = Path(worktree).resolve()
        self.env_extra = env or {}

    def available(self) -> tuple[bool, str]:
        if not (self.worktree / ".git").exists() and not (self.worktree / "HEAD").exists():
            return False, f"not a git worktree: {self.worktree}"
        if shutil.which("git") is None:
            return False, "git not on PATH"
        return True, f"worktree={self.worktree}"

    def _head(self) -> str | None:
        try:
            proc = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=self.worktree, capture_output=True, timeout=20
            )
            return proc.stdout.decode().strip() if proc.returncode == 0 else None
        except Exception:
            return None

    def run(self, request: TestRequest, worktree: Path, evidence_dir: Path) -> TestResult:
        started_at = utc_now()
        t0 = time.monotonic()
        env = dict(os.environ)
        env.update({"PYTHONUNBUFFERED": "1", "PYTHONDONTWRITEBYTECODE": "1"})
        env.update(self.env_extra)

        head = self._head()
        if head != request.commit_sha:
            finished = utc_now()
            return TestResult(
                request.request_id, request.task_id, STALE_TEST, None, started_at, finished,
                int((time.monotonic() - t0) * 1000),
                environment_id=self._env_id(), commit_sha_tested=head, runner_id=self.runner_id,
                error_code=ErrorCode.STALE_TEST.value,
                notes=[f"worktree HEAD {head} != requested {request.commit_sha}; test not run"],
            )

        stdout = b""
        stderr = b""
        exit_code: int | None = None
        status = ERROR
        notes: list[str] = []
        try:
            proc = subprocess.run(
                list(request.command), cwd=str(worktree), capture_output=True,
                timeout=request.timeout_s, env=env,
            )
            stdout, stderr = proc.stdout, proc.stderr
            exit_code = proc.returncode
            ok = exit_code == 0 if request.expected == "EXIT_0" else True
            status = PASS if ok else FAIL
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or b""
            stderr = (exc.stderr or b"") + f"\n[agl] timeout after {request.timeout_s}s".encode()
            exit_code = None
            status = TIMEOUT
            notes.append(f"timed out after {request.timeout_s}s")
        except FileNotFoundError as exc:
            stderr = redact(str(exc)).encode()
            exit_code = None
            status = ERROR
            notes.append("command not found")

        evidence_dir.mkdir(parents=True, exist_ok=True)
        stdout_file = evidence_dir / "stdout.log"
        stderr_file = evidence_dir / "stderr.log"
        stdout_file.write_bytes(stdout)
        stderr_file.write_bytes(stderr)

        return TestResult(
            request.request_id, request.task_id, status, exit_code, started_at, utc_now(),
            int((time.monotonic() - t0) * 1000), environment_id=self._env_id(),
            commit_sha_tested=head, runner_id=self.runner_id,
            stdout_sha256=_sha256(stdout), stderr_sha256=_sha256(stderr),
            stdout_path=str(stdout_file), stderr_path=str(stderr_file), notes=notes,
        )

    @staticmethod
    def _env_id() -> str:
        return f"{platform.system().lower()}-{platform.machine()}-py{sys.version_info.major}.{sys.version_info.minor}"


class ExecutorBridge:
    """Submits TEST_REQUEST, runs it, writes TEST_RESULT + raw logs, then ACKs."""

    def __init__(
        self,
        storage: GitHubStorage,
        ledger: EventLedger,
        *,
        runtime_root: str,
        agent_id: str,
        run_id: str,
        runner: Runner | None = None,
        worktree: str | Path | None = None,
    ) -> None:
        self.storage = storage
        self.ledger = ledger
        self.runtime_root = runtime_root.strip("/")
        self.agent_id = agent_id
        self.run_id = run_id
        self.worktree = Path(worktree).resolve() if worktree else None
        if runner is not None:
            self.runner = runner
        elif self.worktree is not None:
            self.runner = LocalSubprocessRunner(self.worktree)
        else:
            self.runner = BlockedRunner()

    def availability(self) -> dict[str, Any]:
        ok, detail = self.runner.available()
        return {"runner_id": self.runner.runner_id, "available": ok, "detail": detail}

    def submit_request(
        self,
        *,
        task_id: str,
        command: list[str] | tuple[str, ...],
        commit_sha: str,
        spec_hash: str | None = None,
        timeout_s: int = 300,
        expected: str = "EXIT_0",
    ) -> tuple[TestRequest, WriteReceipt | None]:
        request = TestRequest(
            request_id=f"TR-{uuid.uuid4().hex[:12]}",
            task_id=task_id, repo=self.storage.repo, ref=self.storage.ref,
            commit_sha=commit_sha, spec_hash=spec_hash, command=tuple(command),
            timeout_s=timeout_s, requested_by=self.agent_id, run_id=self.run_id,
            created_at=utc_now(), expected=expected,
        )
        receipt = None
        if self.worktree is not None:
            try:
                receipt = self.storage.write_immutable(
                    self._request_path(request), canonical_json_bytes(request.as_dict()),
                    idempotency_key=f"test-request:{request.request_id}",
                    message=f"TEST_REQUEST {request.request_id}",
                )
            except AglError:
                receipt = None
        return request, receipt

    def execute(self, request: TestRequest) -> TestResult:
        evidence_dir = self._local_evidence_dir(request)
        ok, detail = self.runner.available()
        if not ok:
            result = BlockedRunner().run(request, Path("."), evidence_dir)
            self._persist(request, result)
            return result

        worktree = self.worktree
        assert worktree is not None
        result = self.runner.run(request, worktree, evidence_dir)
        self._persist(request, result)
        return result

    # -- persistence --------------------------------------------------------#
    def _task_dir(self, request: TestRequest) -> str:
        return f"{self.runtime_root}/06_evidence/{request.task_id}/{self.run_id}"

    def _request_path(self, request: TestRequest) -> str:
        return f"{self._task_dir(request)}/TEST_REQUEST_{request.request_id}.json"

    def _local_evidence_dir(self, request: TestRequest) -> Path:
        base = self.worktree or Path.cwd()
        return base / self.runtime_root / "06_evidence" / request.task_id / self.run_id

    def _persist(self, request: TestRequest, result: TestResult) -> None:
        """Write logs + TEST_RESULT + ACK into git; ignore failures to stay usable offline."""
        base = self._task_dir(request)
        try:
            if result.stdout_path and Path(result.stdout_path).exists():
                self.storage.write_immutable(
                    f"{base}/stdout_{request.request_id}.log",
                    Path(result.stdout_path).read_bytes(),
                    idempotency_key=f"stdout:{request.request_id}",
                    message=f"stdout {request.request_id}",
                )
                result = _with(result, stdout_path=f"{base}/stdout_{request.request_id}.log")
            if result.stderr_path and Path(result.stderr_path).exists():
                self.storage.write_immutable(
                    f"{base}/stderr_{request.request_id}.log",
                    Path(result.stderr_path).read_bytes(),
                    idempotency_key=f"stderr:{request.request_id}",
                    message=f"stderr {request.request_id}",
                )
                result = _with(result, stderr_path=f"{base}/stderr_{request.request_id}.log")
            result_path = f"{base}/TEST_RESULT_{request.request_id}.json"
            receipt = self.storage.write_immutable(
                result_path, canonical_json_bytes(result.as_dict()),
                idempotency_key=f"test-result:{request.request_id}",
                message=f"TEST_RESULT {request.request_id} {result.status}",
            )
            self.ledger.put_receipt(
                self.agent_id, f"TEST-{request.request_id}",
                result=result.status, evidence_ref=f"{result_path}@{receipt.commit_sha}",
                readback_hash=receipt.content_sha256, commit_sha=receipt.commit_sha,
                writer=self.agent_id,
            )
        except AglError:
            pass

    def ensure_business_acceptance(self) -> None:
        """Refuse to call a passing test 'accepted' without the core Controller."""
        from .poll import core_available

        if not core_available("controller"):
            raise AglError(
                ErrorCode.CONTROLLER_UNAVAILABLE,
                "TEST PASS cannot be promoted to QA_GREEN/business acceptance: "
                "M04 Controller not present on this branch",
            )


def _with(result: TestResult, **changes: Any) -> TestResult:
    data = result.as_dict()
    data.pop("schema_version", None)
    data.pop("kind", None)
    data.update(changes)
    return TestResult(**data)


def load_request(path: str | Path) -> TestRequest:
    import json

    return TestRequest.from_dict(json.loads(Path(path).read_text(encoding="utf-8")))


def default_environment_id() -> str:
    return f"{platform.system().lower()}-{platform.machine()}-py{sys.version_info.major}.{sys.version_info.minor}"
