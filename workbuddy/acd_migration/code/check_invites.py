#!/usr/bin/env python3
# 只读：核对 kaibahaha/xxsc 的待处理协作者邀请与当前协作者列表
import os, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = ""
tp = os.path.join(ROOT, "state", "github_token.txt")
if os.path.exists(tp):
    TOKEN = open(tp, "r", encoding="utf-8").read().strip()

def req(method, path):
    url = "https://api.github.com" + path
    r = urllib.request.Request(url, method=method, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "p1git-invite-check",
    })
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            return resp.status, json.loads(resp.read().decode("utf-8", "ignore") or "[]")
    except urllib.error.HTTPError as e:
        return e.code, []

st, invs = req("GET", "/repos/kaibahaha/xxsc/invitations")
print("PENDING_INVITATIONS http=", st)
for inv in (invs if isinstance(invs, list) else []):
    invitee = (inv.get("invitee") or {}).get("login", "?")
    perms = inv.get("permissions", "?")
    print(f"  invitee={invitee}  perms={perms}  invitation_id={inv.get('id')}")

st2, cols = req("GET", "/repos/kaibahaha/xxsc/collaborators")
print("COLLABORATORS http=", st2)
for c in (cols if isinstance(cols, list) else []):
    print(f"  login={c.get('login')}  perms={c.get('permissions')}")
