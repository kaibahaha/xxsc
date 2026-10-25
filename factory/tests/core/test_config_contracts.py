from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json
import pytest
from factory.agl.config import validate_config
from factory.agl.registry import AgentRegistry
from factory.agl.schemas import (AgentRegistration, CoreError, Event, TaskSpec, digest, import_v41)
from conftest import agent

ROOT = Path(__file__).resolve().parents[3]


def config(n):
    members = [agent(i).to_dict() for i in range(n)]
    return dict(schema_version="2.0", repo="kaibahaha/xxsc", ref="dev/agl-v4.2-codex-controller",
        runtime_root="factory/projects/test", timezone="UTC", agents=members,
        pool={"active_agent_ids": [a["agent_id"] for a in members]})


@pytest.mark.parametrize("n", [2, 3, 4, 5, 6, 8, 10, 12, 20])
def test_dynamic_pool(n):
    cfg = validate_config(config(n), simulation=True)
    assert len(cfg.registry.agents) == n
    # Registration grows dynamically beyond the configured initial pool.
    cfg.registry.register(agent(n))
    assert len(cfg.registry.agents) == n + 1


@pytest.mark.parametrize("case,code", [("one", "POOL_BELOW_TWO"), ("duplicate", "DUPLICATE_AGENT"),
    ("active", "ACTIVE_ID_MISMATCH"), ("timezone", "INVALID_TIMEZONE"),
    ("path", "INVALID_PATH"), ("main", "UNSAFE_REF"), ("unsafe", "UNSAFE_CLAIM_LOCK"),
    ("production", "PRODUCTION_NOT_SUPPORTED")])
def test_invalid_config(case, code):
    data = config(1 if case == "one" else 3)
    if case == "duplicate": data["agents"].append(data["agents"][0])
    if case == "active": data["pool"]["active_agent_ids"] = ["missing"]
    if case == "timezone": data["timezone"] = "Mars/Unverified"
    if case == "path": data["agents"][0]["allowed_writes"] = ["factory/../main"]
    if case == "main": data["ref"] = "main"
    if case == "unsafe": data["controller"] = {"allow_unverified_claim_as_lock": True}
    if case == "production": data["controller"] = {"enable_in_production": True}
    with pytest.raises(CoreError, match=code): validate_config(data)


def test_provider_budget_independent():
    data = config(10)
    for i, record in enumerate(data["agents"]):
        record.update(provider_id="chatgpt" if i < 3 else "workbuddy", account_scope="shared")
    data["provider_quotas"] = [{"provider_id": "chatgpt", "account_scope": "shared", "capacity_verified": True, "capacity": 5, "reserved": 2}]
    assert len(validate_config(data, simulation=True).registry.agents) == 10
    data["agents"][3]["provider_id"] = "chatgpt"
    with pytest.raises(CoreError, match="PROVIDER_QUOTA_EXCEEDED"): validate_config(data)
    data["provider_quotas"][0]["capacity_verified"] = False
    assert len(validate_config(data).registry.agents) == 10  # Intent accepted; no admission inferred.


@pytest.mark.parametrize("name", ["agent_pool.example.json", "mixed_pool.example.json"])
def test_frozen_example_conflicts_are_rejected(name):
    data = json.loads((ROOT / "frameworks/agensh-lite-v4.2/config" / name).read_text())
    with pytest.raises(CoreError, match="DUPLICATE_AGENT"): validate_config(data)


@pytest.mark.parametrize("kind", ["task", "event", "receipt", "note"])
def test_v41_compatibility(kind):
    data = json.loads((ROOT / f"frameworks/agensh-lite-v4.1/examples/example_{kind}.json").read_text())
    imported = import_v41(kind, data, provider_id="test")
    if kind == "task": assert imported.task_id == data["task_id"]
    elif kind == "event": assert imported.payload["legacy_payload_sha256"] == data["payload_sha256"]
    else: assert imported == data
    data["unexpected"] = True
    with pytest.raises(CoreError, match="INVALID_V41_PAYLOAD"): import_v41(kind, data, provider_id="test")


def test_roundtrip_and_version():
    a = agent(0)
    assert AgentRegistration.from_dict(a.to_dict()) == a
    with pytest.raises(CoreError, match="UNSUPPORTED_SCHEMA"): replace(a, schema_version="99")
    with pytest.raises(CoreError, match="UNKNOWN_FIELD"): AgentRegistration.from_dict(dict(a.to_dict(), secret="ignored?"))
    with pytest.raises(CoreError, match="PROBE_PENDING"): replace(a, admission_status="ADMITTED_ACTIVE")


def test_generated_schema_matches_contracts():
    from jsonschema import Draft202012Validator
    from factory.agl.contracts.generate_schema import schema
    checked = json.loads((ROOT / "factory/agl/contracts/core.schema.json").read_text())
    assert checked == schema()
    Draft202012Validator.check_schema(checked)
    Draft202012Validator({**checked, "oneOf": [{"$ref": "#/$defs/AgentRegistration"}]}).validate(agent(0).to_dict())


@pytest.mark.parametrize("ref", ["dev/with space", "dev/../main", "dev/.hidden", "dev/x.lock/y", "dev/double//slash", "dev/new\nline"])
def test_git_ref_validation(ref):
    data = config(3)
    data["ref"] = ref
    with pytest.raises(CoreError, match="UNSAFE_REF"): validate_config(data)


def test_three_chatgpt_two_workbuddy_one_codex_pool():
    data = config(6)
    for record, provider in zip(data["agents"], ["chatgpt"] * 3 + ["workbuddy"] * 2 + ["codex"]):
        record.update(provider_id=provider, account_scope=provider + "-main")
    registry = validate_config(data, simulation=True).registry
    assert [a.provider_id for a in registry.agents.values()].count("chatgpt") == 3
    assert len(registry.agents) == 6
