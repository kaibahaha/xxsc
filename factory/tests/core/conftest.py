from dataclasses import replace
from pathlib import Path
import pytest
from factory.agl.controller import Controller
from factory.agl.leases import SQLiteLeaseBackend
from factory.agl.registry import AgentRegistry
from factory.agl.schemas import AgentRegistration, ClaimProposal, ProviderSession, TaskSpec

SPEC = "a" * 64
COMMIT = "b" * 40


class Clock:
    def __init__(self):
        self.value = 1800000000.0
    def __call__(self):
        return self.value


def agent(i, **kw):
    values = dict(agent_id=f"agent-{i}", provider_id=("chatgpt", "workbuddy", "codex")[i % 3],
        account_scope=f"account-{i % 3}", adapter_id="mock_mailbox", credential_principal=f"principal-{i}",
        capabilities=("develop", "test"), allowed_reads=("factory",), allowed_writes=("factory/owned",),
        allowed_actions=("controller_admin", "registry_admin", "task_admin", "qa", "review", "integrate", "accept"),
        desired_enabled=True, admission_status="MOCK_ACTIVE", health="HEALTHY", independence_group=f"group-{i}")
    values.update(kw)
    return AgentRegistration(**values)


def authenticator(credential):
    # Test-only opaque credential mapping. Caller-supplied ProviderSession is rejected.
    if not isinstance(credential, str) or not credential.startswith("secret-for-"):
        raise ValueError("bad credential")
    i = int(credential.removeprefix("secret-for-"))
    a = agent(i)
    return ProviderSession(agent_id=a.agent_id, provider_id=a.provider_id, principal=a.credential_principal, account_scope=a.account_scope)


def token(i=0):
    return f"secret-for-{i}"


def reconcile(c, key="board"):
    return c.reconcile_board(token(), key, c.board_digest())


def spec(task_id="T", **kw):
    return TaskSpec(task_id=task_id, spec_hash=SPEC, required_capabilities=("develop",), write_paths=("factory/owned/code.py",), **kw)


def proposal(i=0, task_id="T", version=1, **kw):
    values = dict(task_id=task_id, agent_id=f"agent-{i}", provider_id=agent(i).provider_id,
        run_id=f"run-{i}", spec_hash=SPEC, attempt_id=f"attempt-{i}", expected_version=version)
    values.update(kw)
    return ClaimProposal(**values)


@pytest.fixture
def core(tmp_path):
    clock = Clock()
    registry = AgentRegistry([agent(i) for i in range(3)], simulation=True)
    backend = SQLiteLeaseBackend(tmp_path / "core.sqlite")
    c = Controller(backend, registry, authenticator, clock=clock)
    assert c.add_tasks(token(), "tasks", [spec()])["status"] == "CREATED"
    assert reconcile(c)["status"] == "RECONCILED"
    return c, clock, registry
