# -*- coding: utf-8 -*-
"""
P1-GIT-A · GitHub PAT 接入工具（V1.0）

用途：把 classic PAT（ghp_）/ fine-grained PAT（github_pat_）接入 P1-GIT-A 派单链路。
  - 落盘到 p1git/state/github_token.txt（p1git_dispatch.py 优先读取的位置）
  - 同时写入 Windows 凭据管理器（供 git CLI 兜底通道使用）
  - 验证：whoami / OAuth Scopes / 仓库可达性 / 分支存在性
  - 可选：仓库不存在时在认证账号下创建，并初始化实验分支与目录骨架

安全约定：
  - token 只落盘，绝不打印明文、绝不写日志，只显示 prefix 与长度
  - 不 force push、不删历史、不动 C/D 派单与既有结果

用法：
  PY pat_setup.py --token <PAT>                 # 接入并验证
  PY pat_setup.py --token <PAT> --create-repo   # 仓库不可用时在认证账号下创建
  PY pat_setup.py --check                       # 只做只读体检，不写任何凭据
"""

import argparse
import base64
import json
import os
import subprocess
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(BASE, "state")
TOKEN_FILE = os.path.join(STATE_DIR, "github_token.txt")
REPORT_FILE = os.path.join(STATE_DIR, "pat_setup_report.json")

def _load_owner():
    o = os.environ.get("P1GIT_OWNER") or ""
    p = os.path.join(STATE_DIR, "p1git_owner.txt")
    if not o and os.path.exists(p):
        try:
            o = open(p, "r", encoding="utf-8").read().strip()
        except Exception:
            o = ""
    return o or "kaibahaha"


OWNER = _load_owner()
REPO = "xxsc"
BRANCH = "exp/p1-relay-dualwrite-20261023"
ORDERS_DIR = "workbuddy/a_orders"
ACKS_DIR = "workbuddy/acks"
RESULTS_DIR = "results/chatgpt-a"
PROTOCOL_DOC = "docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md"

try:
    import requests
except ImportError:
    sys.exit("缺少 requests：请先 pip install requests")

SESSION = requests.Session()
SESSION.trust_env = False  # 实测 api.github.com / raw.githubusercontent.com 直连可用
SESSION.headers.update({"User-Agent": "P1-GIT-A-pat-setup/1.0"})


def mask(t):
    if not t:
        return "<empty>"
    return "%s***(len=%d)" % (t[:4], len(t))


def api(method, url, token=None, payload=None, tries=3):
    headers = {"Accept": "application/vnd.github+json"}
    if token:
        headers["Authorization"] = "Bearer %s" % token
    last = None
    for i in range(tries):
        try:
            if method == "GET":
                return SESSION.get(url, headers=headers, timeout=30)
            if method == "PUT":
                return SESSION.put(url, headers=headers, json=payload, timeout=60)
            return SESSION.post(url, headers=headers, json=payload, timeout=60)
        except Exception as e:
            last = e
    raise last


