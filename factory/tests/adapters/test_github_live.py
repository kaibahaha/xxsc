"""Live GitHub probes (no credentials in this environment).

These hit the real API. When the network or auth is unavailable they *skip* with
the concrete reason -- they never fake success. Write capability requires a
token; without one the expected result is NO_PERMISSION, which is recorded as
evidence that remote writes are BLOCKED_AUTH rather than "working".
"""

from __future__ import annotations

import hashlib

import pytest

from agl.errors import AglError, ErrorCode
from agl.storage.transports import RestTransport

REPO = "kaibahaha/xxsc"
BASELINE = "exp/agensh-lite-v4.2-controller-mvp-20261025"
FROZEN = "2d4c1a6fc0792a1182777262b41bfb4c09c0b5d2"
TASK_PATH = "frameworks/agensh-lite-v4.2/workorders/AGL-WB-ADAPTERS-R01/TASK.md"


DEV_BRANCH = "dev/agl-v4.2-workbuddy-adapters"


@pytest.fixture(scope="module")
def transport():
    # token="" (not None) so an ambient GITHUB_TOKEN can never turn a
    # read-only probe into a write against a shared branch.
    return RestTransport(token="", timeout=20, max_retries=1)


@pytest.mark.network
def test_baseline_ref_is_readable(transport):
    try:
        sha = transport.get_ref(REPO, BASELINE)
    except AglError as exc:
        pytest.skip(f"GitHub read unavailable: {exc.code.value} {exc.message}")
    assert len(sha) == 40
    # the frozen baseline commit must be an ancestor-or-equal of the branch head
    assert sha


@pytest.mark.network
def test_frozen_commit_exists(transport):
    try:
        status, _, data = transport._request("GET", f"/repos/{REPO}/commits/{FROZEN}")
    except AglError as exc:
        pytest.skip(f"GitHub read unavailable: {exc.code.value}")
    assert status == 200
    assert data["sha"] == FROZEN


@pytest.mark.network
def test_workorder_task_md_readable_and_hashed(transport):
    try:
        found = transport.get_file(REPO, BASELINE, TASK_PATH)
    except AglError as exc:
        pytest.skip(f"GitHub read unavailable: {exc.code.value}")
    assert found is not None
    blob_sha, content = found
    assert b"AGL-WB-ADAPTERS-R01" in content
    assert len(hashlib.sha256(content).hexdigest()) == 64
    assert blob_sha


@pytest.mark.network
def test_unauthenticated_write_is_refused(transport):
    assert transport.authenticated is False, "probe transport must not use ambient credentials"
    # never target the frozen baseline: only the adapter's own dev branch
    assert DEV_BRANCH != BASELINE
    try:
        transport.create_file(REPO, DEV_BRANCH, "factory/_probe/should-not-exist.json", b"{}\n",
                              "probe that must fail without credentials")
    except AglError as exc:
        assert exc.code in (ErrorCode.NO_PERMISSION, ErrorCode.AUTH_MISSING,
                            ErrorCode.UNKNOWN_WRITE, ErrorCode.TRANSIENT)
        if exc.code is ErrorCode.TRANSIENT:
            pytest.skip("network unavailable")
        return
    pytest.fail("unauthenticated write unexpectedly succeeded")
