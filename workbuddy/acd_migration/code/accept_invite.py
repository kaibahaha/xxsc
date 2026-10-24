#!/usr/bin/env python3
# 仅用于：检测并接收发给 kaibahaha 的 OutsiderVictor/xxsc 仓库协作者邀请
# 不做任何其他写操作；无邀请则只报告。
import os, json, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.abspath(__file__))
TOKEN = ""
tp = os.path.join(ROOT, "state", "github_token.txt")
if os.path.exists(tp):
    TOKEN = open(tp, "r", encoding="utf-8").read().strip()

def req(method, path, body=None):
    url = "https://api.github.com" + path
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": "Bearer " + TOKEN,
        "Accept": "application/vnd.github+json",
        "User-Agent": "p1git-invite",
    })
    try:
        with urllib.request.urlopen(r, timeout=20) as resp:
            txt = resp.read().decode("utf-8", "ignore")
            return resp.status, (json.loads(txt) if txt else {})
    except urllib.error.HTTPError as e:
        try:
            b = json.loads(e.read().decode("utf-8", "ignore"))
        except Exception:
            b = {}
        return e.code, b

# 1) 列出待接受的邀请（GET，只读）
st, invs = req("GET", "/user/repository_invitations")
print("INVITATIONS_LIST http=", st)
target = None
for inv in (invs if isinstance(invs, list) else []):
    repo = inv.get("repository") or {}
    full = repo.get("full_name") or ""
    if full.lower() == "outsidervictor/xxsc":
        target = inv
        print("  FOUND pending invite id=", inv.get("id"), "repo=", full)
        break
if not target:
    print("  NO pending invite for OutsiderVictor/xxsc (需在 OutsiderVictor 账号先发出邀请)")

# 2) 若有则接受（PUT）
if target:
    iid = target.get("id")
    st2, _ = req("PUT", f"/user/repository_invitations/{iid}")
    print("ACCEPT http=", st2, "(204=已接受)")

# 3) 复探仓库访问
st3, repo = req("GET", "/repos/OutsiderVictor/xxsc")
print("REPO OutsiderVictor/xxsc http=", st3,
      "perms=", repo.get("permissions"), "visibility=", repo.get("visibility"))
