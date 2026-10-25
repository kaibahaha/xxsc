"""Application-level errors. Do not change public names or inheritance."""

class LedgerError(Exception):
    """Base class for application failures."""


class InvalidRequest(LedgerError, ValueError):
    """Input fails schema or numeric bounds validation."""


class NotFound(LedgerError, LookupError):
    """Referenced account does not exist."""


class Conflict(LedgerError):
    """Idempotency collision, duplicate account, or recipient overflow."""


class InsufficientFunds(LedgerError):
    """A debit cannot be funded without a negative balance."""


class InvariantViolation(LedgerError):
    """Persisted accounting state violates an invariant."""
