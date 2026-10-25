"""Provider-neutral, JSON serializable contracts. No wire field proves authentication."""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from typing import Any, Mapping
import hashlib
import json
import math
import re

SCHEMA_VERSION = "2.0"


class CoreError(ValueError):
    def __init__(self, code: str):
        self.code = code
        super().__init__(code)


def require(condition: bool, code: str) -> None:
    if not condition:
        raise CoreError(code)


def canonical(value: Any) -> str:
    if isinstance(value, Wire):
        value = asdict(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def hex_hash(value: str, length: int = 64) -> bool:
    return isinstance(value, str) and bool(re.fullmatch(r"[0-9a-f]{" + str(length) + "}", value))


def safe_path(path: str) -> bool:
    return (isinstance(path, str) and bool(path) and not path.startswith("/")
            and "\\" not in path and all(p not in ("", ".", "..") for p in path.split("/")))


@dataclass(frozen=True, kw_only=True)
class Wire:
    schema_version: str = SCHEMA_VERSION

    def __post_init__(self):
        require(self.schema_version == SCHEMA_VERSION, "UNSUPPORTED_SCHEMA")

    def to_dict(self) -> dict:
        return json.loads(canonical(self))

    @classmethod
    def from_dict(cls, value: Mapping):
        require(not (set(value) - {f.name for f in fields(cls)}), "UNKNOWN_FIELD")
        try:
            return cls(**value)
        except TypeError:
            raise CoreError("INVALID_CONTRACT_FIELDS") from None


@dataclass(frozen=True, kw_only=True)
class AgentRegistration(Wire):
    agent_id: str
    provider_id: str
    account_scope: str
    adapter_id: str
    credential_principal: str
    capabilities: tuple[str, ...]
    allowed_reads: tuple[str, ...]
    allowed_writes: tuple[str, ...]
    allowed_actions: tuple[str, ...] = ()
    runtime_mode: str = "manual"
    desired_enabled: bool = False
    admission_status: str = "PENDING_PROBE"
    health: str = "UNKNOWN"
    max_inflight: int = 1
    independence_group: str = "UNVERIFIED"
    probe_evidence_refs: tuple[str, ...] = ()

    def __post_init__(self):
        super().__post_init__()
        for name in ("agent_id", "provider_id", "account_scope", "adapter_id", "credential_principal"):
            require(bool(getattr(self, name)), "INVALID_IDENTITY")
        for name in ("capabilities", "allowed_reads", "allowed_writes", "allowed_actions", "probe_evidence_refs"):
            value = getattr(self, name)
            require(isinstance(value, (list, tuple)) and all(isinstance(v, str) and v for v in value), "INVALID_LIST")
            object.__setattr__(self, name, tuple(value))
        require(type(self.desired_enabled) is bool, "INVALID_ENABLED")
        require(type(self.max_inflight) is int and self.max_inflight >= 1, "INVALID_CAPACITY")
        require(self.admission_status in {"REGISTERED", "DESIRED_ENABLED", "PENDING_PROBE", "PROBING", "ADMITTED_ACTIVE", "MOCK_ACTIVE", "DRAINING", "UNAVAILABLE"}, "INVALID_ADMISSION")
        require(self.health in {"HEALTHY", "UNKNOWN", "OFFLINE", "DEGRADED"}, "INVALID_HEALTH")
        require(all(safe_path(p) for p in (*self.allowed_reads, *self.allowed_writes)), "INVALID_PATH")
        if self.admission_status == "ADMITTED_ACTIVE":
            require(bool(self.probe_evidence_refs), "PROBE_PENDING")


@dataclass(frozen=True, kw_only=True)
class ProviderSession(Wire):
    """Output of a trusted Authenticator, never accepted directly from JSON clients."""
    agent_id: str
    provider_id: str
    principal: str
    account_scope: str


@dataclass(frozen=True, kw_only=True)
class TaskSpec(Wire):
    task_id: str
    spec_hash: str
    project_id: str = "default"
    revision: int = 1
    acceptance_criteria: tuple[str, ...] = ()
    dependencies: tuple[str, ...] = ()
    allowed_agents: tuple[str, ...] = ()
    required_capabilities: tuple[str, ...] = ()
    write_paths: tuple[str, ...] = ()
    read_paths: tuple[str, ...] = ()
    priority: int = 0
    commit_sha: str | None = None

    def __post_init__(self):
        super().__post_init__()
        require(bool(self.task_id) and hex_hash(self.spec_hash), "INVALID_TASK")
        require(type(self.revision) is int and self.revision >= 1 and type(self.priority) is int, "INVALID_VERSION")
        for name in ("acceptance_criteria", "dependencies", "allowed_agents", "required_capabilities", "write_paths", "read_paths"):
            value = getattr(self, name)
            require(isinstance(value, (tuple, list)) and all(isinstance(v, str) and v for v in value), "INVALID_LIST")
            require(len(value) == len(set(value)), "DUPLICATE_VALUE")
            object.__setattr__(self, name, tuple(value))
        require(all(safe_path(p) for p in (*self.write_paths, *self.read_paths)), "INVALID_PATH")
        require(self.task_id not in self.dependencies, "DAG_CYCLE")
        require(self.commit_sha is None or hex_hash(self.commit_sha, 40), "INVALID_COMMIT")


@dataclass(frozen=True, kw_only=True)
class ClaimProposal(Wire):
    task_id: str
    agent_id: str
    provider_id: str
    run_id: str
    spec_hash: str
    attempt_id: str
    expected_version: int
    ttl_seconds: float = 300
    commit_sha: str | None = None
    evidence_refs: tuple[str, ...] = ()

    def __post_init__(self):
        super().__post_init__()
        require(all((self.task_id, self.agent_id, self.provider_id, self.run_id, self.attempt_id)), "INVALID_CLAIM")
        require(hex_hash(self.spec_hash) and type(self.expected_version) is int and self.expected_version >= 1, "INVALID_CLAIM")
        require(isinstance(self.ttl_seconds, (float, int)) and math.isfinite(self.ttl_seconds) and 0 < self.ttl_seconds <= 3600, "INVALID_TTL")


@dataclass(frozen=True, kw_only=True)
class LeaseGrant(Wire):
    task_id: str
    agent_id: str
    provider_id: str
    run_id: str
    spec_hash: str
    attempt_id: str
    fencing_epoch: int
    expires_at: float
    task_version: int
    commit_sha: str | None = None
    evidence_refs: tuple[str, ...] = ()


@dataclass(frozen=True, kw_only=True)
class ArtifactEvidence(Wire):
    evidence_id: str
    task_id: str
    spec_hash: str
    commit_sha: str
    runner_agent_id: str
    environment_id: str
    command: str
    exit_code: int
    stdout_sha256: str
    stderr_sha256: str
    evidence_refs: tuple[str, ...]
    test_summary: str

    def __post_init__(self):
        super().__post_init__()
        require(all((self.evidence_id, self.task_id, self.runner_agent_id, self.environment_id, self.command, self.test_summary)) and bool(self.evidence_refs), "MISSING_RUNTIME_EVIDENCE")
        require(hex_hash(self.spec_hash) and hex_hash(self.commit_sha, 40)
                and hex_hash(self.stdout_sha256) and hex_hash(self.stderr_sha256), "INVALID_EVIDENCE_HASH")
        require(type(self.exit_code) is int, "INVALID_EXIT_CODE")


@dataclass(frozen=True, kw_only=True)
class StateTransition(Wire):
    task_id: str
    agent_id: str
    provider_id: str
    run_id: str
    spec_hash: str
    attempt_id: str
    fencing_epoch: int
    expected_version: int
    to_state: str
    commit_sha: str | None = None
    evidence_refs: tuple[str, ...] = ()
    evidence: dict | None = None

    def __post_init__(self):
        super().__post_init__()
        require(all((self.task_id, self.agent_id, self.provider_id, self.run_id, self.attempt_id, self.to_state)), "INVALID_TRANSITION")
        require(hex_hash(self.spec_hash) and type(self.expected_version) is int and self.expected_version >= 1
                and type(self.fencing_epoch) is int and self.fencing_epoch >= 1, "INVALID_FENCE")


TaskTransition = StateTransition


@dataclass(frozen=True, kw_only=True)
class Event(Wire):
    event_id: str
    producer: str
    provider_id: str
    target_agents: tuple[str, ...]
    task_id: str
    kind: str
    summary: str
    observed_at: str
    raw_ref: str
    run_id: str
    source: str = "github"
    project_id: str = "default"
    spec_hash: str | None = None
    attempt_id: str | None = None
    fencing_epoch: int | None = None
    commit_sha: str | None = None
    causation_id: str | None = None
    evidence_refs: tuple[str, ...] = ()
    payload: dict = field(default_factory=dict)

    def __post_init__(self):
        super().__post_init__()
        require(all((self.event_id, self.producer, self.provider_id, self.kind, self.raw_ref, self.run_id)), "INVALID_EVENT")
        require(isinstance(self.target_agents, (tuple, list)) and bool(self.target_agents)
                and all(isinstance(a, str) and a for a in self.target_agents), "INVALID_TARGETS")
        require(len(set(self.target_agents)) == len(self.target_agents), "DUPLICATE_TARGET")
        from datetime import datetime
        try:
            dt = datetime.fromisoformat(self.observed_at.replace("Z", "+00:00"))
            require(dt.tzinfo is not None, "INVALID_TIME")
        except (ValueError, AttributeError):
            raise CoreError("INVALID_TIME") from None
        object.__setattr__(self, "target_agents", tuple(self.target_agents))
        require(self.causation_id != self.event_id, "CAUSATION_CYCLE")
        canonical(self.payload)


UEM = Event


@dataclass(frozen=True, kw_only=True)
class Ack(Wire):
    event_id: str
    agent_id: str
    provider_id: str
    run_id: str
    event_sha256: str
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True, kw_only=True)
class MemoryNote(Wire):
    note_id: str
    type: str
    task_id: str
    agent_id: str
    provider_id: str
    run_id: str
    spec_hash: str
    commit_sha: str | None
    summary: str
    evidence_refs: tuple[str, ...]
    test_id: str | None = None
    detail_ref: str | None = None
    expires_at: float | None = None

    def __post_init__(self):
        super().__post_init__()
        require(self.type in {"FACT", "OBSERVED", "FAIL", "CLAIM", "PATCH_SUMMARY"}, "INVALID_NOTE_TYPE")
        require(0 < len(self.summary) <= 160 and bool(self.evidence_refs), "INVALID_NOTE")
        require(hex_hash(self.spec_hash), "INVALID_SPEC")
        if self.type in {"FAIL", "PATCH_SUMMARY"}:
            require(hex_hash(self.commit_sha, 40) and bool(self.test_id), "MISSING_CANDIDATE_SCOPE")
        if self.type == "CLAIM":
            require(self.expires_at is not None and math.isfinite(self.expires_at), "MISSING_CLAIM_EXPIRY")


