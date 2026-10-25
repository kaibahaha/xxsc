"""Fail-closed config loading. Example intent does not establish runtime admission."""
from dataclasses import dataclass
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import json
import re
from .registry import AgentRegistry
from .schemas import AgentRegistration, require, CoreError, safe_path


@dataclass(frozen=True)
class Config:
    repo: str
    ref: str
    runtime_root: str
    registry: AgentRegistry
    raw: dict


def validate_config(data: dict, *, simulation: bool = False) -> Config:
    require(data.get("schema_version") in {"1.0", "2.0"}, "UNSUPPORTED_SCHEMA")
    require(isinstance(data.get("repo"), str) and bool(re.fullmatch(r"[\w.-]+/[\w.-]+", data["repo"])), "INVALID_REPO")
    ref = data.get("ref", "")
    require(isinstance(ref, str) and ref not in {"main", "master", "refs/heads/main", "refs/heads/master"}
            and ref and not any(c in ref for c in " ~^:?*[\\") and ".." not in ref and "@{" not in ref
            and not re.search(r"[\x00-\x20\x7f]", ref) and "//" not in ref
            and all(not p.startswith(".") and not p.endswith(".lock") for p in ref.split("/"))
            and not ref.startswith("/") and not ref.endswith(("/", ".", ".lock")), "UNSAFE_REF")
    require(safe_path(data.get("runtime_root", "")), "INVALID_PATH")
    try:
        ZoneInfo(data.get("timezone", "UTC"))
    except (ZoneInfoNotFoundError, ValueError, TypeError):
        raise CoreError("INVALID_TIMEZONE") from None
    agents = []
    for item in data.get("agents", []):
        values = dict(item)
        # Explicit legacy aliases. Missing permissions remain empty, never inferred from outbox.
        values["desired_enabled"] = values.pop("enabled", values.get("desired_enabled", False))
        values["max_inflight"] = values.pop("max_inflight_tasks", values.get("max_inflight", 1))
        allowed = AgentRegistration.__dataclass_fields__
        values = {k: v for k, v in values.items() if k in allowed}
        for name, default in {"credential_principal": "UNVERIFIED", "capabilities": (),
                              "allowed_reads": (), "allowed_writes": ()}.items():
            values.setdefault(name, default)
        try:
            agents.append(AgentRegistration.from_dict(values))
        except TypeError:
            raise CoreError("MISSING_AGENT_FIELD") from None
    registry = AgentRegistry(agents, simulation=simulation)
    active = data.get("pool", {}).get("active_agent_ids", [])
    require(len(active) == len(set(active)), "DUPLICATE_ACTIVE_ID")
    require(set(active) == {a.agent_id for a in agents if a.desired_enabled}, "ACTIVE_ID_MISMATCH")
    registry.quotas = data.get("provider_quotas", [])
    registry.check_quotas()
    require(not data.get("controller", {}).get("enable_in_production", False), "PRODUCTION_NOT_SUPPORTED")
    require(not data.get("controller", {}).get("allow_unverified_claim_as_lock", False), "UNSAFE_CLAIM_LOCK")
    return Config(data["repo"], ref, data["runtime_root"], registry, data)


def load_config(path: str | Path, *, simulation: bool = False) -> Config:
    return validate_config(json.loads(Path(path).read_text()), simulation=simulation)
