# R01 contract freeze — schema 2.0

Import with `from factory.agl.contracts import ...`; all data types are keyword-only
frozen dataclasses in `schemas.py`, with `to_dict` / `from_dict`. JSON is canonical
UTF-8 with sorted keys, no whitespace, no NaN. Lists are serialized JSON arrays.
Event producer is the agent identity; `provider_id` is separately bound by authentication.
No input `agent_id`, status, evidence reference or JSON flag proves authentication.

Core credentials go to an injected Authenticator; it must validate a real credential
and return ProviderSession. Do not expose this trusted in-process boundary directly
as a client-controlled session object. Registry admin can change admission only after
actual probe evidence is verified by the integration service. Local tests use mock identities.

ProviderAdapter operations return `status` from SUPPORTED/UNSUPPORTED/UNKNOWN/BLOCKED
plus operation-specific evidence. Git receipts carry repo/ref/path/blob_sha/commit_sha/
hash/error_code. UNKNOWN_WRITE requires read-only reconciliation before retry.
These Protocols freeze signatures, not an implemented Git transport.

LeaseGrant is local authority only after atomic commit. Before cross-cloud execution,
WorkBuddy must publish and independently reread its authoritative grant. There is no
cloud grant/publish implementation in R01. Cloud deployment remains BLOCKED_ATOMIC_LEASE.
ACK is per `(event_id, agent_id)` and requires a stored processing receipt and matching
event digest. External effects need the same idempotency key at their own sink; core
cannot make a remote HTTP effect exactly-once with a local database transaction.

V4.1 JSON Schemas remain read-only; `schemas.import_v41` provides an explicit boundary
for Task/Event/Receipt/Note. Legacy payloads are not directly executable grants.
M02/M06/M08/M10 implementations, CLI, packaging and scheduling remain WorkBuddy-owned.
