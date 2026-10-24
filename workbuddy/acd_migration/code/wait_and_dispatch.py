#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
等 github_token.txt 出现（Device Flow 授权完成）后：
1) whoami
2) 确保目标仓库 + 实验分支存在（OutsiderVictor 优先，否则当前账号下建同名仓库）
3) 立即跑首轮派单 p1git_dispatch.py（含 push + 远程回读 + ACK）
"""
import os
import sys
import time
import json
import subprocess
import requests

BASE = os.path.dirname(os.path.abspath(__file__))
STATE = os.path.join(BASE, "state")
TOKEN_FILE = os.path.join(STATE, "github_token.txt")
PY = r"C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\python.exe"
BRANCH = "exp/p1-relay-dualwrite-20261023"
REPO = "xxsc"
PREFERRED_OWNER = "OutsiderVictor"


S = requests.Session()
S.trust_env = False      # 直连更稳；代理对 github 域名时通时断


def log(m):
    print("[%s] %s" % (time.strftime("%H:%M:%S"), m), flush=True)


def hdr(tok):
    return {"Authorization": "Bearer %s" % tok, "Accept": "application/vnd.github+json",
            "User-Agent": "P1-GIT-A/1.1"}


def ensure_repo_branch(tok, owner):
    base = "https://api.github.com"
    r = S.get("%s/repos/%s/%s" % (base, owner, REPO), headers=hdr(tok), timeout=30)
    if r.status_code == 200:
        log("repo exists: %s/%s (private=%s)" % (owner, REPO, r.json().get("private")))
    else:
        log("repo %s/%s not usable (http=%s) -> create under authenticated user" % (owner, REPO, r.status_code))
        me = S.get("%s/user" % base, headers=hdr(tok), timeout=30).json()
        owner = me["login"]
        r2 = S.get("%s/repos/%s/%s" % (base, owner, REPO), headers=hdr(tok), timeout=30)
        if r2.status_code != 200:
            c = S.post("%s/user/repos" % base, headers=hdr(tok), timeout=30,
                              json={"name": REPO, "private": False, "auto_init": True,
                                    "description": "P1-Git-Drive dualwrite experiment"})
            log("create repo http=%s" % c.status_code)
            if c.status_code not in (200, 201):
                log("create failed: %s" % c.text[:200])
                return None
            time.sleep(2)
        else:
            log("repo exists: %s/%s" % (owner, REPO))

    # 分支
    rb = S.get("%s/repos/%s/%s/branches/%s" % (base, owner, REPO, BRANCH),
                      headers=hdr(tok), timeout=30)
    if rb.status_code == 200:
        log("branch exists: %s" % BRANCH)
        return owner
    ri = S.get("%s/repos/%s/%s" % (base, owner, REPO), headers=hdr(tok), timeout=30)
    default_branch = ri.json().get("default_branch", "main")
    rs = S.get("%s/repos/%s/%s/git/ref/heads/%s" % (base, owner, REPO, default_branch),
                      headers=hdr(tok), timeout=30)
    sha = rs.json()["object"]["sha"]
    rc = S.post("%s/repos/%s/%s/git/refs" % (base, owner, REPO), headers=hdr(tok),
                       timeout=30, json={"ref": "refs/heads/%s" % BRANCH, "sha": sha})
    log("create branch http=%s" % rc.status_code)
    if rc.status_code not in (200, 201):
        log("branch create failed: %s" % rc.text[:200])
        return None
    return owner


def main():
    for _ in range(720):   # 最多等 2 小时
        if os.path.exists(TOKEN_FILE) and os.path.getsize(TOKEN_FILE) > 10:
            break
        time.sleep(10)
    if not os.path.exists(TOKEN_FILE):
        log("token not found, abort")
        return 2
    tok = open(TOKEN_FILE, encoding="utf-8").read().strip()
    me = S.get("https://api.github.com/user", headers=hdr(tok), timeout=30)
    log("authenticated as %s" % me.json().get("login"))

    owner = ensure_repo_branch(tok, PREFERRED_OWNER)
    if not owner:
        log("repo/branch unavailable -> abort")
        return 3

    env = dict(os.environ)
    env["P1GIT_OWNER"] = owner
    env["GITHUB_TOKEN"] = tok
    p = subprocess.run([PY, os.path.join(BASE, "p1git_dispatch.py")], cwd=BASE, env=env,
                       capture_output=True, text=True, timeout=900)
    log("dispatch rc=%s" % p.returncode)
    log("stdout:\n%s" % (p.stdout or "")[-2000:])
    if p.stderr:
        log("stderr:\n%s" % p.stderr[-1000:])
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
