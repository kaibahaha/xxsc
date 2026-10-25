"""Executable LOCAL simulation for reviewers. Does not invoke providers or schedulers."""
from pathlib import Path
from tempfile import TemporaryDirectory
import json
from ..controller import Controller
from ..events import pending_deliveries
from ..leases import SQLiteLeaseBackend
from ..registry import AgentRegistry
from ..replay import rebuild
from ..schemas import AgentRegistration, ClaimProposal, Event, ProviderSession, TaskSpec


def main():
    agents = [AgentRegistration(agent_id=f"demo-{i}", provider_id=f"mock-provider-{i}", account_scope="demo",
        adapter_id="mock", credential_principal=f"mock-principal-{i}", capabilities=("develop",),
        allowed_reads=("demo",), allowed_writes=("demo",), desired_enabled=True,
        admission_status="MOCK_ACTIVE", health="HEALTHY", allowed_actions=("task_admin", "controller_admin")) for i in range(2)]
    credentials = {f"local-demo-credential-{i}": ProviderSession(agent_id=a.agent_id, provider_id=a.provider_id,
        principal=a.credential_principal, account_scope=a.account_scope) for i, a in enumerate(agents)}
    with TemporaryDirectory() as tmp:
        backend = SQLiteLeaseBackend(Path(tmp) / "local.sqlite")
        registry = AgentRegistry(agents, simulation=True)
        c = Controller(backend, registry, credentials.__getitem__)
        credential = "local-demo-credential-0"
        spec = "a" * 64
        assert c.add_tasks(credential, "task", [TaskSpec(task_id="DEMO", spec_hash=spec, write_paths=("demo/result",))])["status"] == "CREATED"
        assert c.reconcile_board(credential, "board", c.board_digest())["status"] == "RECONCILED"
        result = c.claim(credential, "claim", ClaimProposal(task_id="DEMO", agent_id="demo-0", provider_id="mock-provider-0",
            run_id="demo-run", spec_hash=spec, attempt_id="demo-attempt", expected_version=1))
        assert result["status"] == "GRANTED"
        event = Event(event_id="demo-event", producer="demo-0", provider_id="mock-provider-0", target_agents=("demo-1",),
            task_id="DEMO", kind="HANDOFF_READY", summary="local demonstration", observed_at="2026-10-25T00:00:00Z",
            raw_ref="mock://demo", run_id="demo-run")
        assert c.publish(credential, "event", event)["status"] == "PUBLISHED"
        assert c.record_processing("local-demo-credential-1", "processing", "demo-event", "mock://sink-receipt")["status"] == "PROCESSED"
        fresh = Controller(backend, registry, credentials.__getitem__)
        assert rebuild(backend.records()) == fresh.snapshot()
        delivery = pending_deliveries(fresh.snapshot(), "demo-1")
        assert delivery[0]["action"] == "ACK_ONLY"
        print(json.dumps({"mode": "LOCAL_SIMULATION", "authority": backend.authority,
            "lease_status": result["status"], "fencing_epoch": result["lease"]["fencing_epoch"],
            "replay_equal": True, "after_restart_delivery_action": delivery[0]["action"],
            "fresh_board_status": fresh.board()["board_status"], "cloud_deployment": "NOT_DEPLOYED"}, indent=2))


if __name__ == "__main__":
    main()
