"""Read-only reliability audit, including relay grace without inventing native failures."""
from .events import pending_deliveries
from .replay import rebuild
from .schemas import digest


def audit(records, *, now):
    state = rebuild(records)
    return {"record_count": len(records), "head_hash": records[-1]["record_hash"] if records else "0" * 64,
            "state_sha256": digest(state),
            "expired_orphans": [k for k, t in state["tasks"].items()
                                if t.get("lease") and t["lease"]["expires_at"] <= now],
            "delivery_gaps": {a: pending_deliveries(state, a) for a in state["agents"]},
            "denials": [r["result"] for r in records if r["result"].get("status") == "REJECTED"]}


def relay_eligibility(*, source_verified, source_ready_at, native_attempt_at,
                      native_outcome, grace_until, target_missing_verified, now):
    eligible = bool(source_verified and source_ready_at is not None and grace_until is not None
                    and now >= grace_until and target_missing_verified)
    return {"eligible": eligible, "native_outcome": native_outcome or "UNKNOWN",
            "native_attempt_at": native_attempt_at, "source_ready_at": source_ready_at,
            "grace_until": grace_until}
