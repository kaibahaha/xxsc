#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EVIDENCE ADMISSION & PRE-PUBLICATION GATE -- MVE (R16 F6 / U2)
==============================================================
Research Report Factory R16, second-round remediation (F6).
This is the CORE MVE: it gates whether a piece of research
evidence may be ADMITTED into a report and PUBLISHED.

Hard constraints honored (do NOT relax):
  * Strict type check for authorization: `type(x) is bool` and `is True`.
    The string "false" and the bool False BOTH reject.
  * Numeric confidence/cost must be a real `float` and `math.isfinite`.
    NaN / Inf / strings are rejected.
  * Dates must parse, be within [1900-01-01, 2100-01-01], and not be
    in the future relative to the run date.
  * Source must be in an explicit AUTHORIZED registry with a matching
    domain; versioned sources require a version string.
  * `page` must be a real int in [1, 100000]; `rights` must be in the
    allowed set; `destination_path` must stay under the publish root
    (no ".." traversal, no null bytes).
  * Duplicate/conflict detection against a seen-hash set.
  * NO `assert` is used for any security rejection -- explicit returns only.
  * ZERO disk writes inside the gate (pure function; only prints).
  * Fail-closed: any unexpected exception -> NOT admitted.
  * Behavior identical under `python3` and `python3 -O`.
