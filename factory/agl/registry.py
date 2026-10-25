"""Dynamic identities and provider/account scoped admission; no global upper bound."""
from dataclasses import replace
from collections import Counter
from .schemas import AgentRegistration, CoreError, ProviderSession, require


def path_allowed(path: str, prefixes) -> bool:
    return any(path == p or path.startswith(p + "/") for p in prefixes)


class AgentRegistry:
    def __init__(self, agents, *, simulation: bool = False, quotas=()):
        self.simulation = simulation
        self.quotas = list(quotas)
        self.agents = {}
        for agent in agents:
            self.register(agent)
        require(sum(a.desired_enabled for a in self.agents.values()) >= 2, "POOL_BELOW_TWO")

    def register(self, agent: AgentRegistration):
        require(agent.agent_id not in self.agents, "DUPLICATE_AGENT")
        self.agents[agent.agent_id] = agent
        try:
            self.check_quotas()
        except CoreError:
            del self.agents[agent.agent_id]
            raise

    def check_quotas(self):
        counts = Counter((a.provider_id, a.account_scope) for a in self.agents.values() if a.desired_enabled)
        for policy in self.quotas:
            require(type(policy.get("capacity_verified")) is bool, "INVALID_QUOTA")
            if policy["capacity_verified"]:
                capacity, reserved = policy.get("capacity"), policy.get("reserved", 0)
                require(type(capacity) is int and type(reserved) is int and 0 <= reserved <= capacity, "INVALID_QUOTA")
                require(counts[policy["provider_id"], policy["account_scope"]] <= capacity - reserved, "PROVIDER_QUOTA_EXCEEDED")

    def authenticate(self, session: ProviderSession) -> AgentRegistration:
        agent = self.agents.get(session.agent_id)
        require(agent is not None, "UNKNOWN_AGENT")
        require((agent.provider_id, agent.account_scope, agent.credential_principal) ==
                (session.provider_id, session.account_scope, session.principal), "AUTH_SCOPE_MISMATCH")
        return agent

    def eligible(self, agent: AgentRegistration, task: dict):
        admitted = {"ADMITTED_ACTIVE"} | ({"MOCK_ACTIVE"} if self.simulation else set())
        require(agent.desired_enabled and agent.admission_status in admitted and agent.health == "HEALTHY", "AGENT_NOT_ADMITTED")
        require(not task["allowed_agents"] or agent.agent_id in task["allowed_agents"], "TASK_AGENT_DENIED")
        require(set(task["required_capabilities"]) <= set(agent.capabilities), "CAPABILITY_DENIED")
        require(all(path_allowed(p, agent.allowed_reads) for p in task["read_paths"]), "READ_PATH_DENIED")
        require(all(path_allowed(p, agent.allowed_writes) for p in task["write_paths"]), "PATH_DENIED")

    def draining(self, agent_id: str):
        self.agents[agent_id] = replace(self.agents[agent_id], admission_status="DRAINING")
