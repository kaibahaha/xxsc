"""Short-transaction deterministic controller. All public writes require credentials."""
from __future__ import annotations
from copy import deepcopy
import math
import time
from .leases import SQLiteLeaseBackend
from .registry import AgentRegistry
from .replay import board_projection
from .schemas import (Ack, AgentRegistration, ArtifactEvidence, ClaimProposal, CoreError,
                      Event, Handoff, LeaseGrant, MemoryNote, ProviderSession,
                      StateTransition, TaskSpec, digest, hex_hash, require)
from .task_state import (AUTHORITY_STAGES, GATE_ACTIONS, TRANSITIONS, dependencies_done, expire_tasks,
                         fence, invalidate, retire_authority, revoke_lease, validate_dag)


class Controller:
    def __init__(self, backend: SQLiteLeaseBackend, registry: AgentRegistry, authenticate,
                 *, clock=time.time, evidence_verifier=None):
        self.backend, self.authenticate = backend, authenticate
        self.clock, self.evidence_verifier = clock, evidence_verifier
        self.simulation = registry.simulation
        self._board_ready = False  # Every fresh process must reconcile before new grants.
        initial = {k: a.to_dict() for k, a in registry.agents.items()}
        now = self._now()
        request = {"kind": "BOOTSTRAP", "agents": initial, "simulation": self.simulation, "quotas": registry.quotas}
        def bootstrap(state):
            state["agents"] = initial
            state["meta"] = {"board": "UNKNOWN", "last_time": now, "simulation": self.simulation, "quotas": registry.quotas, "registry_version": 1}
            return {"status": "INITIALIZED", "authority": backend.authority, "simulation": self.simulation}
        initialized = backend.transact("bootstrap", request, now, bootstrap, initialize=True)
        require(initialized["simulation"] == self.simulation, "SIMULATION_MODE_MISMATCH")

    def _now(self):
        now = self.clock()
        require(isinstance(now, (int, float)) and math.isfinite(now), "INVALID_CLOCK")
        return float(now)

    def _session(self, credential):
        try:
            session = self.authenticate(credential)
        except Exception:
            raise CoreError("AUTHENTICATION_FAILED") from None
        require(isinstance(session, ProviderSession), "AUTHENTICATION_FAILED")
        return session

    def _agent(self, state, session):
        record = state["agents"].get(session.agent_id)
        require(record is not None, "UNKNOWN_AGENT")
        agent = AgentRegistration.from_dict(record)
        require((agent.provider_id, agent.account_scope, agent.credential_principal) ==
                (session.provider_id, session.account_scope, session.principal), "AUTH_SCOPE_MISMATCH")
        return agent

    def _action(self, agent, action):
        require(agent.desired_enabled and agent.health == "HEALTHY"
                and agent.admission_status in ({"ADMITTED_ACTIVE", "MOCK_ACTIVE"} if self.simulation else {"ADMITTED_ACTIVE"})
                and action in agent.allowed_actions, "ACTION_DENIED")

    def _write(self, credential, command_id, kind, payload, mutate, *, needs_board=False):
        require(isinstance(command_id, str) and bool(command_id), "MISSING_IDEMPOTENCY_KEY")
        session = self._session(credential)
        now = self._now()
        request = {"kind": kind, "actor": session.to_dict(), "payload": payload}
        def apply(state):
            try:
                require(now >= state["meta"]["last_time"], "CLOCK_REGRESSION")
                state["meta"]["last_time"] = now
                agent = self._agent(state, session)
                if needs_board:
                    require(self._board_ready and state["meta"].get("board") == "KNOWN", "BOARD_UNKNOWN")
                expire_tasks(state, now)
                # Domain validation must not leave partially mutated state on denial.
                safe = deepcopy(state)
                try:
                    return mutate(state, agent, now)
                except CoreError:
                    state.clear()
                    state.update(safe)
                    raise
            except CoreError as exc:
                return {"status": "REJECTED", "error_code": exc.code}
        try:
            return self.backend.transact(session.agent_id + ":" + command_id, request, now, apply)
        except CoreError:
            raise
        except Exception as exc:
            self._board_ready = False
            return {"status": "UNKNOWN_WRITE", "error_code": type(exc).__name__,
                    "command_id": session.agent_id + ":" + command_id,
                    "reconcile_request": request}

    def board_digest(self):
        state = self.snapshot()
        return digest({"tasks": state["tasks"], "agents": state["agents"]})

    def reconcile_board(self, credential, command_id, expected_digest):
        def mutate(state, agent, now):
            self._action(agent, "controller_admin")
            require(digest({"tasks": state["tasks"], "agents": state["agents"]}) == expected_digest, "BOARD_CONFLICT")
            state["meta"]["board"] = "KNOWN"
            return {"status": "RECONCILED", "digest": expected_digest}
        result = self._write(credential, command_id, "RECONCILE_BOARD", {"digest": expected_digest}, mutate)
        # A replayed successful reconciliation cannot establish freshness for this instance.
        if result["status"] == "RECONCILED":
            self._board_ready = self.board_digest() == expected_digest
        return result

    def mark_board_unknown(self, credential, command_id, reason):
        self._board_ready = False
        def mutate(state, agent, now):
            self._action(agent, "controller_admin")
            state["meta"]["board"] = "UNKNOWN"
            state["meta"]["board_error"] = reason
            return {"status": "BOARD_UNKNOWN"}
        return self._write(credential, command_id, "BOARD_UNKNOWN", {"reason": reason}, mutate)

    def registry_version(self):
        # Pre-fix journals have implicit registry version 1; no startup migration writes.
        return self.snapshot()["meta"].get("registry_version", 1)

    @staticmethod
    def _check_registry_version(state, expected_version):
        current = state["meta"].get("registry_version", 1)
        require(expected_version is None or (type(expected_version) is int and expected_version == current),
                "REGISTRY_VERSION_CONFLICT")
        return current

    def _registry_changes(self, state, registrations, quotas):
        ids = [a.agent_id for a in registrations]
        require(len(ids) == len(set(ids)), "DUPLICATE_AGENT")
        merged = dict(state["agents"])
        changed = set()
        for registration in registrations:
            require(self.simulation or registration.admission_status != "MOCK_ACTIVE", "MOCK_NOT_PRODUCTION")
            record = registration.to_dict()
            old = merged.get(registration.agent_id)
            if old:
                require(all(old[k] == record[k] for k in ("provider_id", "account_scope", "credential_principal")),
                        "IDENTITY_CHANGE_REQUIRES_NEW_AGENT")
            if old != record:
                changed.add(registration.agent_id)
            merged[registration.agent_id] = record
        policies = state["meta"].get("quotas", []) if quotas is None else quotas
        AgentRegistry([AgentRegistration.from_dict(a) for a in merged.values()],
                      simulation=self.simulation, quotas=policies)
        if not changed and policies == state["meta"].get("quotas", []):
            return False
        state["agents"] = merged
        state["meta"]["quotas"] = deepcopy(policies)
        state["meta"]["registry_version"] = state["meta"].get("registry_version", 1) + 1
        # Any permission/admission edit fences the identity's old authority.
        for task in state["tasks"].values():
            if task.get("lease") and task["lease"]["agent_id"] in changed:
                retire_authority(task)
        return True

    def apply_registry(self, credential, command_id, registrations: list[AgentRegistration], *,
                       expected_version: int, quotas=None):
        """Authorized versioned upserts; omissions never delete identities or history.

        Startup registry objects are intent only. Apply changes explicitly after authentication.
        Admission probe references are verified by the trusted integration service.
        """
        def mutate(state, agent, now):
            self._action(agent, "registry_admin")
            require(type(expected_version) is int and expected_version >= 1, "REGISTRY_VERSION_CONFLICT")
            self._check_registry_version(state, expected_version)
            changed = self._registry_changes(state, registrations, quotas)
            return {"status": "REGISTRY_UPDATED" if changed else "REGISTRY_UNCHANGED",
                    "registry_version": state["meta"].get("registry_version", 1)}
        payload = {"registrations": [a.to_dict() for a in registrations],
                   "expected_version": expected_version, "quotas": quotas}
        return self._write(credential, command_id, "APPLY_REGISTRY", payload, mutate)

    def register_agent(self, credential, command_id, registration: AgentRegistration, *, expected_version=None):
        # Compatible single-add API; config changes should use apply_registry with explicit CAS.
        def mutate(state, agent, now):
            self._action(agent, "registry_admin")
            self._check_registry_version(state, expected_version)
            old = state["agents"].get(registration.agent_id)
            if old:
                require(old == registration.to_dict(), "DUPLICATE_AGENT")
                return {"status": "DUPLICATE", "registry_version": state["meta"].get("registry_version", 1)}
            self._registry_changes(state, [registration], None)
            return {"status": "REGISTERED", "registry_version": state["meta"]["registry_version"]}
        payload = registration.to_dict()
        if expected_version is not None:
            payload = {"registration": payload, "expected_version": expected_version}
        return self._write(credential, command_id, "REGISTER_AGENT", payload, mutate)

    def update_health(self, credential, command_id, agent_id, *, health, admission_status, expected_version=None):
        def mutate(state, agent, now):
            self._action(agent, "registry_admin")
            self._check_registry_version(state, expected_version)
            require(agent_id in state["agents"], "UNKNOWN_AGENT")
            record = dict(state["agents"][agent_id], health=health, admission_status=admission_status)
            validated = AgentRegistration.from_dict(record)
            require(admission_status in {"DRAINING", "UNAVAILABLE"}, "READMISSION_REQUIRES_PROBE")
            self._registry_changes(state, [validated], None)
            return {"status": "UPDATED", "registry_version": state["meta"].get("registry_version", 1)}
        payload = {"agent_id": agent_id, "health": health, "admission_status": admission_status}
        if expected_version is not None:
            payload["expected_version"] = expected_version
        return self._write(credential, command_id, "UPDATE_HEALTH", payload, mutate)

    def add_tasks(self, credential, command_id, specs: list[TaskSpec]):
        def mutate(state, agent, now):
            self._action(agent, "task_admin")
            for spec in specs:
                require(spec.task_id not in state["tasks"], "DUPLICATE_TASK")
                require(set(spec.allowed_agents) <= set(state["agents"]), "UNKNOWN_AGENT")
                state["tasks"][spec.task_id] = dict(spec.to_dict(), status="READY", version=1,
                    fencing_epoch=0, lease=None, lease_phase=None, created_at=now, author=None,
                    candidate_commit=None, qa_evidence=None)
            validate_dag(state["tasks"])
            return {"status": "CREATED", "task_ids": [s.task_id for s in specs]}
        return self._write(credential, command_id, "ADD_TASKS", [s.to_dict() for s in specs], mutate)

    def _eligible_for_phase(self, state, agent, task):
        stage = AUTHORITY_STAGES.get(task["status"])
        eligibility = task
        if stage:
            self._action(agent, stage)
            if task["status"] in {"QA_PENDING", "QA_GREEN"}:
                author = state["agents"][task["author"]]
                require(agent.agent_id != task["author"] and agent.independence_group != "UNVERIFIED"
                        and agent.independence_group != author["independence_group"], "INDEPENDENCE_REQUIRED")
            # Acceptance authority permits reading the candidate, not developer writes.
            eligibility = dict(task, required_capabilities=[], write_paths=[])
        AgentRegistry([AgentRegistration.from_dict(a) for a in state["agents"].values()],
                      simulation=self.simulation).eligible(agent, eligibility)

    def claim(self, credential, command_id, proposal: ClaimProposal):
        def mutate(state, agent, now):
            require((proposal.agent_id, proposal.provider_id) == (agent.agent_id, agent.provider_id), "AUTH_SCOPE_MISMATCH")
            require(proposal.task_id in state["tasks"], "UNKNOWN_TASK")
            task = state["tasks"][proposal.task_id]
            self._eligible_for_phase(state, agent, task)
            require(task["spec_hash"] == proposal.spec_hash, "SPEC_MISMATCH")
            require(task["version"] == proposal.expected_version, "VERSION_CONFLICT")
            require((task["status"] == "READY" or task["status"] in AUTHORITY_STAGES)
                    and task["lease"] is None, "LEASE_CONFLICT")
            stage = task["status"] in AUTHORITY_STAGES
            if stage:
                require(proposal.commit_sha == task["candidate_commit"], "STALE_COMMIT")
            require(dependencies_done(task, state["tasks"]), "DEPENDENCY_NOT_DONE")
            require(sum(t.get("lease") is not None and t["lease"]["agent_id"] == agent.agent_id
                        for t in state["tasks"].values()) < agent.max_inflight, "WIP_LIMIT")
            task["fencing_epoch"] += 1
            task["version"] += 1
            task["lease_phase"] = task["status"] if stage else "EXECUTION"
            if not stage:
                task["status"] = "CLAIMED"
            grant = LeaseGrant(task_id=task["task_id"], agent_id=agent.agent_id, provider_id=agent.provider_id,
                run_id=proposal.run_id, spec_hash=task["spec_hash"], attempt_id=proposal.attempt_id,
                fencing_epoch=task["fencing_epoch"], expires_at=now + proposal.ttl_seconds,
                task_version=task["version"], commit_sha=task["candidate_commit"] if stage else task["commit_sha"])
            task["lease"] = grant.to_dict()
            if not stage:
                task["author"] = agent.agent_id
            return {"status": "GRANTED", "authority": self.backend.authority, "lease": grant.to_dict()}
        result = self._write(credential, command_id, "CLAIM", proposal.to_dict(), mutate, needs_board=True)
        if result["status"] == "GRANTED":
            # Retries may retrieve historical grants, but never report them as currently valid.
            try:
                state = self.backend.snapshot()
                task = state["tasks"][proposal.task_id]
                require(self._now() >= state["meta"]["last_time"], "CLOCK_REGRESSION")
                require(task.get("lease") == result["lease"] and result["lease"]["expires_at"] > self._now(), "LATE_STALE_ATTEMPT")
                require(self._board_ready and state["meta"]["board"] == "KNOWN", "BOARD_UNKNOWN")
            except CoreError as exc:
                return {"status": "REJECTED", "error_code": exc.code}
            except Exception as exc:
                self._board_ready = False
                return {"status": "UNKNOWN_WRITE", "error_code": type(exc).__name__}
        return result

    def renew(self, credential, command_id, grant: LeaseGrant, ttl_seconds=300):
        def mutate(state, agent, now):
            require(math.isfinite(ttl_seconds) and 0 < ttl_seconds <= 3600, "INVALID_TTL")
            require(grant.task_id in state["tasks"], "UNKNOWN_TASK")
            task = state["tasks"][grant.task_id]
            lease = fence(task, grant.attempt_id, grant.fencing_epoch, now)
            require(lease["agent_id"] == agent.agent_id and lease["provider_id"] == agent.provider_id, "AUTH_SCOPE_MISMATCH")
            self._eligible_for_phase(state, agent, task)
            lease["expires_at"] = max(lease["expires_at"], now + ttl_seconds)
            return {"status": "RENEWED", "lease": deepcopy(lease)}
        result = self._write(credential, command_id, "RENEW", {"grant": grant.to_dict(), "ttl": ttl_seconds}, mutate, needs_board=True)
        if result["status"] == "RENEWED":
            state = self.snapshot()
            task = state["tasks"][grant.task_id]
            if self._now() < state["meta"]["last_time"]:
                return {"status": "REJECTED", "error_code": "CLOCK_REGRESSION"}
            if (not self._board_ready or state["meta"]["board"] != "KNOWN"):
                return {"status": "REJECTED", "error_code": "BOARD_UNKNOWN"}
            if task.get("lease") != result["lease"] or result["lease"]["expires_at"] <= self._now():
                return {"status": "REJECTED", "error_code": "LATE_STALE_ATTEMPT"}
        return result

    def transition(self, credential, command_id, transition: StateTransition):
        def mutate(state, agent, now):
            t = transition
            require((t.agent_id, t.provider_id) == (agent.agent_id, agent.provider_id), "AUTH_SCOPE_MISMATCH")
            require(t.task_id in state["tasks"], "UNKNOWN_TASK")
            task = state["tasks"][t.task_id]
            lease = fence(task, t.attempt_id, t.fencing_epoch, now)
            require(task["spec_hash"] == t.spec_hash, "SPEC_MISMATCH")
            require(task["version"] == t.expected_version, "VERSION_CONFLICT")
            require(t.to_state in TRANSITIONS.get(task["status"], set()), "ILLEGAL_TRANSITION")
            require(lease["agent_id"] == agent.agent_id, "LEASE_OWNER_REQUIRED")
            require(task.get("lease_phase", "EXECUTION") ==
                    (task["status"] if task["status"] in AUTHORITY_STAGES else "EXECUTION"), "PHASE_AUTHORITY_REQUIRED")
            self._eligible_for_phase(state, agent, task)
            gate = GATE_ACTIONS.get(t.to_state)
            if gate:
                require(not any(n["type"] == "FAIL" and n["task_id"] == t.task_id
                                and n["spec_hash"] == t.spec_hash and n["commit_sha"] == task["candidate_commit"]
                                for n in state["notes"].values()), "CANDIDATE_RECHECK_REQUIRED")
                self._action(agent, gate)
                require(bool(t.evidence_refs), "MISSING_GATE_EVIDENCE")
                if t.to_state in {"QA_GREEN", "REVIEW_APPROVED"}:
                    author = state["agents"][task["author"]]
                    require(agent.agent_id != task["author"] and agent.independence_group != "UNVERIFIED"
                            and agent.independence_group != author["independence_group"], "INDEPENDENCE_REQUIRED")
            if t.to_state == "SUBMITTED":
                require(hex_hash(t.commit_sha, 40), "INVALID_COMMIT")
                task["candidate_commit"] = t.commit_sha
            elif task["candidate_commit"]:
                require(t.commit_sha == task["candidate_commit"], "STALE_COMMIT")
            if t.to_state == "QA_GREEN":
                require(t.evidence is not None and self.evidence_verifier is not None, "BLOCKED_EXECUTOR")
                evidence = ArtifactEvidence.from_dict(t.evidence)
                require(evidence.task_id == t.task_id and evidence.spec_hash == t.spec_hash
                        and evidence.commit_sha == task["candidate_commit"] and evidence.exit_code == 0
                        and evidence.runner_agent_id == agent.agent_id, "STALE_OR_FAILED_TEST")
                try:
                    verified = self.evidence_verifier(evidence) is True
                except Exception:
                    verified = False
                require(verified, "UNVERIFIED_RUNTIME_EVIDENCE")
                task["qa_evidence"] = evidence.to_dict()
            task["status"] = t.to_state
            task["version"] += 1
            if t.to_state in AUTHORITY_STAGES or t.to_state == "DONE":
                # Completing a phase revokes its token but preserves submitted/accepted facts.
                revoke_lease(task)
            elif t.to_state in {"FAILED", "BLOCKED"}:
                task["lease_phase"] = "EXECUTION"
            if t.to_state == "READY":
                invalidate(task)
            return {"status": "ACCEPTED", "task": deepcopy(task)}
        return self._write(credential, command_id, "TRANSITION", transition.to_dict(), mutate, needs_board=True)

    def publish(self, credential, command_id, event: Event):
        def mutate(state, agent, now):
            require((event.producer, event.provider_id) == (agent.agent_id, agent.provider_id), "AUTH_SCOPE_MISMATCH")
            require(set(event.target_agents) <= set(state["agents"]), "UNKNOWN_TARGET")
            if event.event_id in state["events"]:
                require(state["events"][event.event_id]["event"] == event.to_dict(), "EVENT_ID_COLLISION")
                return {"status": "DUPLICATE", "event_sha256": digest(event)}
            require(not event.causation_id or event.causation_id in state["events"], "CAUSATION_MISSING")
            state["events"][event.event_id] = {"event": event.to_dict(), "sha256": digest(event), "order": len(state["events"]) + 1}
            return {"status": "PUBLISHED", "event_sha256": digest(event)}
        return self._write(credential, command_id, "PUBLISH", event.to_dict(), mutate)

    @staticmethod
    def _target(state, event_id, agent_id):
        require(event_id in state["events"], "UNKNOWN_EVENT")
        entry = state["events"][event_id]
        require(agent_id in entry["event"]["target_agents"], "TARGET_DENIED")
        return entry

    def record_processing(self, credential, command_id, event_id, effect_ref):
        """Record sink-confirmed processing; remote sinks must deduplicate the returned key."""
        def mutate(state, agent, now):
            self._target(state, event_id, agent.agent_id)
            require(bool(effect_ref), "MISSING_PROCESSING_EVIDENCE")
            key = digest([event_id, agent.agent_id])
            if key in state["effects"]:
                require(state["effects"][key]["effect_ref"] == effect_ref, "EFFECT_COLLISION")
                return {"status": "ALREADY_PROCESSED", "idempotency_key": key}
            state["effects"][key] = {"event_id": event_id, "agent_id": agent.agent_id, "effect_ref": effect_ref}
            return {"status": "PROCESSED", "idempotency_key": key}
        return self._write(credential, command_id, "PROCESS", {"event_id": event_id, "effect_ref": effect_ref}, mutate)

    def ack(self, credential, command_id, ack: Ack):
        def mutate(state, agent, now):
            require((ack.agent_id, ack.provider_id) == (agent.agent_id, agent.provider_id), "AUTH_SCOPE_MISMATCH")
            entry = self._target(state, ack.event_id, agent.agent_id)
            require(ack.event_sha256 == entry["sha256"], "ACK_HASH_MISMATCH")
            key = digest([ack.event_id, agent.agent_id])
            require(key in state["effects"] and state["effects"][key]["effect_ref"] in ack.evidence_refs, "ACK_UNVERIFIED")
            if key in state["acks"]:
                return {"status": "DUPLICATE_ACK"}
            state["acks"][key] = ack.to_dict()
            # Never skip an earlier unacknowledged target event, even if ACKs arrive out of order.
            cause = entry["event"].get("causation_id")
            if cause:
                require(cause in state["events"], "CAUSATION_MISSING")
                if agent.agent_id in state["events"][cause]["event"]["target_agents"]:
                    require(digest([cause, agent.agent_id]) in state["acks"], "CAUSATION_NOT_ACKED")
            source = entry["event"]["source"]
            cursor = 0
            for e in state["events"].values():
                if e["event"]["source"] != source or agent.agent_id not in e["event"]["target_agents"]:
                    continue
                if digest([e["event"]["event_id"], agent.agent_id]) not in state["acks"]:
                    break
                cursor = e["order"]
            state["cursors"][digest([agent.agent_id, source])] = cursor
            return {"status": "ACK_RECORDED", "cursor": cursor}
        return self._write(credential, command_id, "ACK", ack.to_dict(), mutate)

    def put_note(self, credential, command_id, note: MemoryNote):
        return self._immutable(credential, command_id, "NOTE", "notes", note.note_id, note)

    def save_handoff(self, credential, command_id, handoff: Handoff):
        # Stale handoffs remain history; resume must check current lease before acting.
        return self._immutable(credential, command_id, "HANDOFF", "handoffs", handoff.handoff_id, handoff)

    def _immutable(self, credential, command_id, kind, collection, key, value):
        def mutate(state, agent, now):
            require((value.agent_id, value.provider_id) == (agent.agent_id, agent.provider_id), "AUTH_SCOPE_MISMATCH")
            require(value.task_id in state["tasks"] and state["tasks"][value.task_id]["spec_hash"] == value.spec_hash, "SPEC_MISMATCH")
            data = value.to_dict()
            if key in state[collection]:
                require(state[collection][key] == data, "IMMUTABLE_COLLISION")
                return {"status": "DUPLICATE"}
            state[collection][key] = data
            return {"status": "STORED"}
        return self._write(credential, command_id, kind, value.to_dict(), mutate)

    def snapshot(self):
        try:
            return self.backend.snapshot()
        except Exception:
            self._board_ready = False
            raise

    def board(self):
        projection = board_projection(self.snapshot())
        if not self._board_ready:
            projection["board_status"] = "UNKNOWN"
        return projection

    def ready_tasks(self, credential):
        session = self._session(credential)
        state = self.snapshot()
        require(self._board_ready and state["meta"]["board"] == "KNOWN", "BOARD_UNKNOWN")
        agent = self._agent(state, session)
        registry = AgentRegistry([AgentRegistration.from_dict(a) for a in state["agents"].values()], simulation=self.simulation)
        ready = []
        for task in state["tasks"].values():
            if task["status"] != "READY" or not dependencies_done(task, state["tasks"]):
                continue
            try:
                registry.eligible(agent, task)
            except CoreError:
                continue
            ready.append(deepcopy(task))
        # Priority aging prevents an endless stream of newer high-priority work starving old work.
        now = self._now()
        return sorted(ready, key=lambda t: (-(t["priority"] + int((now - t["created_at"]) // 300)), t["created_at"], t["task_id"]))

    def recover(self, credential, command_id):
        def mutate(state, agent, now):
            self._action(agent, "controller_admin")
            return {"status": "RECOVERED", "projection": board_projection(state)}
        return self._write(credential, command_id, "RECOVER", {}, mutate)
