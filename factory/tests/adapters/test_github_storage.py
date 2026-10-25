"""M02 storage adapter: real git semantics + REST error classification.

``real_git`` tests exercise genuine blob/tree/commit creation and
``git update-ref <ref> <new> <old>`` CAS against a local bare repository.
``mock`` tests inject transport-level HTTP failures to prove the error taxonomy;
they are not evidence of any real GitHub call.
"""

from __future__ import annotations

import io
import json
import subprocess
import urllib.error
from email.message import Message
from pathlib import Path

import pytest

from agl.errors import AglError, ErrorCode, redact
from agl.storage.github import GitHubStorage, sha256_hex
from agl.storage.transports import LocalGitTransport, RestTransport


def head(bare: Path, ref: str = "exp/test") -> str:
    return subprocess.run(
        ["git", "rev-parse", f"refs/heads/{ref}"], cwd=str(bare), capture_output=True, text=True
    ).stdout.strip()


@pytest.mark.real_git
def test_read_ref_returns_real_commit(storage):
    info = storage.read_ref()
    assert info.ref == "exp/test"
    assert len(info.commit_sha) == 40
    assert info.transport == "local_git"


@pytest.mark.real_git
def test_write_then_independent_readback(storage, bare_remote):
    body = b'{"hello":"world"}\n'
    receipt = storage.write_immutable("factory/probe/x.json", body, idempotency_key="op-1")
    assert receipt.status == "CREATED"
    assert receipt.content_sha256 == sha256_hex(body)

    # blob sha must equal what git itself computes for these bytes
    expected_blob = subprocess.run(
        ["git", "hash-object", "-t", "blob", "--stdin"], input=body,
        cwd=str(bare_remote), capture_output=True,
    ).stdout.decode().strip()
    assert receipt.blob_sha == expected_blob

    rb = storage.readback(receipt)
    assert rb.matches is True
    assert rb.readback_sha256 == receipt.content_sha256
    assert rb.readback_blob_sha == receipt.blob_sha
    assert rb.method.endswith("independent_get")
    assert head(bare_remote) == receipt.commit_sha


@pytest.mark.real_git
def test_idempotent_replay_creates_no_new_commit(storage, bare_remote):
    storage.write_immutable("factory/probe/idem.json", b"same\n", idempotency_key="k")
    before = head(bare_remote)
    again = storage.write_immutable("factory/probe/idem.json", b"same\n", idempotency_key="k")
    assert again.status == "IDEMPOTENT_REPLAY"
    assert head(bare_remote) == before
    assert again.commit_sha == before


@pytest.mark.real_git
def test_different_content_same_path_is_conflict(storage, bare_remote):
    storage.write_immutable("factory/probe/conflict.json", b"first\n")
    before = head(bare_remote)
    with pytest.raises(AglError) as exc:
        storage.write_immutable("factory/probe/conflict.json", b"second\n")
    assert exc.value.code is ErrorCode.CONFLICT
    assert head(bare_remote) == before
    # original content survives untouched
    assert storage.read_file("factory/probe/conflict.json").content == b"first\n"


@pytest.mark.real_git
def test_write_outside_whitelist_rejected(storage):
    with pytest.raises(AglError) as exc:
        storage.write_immutable("frameworks/other/README.md", b"nope")
    assert exc.value.code is ErrorCode.PATH_NOT_WHITELISTED


@pytest.mark.real_git
def test_path_traversal_rejected(storage):
    with pytest.raises(AglError):
        storage.write_immutable("factory/../../etc/passwd", b"x")


def test_protected_ref_cannot_be_bound(bare_remote):
    with pytest.raises(AglError) as exc:
        GitHubStorage(LocalGitTransport(bare_remote), "kaibahaha/xxsc", "main")
    assert exc.value.code is ErrorCode.NO_PERMISSION


@pytest.mark.real_git
def test_cas_projection_conflict_and_success(storage, bare_remote):
    path = "factory/probes/BOARD.md"
    first = storage.cas_publish_projection(path, b"v1\n", None)
    assert first.status == "CREATED"

    with pytest.raises(AglError) as exc:
        storage.cas_publish_projection(path, b"v2\n", "0" * 40)
    assert exc.value.code is ErrorCode.CONFLICT

    second = storage.cas_publish_projection(path, b"v2\n", first.blob_sha)
    assert second.status == "CREATED"
    assert storage.read_file(path).content == b"v2\n"

    third = storage.cas_publish_projection(path, b"v2\n", second.blob_sha)
    assert third.status == "IDEMPOTENT_REPLAY"


