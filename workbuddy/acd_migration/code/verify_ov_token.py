#!/usr/bin/env python3
# 静默验证 OutsiderVictor classic PAT：身份 / scope / 对目标仓库写权限（不打印 token）
import os, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = open(os.path.join(ROOT, "state", "github_token_outsidervictor.txt"),
             "r", encoding="utf-8").read().strip()

def req(method, path):
    url = "https://api.github.com" + path
    r = urllib.request.Request(url, method=method, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "p1git-verify",
    })
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            return resp.status, dict(resp.headers), json.loads(resp.read().decode("utf-8", "ignore") or "{}")
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), {}

st, hdrs, me = req("GET", "/user")
print("WHOAMI         :", st, "login=", me.get("login"), "id=", me.get("id"))
print("SCOPES         :", hdrs.get("X-OAuth-Scopes"))
print("RATELIMIT_LEFT :", hdrs.get("X-RateLimit-Remaining"))
st2, _, repo = req("GET", "/repos/OutsiderVictor/xxsc")
print("REPO OutsiderVictor/xxsc:", st2, "perms=", repo.get("permissions"), "visibility=", repo.get("visibility"))
