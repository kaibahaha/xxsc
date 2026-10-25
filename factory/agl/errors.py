"""Typed error taxonomy for the adapter plane.

The workorder requires distinct, machine-readable outcomes instead of generic
exceptions:

    NO_PERMISSION / NOT_FOUND / CONFLICT / UNKNOWN_WRITE / RATE_LIMITED
    BLOCKED_EXECUTOR / BLOCKED_PROVIDER / CONTROLLER_UNAVAILABLE / STALE_TEST

Every error message is passed through :func:`redact` so that a leaked token can
never end up in logs, receipts or Git commits.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Iterable


class ErrorCode(str, Enum):
    OK = "OK"
    # Git / transport
    NO_PERMISSION = "NO_PERMISSION"
    NOT_FOUND = "NOT_FOUND"
    CONFLICT = "CONFLICT"
    COLLISION = "COLLISION"          # same event_id, different payload
    UNKNOWN_WRITE = "UNKNOWN_WRITE"  # write may or may not have landed
    RATE_LIMITED = "RATE_LIMITED"
    TRANSIENT = "TRANSIENT"
    AUTH_MISSING = "AUTH_MISSING"
    # adapter / provider
    BLOCKED_PROVIDER = "BLOCKED_PROVIDER"
    PROBE_PENDING = "PROBE_PENDING"
    ADMISSION_DENIED = "ADMISSION_DENIED"
    DRAINING = "DRAINING"
    # execution
    BLOCKED_EXECUTOR = "BLOCKED_EXECUTOR"
    STALE_TEST = "STALE_TEST"
    EXEC_TIMEOUT = "EXEC_TIMEOUT"
    # config / core
    SCHEMA_INVALID = "SCHEMA_INVALID"
    DUPLICATE_AGENT_ID = "DUPLICATE_AGENT_ID"
    N_TOO_SMALL = "N_TOO_SMALL"
    ACTIVE_MISMATCH = "ACTIVE_MISMATCH"
    PROVIDER_QUOTA_EXCEEDED = "PROVIDER_QUOTA_EXCEEDED"
    INVALID_TIMEZONE = "INVALID_TIMEZONE"
    PATH_NOT_WHITELISTED = "PATH_NOT_WHITELISTED"
    CONTROLLER_UNAVAILABLE = "CONTROLLER_UNAVAILABLE"
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"
    INVALID_INPUT = "INVALID_INPUT"


RETRYABLE = {
    ErrorCode.TRANSIENT,
    ErrorCode.RATE_LIMITED,
    ErrorCode.UNKNOWN_WRITE,  # retry only through reconcile, never blind
}


@dataclass
class AglError(Exception):
    code: ErrorCode
    message: str
    detail: dict[str, Any] = field(default_factory=dict)
    retryable: bool = False

    def __post_init__(self) -> None:
        self.message = redact(self.message)
        self.retryable = self.retryable or self.code in RETRYABLE
        super().__init__(f"{self.code.value}: {self.message}")

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code.value,
            "message": self.message,
            "detail": {k: redact(str(v)) for k, v in self.detail.items()},
            "retryable": self.retryable,
        }


_TOKEN_PATTERNS = (
    re.compile(r"(gh[pousr]_[A-Za-z0-9]{16,})"),
    re.compile(r"(github_pat_[A-Za-z0-9_]{20,})"),
    re.compile(r"(?i)(authorization:\s*(?:bearer|token)\s+)(\S+)"),
    re.compile(r"(?i)(token=)([^&\s]+)"),
)


def redact(text: str, secrets: Iterable[str] = ()) -> str:
    """Mask credentials in any user-visible string."""
    if not text:
        return text
    out = text
    for secret in secrets:
        if secret and len(secret) >= 8:
            out = out.replace(secret, "***REDACTED***")
    for pattern in _TOKEN_PATTERNS:
        if pattern.groups >= 2:
            out = pattern.sub(lambda m: m.group(1) + "***REDACTED***", out)
        else:
            out = pattern.sub("***REDACTED***", out)
    return out


def ensure(condition: bool, code: ErrorCode, message: str, **detail: Any) -> None:
    if not condition:
        raise AglError(code, message, detail)
