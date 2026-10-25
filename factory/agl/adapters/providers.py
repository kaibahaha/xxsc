"""Provider-specific adapters.

Each class only narrows capabilities compared with a successful mailbox probe.
Nothing in this file may claim a capability that no real call established:

===========  ======  =====  =======  =======  ========  ========
provider     read    write  reread   trigger  execute   schedule
===========  ======  =====  =======  =======  ========  ========
chatgpt      probe   NO     n/a      NO       NO        UNKNOWN
workbuddy    probe   probe  probe    NO*      runner?   UNKNOWN
codex        probe   probe  probe    NO       UNKNOWN   UNKNOWN
custom       declared->UNKNOWN until probed
===========  ======  =====  =======  =======  ========  ========

``probe`` means the state comes from an actual call (write probe into the
agent's own outbox). ``NO`` means structurally unsupported for that platform in
this deployment. ``runner?`` means SUPPORTED only when a real runner is
available, otherwise BLOCKED_EXECUTOR.

\* a webhook is only reported if one was explicitly configured *and* verified;
configuring a URL is not evidence that it fires.
"""

from __future__ import annotations

from typing import Any

from ..storage.github import utc_now
from .github_mailbox import AdapterContext, GitHubMailboxAdapter
from .registry_view import AgentRecord
from .types import CapState, CapabilityItem


class ChatGptAdapter(GitHubMailboxAdapter):
    """ChatGPT scheduled workbench: reads the repository, never writes it."""

    provider_id = "chatgpt"
    supports_publish = False

    def probe(self, principal=None, scope=None):
        probe = super().probe(principal, scope)
        items = dict(probe.items)
        items["write"] = self._item(
            "write", CapState.UNSUPPORTED,
            "chat connector has no repository write API in this deployment; "
            "outputs are produced as TEST_REQUEST / notes for a runner to commit",
            method="STATIC",
        )
        items["reread"] = self._item(
            "reread", CapState.UNSUPPORTED, "nothing written by this adapter", method="STATIC"
        )
        items["trigger"] = self._item(
            "trigger", CapState.UNSUPPORTED,
            "provider offers no webhook/API to wake a scheduled chat task",
            method="STATIC",
        )
        items["execute"] = self._item(
            "execute", CapState.UNSUPPORTED,
            "chat sessions have no verified shell/CI execution tool",
            method="STATIC",
        )
        return type(probe)(
            agent_id=probe.agent_id, provider_id=probe.provider_id,
            adapter_id=probe.adapter_id, items=items, probed_at=utc_now(),
            transport=probe.transport,
        )


class WorkBuddyAdapter(GitHubMailboxAdapter):
    """WorkBuddy cloud/IDE session: may write its own outbox and run code."""

    provider_id = "workbuddy"

    def _execute_item(self) -> CapabilityItem:
        if self.ctx.runner_available:
            return self._item(
                "execute", CapState.SUPPORTED,
                "local/cloud runner available for TEST_REQUEST execution",
                method="REAL", evidence="runner:local-subprocess",
            )
        return self._item(
            "execute", CapState.BLOCKED,
            "no runner bound to this session -> BLOCKED_EXECUTOR",
            method="STATIC",
        )

    def _trigger_item(self) -> CapabilityItem:
        if self.ctx.webhook_url:
            return self._item(
                "trigger", CapState.UNKNOWN,
                f"webhook configured at {self.ctx.webhook_url} but never observed firing",
                method="STATIC",
            )
        return self._item(
            "trigger", CapState.UNSUPPORTED,
            "no webhook receiver verified; Git mailbox + own cadence only",
            method="STATIC",
        )


class CodexAdapter(GitHubMailboxAdapter):
    """Codex: independent developer; credentials here are not assumed."""

    provider_id = "codex"

    def _execute_item(self) -> CapabilityItem:
        return self._item(
            "execute", CapState.UNKNOWN,
            "Codex cloud execution exists on its own platform; no verified endpoint from here",
            method="STATIC",
        )


class CustomAdapter(GitHubMailboxAdapter):
    """Any future provider: declared in config, verified only by probing."""

    def __init__(self, record: AgentRecord, ctx: AdapterContext, provider_id: str) -> None:
        super().__init__(record, ctx)
        self.provider_id = provider_id

    def _execute_item(self) -> CapabilityItem:
        return self._item(
            "execute", CapState.UNKNOWN,
            f"custom provider {self.provider_id}: execution not probed",
            method="STATIC",
        )


_PROVIDERS = {
    "chatgpt": ChatGptAdapter,
    "workbuddy": WorkBuddyAdapter,
    "codex": CodexAdapter,
}


def build_adapter(record: AgentRecord, ctx: AdapterContext) -> GitHubMailboxAdapter:
    cls = _PROVIDERS.get(record.provider_id)
    if cls is None:
        return CustomAdapter(record, ctx, record.provider_id)
    return cls(record, ctx)


def capability_matrix(probes: list[Any]) -> dict[str, dict[str, str]]:
    """Compact provider x operation matrix used by the delivery document."""
    from .types import OPS

    matrix: dict[str, dict[str, str]] = {}
    for probe in probes:
        row = {op: probe.items[op].state.value if op in probe.items else "UNKNOWN" for op in OPS}
        key = f"{probe.provider_id}:{probe.agent_id}"
        matrix[key] = row
    return matrix
