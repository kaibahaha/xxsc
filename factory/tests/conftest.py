"""Shared fixtures.

Tests use **real git plumbing against a local bare repository** (marker
``real_git``), so commit/blob SHAs, CAS ref updates and independent readback are
genuine git semantics -- only the network hop is absent. Tests that simulate a
transport error or a provider are marked ``mock`` and never count as evidence of
cross-platform connectivity.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

FACTORY = Path(__file__).resolve().parents[1]
TESTS = Path(__file__).resolve().parent
REPO = FACTORY.parent
sys.path.insert(0, str(FACTORY))
sys.path.insert(0, str(TESTS))

from agl.storage.github import GitHubStorage  # noqa: E402
from agl.storage.ledger import EventLedger  # noqa: E402
from agl.storage.transports import LocalGitTransport  # noqa: E402

RUNTIME_ROOT = "factory/projects/AGL-SHADOW-001"


def git(cwd: Path, *args: str) -> str:
    proc = subprocess.run(["git", *args], cwd=str(cwd), capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {proc.stderr}")
    return proc.stdout.strip()


@pytest.fixture(scope="session")
def repo_root() -> Path:
    return REPO


@pytest.fixture
def bare_remote(tmp_path: Path) -> Path:
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    seed = tmp_path / "seed"
    subprocess.run(["git", "init", "-q", str(seed)], check=True)
    git(seed, "config", "user.email", "seed@agl.local")
    git(seed, "config", "user.name", "seed")

    (seed / "frameworks/agensh-lite-v4.2").mkdir(parents=True)
    (seed / "frameworks/agensh-lite-v4.2/README.md").write_text("# frozen baseline\n", encoding="utf-8")
    root = seed / RUNTIME_ROOT
    (root / "08_projections").mkdir(parents=True)
    (root / "08_projections/BOARD.md").write_text("# BOARD\n\ninitial\n", encoding="utf-8")
    (root / "01_tasks/TASK-1").mkdir(parents=True)
    (root / "01_tasks/TASK-1/TASK.md").write_text(
        "# Wire the storage adapter\nSTATUS: READY\nCAPABILITIES: code_execution, git_write\n"
        "PRIORITY: P1\nSPEC_HASH: " + "a" * 64 + "\n",
        encoding="utf-8",
    )
    (root / "01_tasks/TASK-2").mkdir(parents=True)
    (root / "01_tasks/TASK-2/TASK.md").write_text(
        "# Downstream task\nSTATUS: READY\nDEPENDS_ON: TASK-1\nCAPABILITIES: code_execution\n",
        encoding="utf-8",
    )
    (root / "01_tasks/TASK-3").mkdir(parents=True)
    (root / "01_tasks/TASK-3/TASK.md").write_text(
        "# Review the interface handoff\nSTATUS: READY\nCAPABILITIES: review\nPRIORITY: P2\n",
        encoding="utf-8",
    )
    git(seed, "add", "-A")
    git(seed, "commit", "-qm", "seed baseline")
    git(seed, "branch", "-M", "exp/test")
    git(seed, "remote", "add", "origin", str(bare))
    git(seed, "push", "-q", "origin", "exp/test")
    return bare


@pytest.fixture
def storage(bare_remote: Path) -> GitHubStorage:
    return GitHubStorage(
        LocalGitTransport(bare_remote),
        "kaibahaha/xxsc",
        "exp/test",
        allowed_prefixes=("factory",),
    )


@pytest.fixture
def ledger(storage: GitHubStorage) -> EventLedger:
    return EventLedger(storage, RUNTIME_ROOT)


@pytest.fixture
def pool_config(tmp_path: Path) -> Path:
    from agl.support.poolgen import build_pool

    cfg = build_pool(
        6,
        mix={"chatgpt": 3, "workbuddy": 2, "codex": 1},
        admission="ADMITTED_ACTIVE",
        project_id="AGL-SHADOW-001",
        ref="exp/test",
        runtime_root=RUNTIME_ROOT,
    )
    path = tmp_path / "pool.json"
    path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
    return path


@pytest.fixture
def cli_argv(pool_config: Path, bare_remote: Path):
    def build(*args: str, apply: bool = False) -> list[str]:
        argv = [*args, "--config", str(pool_config), "--transport", "local",
                "--local-remote", str(bare_remote)]
        if apply:
            argv += ["--apply", "--repo", "kaibahaha/xxsc", "--branch", "exp/test",
                     "--project", "AGL-SHADOW-001"]
        return argv

    return build
