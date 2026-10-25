"""Git transports used by the M02 storage adapter.

Two interchangeable implementations of :class:`GitTransport`:

``RestTransport``
    GitHub REST v3 over stdlib ``urllib`` (no third-party dependency). Used for
    the real repository. Handles auth, rate limits, conditional updates and
    error classification.

``LocalGitTransport``
    Real ``git`` plumbing against a local **bare** repository. Not a mock: it
    creates genuine blobs, trees and commits, and uses
    ``git update-ref <ref> <new> <old>`` as a true compare-and-swap. This is how
    the adapter is verified end-to-end without network or credentials.

Both return the same primitive tuples so the storage adapter stays transport
agnostic:
    get_ref            -> commit sha
    get_file           -> (blob_sha, bytes) | None
    create_file        -> (commit_sha, blob_sha)
    update_file        -> (commit_sha, blob_sha)   with expected_blob_sha CAS
    list_dir           -> list[str]
"""

from __future__ import annotations

import base64
import json
import os
import re
import shutil
import subprocess
import tempfile
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Protocol

from ..errors import AglError, ErrorCode, redact


class GitTransport(Protocol):
    kind: str

    def get_ref(self, repo: str, ref: str) -> str: ...

    def get_file(self, repo: str, ref: str, path: str) -> tuple[str, bytes] | None: ...

    def create_file(
        self, repo: str, branch: str, path: str, content: bytes, message: str
    ) -> tuple[str, str]: ...

    def update_file(
        self,
        repo: str,
        branch: str,
        path: str,
        content: bytes,
        message: str,
        expected_blob_sha: str,
    ) -> tuple[str, str]: ...

    def list_dir(self, repo: str, ref: str, path: str) -> list[str]: ...


# --------------------------------------------------------------------------- #
# REST
# --------------------------------------------------------------------------- #

_RATE_HEADERS = ("x-ratelimit-remaining", "x-ratelimit-reset", "retry-after")


def _norm_path(path: str) -> str:
    p = path.strip().lstrip("/")
    if not p:
        raise AglError(ErrorCode.INVALID_INPUT, "empty git path")
    if ".." in p.split("/"):
        raise AglError(ErrorCode.INVALID_INPUT, f"path traversal rejected: {path}")
    return p


