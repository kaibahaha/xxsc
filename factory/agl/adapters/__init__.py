"""M06 adapter package: provider adapters, registry view, admission gate."""

from .base import AgentAdapter
from .github_mailbox import AdapterContext, GitHubMailboxAdapter, parse_task_markdown
from .providers import (
    ChatGptAdapter,
    CodexAdapter,
    CustomAdapter,
    WorkBuddyAdapter,
    build_adapter,
    capability_matrix,
)
from .registry_view import (
    AgentRecord,
    RegistryView,
    ValidationIssue,
    ValidationReport,
    validate_config,
)
from .types import (
    OPS,
    AdmissionDecision,
    CapabilityItem,
    CapabilityProbe,
    CapState,
    HealthObservation,
    ReadResult,
    ScheduleObservation,
)

__all__ = [
    "AgentAdapter",
    "AdapterContext",
    "GitHubMailboxAdapter",
    "parse_task_markdown",
    "ChatGptAdapter",
    "CodexAdapter",
    "CustomAdapter",
    "WorkBuddyAdapter",
    "build_adapter",
    "capability_matrix",
    "AgentRecord",
    "RegistryView",
    "ValidationIssue",
    "ValidationReport",
    "validate_config",
    "OPS",
    "AdmissionDecision",
    "CapabilityItem",
    "CapabilityProbe",
    "CapState",
    "HealthObservation",
    "ReadResult",
    "ScheduleObservation",
]
