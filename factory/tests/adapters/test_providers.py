"""Provider capability probes.

These run against a **local bare repository**, so ``method`` is ``LOCAL_GIT``.
They prove the adapter logic (what is allowed to be claimed per platform) but
are NOT evidence of a live cross-platform connection; such evidence requires a
real credential and is marked BLOCKED in the delivery report.
"""

from __future__ import annotations

import pytest

from agl.adapters.github_mailbox import AdapterContext
from agl.adapters.providers import build_adapter, capability_matrix
from agl.adapters.registry_view import RegistryView
from agl.adapters.types import OPS, CapState
from agl.support.poolgen import build_pool


@pytest.fixture
def registry(tmp_path):
    cfg = build_pool(3, mix={"chatgpt": 1, "workbuddy": 1, "codex": 1},
                     admission="ADMITTED_ACTIVE", ref="exp/test")
    return RegistryView.from_config(cfg)


def _ctx(storage, ledger, runner=False, write_probe=True):
    return AdapterContext(storage=storage, ledger=ledger,
                          runtime_root="factory/projects/AGL-SHADOW-001",
                          run_id="RUN-PROBE-1", runner_available=runner,
                          write_probe=write_probe)


@pytest.mark.real_git
def test_chatgpt_is_read_only_and_cannot_trigger(registry, storage, ledger):
    rec = next(a for a in registry.enabled_agents() if a.provider_id == "chatgpt")
    probe = build_adapter(rec, _ctx(storage, ledger)).probe()
    assert probe.state("read") is CapState.SUPPORTED
    assert probe.state("write") is CapState.UNSUPPORTED
    assert probe.state("reread") is CapState.UNSUPPORTED
    assert probe.state("trigger") is CapState.UNSUPPORTED
    assert probe.state("execute") is CapState.UNSUPPORTED
    assert probe.state("schedule") is CapState.UNKNOWN
    assert probe.items["read"].method == "LOCAL_GIT"
    assert probe.transport == "local_git"


@pytest.mark.real_git
def test_workbuddy_writes_own_outbox_and_reports_executor(registry, storage, ledger):
    rec = next(a for a in registry.enabled_agents() if a.provider_id == "workbuddy")
    probe = build_adapter(rec, _ctx(storage, ledger, runner=False)).probe()
    assert probe.state("write") is CapState.SUPPORTED
    assert probe.state("reread") is CapState.SUPPORTED
    assert probe.state("execute") is CapState.BLOCKED  # no runner -> BLOCKED_EXECUTOR
    assert "BLOCKED_EXECUTOR" in probe.items["execute"].detail

    with_runner = build_adapter(rec, _ctx(storage, ledger, runner=True)).probe()
    assert with_runner.state("execute") is CapState.SUPPORTED


@pytest.mark.real_git
def test_codex_execution_is_unknown_not_assumed(registry, storage, ledger):
    rec = next(a for a in registry.enabled_agents() if a.provider_id == "codex")
    probe = build_adapter(rec, _ctx(storage, ledger)).probe()
    assert probe.state("execute") is CapState.UNKNOWN
    assert probe.state("write") is CapState.SUPPORTED


@pytest.mark.real_git
def test_read_only_probe_marks_write_unsupported(registry, storage, ledger):
    rec = next(a for a in registry.enabled_agents() if a.provider_id == "workbuddy")
    probe = build_adapter(rec, _ctx(storage, ledger, write_probe=False)).probe()
    assert probe.state("write") is CapState.UNSUPPORTED
    assert probe.items["write"].method == "STATIC"


@pytest.mark.real_git
def test_custom_provider_falls_back_to_custom_adapter(registry, storage, ledger):
    from agl.support.poolgen import build_pool

    cfg = build_pool(2, mix={"chatgpt": 1, "acme": 1}, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["provider_schedules"]["acme"] = {"account_scope": "acme-main", "interval_minutes": 30}
    reg = RegistryView.from_config(cfg)
    rec = next(a for a in reg.enabled_agents() if a.provider_id == "acme")
    adapter = build_adapter(rec, _ctx(storage, ledger))
    probe = adapter.probe()
    assert type(adapter).__name__ == "CustomAdapter"
    assert probe.state("execute") is CapState.UNKNOWN


@pytest.mark.real_git
def test_matrix_has_all_operations_for_each_provider(registry, storage, ledger):
    probes = [build_adapter(rec, _ctx(storage, ledger)).probe()
              for rec in registry.enabled_agents()]
    matrix = capability_matrix(probes)
    assert len(matrix) == 3
    for row in matrix.values():
        assert set(row) == set(OPS)
        assert all(value in {s.value for s in CapState} for value in row.values())


@pytest.mark.real_git
def test_blocked_read_never_reports_supported(bare_remote):
    from agl.errors import AglError, ErrorCode
    from agl.storage.github import GitHubStorage
    from agl.storage.transports import LocalGitTransport

    cfg = build_pool(2, mix={"workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test")
    reg = RegistryView.from_config(cfg)
    rec = reg.enabled_agents()[0]

    class Denied(LocalGitTransport):
        def get_ref(self, repo, ref):
            raise AglError(ErrorCode.NO_PERMISSION, "403 no access")

    storage = GitHubStorage(Denied(bare_remote), "kaibahaha/xxsc", "exp/test")
    probe = build_adapter(rec, _ctx(storage, None)).probe()
    assert probe.state("read") is CapState.BLOCKED
    assert "NO_PERMISSION" in probe.items["read"].detail