class RestTransport:
    """GitHub REST v3 transport (stdlib only)."""

    kind = "github_rest"

    def __init__(
        self,
        token: str | None = None,
        base_url: str = "https://api.github.com",
        timeout: float = 30.0,
        max_retries: int = 2,
        backoff: tuple[float, ...] = (1.0, 3.0, 8.0),
        user_agent: str = "agl-adapter/4.2",
        retry_sleep=time.sleep,
    ) -> None:
        self._token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_retries = max_retries
        self.backoff = backoff
        self.user_agent = user_agent
        self._sleep = retry_sleep

    # -- low level ---------------------------------------------------------- #
    @property
    def authenticated(self) -> bool:
        return bool(self._token)

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": self.user_agent,
        }
        if self._token:
            headers["Authorization"] = f"Bearer {self._token}"
        return headers

    def _request(
        self,
        method: str,
        api_path: str,
        body: dict[str, Any] | None = None,
        *,
        allow_404: bool = False,
        write: bool = False,
    ) -> tuple[int, dict[str, str], Any]:
        url = f"{self.base_url}{api_path}"
        payload = json.dumps(body).encode() if body is not None else None
        last_error: Exception | None = None
        attempts = self.max_retries + 1
        for attempt in range(attempts):
            req = urllib.request.Request(url, data=payload, method=method, headers=self._headers())
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    raw = resp.read().decode("utf-8", "replace")
                    headers = {k.lower(): v for k, v in resp.headers.items()}
                    data = json.loads(raw) if raw.strip() else None
                    return resp.status, headers, data
            except urllib.error.HTTPError as exc:  # type: ignore[union-attr]
                raw = exc.read().decode("utf-8", "replace")
                headers = {k.lower(): v for k, v in (exc.headers or {}).items()}
                msg = self._api_message(raw)
                if exc.code == 404:
                    if allow_404:
                        return 404, headers, None
                    raise AglError(ErrorCode.NOT_FOUND, f"404 {method} {api_path}: {msg}") from None
                if exc.code in (401,):
                    raise AglError(ErrorCode.NO_PERMISSION, f"401 {method} {api_path}: {msg}") from None
                if exc.code == 403:
                    remaining = headers.get("x-ratelimit-remaining")
                    if remaining == "0" or "rate limit" in msg.lower():
                        raise AglError(
                            ErrorCode.RATE_LIMITED,
                            f"403 rate limited: {msg}",
                            {"reset": headers.get("x-ratelimit-reset")},
                        ) from None
                    raise AglError(ErrorCode.NO_PERMISSION, f"403 {method} {api_path}: {msg}") from None
                if exc.code in (409, 422):
                    raise AglError(ErrorCode.CONFLICT, f"{exc.code} {method} {api_path}: {msg}") from None
                if exc.code >= 500:
                    last_error = AglError(ErrorCode.TRANSIENT, f"{exc.code} {method} {api_path}: {msg}")
                else:
                    raise AglError(ErrorCode.INVALID_INPUT, f"{exc.code} {method} {api_path}: {msg}") from None
            except (urllib.error.URLError, TimeoutError, ConnectionError, OSError) as exc:
                last_error = AglError(
                    ErrorCode.TRANSIENT,
                    f"network error {method} {api_path}: {redact(str(exc), [self._token or ''])}",
                )
            if attempt < attempts - 1:
                self._sleep(self.backoff[min(attempt, len(self.backoff) - 1)])
        assert last_error is not None
        if write:
            raise AglError(
                ErrorCode.UNKNOWN_WRITE,
                f"write outcome unknown after {attempts} attempts: {last_error.message}",
                {"method": method, "path": api_path},
            )
        raise last_error

    @staticmethod
    def _api_message(raw: str) -> str:
        try:
            payload = json.loads(raw)
            return str(payload.get("message", raw))[:400]
        except Exception:
            return raw[:400]

    def _repo_path(self, repo: str) -> str:
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repo):
            raise AglError(ErrorCode.INVALID_INPUT, f"invalid repo slug: {repo}")
        return f"/repos/{repo}"

    # -- primitive ops ------------------------------------------------------ #
    def get_ref(self, repo: str, ref: str) -> str:
        quoted = urllib.parse.quote(ref, safe="/")
        status, _, data = self._request(
            "GET", f"{self._repo_path(repo)}/git/ref/heads/{quoted}", allow_404=True
        )
        if status == 404:
            raise AglError(ErrorCode.NOT_FOUND, f"ref not found: {repo}@{ref}")
        return str(data["object"]["sha"])

    def get_file(self, repo: str, ref: str, path: str) -> tuple[str, bytes] | None:
        quoted_ref = urllib.parse.quote(ref, safe="/")
        status, _, data = self._request(
            "GET",
            f"{self._repo_path(repo)}/contents/{_norm_path(path)}?ref={quoted_ref}",
            allow_404=True,
        )
        if status == 404:
            return None
        if isinstance(data, list):
            raise AglError(ErrorCode.INVALID_INPUT, f"{path} is a directory, not a file")
        if data.get("encoding") != "base64" or "content" not in data:
            # very large files return no content; fetch the blob explicitly
            blob = self._request("GET", f"{self._repo_path(repo)}/git/blobs/{data['sha']}")[2]
            return str(blob["sha"]), base64.b64decode(blob["content"])
        return str(data["sha"]), base64.b64decode(data["content"])

    def create_file(
        self, repo: str, branch: str, path: str, content: bytes, message: str
    ) -> tuple[str, str]:
        body = {
            "message": message,
            "content": base64.b64encode(content).decode(),
            "branch": branch,
        }
        _, _, data = self._request(
            "PUT", f"{self._repo_path(repo)}/contents/{_norm_path(path)}", body, write=True
        )
        return str(data["commit"]["sha"]), str(data["content"]["sha"])

    def update_file(
        self,
        repo: str,
        branch: str,
        path: str,
        content: bytes,
        message: str,
        expected_blob_sha: str,
    ) -> tuple[str, str]:
        body = {
            "message": message,
            "content": base64.b64encode(content).decode(),
            "branch": branch,
            "sha": expected_blob_sha,
        }
        _, _, data = self._request(
            "PUT", f"{self._repo_path(repo)}/contents/{_norm_path(path)}", body, write=True
        )
        return str(data["commit"]["sha"]), str(data["content"]["sha"])

    def list_dir(self, repo: str, ref: str, path: str) -> list[str]:
        quoted_ref = urllib.parse.quote(ref, safe="/")
        status, _, data = self._request(
            "GET",
            f"{self._repo_path(repo)}/contents/{_norm_path(path)}?ref={quoted_ref}",
            allow_404=True,
        )
        if status == 404 or not isinstance(data, list):
            return []
        return sorted(entry["name"] for entry in data)