@dataclass(frozen=True, kw_only=True)
class Handoff(Wire):
    handoff_id: str
    task_id: str
    agent_id: str
    provider_id: str
    run_id: str
    spec_hash: str
    attempt_id: str
    fencing_epoch: int
    commit_sha: str | None
    decision_log: tuple[str, ...]
    open_issues: tuple[str, ...]
    next_action: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self):
        super().__post_init__()
        require(all((self.handoff_id, self.task_id, self.agent_id, self.run_id, self.next_action)) and hex_hash(self.spec_hash), "INVALID_HANDOFF")


def import_v41(kind: str, data: dict, *, provider_id: str | None = None):
    """Validate against frozen V4.1, preserve provenance, never infer admission.

    jsonschema is needed only at this legacy boundary, not by the core runtime.
    Receipt/Note remain validated legacy dictionaries because V4.1 lacks an
    authenticated recipient (Receipt) or exact test scope (Note).
    """
    from pathlib import Path
    from jsonschema import Draft202012Validator, FormatChecker
    require(kind in {"task", "event", "receipt", "note"}, "UNKNOWN_LEGACY_TYPE")
    schema_path = Path(__file__).resolve().parents[2] / "frameworks/agensh-lite-v4.1/schemas" / (kind + ".schema.json")
    schema = json.loads(schema_path.read_text())
    errors = list(Draft202012Validator(schema, format_checker=FormatChecker()).iter_errors(data))
    require(not errors, "INVALID_V41_PAYLOAD")
    if kind == "task":
        require(data["status"] == "READY", "LEGACY_STATE_REQUIRES_REVIEW")
        return TaskSpec.from_dict({k: v for k, v in data.items() if k != "status"})
    if kind == "event":
        require(bool(provider_id), "PROVIDER_BINDING_REQUIRED")
        values = {k: v for k, v in data.items() if k != "payload_sha256"}
        values.update(schema_version=SCHEMA_VERSION, provider_id=provider_id)
        # Preserve the external byte hash as provenance; it is not our canonical envelope hash.
        values["payload"] = {"legacy_payload_sha256": data.get("payload_sha256")}
        require(bool(values.get("run_id")), "LEGACY_RUN_ID_REQUIRED")
        return Event.from_dict(values)
    return json.loads(canonical(data))
