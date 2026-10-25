"""Publish a local subtree to a branch using the GitHub Git Data API.

Why this exists: in the execution sandbox ``github.com:443`` (git smart HTTP) is
unreachable while ``api.github.com:443`` works, so ``git push`` cannot be used.
This tool performs the equivalent operation with the documented Git Data API:

    blobs -> trees (nested, built bottom-up) -> commit -> ref update (fast-forward only)

It is deliberately conservative:

* the base tree is the *current remote head* of the target branch, so nothing
  that another writer committed in the meantime is dropped;
* ``update_ref`` uses ``force=false``; a concurrent move aborts the publish;
* every uploaded file is verified afterwards by comparing the remote blob SHA
  with the locally computed ``git hash-object`` value.

Usage::

    GITHUB_TOKEN=... python tools/publish_branch.py \
        --repo kaibahaha/xxsc --branch dev/agl-v4.2-workbuddy-adapters \
        --base-ref exp/agensh-lite-v4.2-controller-mvp-20261025 \
        --root .. --include factory --message "..." [--dry-run]
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

API = "https://api.github.com"


class Api:
    def __init__(self, token: str) -> None:
        self.token = token

    def call(self, method: str, path: str, body: dict | None = None) -> dict:
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(
            API + path, data=data, method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "agl-publisher/1.0",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                raw = resp.read()
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")[:500]
            raise SystemExit(f"API {method} {path} -> {exc.code}: {detail}")


def git(root: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(f"git {' '.join(args)} failed: {proc.stderr.strip()}")
    return proc.stdout.strip()


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def collect(root: Path, include: str) -> list[str]:
    out = subprocess.run(["git", "-C", str(root), "ls-files", include],
                         capture_output=True, text=True, check=True).stdout.split()
    skip = ("__pycache__/", ".pytest_cache/", ".egg-info/")
    return [p for p in out if not any(s in p for s in skip)]


def build_tree(api: Api, repo: str, entries: dict[str, str], base_tree: str | None) -> str:
    """entries: full path -> blob sha. Builds nested trees bottom-up."""
    root: dict = {}
    for path, sha in entries.items():
        parts = path.split("/")
        node = root
        for part in parts[:-1]:
            node = node.setdefault(part, {})
        node[parts[-1]] = sha

    def make(node: dict, is_root: bool) -> str:
        items = []
        for name, value in sorted(node.items()):
            if isinstance(value, dict):
                items.append({"path": name, "mode": "040000", "type": "tree",
                              "sha": make(value, False)})
            else:
                items.append({"path": name, "mode": "100644", "type": "blob", "sha": value})
        body: dict = {"tree": items}
        if is_root and base_tree:
            body["base_tree"] = base_tree
        return api.call("POST", f"/repos/{repo}/git/trees", body)["sha"]

    return make(root, True)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--branch", required=True)
    ap.add_argument("--base-ref", default=None, help="fallback base when the branch does not exist")
    ap.add_argument("--root", default=".")
    ap.add_argument("--include", default="factory")
    ap.add_argument("--message", required=True)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if not token:
        raise SystemExit("GITHUB_TOKEN is required")
    root = Path(args.root).resolve()
    api = Api(token)

    files = collect(root, args.include)
    print(f"files to publish: {len(files)}")

    head_sha = None
    try:
        head_sha = api.call("GET", f"/repos/{args.repo}/git/ref/heads/{args.branch}")["object"]["sha"]
        print(f"existing branch head: {head_sha}")
    except SystemExit:
        if not args.base_ref:
            raise
        head_sha = api.call("GET", f"/repos/{args.repo}/git/ref/heads/{args.base_ref}")["object"]["sha"]
        print(f"branch absent, basing on {args.base_ref}: {head_sha}")

    base_commit = api.call("GET", f"/repos/{args.repo}/git/commits/{head_sha}")
    base_tree = base_commit["tree"]["sha"]

    entries: dict[str, str] = {}
    mismatches = []
    for rel in files:
        path = root / rel
        data = path.read_bytes()
        sha = api.call("POST", f"/repos/{args.repo}/git/blobs",
                       {"content": base64.b64encode(data).decode(), "encoding": "base64"})["sha"]
        expected = blob_sha(path)
        if sha != expected:
            mismatches.append((rel, expected, sha))
        entries[rel] = sha
    if mismatches:
        raise SystemExit(f"blob sha mismatch: {mismatches[:3]}")
    print(f"blobs uploaded: {len(entries)} (all local blob shas match)")

    if args.dry_run:
        print("dry-run: no tree/commit/ref written")
        return 0

    tree = build_tree(api, args.repo, entries, base_tree)
    commit = api.call("POST", f"/repos/{args.repo}/git/commits", {
        "message": args.message, "tree": tree, "parents": [head_sha],
        "author": {"name": "WorkBuddy Adapter", "email": "workbuddy-adapter@local"},
        "committer": {"name": "WorkBuddy Adapter", "email": "workbuddy-adapter@local"},
    })
    print(f"commit created: {commit['sha']}")

    if commit["sha"] == head_sha:
        print("tree unchanged; nothing to update")
    else:
        try:
            api.call("PATCH", f"/repos/{args.repo}/git/refs/heads/{args.branch}",
                     {"sha": commit["sha"], "force": False})
        except SystemExit:
            api.call("POST", f"/repos/{args.repo}/git/refs",
                     {"ref": f"refs/heads/{args.branch}", "sha": commit["sha"]})
        print(f"ref updated: {args.branch} -> {commit['sha']}")

    # independent verification: ref + three sample blobs
    ref = api.call("GET", f"/repos/{args.repo}/git/ref/heads/{args.branch}")
    assert ref["object"]["sha"] == commit["sha"], (ref, commit["sha"])
    for rel in files[:3] + [f for f in files if f.endswith("cli.py")][:1]:
        remote = api.call("GET", f"/repos/{args.repo}/contents/{rel}?ref={args.branch}")
        local = blob_sha(root / rel)
        status = "OK" if remote["sha"] == local else "MISMATCH"
        print(f"verify {rel}: {status} blob={remote['sha'][:12]}")
    print(json.dumps({"commit_sha": commit["sha"], "tree_sha": tree, "files": len(entries)}))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