@pytest.mark.real_git
def test_unknown_write_is_reconciled_by_reading(bare_remote):
    """Transport reports UNKNOWN_WRITE although the commit landed -> reconcile."""

    class AmbiguousTransport(LocalGitTransport):
        def create_file(self, repo, branch, path, content, message):
            super().create_file(repo, branch, path, content, message)
            raise AglError(ErrorCode.UNKNOWN_WRITE, "connection reset after send")

    storage = GitHubStorage(AmbiguousTransport(bare_remote), "kaibahaha/xxsc", "exp/test",
                            allowed_prefixes=("factory",))
    receipt = storage.write_immutable("factory/probe/ambiguous.json", b"landed\n")
    assert receipt.status == "CREATED_RECONCILED"
    assert receipt.attempts == 1


# --------------------------------------------------------------------------- #
# REST classification (mock transport failures, no network)
# --------------------------------------------------------------------------- #


def _http_error(code: int, body: dict | None = None, headers: dict | None = None):
    msg = Message()
    for key, value in (headers or {}).items():
        msg[key] = value
    payload = json.dumps(body or {"message": "err"}).encode()
    return urllib.error.HTTPError("https://api.github.com/x", code, "err", msg, io.BytesIO(payload))


def test_rest_404_becomes_none_for_read(monkeypatch):
    transport = RestTransport(token="ghp_" + "a" * 30, max_retries=0)
    monkeypatch.setattr("agl.storage.transports.urllib.request.urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(_http_error(404)))
    assert transport.get_file("o/r", "main", "missing.txt") is None


def test_rest_401_is_no_permission(monkeypatch):
    transport = RestTransport(token="ghp_" + "b" * 30, max_retries=0)
    monkeypatch.setattr("agl.storage.transports.urllib.request.urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(_http_error(401)))
    with pytest.raises(AglError) as exc:
        transport.get_ref("o/r", "main")
    assert exc.value.code is ErrorCode.NO_PERMISSION


def test_rest_rate_limit_detected(monkeypatch):
    transport = RestTransport(max_retries=0)
    monkeypatch.setattr(
        "agl.storage.transports.urllib.request.urlopen",
        lambda *a, **k: (_ for _ in ()).throw(
            _http_error(403, {"message": "API rate limit exceeded"}, {"x-ratelimit-remaining": "0"})
        ),
    )
    with pytest.raises(AglError) as exc:
        transport.get_ref("o/r", "main")
    assert exc.value.code is ErrorCode.RATE_LIMITED


def test_rest_422_is_conflict(monkeypatch):
    transport = RestTransport(token="ghp_" + "c" * 30, max_retries=0)
    monkeypatch.setattr("agl.storage.transports.urllib.request.urlopen",
                        lambda *a, **k: (_ for _ in ()).throw(_http_error(422)))
    with pytest.raises(AglError) as exc:
        transport.create_file("o/r", "dev", "p.json", b"{}", "msg")
    assert exc.value.code is ErrorCode.CONFLICT


def test_rest_500_retries_then_transient(monkeypatch):
    calls = {"n": 0}

    def boom(*a, **k):
        calls["n"] += 1
        raise _http_error(500)

    transport = RestTransport(max_retries=1, retry_sleep=lambda s: None)
    monkeypatch.setattr("agl.storage.transports.urllib.request.urlopen", boom)
    with pytest.raises(AglError) as exc:
        transport.get_ref("o/r", "main")
    assert exc.value.code is ErrorCode.TRANSIENT
    assert calls["n"] == 2


def test_rest_network_failure_on_put_is_unknown_write(monkeypatch):
    transport = RestTransport(token="ghp_" + "d" * 30, max_retries=1, retry_sleep=lambda s: None)
    monkeypatch.setattr(
        "agl.storage.transports.urllib.request.urlopen",
        lambda *a, **k: (_ for _ in ()).throw(urllib.error.URLError("connection reset")),
    )
    with pytest.raises(AglError) as exc:
        transport.create_file("o/r", "dev", "p.json", b"{}", "msg")
    assert exc.value.code is ErrorCode.UNKNOWN_WRITE


def test_token_never_leaks_into_error_text():
    token = "ghp_" + "z" * 36
    exc = AglError(ErrorCode.NO_PERMISSION, f"401 with Authorization: Bearer {token}")
    assert token not in exc.message
    assert "***REDACTED***" in exc.message
    assert token not in json.dumps(exc.to_dict())
    assert redact("token=abc1234567890") == "token=***REDACTED***"


def test_rest_transport_reports_auth_state(monkeypatch):
    assert RestTransport(token="x" * 20).authenticated is True
    monkeypatch.setenv("GITHUB_TOKEN", "ghp_" + "e" * 30)
    assert RestTransport(token=None).authenticated is True
    # explicit empty string must override the ambient token
    assert RestTransport(token="").authenticated is False