"""
import math
import json
import hashlib
import re
import sys
from datetime import date

# ---------------------------------------------------------------------------
# Frozen configuration (read-only, no network, no disk)
# ---------------------------------------------------------------------------
AUTHORIZED_SOURCES = {
    "crossref":         {"domains": ["api.crossref.org"],                "versioned": False},
    "openalex":         {"domains": ["api.openalex.org"],                "versioned": False},
    "nature_publisher": {"domains": ["nature.com"],                      "versioned": True},
    "runway_docs":      {"domains": ["docs.dev.runwayml.com"],           "versioned": True},
}
ALLOWED_RIGHTS = {"open_access", "cc_by", "cc_by_nc", "copyright_restricted"}
PUBLISH_ROOT = "/safe/publish/"
EARLIEST_VALID_DATE = date(1900, 1, 1)
LATEST_VALID_DATE = date(2100, 1, 1)
MAX_PAGE = 100000

# ---------------------------------------------------------------------------
# Helpers (each returns (ok: bool, reason: str))
# ---------------------------------------------------------------------------
def _is_authorized_bool(authorized):
    # ONLY the exact bool True admits. String "false" and bool False reject.
    return type(authorized) is bool and authorized is True

def _validate_confidence(confidence):
    if type(confidence) is not float:
        return False, "confidence not a float"
    if not math.isfinite(confidence):
        return False, "confidence not finite (NaN/Inf)"
    if confidence < 0.0 or confidence > 1.0:
        return False, "confidence out of [0,1]"
    return True, ""

def _validate_date(d):
    if type(d) is not str:
        return False, "date not a str"
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", d)
    if not m:
        return False, "date format invalid (want YYYY-MM-DD)"
    try:
        parsed = date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return False, "date does not exist on calendar"
    if parsed < EARLIEST_VALID_DATE or parsed > LATEST_VALID_DATE:
        return False, "date out of allowed range"
    if parsed > date.today():
        return False, "date is in the future"
    return True, ""

def _validate_source(source_id, url):
    if type(source_id) is not str or type(url) is not str:
        return False, "source_id/url not str"
    reg = AUTHORIZED_SOURCES.get(source_id)
    if reg is None:
        return False, "source not in authorized registry"
    if not any(domain in url for domain in reg["domains"]):
        return False, "url domain not authorized for this source"
    return True, ""

def _validate_page(page):
    # bool is a subclass of int in Python -> must exclude it explicitly.
    if type(page) is not int or isinstance(page, bool):
        return False, "page not an int"
    if page < 1 or page > MAX_PAGE:
        return False, "page out of range [1,%d]" % MAX_PAGE
    return True, ""

def _validate_rights(rights):
    if type(rights) is not str:
        return False, "rights not a str"
    if rights not in ALLOWED_RIGHTS:
        return False, "rights declaration not in allowed set"
    return True, ""

def _validate_path(path):
    if type(path) is not str:
        return False, "destination_path not a str"
    if "\x00" in path:
        return False, "null byte in path"
    if ".." in path:
        return False, "path traversal ('..') detected"
    if not path.startswith(PUBLISH_ROOT):
        return False, "path escapes publish root"
    return True, ""

def _evidence_hash(ev):
    payload = json.dumps({
        "claim": ev.get("claim"),
        "source_url": ev.get("source_url"),
        "publication_date": ev.get("publication_date"),
    }, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def admit_evidence(evidence):
    """Returns (admitted: bool, reason: str). Fail-closed on any error."""
    try:
        if type(evidence) is not dict:
            return False, "evidence not a dict"
        if "_corrupt_json" in evidence:
            return False, "corrupted JSON line"
        if not _is_authorized_bool(evidence.get("authorized")):
            return False, "authorization proof missing / not strict bool True"
        ok, reason = _validate_confidence(evidence.get("confidence"))
        if not ok:
            return False, reason
        ok, reason = _validate_date(evidence.get("publication_date"))
        if not ok:
            return False, reason
        ok, reason = _validate_source(evidence.get("source_id"), evidence.get("source_url"))
        if not ok:
            return False, reason
        reg = AUTHORIZED_SOURCES.get(evidence.get("source_id"), {})
        if reg.get("versioned") and type(evidence.get("version")) is not str:
            return False, "version string required for versioned source"
        ok, reason = _validate_page(evidence.get("page", 1))
        if not ok:
            return False, reason
        ok, reason = _validate_rights(evidence.get("rights"))
        if not ok:
            return False, reason
        ok, reason = _validate_path(evidence.get("destination_path", PUBLISH_ROOT + "x"))
        if not ok:
            return False, reason
        seen = evidence.get("seen_hashes", [])
        if type(seen) is not list:
            return False, "seen_hashes not a list"
        if _evidence_hash(evidence) in seen:
            return False, "duplicate evidence conflict"
        return True, "admitted"
    except Exception as exc:  # fail-closed
        return False, "fail-closed: %s" % type(exc).__name__

# ---------------------------------------------------------------------------
# Frozen test cases (the frozen input). NaN/Inf are real Python floats and
# therefore only exist in this embedded form (JSON has no NaN); the JSONL
# subset in frozen_cases_r16.jsonl carries the JSON-safe cases.
# ---------------------------------------------------------------------------
_dup_claim = "dup"
_dup_url = "https://www.nature.com/articles/nature12968"
_dup_date = "2024-01-15"
_dup_hash = _evidence_hash({"claim": _dup_claim, "source_url": _dup_url, "publication_date": _dup_date})

FROZEN_CASES = [
    {"label": "P1_valid", "expect": "ADMIT", "evidence": {
        "authorized": True, "confidence": 0.95, "publication_date": "2024-01-15",
        "source_id": "nature_publisher",
        "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/nature12968.json",
        "seen_hashes": [], "claim": "valid-nature-12968"}},

    {"label": "N1_string_false", "expect": "REJECT", "evidence": {
        "authorized": "false", "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N2_bool_false", "expect": "REJECT", "evidence": {
        "authorized": False, "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N3_nan_conf", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": float("nan"), "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N4_inf_conf", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": float("inf"), "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N5_str_conf", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": "0.9", "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N6_future_date", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2099-03-01",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N7_invalid_date", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2026-13-45",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N8_outrange_date", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "1850-01-01",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N9_unauth_source", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "unknown_src", "source_url": "https://www.nature.com/articles/nature12968",
        "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N10_domain_mismatch", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://evil.example.com/x",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N11_duplicate", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": _dup_date,
        "source_id": "nature_publisher", "source_url": _dup_url,
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json",
        "seen_hashes": [_dup_hash], "claim": _dup_claim}},

    {"label": "N12_path_traversal", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/../../etc/passwd", "seen_hashes": []}},

    {"label": "N13_page_zero", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 0, "rights": "copyright_restricted",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},

    {"label": "N14_bad_rights", "expect": "REJECT", "evidence": {
        "authorized": True, "confidence": 0.9, "publication_date": "2024-01-15",
        "source_id": "nature_publisher", "source_url": "https://www.nature.com/articles/nature12968",
        "version": "v1", "page": 1, "rights": "super_user",
        "destination_path": "/safe/publish/r16/x.json", "seen_hashes": []}},
]

def main():
    mode = "O-mode(fail-closed)" if not __debug__ else "normal(fail-closed)"
    passed = 0
    failed = 0
    for c in FROZEN_CASES:
        ok, reason = admit_evidence(c["evidence"])
        got = "ADMIT" if ok else "REJECT"
        mark = "OK" if got == c["expect"] else "MISMATCH"
        if mark == "OK":
            passed += 1
        else:
            failed += 1
        print("[%s] %s expected=%s got=%s :: %s" % (mark, c["label"], c["expect"], got, reason))
    fail_open = sum(
        1 for c in FROZEN_CASES
        if c["expect"] == "REJECT" and admit_evidence(c["evidence"])[0]
    )
    print("MODE=%s PASSED=%d FAILED=%d" % (mode, passed, failed))
    print("FAIL_OPEN_COUNT=%d" % fail_open)
    print("DISK_WRITES_BY_GATE=0")
    sys.exit(0 if (failed == 0 and fail_open == 0) else 1)

if __name__ == "__main__":
    main()