def save_token(tok):
    os.makedirs(STATE_DIR, exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8", newline="\n") as f:
        f.write(tok.strip())
    try:
        os.chmod(TOKEN_FILE, 0o600)
    except Exception:
        pass
    # 同步给 git CLI 兜底通道（Windows 凭据管理器）
    try:
        subprocess.run(["cmdkey", "/add:github.com", "/user:x-access-token",
                        "/pass:%s" % tok.strip()],
                       capture_output=True, text=True, timeout=30,
                       encoding="utf-8", errors="ignore")
    except Exception:
        pass


def load_existing_token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not t and os.path.exists(TOKEN_FILE):
        t = open(TOKEN_FILE, "r", encoding="utf-8").read().strip()
    return t


def put_file(owner, path, content, msg, branch, token):
    url = "https://api.github.com/repos/%s/%s/contents/%s" % (owner, REPO, path)
    payload = {
        "message": msg,
        "branch": branch,
        "content": base64.b64encode(content.encode("utf-8")).decode("ascii"),
    }
    return api("PUT", url, token=token, payload=payload)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--token", default="", help="GitHub PAT（ghp_ / github_pat_）")
    ap.add_argument("--create-repo", action="store_true",
                    help="仓库不可用时，在认证账号下创建同名仓库")
    ap.add_argument("--check", action="store_true", help="只读体检，不写凭据")
    args = ap.parse_args()

    report = {"token_masked": None, "login": None, "scopes": None,
              "repo_check": None, "branch_check": None, "action": None,
              "ok": False, "note": None}

    tok = (args.token or "").strip() or load_existing_token()
    if not tok:
        sys.exit("缺少凭据：请提供 --token <PAT>，或先把 token 写入 "
                 "state/github_token.txt 后再运行")

    if tok:
        report["token_masked"] = mask(tok)
        print("TOKEN=%s" % report["token_masked"])
    else:
        print("TOKEN=<未配置>")

    # 1) whoami
    r = api("GET", "https://api.github.com/user", token=tok)
    if r.status_code != 200:
        report["note"] = "whoami failed http=%s %s" % (r.status_code, r.text[:160])
        print("WHOAMI=FAIL http=%s" % r.status_code)
        if r.status_code == 401:
            print("原因=token 无效或已过期")
        print(json.dumps(report, ensure_ascii=False, indent=2))
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 2

    me = r.json()
    login = me.get("login")
    report["login"] = login
    report["scopes"] = r.headers.get("X-OAuth-Scopes", "")
    print("LOGIN=%s" % login)
    print("SCOPES=%s" % (report["scopes"] or "(fine-grained 或未知)"))

    if not args.check:
        save_token(tok)
        print("SAVED=%s" % TOKEN_FILE)
        report["action"] = "token_saved"

    # 2) 仓库可达性（404 = 不存在 或 私有无权限，需 token 才能区分）
    rr = api("GET", "https://api.github.com/repos/%s/%s" % (OWNER, REPO), token=tok)
    report["repo_check"] = "http=%s" % rr.status_code
    print("REPO=%s/%s -> http=%s" % (OWNER, REPO, rr.status_code))

    eff_owner = OWNER
    if rr.status_code == 404:
        print("判定=仓库不存在，或存在但当前 token 无读权限（GitHub 两者都返回 404）")
        if not args.create_repo:
            report["note"] = ("仓库不可用；请确认仓库名/归属，或加 --create-repo "
                              "在 %s 名下创建" % login)
            print(json.dumps(report, ensure_ascii=False, indent=2))
            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            return 3
        cr = api("POST", "https://api.github.com/user/repos", token=tok,
                 payload={"name": REPO, "private": True,
                          "description": "P1-GIT-A dualwrite relay (exp)",
                          "auto_init": True})
        print("CREATE_REPO(%s/%s) -> http=%s" % (login, REPO, cr.status_code))
        if cr.status_code not in (200, 201):
            report["note"] = "create failed: %s" % cr.text[:200]
            print(json.dumps(report, ensure_ascii=False, indent=2))
            with open(REPORT_FILE, "w", encoding="utf-8") as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            return 4
        eff_owner = login
        report["action"] = "repo_created"
        print("CREATED=%s/%s" % (eff_owner, REPO))

    # 3) 分支 + 目录骨架
    br = api("GET", "https://api.github.com/repos/%s/%s/branches/%s"
             % (eff_owner, REPO, BRANCH), token=tok)
    report["branch_check"] = "http=%s" % br.status_code
    print("BRANCH=%s -> http=%s" % (BRANCH, br.status_code))

    if args.check:
        report["ok"] = True
        report["effective_target"] = "%s/%s@%s" % (eff_owner, REPO, BRANCH)
        report["note"] = "只读体检完成，未写入仓库任何内容"
        print("CHECK_ONLY=1（未写入仓库）")
        print("TARGET=%s" % report["effective_target"])
        with open(REPORT_FILE, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        return 0

    if br.status_code != 200:
        # 从默认分支创建实验分支
        info = api("GET", "https://api.github.com/repos/%s/%s" % (eff_owner, REPO),
                   token=tok).json()
        default_branch = info.get("default_branch", "main")
        sha = api("GET", "https://api.github.com/repos/%s/%s/commits/%s"
                  % (eff_owner, REPO, default_branch), token=tok).json().get("sha")
        cb = api("POST", "https://api.github.com/repos/%s/%s/git/refs"
                 % (eff_owner, REPO), token=tok,
                 payload={"ref": "refs/heads/%s" % BRANCH, "sha": sha})
        print("CREATE_BRANCH -> http=%s" % cb.status_code)
        report["branch_check"] += " created=http=%s" % cb.status_code
        if cb.status_code not in (200, 201):
            report["note"] = "branch create failed: %s" % cb.text[:200]

    for d in (ORDERS_DIR, ACKS_DIR, RESULTS_DIR):
        seed = "%s/.gitkeep" % d
        pr = put_file(eff_owner, seed, "", "P1-GIT-A: seed %s" % d, BRANCH, tok)
        print("SEED %s -> http=%s" % (seed, pr.status_code))

    sd = os.path.dirname(PROTOCOL_DOC)
    pr = put_file(eff_owner, "%s/.gitkeep" % sd, "", "P1-GIT-A: seed %s" % sd,
                  BRANCH, tok)
    print("SEED %s/.gitkeep -> http=%s" % (sd, pr.status_code))

    report["ok"] = True
    report["effective_target"] = "%s/%s@%s" % (eff_owner, REPO, BRANCH)

    try:
        with open(os.path.join(STATE_DIR, "p1git_owner.txt"), "w", encoding="utf-8") as f:
            f.write(eff_owner)
        print("OWNER_FILE=%s -> %s" % (os.path.join(STATE_DIR, "p1git_owner.txt"), eff_owner))
    except Exception as e:
        print("OWNER_FILE_WRITE_FAILED: %s" % repr(e)[:120])

    print("READY=%s" % report["effective_target"])
    if eff_owner != OWNER:
        print("注意=OWNER 已变为 %s；后续派单需 env P1GIT_OWNER=%s" % (eff_owner, eff_owner))

    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