# --------------------------------------------------------------------------- #
# Local bare repository (real git plumbing)
# --------------------------------------------------------------------------- #


class LocalGitTransport:
    """Real git object operations against a local bare repository.

    CAS is enforced by ``git update-ref <ref> <new> <old>`` which fails if the
    branch moved between read and write -- the same optimistic-concurrency
    contract the REST transport gets from the ``sha`` parameter.
    """

    kind = "local_git"

    def __init__(self, bare_repo: str | Path, author_name: str = "agl-adapter",
                 author_email: str = "adapter@agl.local", timeout: float = 30.0) -> None:
        self.bare = Path(bare_repo).resolve()
        if not (self.bare / "HEAD").exists() and not (self.bare / "objects").exists():
            raise AglError(ErrorCode.NOT_FOUND, f"not a git repository: {self.bare}")
        self.author_name = author_name
        self.author_email = author_email
        self.timeout = timeout
        self._tmpdir = Path(tempfile.mkdtemp(prefix="agl-git-"))

    # -- helpers ------------------------------------------------------------ #
    def _env(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        env = dict(os.environ)
        env.update(
            {
                "GIT_AUTHOR_NAME": self.author_name,
                "GIT_AUTHOR_EMAIL": self.author_email,
                "GIT_COMMITTER_NAME": self.author_name,
                "GIT_COMMITTER_EMAIL": self.author_email,
                "GIT_TERMINAL_PROMPT": "0",
            }
        )
        if extra:
            env.update(extra)
        return env

    def _git(
        self,
        *args: str,
        input_bytes: bytes | None = None,
        check: bool = True,
        env_extra: dict[str, str] | None = None,
    ) -> subprocess.CompletedProcess[bytes]:
        proc = subprocess.run(
            ["git", *args],
            cwd=str(self.bare),
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=self._env(env_extra),
            timeout=self.timeout,
        )
        if check and proc.returncode != 0:
            raise AglError(
                ErrorCode.INVALID_INPUT,
                f"git {' '.join(args)} failed: {proc.stderr.decode('utf-8', 'replace').strip()[:300]}",
            )
        return proc

    def _commit_sha(self, ref: str) -> str:
        proc = self._git("rev-parse", "--verify", f"refs/heads/{ref}^{{commit}}", check=False)
        if proc.returncode != 0:
            raise AglError(ErrorCode.NOT_FOUND, f"ref not found: {ref}")
        return proc.stdout.decode().strip()

    def _commit_tree(self, parent: str, updates: dict[str, str], message: str) -> str:
        index = self._tmpdir / f"index-{time.time_ns()}"
        env = {"GIT_INDEX_FILE": str(index)}
        try:
            self._git("read-tree", f"{parent}^{{tree}}", env_extra=env)
            for path, blob in updates.items():
                self._git(
                    "update-index", "--add", "--cacheinfo", f"100644,{blob},{path}", env_extra=env
                )
            tree = self._git("write-tree", env_extra=env).stdout.decode().strip()
            commit = self._git(
                "commit-tree", tree, "-p", parent, "-m", message
            ).stdout.decode().strip()
            return commit
        finally:
            index.unlink(missing_ok=True)

    def _write_blob(self, content: bytes) -> str:
        return self._git("hash-object", "-w", "--stdin", input_bytes=content).stdout.decode().strip()

    # -- primitive ops ------------------------------------------------------ #
    def get_ref(self, repo: str, ref: str) -> str:
        return self._commit_sha(ref)

    def get_file(self, repo: str, ref: str, path: str) -> tuple[str, bytes] | None:
        p = _norm_path(path)
        spec = f"refs/heads/{ref}:{p}"
        blob_proc = self._git("rev-parse", "--verify", spec, check=False)
        if blob_proc.returncode != 0:
            return None
        blob_sha = blob_proc.stdout.decode().strip()
        content = self._git("cat-file", "-p", blob_sha).stdout
        return blob_sha, content

    def create_file(
        self, repo: str, branch: str, path: str, content: bytes, message: str
    ) -> tuple[str, str]:
        p = _norm_path(path)
        if self.get_file(repo, branch, p) is not None:
            # caller must pre-check; race here is a genuine conflict
            raise AglError(ErrorCode.CONFLICT, f"file already exists: {p}")
        parent = self._commit_sha(branch)
        blob = self._write_blob(content)
        commit = self._commit_tree(parent, {p: blob}, message)
        proc = self._git("update-ref", f"refs/heads/{branch}", commit, parent, check=False)
        if proc.returncode != 0:
            raise AglError(ErrorCode.CONFLICT, f"CAS failed on {branch}: {proc.stderr.decode()[:200]}")
        return commit, blob

    def update_file(
        self,
        repo: str,
        branch: str,
        path: str,
        content: bytes,
        message: str,
        expected_blob_sha: str,
    ) -> tuple[str, str]:
        p = _norm_path(path)
        current = self.get_file(repo, branch, p)
        if current is None:
            raise AglError(ErrorCode.NOT_FOUND, f"file not found for update: {p}")
        if current[0] != expected_blob_sha:
            raise AglError(
                ErrorCode.CONFLICT,
                f"blob sha mismatch on {p}",
                {"expected": expected_blob_sha, "actual": current[0]},
            )
        parent = self._commit_sha(branch)
        blob = self._write_blob(content)
        commit = self._commit_tree(parent, {p: blob}, message)
        proc = self._git("update-ref", f"refs/heads/{branch}", commit, parent, check=False)
        if proc.returncode != 0:
            raise AglError(ErrorCode.CONFLICT, f"CAS failed on {branch}")
        return commit, blob

    def list_dir(self, repo: str, ref: str, path: str) -> list[str]:
        """Immediate children only (mirrors the REST contents API)."""
        p = _norm_path(path).rstrip("/")
        proc = self._git("ls-tree", f"refs/heads/{ref}", "--", f"{p}/", check=False)
        if proc.returncode != 0 or not proc.stdout:
            return []
        names: list[str] = []
        for line in proc.stdout.decode().splitlines():
            meta, _, name = line.partition("\t")
            kind = meta.split()[1] if len(meta.split()) > 1 else ""
            short = name.rsplit("/", 1)[-1]
            names.append(short + ("/" if kind == "tree" else ""))
        return sorted(names)

    def close(self) -> None:
        shutil.rmtree(self._tmpdir, ignore_errors=True)
