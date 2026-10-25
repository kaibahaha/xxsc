"""Registry / pool configuration: N>=2 with no fixed ceiling, fail-closed."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from agl.adapters.registry_view import RegistryView, validate_config
from agl.errors import AglError
from agl.support.poolgen import build_pool


@pytest.mark.parametrize("n", [2, 3, 5, 6, 10, 20])
def test_supported_pool_sizes(n):
    cfg = build_pool(n, admission="ADMITTED_ACTIVE", ref="exp/test")
    report = validate_config(cfg)
    assert report.ok, [i.as_dict() for i in report.errors()]
    assert report.pool_size == n
    view = RegistryView.from_config(cfg)
    assert len(view.enabled_agents()) == n
    assert len(view.eligible_agents()) == n


def test_single_agent_pool_rejected():
    cfg = build_pool(1, admission="ADMITTED_ACTIVE", ref="exp/test")
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "N_TOO_SMALL" for i in report.errors())


def test_duplicate_agent_id_rejected():
    cfg = build_pool(4, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["agents"].append(copy.deepcopy(cfg["agents"][0]))
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "DUPLICATE_AGENT_ID" for i in report.errors())


def test_active_ids_must_equal_enabled():
    cfg = build_pool(4, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["pool"]["active_agent_ids"] = cfg["pool"]["active_agent_ids"][:-1]
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "ACTIVE_MISMATCH" for i in report.errors())


def test_protected_ref_rejected():
    cfg = build_pool(2, admission="ADMITTED_ACTIVE", ref="main")
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "NO_PERMISSION" for i in report.errors())


def test_invalid_timezone_rejected():
    cfg = build_pool(2, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["timezone"] = "Mars/Olympus"
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "INVALID_TIMEZONE" for i in report.errors())


def test_verified_provider_quota_enforced():
    """ChatGPT: 4 agents but verified capacity 3 -> refused, other providers unaffected."""
    cfg = build_pool(6, mix={"chatgpt": 4, "workbuddy": 2}, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["provider_schedules"]["chatgpt"]["capacity_verified"] = True
    cfg["provider_schedules"]["chatgpt"]["capacity"] = 3
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "PROVIDER_QUOTA_EXCEEDED" for i in report.errors())

    ok_cfg = build_pool(6, mix={"chatgpt": 3, "workbuddy": 3}, admission="ADMITTED_ACTIVE", ref="exp/test")
    ok_cfg["provider_schedules"]["chatgpt"]["capacity_verified"] = True
    ok_cfg["provider_schedules"]["chatgpt"]["capacity"] = 3
    assert validate_config(ok_cfg).ok


def test_unverified_quota_is_warning_not_unlimited():
    cfg = build_pool(6, mix={"chatgpt": 5, "workbuddy": 1}, admission="ADMITTED_ACTIVE", ref="exp/test")
    report = validate_config(cfg)
    assert report.ok
    assert any(i.code == "QUOTA_UNVERIFIED" for i in report.warnings())
    view = RegistryView.from_config(cfg)
    cap = view.provider_capacity("chatgpt")
    assert cap["state"] == "UNVERIFIED"
    assert cap["capacity"] == 3  # 5 budget - 2 reserved, reported as unverified


def test_outbox_outside_own_scope_rejected():
    cfg = build_pool(2, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["agents"][0]["outbox"] = "05_outbox/SOMEONE_ELSE"
    report = validate_config(cfg)
    assert not report.ok
    assert any(i.code == "PATH_NOT_WHITELISTED" for i in report.errors())


def test_shipped_example_configs_have_duplicate_ids(repo_root: Path):
    """The frozen examples contain two agents named WORKBUDDY_DEV_01.

    This is a real defect found by reading the repository; the validator must
    refuse it rather than silently pick one.
    """
    for name in ("agent_pool.example.json", "mixed_pool.example.json"):
        path = repo_root / "frameworks/agensh-lite-v4.2/config" / name
        if not path.exists():
            pytest.skip(f"example missing: {path}")
        report = validate_config(json.loads(path.read_text(encoding="utf-8")))
        assert not report.ok, name
        assert any(i.code == "DUPLICATE_AGENT_ID" for i in report.errors()), name


def test_admission_gate_fails_closed():
    cfg = build_pool(3, admission="PENDING_PROBE", ref="exp/test")
    view = RegistryView.from_config(cfg)
    for rec in view.enabled_agents():
        decision = view.admission(rec.agent_id)
        assert not decision.allowed
        assert decision.reason.startswith("PROBE_PENDING") or decision.reason == "NOT_PROBED"
    assert view.eligible_agents() == []


def test_draining_and_disabled_agents_cannot_claim():
    cfg = build_pool(4, admission="ADMITTED_ACTIVE", ref="exp/test")
    cfg["agents"][0]["admission_status"] = "DRAINING"
    cfg["agents"][1]["enabled"] = False
    cfg["pool"]["active_agent_ids"] = [a["agent_id"] for a in cfg["agents"] if a["enabled"]]
    view = RegistryView.from_config(cfg)
    assert not view.admission(cfg["agents"][0]["agent_id"]).allowed
    assert view.admission(cfg["agents"][0]["agent_id"]).reason == "ADMISSION_DRAINING"
    assert not view.admission(cfg["agents"][1]["agent_id"]).allowed
    assert view.admission(cfg["agents"][1]["agent_id"]).reason == "AGENT_DISABLED"


def test_unknown_agent_is_denied():
    view = RegistryView.from_config(build_pool(2, admission="ADMITTED_ACTIVE", ref="exp/test"))
    decision = view.admission("GHOST_99")
    assert not decision.allowed and decision.reason == "UNKNOWN_AGENT"


def test_write_scope_check():
    view = RegistryView.from_config(build_pool(2, admission="ADMITTED_ACTIVE", ref="exp/test"))
    agent = view.enabled_agents()[0]
    assert view.can_write(agent.agent_id, f"05_outbox/{agent.agent_id}/RUN-1/EV-1.json")
    assert not view.can_write(agent.agent_id, "05_outbox/OTHER/RUN-1/EV-1.json")


def test_error_from_invalid_config_carries_code():
    with pytest.raises(AglError) as exc:
        RegistryView.from_config(build_pool(1, admission="ADMITTED_ACTIVE", ref="exp/test"))
    assert exc.value.code.value == "N_TOO_SMALL"
