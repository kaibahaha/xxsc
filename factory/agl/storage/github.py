"""M02 -- GitHub Storage Adapter.

Contract implemented here (see workorders/INTERFACE_HANDOFF.md §4):

    read_ref(branch)                                   -> RefInfo
    read_file(path, ref)                               -> FileSnapshot
    write_immutable(path, content, idempotency_key)    -> WriteReceipt
    readback(receipt)                                  -> VerifiedReadback
    cas_publish_projection(path, content, expected)    -> WriteReceipt

Design decisions
----------------
* **Immutable first.** ``write_immutable`` never overwrites. If the path already
  exists the adapter compares the canonical content hash:
  equal -> ``IDEMPOTENT_REPLAY`` (no commit), different -> ``CONFLICT``.
  This is the Git analogue of Microsoft Agensh's ``(dedup_key, agent)`` unique
  key in ``mini-router/src/state.ts``: repeated delivery of the same event is
  absorbed, a colliding payload is refused rather than overwritten.
* **Write then independent readback.** A successful PUT is only *WRITTEN*; the
  adapter issues a second, independent read and recomputes the hash before
  returning ``READBACK_VERIFIED``. If the write call fails at the network layer
  the outcome is ``UNKNOWN_WRITE`` and the adapter reconciles by reading, never
  by blind re-POST.
* **Protected refs.** ``main``/``master`` are read-only by construction; the
  workorder forbids touching them from an adapter.
* **Path whitelist.** Writes outside ``allowed_prefixes`` are refused before any
  network call.
* **Token safety.** Every message passes through :func:`redact`.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Sequence

from ..errors import AglError, ErrorCode
from .transports import GitTransport, LocalGitTransport, RestTransport, _norm_path

PROTECTED_REFS = {"main", "master"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_json_bytes(payload: Any) -> bytes:
    """Deterministic JSON: sorted keys, no NaN, UTF-8, trailing newline."""
    text = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
                      allow_nan=False)
    return (text + "\n").encode("utf-8")


@dataclass(frozen=True)
class RefInfo:
    repo: str
    ref: str
    commit_sha: str
    transport: str
    observed_at: str


@dataclass(frozen=True)
class FileSnapshot:
    repo: str
    ref: str
    path: str
    exists: bool
    blob_sha: str | None
    commit_sha: str
    content: bytes
    sha256: str | None
    observed_at: str

    @property
    def text(self) -> str:
        return self.content.decode("utf-8", "replace")


@dataclass(frozen=True)
class WriteReceipt:
    status: str            # CREATED | CREATED_RECONCILED | IDEMPOTENT_REPLAY
    repo: str
    ref: str
    path: str
    commit_sha: str
    blob_sha: str
    content_sha256: str
    idempotency_key: str | None
    attempts: int
    transport: str
    observed_at: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "repo": self.repo,
            "ref": self.ref,
            "path": self.path,
            "commit_sha": self.commit_sha,
            "blob_sha": self.blob_sha,
            "content_sha256": self.content_sha256,
            "idempotency_key": self.idempotency_key,
            "attempts": self.attempts,
            "transport": self.transport,
            "observed_at": self.observed_at,
        }


@dataclass(frozen=True)
class VerifiedReadback:
    receipt: WriteReceipt
    readback_sha256: str | None
    readback_blob_sha: str | None
    readback_commit_sha: str | None
    matches: bool
    method: str
    verified_at: str
    detail: dict[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.receipt.path,
            "expected_sha256": self.receipt.content_sha256,
            "readback_sha256": self.readback_sha256,
            "expected_blob_sha": self.receipt.blob_sha,
            "readback_blob_sha": self.readback_blob_sha,
            "commit_sha_written": self.receipt.commit_sha,
            "commit_sha_read": self.readback_commit_sha,
            "matches": self.matches,
            "method": self.method,
            "verified_at": self.verified_at,
            **self.detail,
        }


class GitHubStorage:
    """Transport-agnostic repository adapter."""

    def __init__(
        self,
        transport: GitTransport,
        repo: str,
        ref: str,
        *,
        allowed_prefixes: Sequence[str] | None = None,
        max_retries: int = 2,
        backoff: Sequence[float] = (0.2, 0.8, 2.0),
        sleep=time.sleep,
    ) -> None:
        self.transport = transport
        self.repo = repo
        self.ref = ref
        self.allowed_prefixes = tuple(p.strip("/") for p in allowed_prefixes or ())
        self.max_retries = max_retries
        self.backoff = tuple(backoff)
        self._sleep = sleep
        if ref in PROTECTED_REFS:
            raise AglError(ErrorCode.NO_PERMISSION, f"refusing to bind adapter to protected ref {ref}")

    # -- guards -------------------------------------------------------------#
    def _check_write_path(self, path: str) -> str:
        p = _norm_path(path)
        if self.ref in PROTECTED_REFS:
            raise AglError(ErrorCode.NO_PERMISSION, f"writes to {self.ref} are forbidden")
        if self.allowed_prefixes and not any(
            p == prefix or p.startswith(prefix + "/") for prefix in self.allowed_prefixes
        ):
            raise AglError(
                ErrorCode.PATH_NOT_WHITELISTED,
                f"{p} is outside allowed prefixes {list(self.allowed_prefixes)}",
            )
        return p

    # -- reads --------------------------------------------------------------#
    def read_ref(self) -> RefInfo:
        sha = self.transport.get_ref(self.repo, self.ref)
        return RefInfo(self.repo, self.ref, sha, self.transport.kind, utc_now())

    def read_file(self, path: str, ref: str | None = None) -> FileSnapshot:
        path = _norm_path(path)
        ref = ref or self.ref
        commit_sha = self.transport.get_ref(self.repo, ref)
        found = self.transport.get_file(self.repo, ref, path)
        if found is None:
            return FileSnapshot(self.repo, ref, path, False, None, commit_sha, b"", None, utc_now())
        blob_sha, content = found
        return FileSnapshot(
            self.repo, ref, path, True, blob_sha, commit_sha, content, sha256_hex(content), utc_now()
        )

    def list_files(self, prefix: str, ref: str | None = None) -> list[str]:
        """Immediate children, normalised without trailing slashes for both transports."""
        return [name.rstrip("/") for name in self.transport.list_dir(self.repo, ref or self.ref, prefix)]

    # -- writes -------------------------------------------------------------#
    def write_immutable(
        self,
        path: str,
        content: bytes | str,
        idempotency_key: str | None = None,
        *,
        message: str | None = None,
    ) -> WriteReceipt:
        path = self._check_write_path(path)
        payload = content.encode("utf-8") if isinstance(content, str) else content
        digest = sha256_hex(payload)

        existing = self.read_file(path)
        if existing.exists:
            if existing.sha256 == digest:
                return WriteReceipt(
                    "IDEMPOTENT_REPLAY", self.repo, self.ref, path,
                    existing.commit_sha, existing.blob_sha or "", digest,
                    idempotency_key, 0, self.transport.kind, utc_now(),
                )
            raise AglError(
                ErrorCode.CONFLICT,
                f"immutable target already exists with different content: {path}",
                {"existing_sha256": existing.sha256, "incoming_sha256": digest,
                 "existing_blob_sha": existing.blob_sha},
            )

        commit_msg = message or f"agl: add {path}" + (f" [{idempotency_key}]" if idempotency_key else "")
        attempt = 0
        last: AglError | None = None
        while attempt <= self.max_retries:
            attempt += 1
            try:
                commit_sha, blob_sha = self.transport.create_file(
                    self.repo, self.ref, path, payload, commit_msg
                )
                receipt = WriteReceipt(
                    "CREATED", self.repo, self.ref, path, commit_sha, blob_sha, digest,
                    idempotency_key, attempt, self.transport.kind, utc_now(),
                )
                return self._verify_or_raise(receipt)
            except AglError as exc:
                last = exc
                if exc.code is ErrorCode.UNKNOWN_WRITE:
                    reconciled = self._reconcile_after_unknown(path, digest, idempotency_key, attempt)
                    if reconciled is not None:
                        return reconciled
                    if attempt <= self.max_retries:
                        continue
                elif exc.code in (ErrorCode.TRANSIENT, ErrorCode.RATE_LIMITED):
                    if attempt <= self.max_retries:
                        self._sleep(self.backoff[min(attempt - 1, len(self.backoff) - 1)])
                        continue
                elif exc.code is ErrorCode.CONFLICT:
                    # someone created the file between our pre-read and write
                    after = self.read_file(path)
                    if after.exists and after.sha256 == digest:
                        return WriteReceipt(
                            "IDEMPOTENT_REPLAY", self.repo, self.ref, path, after.commit_sha,
                            after.blob_sha or "", digest, idempotency_key, attempt,
                            self.transport.kind, utc_now(),
                        )
                    raise AglError(
                        ErrorCode.CONFLICT, f"concurrent create conflict on {path}",
                        {"incoming_sha256": digest, "existing_sha256": after.sha256},
                    ) from exc
                else:
                    raise
        assert last is not None
        raise last

    def _reconcile_after_unknown(
        self, path: str, digest: str, idempotency_key: str | None, attempt: int
    ) -> WriteReceipt | None:
        """Read-only reconciliation after a write whose outcome we do not know."""
        snap = self.read_file(path)
        if not snap.exists:
            return None
        if snap.sha256 != digest:
            raise AglError(
                ErrorCode.CONFLICT,
                f"reconcile found different content at {path} -- refusing to overwrite",
                {"existing_sha256": snap.sha256, "incoming_sha256": digest},
            )
        receipt = WriteReceipt(
            "CREATED_RECONCILED", self.repo, self.ref, path, snap.commit_sha,
            snap.blob_sha or "", digest, idempotency_key, attempt, self.transport.kind, utc_now(),
        )
        return self._verify_or_raise(receipt)

    def _verify_or_raise(self, receipt: WriteReceipt) -> WriteReceipt:
        rb = self.readback(receipt)
        if not rb.matches:
            raise AglError(
                ErrorCode.UNKNOWN_WRITE,
                f"readback mismatch after write: {receipt.path}",
                {"expected_sha256": receipt.content_sha256, "readback_sha256": rb.readback_sha256},
            )
        return receipt

    def readback(self, receipt: WriteReceipt) -> VerifiedReadback:
        """Independent second read; recomputes hash from raw bytes."""
        snap = self.read_file(receipt.path, receipt.ref)
        matches = bool(
            snap.exists
            and snap.sha256 == receipt.content_sha256
            and (snap.blob_sha or "") == receipt.blob_sha
            and snap.commit_sha == receipt.commit_sha
        )
        return VerifiedReadback(
            receipt=receipt,
            readback_sha256=snap.sha256,
            readback_blob_sha=snap.blob_sha,
            readback_commit_sha=snap.commit_sha,
            matches=matches,
            method=f"{self.transport.kind}:independent_get",
            verified_at=utc_now(),
            detail={"repo": self.repo, "ref": self.ref, "path": receipt.path},
        )

    def cas_publish_projection(
        self,
        path: str,
        content: bytes | str,
        expected_blob_sha: str | None,
        *,
        message: str | None = None,
        max_attempts: int = 3,
    ) -> WriteReceipt:
        """Single-writer projection update guarded by blob-SHA CAS.

        ``expected_blob_sha=None`` means "must not exist yet" (create).
        """
        path = self._check_write_path(path)
        payload = content.encode("utf-8") if isinstance(content, str) else content
        digest = sha256_hex(payload)
        for attempt in range(1, max_attempts + 1):
            current = self.read_file(path)
            if expected_blob_sha is None:
                if current.exists:
                    if current.sha256 == digest:
                        return WriteReceipt(
                            "IDEMPOTENT_REPLAY", self.repo, self.ref, path, current.commit_sha,
                            current.blob_sha or "", digest, None, attempt, self.transport.kind,
                            utc_now(),
                        )
                    raise AglError(
                        ErrorCode.CONFLICT, f"projection exists and CAS precondition was 'absent': {path}"
                    )
                commit_sha, blob_sha = self.transport.create_file(
                    self.repo, self.ref, path, payload, message or f"agl: projection {path}"
                )
            else:
                if not current.exists:
                    raise AglError(ErrorCode.NOT_FOUND, f"projection missing: {path}")
                if current.blob_sha != expected_blob_sha:
                    raise AglError(
                        ErrorCode.CONFLICT,
                        f"projection CAS mismatch on {path}",
                        {"expected": expected_blob_sha, "actual": current.blob_sha},
                    )
                if current.sha256 == digest:
                    return WriteReceipt(
                        "IDEMPOTENT_REPLAY", self.repo, self.ref, path, current.commit_sha,
                        current.blob_sha or "", digest, None, attempt, self.transport.kind, utc_now(),
                    )
                commit_sha, blob_sha = self.transport.update_file(
                    self.repo, self.ref, path, payload, message or f"agl: projection {path}",
                    expected_blob_sha,
                )
            receipt = WriteReceipt(
                "CREATED", self.repo, self.ref, path, commit_sha, blob_sha, digest, None,
                attempt, self.transport.kind, utc_now(),
            )
            return self._verify_or_raise(receipt)
        raise AglError(ErrorCode.CONFLICT, f"projection CAS retries exhausted for {path}")


def open_storage(
    repo: str,
    ref: str,
    *,
    transport: str = "auto",
    token: str | None = None,
    local_remote: str | None = None,
    allowed_prefixes: Sequence[str] | None = None,
    api_base: str = "https://api.github.com",
) -> GitHubStorage:
    """Factory used by the CLI and tests.

    ``transport=auto`` prefers the REST transport when a token is present or a
    local remote was not supplied, otherwise the local bare repository.
    """
    if transport == "local":
        if not local_remote:
            raise AglError(ErrorCode.INVALID_INPUT, "--local-remote is required for transport=local")
        return GitHubStorage(
            LocalGitTransport(local_remote), repo, ref, allowed_prefixes=allowed_prefixes
        )
    if transport == "api":
        return GitHubStorage(
            RestTransport(token=token, base_url=api_base), repo, ref,
            allowed_prefixes=allowed_prefixes,
        )
    if local_remote:
        return GitHubStorage(
            LocalGitTransport(local_remote), repo, ref, allowed_prefixes=allowed_prefixes
        )
    return GitHubStorage(
        RestTransport(token=token, base_url=api_base), repo, ref, allowed_prefixes=allowed_prefixes
    )
