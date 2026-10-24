#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P1-GIT-A/C/D | WorkBuddy Git 派单工位 V1.1（物理顺序解题版，--line 选 A/C/D）
---------------------------------------------------------------
北京时间每 30 分钟（整点 / 半点）向实验分支提交一份真实的 CHATGPT_{A/C/D} 物理顺序解题派单（由 --line 指定线路），
从 GitHub 远程独立回读校验，再检查 A 的交付并写自己的 ACK。

WorkBuddy 职责边界（协议 V1.1）：
  只发布真实 Git 任务指令、提交派单、独立回读、写自己的 ACK。
  不替 A 解题，不修改 A 的原始答案，不改动 C/D 派单与既有结果。

序列公式（P1 A 物理顺序）：
  GLOBAL_SEQ = 1 + floor((SLOT - ANCHOR) / 30m)      # 30 分钟一格；ANCHOR=2026-10-23T18:00:00+08:00
  QUESTION_NO = ((GLOBAL_SEQ - 1) mod 24) + 1        # 物理教师版 PDF 题号 1..24 顺序循环
  SCHEDULE_ID = CHATGPT_A_<SLOT_ISO>
"""
import os
import sys
import json
import time
import hashlib
import subprocess
import traceback
from datetime import datetime, timedelta, timezone

import requests

# ============ 线路选择（A / C / D） ============
LINE = "A"
for _i, _a in enumerate(sys.argv):
    if _a == "--line" and _i + 1 < len(sys.argv):
        LINE = sys.argv[_i + 1].strip().upper()[:1]
ASSIGNEE = "CHATGPT_%s" % LINE
Q_OFFSET = {"A": 0, "C": 8, "D": 16}.get(LINE, 0)

# ============ 固定资源 ============
def _load_owner():
    """仓库归属：env P1GIT_OWNER > state/p1git_owner.txt > 默认 kaibahaha"""
    o = os.environ.get("P1GIT_OWNER") or ""
    if not o:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         "state", "p1git_owner.txt")
        if os.path.exists(p):
            try:
                o = open(p, "r", encoding="utf-8").read().strip()
            except Exception:
                o = ""
    return o or "kaibahaha"


OWNER = _load_owner()
REPO = "xxsc"
BRANCH = "exp/p1-relay-dualwrite-20261023"
PROTOCOL_DOC = "docs/03-testing/2026-10-23-P1-Git-Drive-dualwrite-protocol.md"
ORDERS_DIR = "workbuddy/%s_orders" % LINE.lower()
ACKS_DIR = "workbuddy/acks"
A_RESULT_DIR = "results/chatgpt-%s" % LINE.lower()

# 教师 PDF 来源（与 P1-RELAY relay_lib.SOURCES 一致，不得改动）
TEACHER_PDF = {
    "source_key": "PHYSICS",
    "filename": "2025北京五十中高一10月月考物理（教师版）.pdf",
    "gdrive_file_id": "1p6pOP5mWVN9-gYBBxtn3uB7RjUOm6jl5",
    "question_range": [1, 24],
}

BASE = os.path.dirname(os.path.abspath(__file__))
REPO_DIR = os.path.join(BASE, "repo", REPO)
STATE_DIR = os.path.join(BASE, "state")
LOG_DIR = os.path.join(STATE_DIR, "logs")
os.makedirs(STATE_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

CST = timezone(timedelta(hours=8))
ANCHOR = datetime(2026, 10, 23, 18, 0, 0, tzinfo=CST)   # GLOBAL_SEQ=1 的锚点
STOP_AT = datetime(2026, 10, 25, 12, 0, 0, tzinfo=CST)  # 停止派单/Git 写入
# 派单频率：每 30 分钟一格（整点/半点），由 main() 向下取整实现
Q_MIN, Q_MAX = TEACHER_PDF["question_range"]


def _load_token():
    t = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN") or ""
    if not t:
        for p in (os.path.join(STATE_DIR, "github_token.txt"),
                  os.path.join(BASE, ".github_token")):
            if os.path.exists(p):
                t = open(p, "r", encoding="utf-8").read().strip()
                if t:
                    break
    return t


TOKEN = _load_token()


def now_cst():
    return datetime.now(CST)


def log(msg):
    line = "[%s] %s" % (now_cst().strftime("%Y-%m-%d %H:%M:%S"), msg)
    print(line, flush=True)
    try:
        with open(os.path.join(LOG_DIR, "p1git_dispatch.log"), "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def run_git(args, cwd=REPO_DIR):
    e = dict(os.environ)
    e["GIT_TERMINAL_PROMPT"] = "0"
    p = subprocess.run(["git"] + args, cwd=cwd, env=e,
                       capture_output=True, text=True, timeout=180)
    return p.returncode, (p.stdout or "").strip(), (p.stderr or "").strip()


def remote_url():
    if TOKEN:
        return "https://x-access-token:%s@github.com/%s/%s.git" % (TOKEN, OWNER, REPO)
    return "https://github.com/%s/%s.git" % (OWNER, REPO)


SESSION = requests.Session()
SESSION.trust_env = False      # 实测 api/raw 直连可用，代理对 github.com 系列不稳定
SESSION.headers.update({"User-Agent": "P1-GIT-A/1.1"})


def _req(method, url, headers=None, json_body=None, timeout=30, tries=3):
    """带重试的 HTTP 请求（本机代理对 github 域名时通时断，直连 Session + 重试）"""
    last = None
    for i in range(tries):
        try:
            if method == "GET":
                return SESSION.get(url, headers=headers, timeout=timeout)
            return SESSION.put(url, headers=headers, json=json_body, timeout=timeout)
        except Exception as e:
            last = e
            time.sleep(2 + 2 * i)
    raise last


def raw_get(path, ref=None):
    """从 GitHub 远程独立读取（不走本地 git objects）。
    私有仓库的 raw.githubusercontent.com 不接受 Bearer 认证，404 时回退 Contents API。"""
    ref = ref or BRANCH
    url = "https://raw.githubusercontent.com/%s/%s/%s/%s" % (OWNER, REPO, ref, path)
    headers = {}
    if TOKEN:
        headers["Authorization"] = "Bearer %s" % TOKEN
    r = None
    try:
        r = _req("GET", url, headers=headers, timeout=30, tries=4)
    except Exception:
        r = None
    if r is not None and r.status_code == 200:
        return 200, r.text

    if TOKEN:
        aurl = "https://api.github.com/repos/%s/%s/contents/%s?ref=%s" % (
            OWNER, REPO, path, ref)
        try:
            ar = _req("GET", aurl,
                      headers={"Authorization": "Bearer %s" % TOKEN,
                               "Accept": "application/vnd.github+json"},
                      timeout=30, tries=3)
        except Exception as e:
            return -1, "EXC:%s" % type(e).__name__
        if ar.status_code == 200:
            import base64 as _b
            try:
                return 200, _b.b64decode(ar.json()["content"]).decode("utf-8")
            except Exception:
                return 200, ar.json().get("content", "")
        return ar.status_code, ar.text[:200]

    if r is None:
        return -1, "EXC"
    return r.status_code, r.text


# ---------------- API 提交通道（github.com 不可达时的等价 Git 写入） ----------------
def api_head_sha():
    if not TOKEN:
        return ""
    try:
        r = _req("GET", "https://api.github.com/repos/%s/%s/commits/%s"
                 % (OWNER, REPO, BRANCH),
                 headers={"Authorization": "Bearer %s" % TOKEN,
                          "Accept": "application/vnd.github+json"}, timeout=30, tries=3)
        return r.json().get("sha", "") if r.status_code == 200 else ""
    except Exception:
        return ""


def api_put_file(rel_path, content, commit_msg):
    """用 Contents REST API 写入单个文件（等价于一次 git commit + push）。
    返回 (ok, commit_sha_or_error)

    三线路(A/C/D)同写一条分支 exp/...，若同一 tick 并发提交会让分支 HEAD 漂移，
    GitHub Contents API 可能返回 409("is at X but expected Y")——这是分支引用层的
    乐观锁冲突，非文件本身冲突（每次写的是不同路径）。对 409/5xx 做带退避的重试，
    重试前重新探测远端是否已存在该文件，落定后即可成功。
    """
    if not TOKEN:
        return False, "NO_TOKEN"
    url = "https://api.github.com/repos/%s/%s/contents/%s" % (OWNER, REPO, rel_path)
    headers = {"Authorization": "Bearer %s" % TOKEN, "Accept": "application/vnd.github+json"}
    import base64 as _b
    payload = {"message": commit_msg, "branch": BRANCH,
               "content": _b.b64encode(content.encode("utf-8")).decode("ascii")}
    for attempt in range(1, 6):
        code, _t = raw_get(rel_path)
        if code == 200:            # 已存在 -> 视为重复，不覆盖
            return False, "EXISTS_ON_REMOTE"
        try:
            r = _req("PUT", url, headers=headers, json_body=payload, timeout=60, tries=2)
        except Exception as e:
            if attempt >= 5:
                return False, "EXC:%s" % type(e).__name__
            time.sleep(3 * attempt)
            continue
        if r.status_code in (200, 201):
            return True, r.json().get("commit", {}).get("sha", "")
        # 并发分支 HEAD 漂移 -> 409；5xx 瞬时 -> 退避重试
        if r.status_code == 409 or (r.status_code >= 500 and attempt < 5):
            log("api_put 409/5xx (attempt %d) on %s, backoff retry" % (attempt, rel_path))
            time.sleep(3 * attempt)
            continue
        return False, "HTTP%s:%s" % (r.status_code, r.text[:200])
    return False, "HTTP_RETRIES_EXHAUSTED:%s" % rel_path


def ensure_repo():
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        os.makedirs(os.path.dirname(REPO_DIR), exist_ok=True)
        # 本地存在非 git 的同名目录（此前写过的派单草稿）会挡住 clone：
        # 先整体改名保留草稿，不让本地残留污染后续 git 通道
        if os.path.isdir(REPO_DIR) and os.listdir(REPO_DIR):
            import shutil
            shutil.move(REPO_DIR, REPO_DIR + "_draft_" + time.strftime("%Y%m%d%H%M%S"))
        rc, out, err = run_git(["clone", "--branch", BRANCH, remote_url(), REPO_DIR],
                               cwd=os.path.dirname(REPO_DIR))
        if rc != 0:
            return False, "clone failed rc=%s err=%s" % (rc, (err or out)[:300])
        return True, "cloned %s" % BRANCH
    for cmd in (["fetch", "origin", BRANCH], ["checkout", BRANCH],
                ["reset", "--hard", "origin/%s" % BRANCH]):
        rc, out, err = run_git(cmd)
        if rc != 0:
            return False, "%s failed rc=%s err=%s" % (cmd[0], rc, (err or out)[:300])
    return True, "synced %s" % BRANCH


def head_sha():
    if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
        return ""            # 本地无克隆时静默返回，避免 FATAL 掩盖真实失败原因
    rc, out, err = run_git(["rev-parse", "HEAD"])
    return out if rc == 0 else ""


def relay_questions(seq):
    """接力两题：Buddy 做 q_buddy，ChatGPT 做 q_chat（不同题，依次错开）。"""
    span = (Q_MAX - Q_MIN + 1)
    q_buddy = ((seq - 1 + Q_OFFSET) % span) + Q_MIN
    q_chat = ((seq - 1 + Q_OFFSET + 1) % span) + Q_MIN
    return q_buddy, q_chat


def seq_and_question(slot_dt):
    delta = slot_dt - ANCHOR
    seq = int(delta.total_seconds() // 1800) + 1  # 30 分钟一格
    if seq < 1:
        seq = 1
    q_buddy, _qc = relay_questions(seq)
    return seq, q_buddy


def build_order(task_id, slot_dt, created_dt, input_commit, seq, qno):
    sid = "%s_%s" % (ASSIGNEE, slot_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00"))
    relay = LINE in ("C", "D")
    q_buddy, q_chat = relay_questions(seq)
    if relay:
        title = "%s | %s 接力解题派单（Buddy 做 Q%d，ChatGPT 做 Q%d）" % (
            task_id, ASSIGNEE, q_buddy, q_chat)
    else:
        title = "%s | %s 物理顺序解题派单（git-only 测试，不写 Drive）" % (task_id, ASSIGNEE)
    L = []
    L.append("# %s" % title)
    L.append("")
    L.append("## 1. 元信息")
    L.append("")
    L.append("| 字段 | 值 |")
    L.append("|---|---|")
    L.append("| TASK_ID | `%s` |" % task_id)
    L.append("| ASSIGNEE | `%s` |" % ASSIGNEE)
    L.append("| DISPATCHER | `WORKBUDDY`（P1-GIT-%s 工位 V1.1） |" % LINE)
    L.append("| 计划时刻（北京） | `%s` |" % slot_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00"))
    L.append("| CREATED_AT | `%s` |" % created_dt.strftime("%Y-%m-%dT%H:%M:%S+08:00"))
    L.append("| SCHEDULE_ID | `%s` |" % sid)
    L.append("| GLOBAL_SEQ | `%d` |" % seq)
    if relay:
        L.append("| QUESTION_NO (Buddy 段) | `Q%d` |" % q_buddy)
        L.append("| QUESTION_NO (ChatGPT 段) | `Q%d` |" % q_chat)
    else:
        L.append("| QUESTION_NO | `Q%d` |" % qno)
    L.append("| SOURCE_KEY | `%s` |" % TEACHER_PDF["source_key"])
    L.append("| 教师PDF来源ID（Google Drive） | `%s` |" % TEACHER_PDF["gdrive_file_id"])
    L.append("| 教师PDF文件名 | `%s` |" % TEACHER_PDF["filename"])
    L.append("| INPUT_COMMIT | `%s` |" % (input_commit or "UNKNOWN"))
    L.append("| REPO / BRANCH | `%s/%s` / `%s` |" % (OWNER, REPO, BRANCH))
    L.append("| 协议 | `%s` |" % PROTOCOL_DOC)
    L.append("| 实验截止 | `2026-10-25T12:00:00+08:00` |")
    L.append("")

    if relay:
        L.append("## 2. RELAY 接力结构（两题两段）")
        L.append("")
        L.append("- **第 1 段 · Buddy 自解**：WorkBuddy 选 **第 %d 题（Q%d）**，独立完成并交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（地址与原来一致，不另建镜像）。" % (q_buddy, q_buddy))
        L.append("- **第 2 段 · ChatGPT 接手**：再选 **第 %d 题（Q%d）**，由 ChatGPT 读取本派单后在 git 完成并回写。" % (q_chat, q_chat))
        L.append("- 两题不同、互不影响；Buddy 不替 ChatGPT 作答，ChatGPT 不修改 Buddy 的交付。")
        L.append("- **交付覆盖规则（2026-10-24 起生效）**：ChatGPT 段**只回写 git，不额外镜像 Drive**。本规则取代 `TASK-P1-GIT-C/D-20261024-0030` 及更早订单中的「ChatGPT 段（Drive 镜像）：同文件名写入 C/D 资料夹」一句；历史订单不改写，一切以本派单为准。覆盖规则明确前，不得按旧句执行任何 Drive 写入。")
        L.append("")
        L.append("## 3. OBJECTIVE · Buddy 段（自解 Q%d）" % q_buddy)
        L.append("")
        L.append("WorkBuddy 独立求解 **%s 第 %d 题（Q%d）**，来源教师版 PDF：" % (TEACHER_PDF["filename"], q_buddy, q_buddy))
        L.append("`%s`（Google Drive file ID `%s`）。" % (TEACHER_PDF["filename"], TEACHER_PDF["gdrive_file_id"]))
        L.append("")
        L.append("要求：完整读题后给出分步推导与最终答案；结果交付到 Drive 账本 DOCX `1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6`（与 ChatGPT 段同任务目录，与原来一致）。")
        L.append("")
        L.append("## 4. OBJECTIVE · ChatGPT 段（接手 Q%d，git 回写）" % q_chat)
        L.append("")
        L.append("ChatGPT 独立求解 **%s 第 %d 题（Q%d）**，来源同上教师版 PDF。" % (TEACHER_PDF["filename"], q_chat, q_chat))
        L.append("")
        L.append("要求：")
        L.append("1. 完整读题后给出**分步推导**，写明所用物理规律与公式；")
        L.append("2. 给出**最终答案**：选择题只写大写字母 `A/B/C/D`；计算/解答题写数值+单位或表达式；")
        L.append("3. 不得向 WorkBuddy 索取答案，不得引用他人结果；")
        L.append("")
        L.append("## 5. INPUT_FILES")
        L.append("")
        L.append("- 教师版 PDF（Google Drive）：`%s`（file id `%s`）" % (TEACHER_PDF["filename"], TEACHER_PDF["gdrive_file_id"]))
        L.append("- 本派单文件：`%s/TASK-%s.md`（分支 `%s`）" % (ORDERS_DIR, task_id, BRANCH))
        L.append("- 实验协议：`%s`" % PROTOCOL_DOC)
        L.append("")
        L.append("## 6. ACCEPTANCE_CRITERIA")
        L.append("")
        L.append("1. Buddy 段：WorkBuddy 完成 Q%d 并交付到 Drive 账本 DOCX 1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6（地址与原来一致，不另建镜像）；" % q_buddy)
        L.append("2. ChatGPT 段：结果文件名 `%s/%s.md`，正文开头标注 `TASK_ID`、`SCHEDULE_ID`、`GLOBAL_SEQ`、`QUESTION_NO`、`INPUT_COMMIT`；" % (A_RESULT_DIR, task_id))
        L.append("3. ChatGPT 段结果**回写 git**：`%s/%s.md`（分支 `%s`）——**唯一交付地，不额外镜像 Drive**；本要求取代 20261024-0030 及更早订单中的「Drive 镜像」一句，历史订单不改写、以本派单为准；" % (A_RESULT_DIR, task_id, BRANCH))
        L.append("4. 只提交自己的结果文件，不修改 WorkBuddy 的 `%s/`、不修改另一段的派单与既有结果；" % ORDERS_DIR)
        L.append("5. 正文完整，不使用占位符；若读不到题图，依据题干文字作答并注明「未读图」。")
        L.append("")
        L.append("## 7. RESULT_EXPECTED_PATH")
        L.append("")
        L.append("- Buddy 段（Drive）：账本 DOCX 1h_9jKCPw8ecUFNKc9E3-nRrg6fWpzco6 / `%s.md`（与原来一致）" % task_id)
        L.append("- ChatGPT 段（git，唯一交付地）：`%s/%s.md`（分支 `%s`）；**只回写 git，不额外镜像 Drive**（本规则取代 20261024-0030 及更早订单中的「ChatGPT 段（Drive 镜像）：同文件名写入 C/D 资料夹」一句，以本派单为准）" % (A_RESULT_DIR, task_id, BRANCH))
        L.append("")
        L.append("## 8. OUTPUT_CONTRACT（ChatGPT 段）")
        L.append("")
        L.append("```")
        L.append("TASK_ID=%s" % task_id)
        L.append("SCHEDULE_ID=%s" % sid)
        L.append("GLOBAL_SEQ=%d" % seq)
        L.append("QUESTION_NO=Q%d" % q_chat)
        L.append("INPUT_COMMIT=%s" % (input_commit or "UNKNOWN"))
        L.append("RESULT=%s/%s.md" % (A_RESULT_DIR, task_id))
        L.append("```")
        L.append("")
        L.append("## 9. 隔离声明")
        L.append("")
        L.append("WorkBuddy 只负责发布本指令、提交派单、回读 ChatGPT 段结果与写自己的 ACK；")
        L.append("不替 ChatGPT 作答，不修改 ChatGPT 的原始答案，不覆盖任何其它派单、结果或既有代码。")
    else:
        # A：git-only 测试，不让 ChatGPT 写 Drive
        L.append("## 2. OBJECTIVE（解题要求，git-only）")
        L.append("")
        L.append("独立求解 **%s 第 %d 题（Q%d）**，来源教师版 PDF：" % (TEACHER_PDF["filename"], qno, qno))
        L.append("`%s`（Google Drive file ID `%s`）。" % (TEACHER_PDF["filename"], TEACHER_PDF["gdrive_file_id"]))
        L.append("")
        L.append("要求：")
        L.append("1. 完整读题后给出**分步推导**，写明所用物理规律与公式；")
        L.append("2. 给出**最终答案**：选择题只写大写字母 `A/B/C/D`；计算/解答题写数值+单位或表达式；")
        L.append("3. 不得向 WorkBuddy 索取答案，不得引用他人结果；")
        L.append("")
        L.append("## 3. INPUT_FILES")
        L.append("")
        L.append("- 教师版 PDF（Google Drive）：`%s`（file id `%s`）" % (TEACHER_PDF["filename"], TEACHER_PDF["gdrive_file_id"]))
        L.append("- 本派单文件：`%s/TASK-%s.md`（分支 `%s`）" % (ORDERS_DIR, task_id, BRANCH))
        L.append("- 实验协议：`%s`" % PROTOCOL_DOC)
        L.append("")
        L.append("## 4. ACCEPTANCE_CRITERIA（git-only，不写 Drive）")
        L.append("")
        L.append("1. 结果文件名 `%s/%s.md`，正文开头标注 `TASK_ID`、`SCHEDULE_ID`、`GLOBAL_SEQ`、`QUESTION_NO`、`INPUT_COMMIT`；" % (A_RESULT_DIR, task_id))
        L.append("2. **仅回写 git**：`%s/%s.md`（分支 `%s`）；本次不要求写入 Google Drive；" % (A_RESULT_DIR, task_id, BRANCH))
        L.append("3. 正文完整，不使用占位符；若读不到题图，依据题干文字作答并注明「未读图」。")
        L.append("")
        L.append("## 5. RESULT_EXPECTED_PATH")
        L.append("")
        L.append("- GitHub（唯一交付地）：`%s/%s.md`" % (A_RESULT_DIR, task_id))
        L.append("")
        L.append("## 6. OUTPUT_CONTRACT")
        L.append("")
        L.append("```")
        L.append("TASK_ID=%s" % task_id)
        L.append("SCHEDULE_ID=%s" % sid)
        L.append("GLOBAL_SEQ=%d" % seq)
        L.append("QUESTION_NO=Q%d" % qno)
        L.append("INPUT_COMMIT=%s" % (input_commit or "UNKNOWN"))
        L.append("RESULT=%s/%s.md" % (A_RESULT_DIR, task_id))
        L.append("```")
        L.append("")
        L.append("## 7. 隔离声明")
        L.append("")
        L.append("WorkBuddy 只负责发布本指令、提交派单、回读 A 结果与写自己的 ACK；")
        L.append("不替 A 解题，不修改 A 的原始答案，不覆盖任何 C/D 派单、结果或既有代码。")
    L.append("")
    return "\n".join(L), sid


def check_a_result(task_id):
    rel = "%s/%s.md" % (A_RESULT_DIR, task_id)
    code, text = raw_get(rel)
    if code == 200 and text.strip():
        return "A_RESULT_GIT_VERIFIED", len(text)
    if code == 200:
        return "A_RESULT_PENDING_WORK_RELAY", 0
    return "A_RESULT_NOT_SEEN", 0


def drive_probe(task_id):
    """只读探测 Google Drive 端是否已有同题结果（不写入、不修改）"""
    try:
        sys.path.insert(0, r"C:\Users\Administrator\.workbuddy\gdrive")
        import gdrive_core as g  # noqa
        svc = g.get_service()
        q = "name = '%s.md' and trashed = false" % task_id
        res = svc.files().list(q=q, fields="files(id,name,modifiedTime)").execute()
        files = res.get("files", [])
        if files:
            return "DRIVE_SEEN", files[0]["id"]
        return "DRIVE_NOT_SEEN", ""
    except Exception as e:
        return "DRIVE_PROBE_UNAVAILABLE", repr(e)[:120]


def main():
    started = now_cst()
    # 三线路错峰：基于 LINE 的确定性偏移，避免同一 tick 三进程同时打同一分支 HEAD 触发 409
    _jitter = {"A": 0, "C": 7, "D": 15}.get(LINE, 0)
    if _jitter:
        log("line=%s stagger sleep %ds" % (LINE, _jitter))
        time.sleep(_jitter)
    # 偏移 <30m，不跨 slot 边界，TASK_ID/SEQ 计算不受影响
    started = now_cst()
    log("=== RUN START line=%s trigger=%s ===" % (LINE, started.strftime("%Y-%m-%dT%H:%M:%S+08:00")))
    report = {"planned_at": started.strftime("%Y-%m-%dT%H:%M:%S+08:00"), "actual_at": None,
              "task_id": None, "order_path": None, "commit_sha": None, "remote_readback": None,
              "a_result_status": None, "failure_reason": None, "codex_escalated": False,
              "state": None}

    if started >= STOP_AT:
        log("STOP window passed -> read-only")
        report["state"] = "READ_ONLY_AFTER_STOP"
        write_report(report)
        return 0

    api_ok = bool(TOKEN) and bool(api_head_sha())
    if api_ok:
        log("channel=REST_API (api.github.com reachable)")
    else:
        ok, msg = ensure_repo()
        log("ensure_repo: %s | %s" % (ok, msg))
        if not ok and not TOKEN:
            report["state"] = "ERROR"
            report["failure_reason"] = "ENSURE_REPO_FAILED: %s" % msg
            write_report(report)
            write_ticket(report, msg)
            return 2
        if not ok:
            log("git channel unavailable; will still try REST API later")

    # 30 分钟一格：把当前时间向下取整到 :00 / :30 边界
    grid_min = (started.minute // 30) * 30
    slot_dt = started.replace(minute=grid_min, second=0, microsecond=0)
    task_id = "P1-GIT-%s-%s-%s%02d" % (
        LINE, slot_dt.strftime("%Y%m%d"), slot_dt.strftime("%H"), slot_dt.minute)
    rel_order = "%s/TASK-%s.md" % (ORDERS_DIR, task_id)
    abs_order = os.path.join(REPO_DIR, rel_order)

    if os.path.exists(abs_order):
        log("DUPLICATE_SKIP(local) %s" % task_id)
        report.update({"state": "DUPLICATE_SKIP", "task_id": task_id})
        write_report(report)
        return 0
    code, _ = raw_get(rel_order)
    if code == 200:
        log("DUPLICATE_SKIP(remote) %s" % task_id)
        report.update({"state": "DUPLICATE_SKIP", "task_id": task_id})
        write_report(report)
        return 0

    input_commit = api_head_sha() or head_sha()
    seq, qno = seq_and_question(slot_dt)
    _relay = LINE in ("C", "D")
    _qb, _qc = relay_questions(seq)
    _qtag = "Q%d/Q%d" % (_qb, _qc) if _relay else "Q%d" % _qb
    body, sid = build_order(task_id, slot_dt, started, input_commit, seq, qno)
    chash = hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]

    os.makedirs(os.path.dirname(abs_order), exist_ok=True)
    with open(abs_order, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    log("order written %s seq=%d q=%s hash=%s" % (rel_order, seq, _qtag, chash))

    # ---- 提交：REST API 优先（不受 github.com 端点波动影响），git CLI 兜底 ----
    sha, channel, api_err = "", "", ""
    commit_msg = "P1-GIT-%s: dispatch %s (seq=%d %s, input=%s)" % (
        LINE, task_id, seq, _qtag, input_commit[:8])
    if TOKEN:
        okp, res = api_put_file(rel_order, body, commit_msg)
        if okp:
            sha, channel = res, "REST_API"
            log("committed via REST API sha=%s" % sha)
        elif res == "EXISTS_ON_REMOTE":
            log("DUPLICATE_SKIP(remote via API) %s" % task_id)
            report.update({"state": "DUPLICATE_SKIP", "task_id": task_id,
                           "order_path": rel_order})
            write_report(report)
            return 0
        else:
            api_err = res
            log("API put failed: %s -> try git" % res)

    if not sha:
        if not os.path.isdir(os.path.join(REPO_DIR, ".git")):
            ok2, msg2 = ensure_repo()
            if not ok2:
                report.update({"state": "ERROR", "task_id": task_id,
                               "order_path": rel_order,
                               "failure_reason": "NO_WRITE_CHANNEL: api=%s git=%s"
                                                 % (api_err or "no_token", msg2)})
                write_report(report)
                write_ticket(report, "%s | %s" % (api_err, msg2))
                return 4
        rc, out, err = run_git(["add", "--", rel_order])
        if rc != 0:
            report.update({"state": "ERROR", "task_id": task_id, "order_path": rel_order,
                           "failure_reason": "GIT_ADD_FAILED: %s" % (err or out)[:300]})
            write_report(report); write_ticket(report, err or out); return 4
        rc, out, err = run_git(["commit", "-m", commit_msg])
        if rc != 0:
            report.update({"state": "ERROR", "task_id": task_id, "order_path": rel_order,
                           "failure_reason": "GIT_COMMIT_FAILED: %s" % (err or out)[:300]})
            write_report(report); write_ticket(report, err or out); return 5
        rc, out, err = run_git(["push", "origin", "HEAD:%s" % BRANCH])
        if rc != 0:
            run_git(["reset", "--soft", "HEAD~1"])
            report.update({"state": "ERROR", "task_id": task_id, "order_path": rel_order,
                           "failure_reason": "GIT_PUSH_FAILED: %s" % (err or out)[:300]})
            write_report(report); write_ticket(report, err or out); return 6
        sha, channel = head_sha(), "GIT_CLI"
        log("pushed via git sha=%s" % sha)

    rb_state, rb_detail = "READBACK_FAILED", ""
    for _ in range(3):
        c, t = raw_get(rel_order)
        if c == 200 and task_id in t and sid in t and ("GLOBAL_SEQ" in t):
            rb_state = "ORDER_GIT_VERIFIED"
            rb_detail = "http=200 bytes=%d task_id=OK schedule_id=OK content_hash=%s" % (
                len(t.encode("utf-8")), chash)
            break
        rb_detail = "http=%s bytes=%d" % (c, len(t))
        time.sleep(5)
    log("readback %s | %s" % (rb_state, rb_detail))

    a_state, a_len = check_a_result(task_id)
    d_state, d_id = drive_probe(task_id)
    run_id = started.strftime("%Y%m%dT%H%M%S")
    ack_rel = "%s/%s-%s.json" % (ACKS_DIR, task_id, run_id)
    ack = {
        "task_id": task_id, "run_id": run_id, "role": "WORKBUDDY",
        "created_at": started.strftime("%Y-%m-%dT%H:%M:%S+08:00"),
        "repo": "%s/%s" % (OWNER, REPO), "branch": BRANCH,
        "schedule_id": sid, "global_seq": seq, "question_no": _qtag,
        "teacher_pdf_gdrive_id": TEACHER_PDF["gdrive_file_id"],
        "order_path": rel_order, "order_commit": sha, "order_content_sha256_16": chash,
        "remote_readback": rb_state, "remote_readback_detail": rb_detail,
        "a_result_path": "%s/%s.md" % (A_RESULT_DIR, task_id),
        "a_result_status": a_state, "a_result_bytes": a_len,
        "a_drive_status": d_state, "a_drive_file_id": d_id,
        "status": rb_state if a_state == "A_RESULT_NOT_SEEN" else a_state,
        "note": "WorkBuddy 只写自己的派单与 ACK；不替 A 解题，不修改 A 的原始答案。",
    }
    ack_text = json.dumps(ack, ensure_ascii=False, indent=2)
    abs_ack = os.path.join(REPO_DIR, ack_rel)
    os.makedirs(os.path.dirname(abs_ack), exist_ok=True)
    with open(abs_ack, "w", encoding="utf-8", newline="\n") as f:
        f.write(ack_text)
    ack_channel = ""
    if TOKEN:
        oka, resa = api_put_file(ack_rel, ack_text,
                                 "P1-GIT-%s: ack %s %s" % (LINE, task_id, a_state))
        ack_channel = "REST_API" if oka else "FAILED:%s" % resa
        log("ack via API: %s" % ack_channel)
    if ack_channel != "REST_API" and os.path.isdir(os.path.join(REPO_DIR, ".git")):
        if run_git(["add", "--", ack_rel])[0] == 0:
            if run_git(["commit", "-m", "P1-GIT-%s: ack %s %s" % (LINE, task_id, a_state)])[0] == 0:
                if run_git(["push", "origin", "HEAD:%s" % BRANCH])[0] != 0:
                    run_git(["reset", "--soft", "HEAD~1"])
                    log("ack push failed")
                else:
                    ack_channel = "GIT_CLI"

    report.update({"task_id": task_id, "order_path": rel_order, "commit_sha": sha,
                   "remote_readback": "%s (%s)" % (rb_state, rb_detail),
                   "a_result_status": a_state, "state": rb_state,
                   "global_seq": seq, "question_no": _qtag, "schedule_id": sid,
                   "ack_path": ack_rel, "actual_at": now_cst().strftime("%Y-%m-%dT%H:%M:%S+08:00")})
    write_report(report)
    log("=== RUN END %s ===" % rb_state)
    return 0


def write_report(report):
    with open(os.path.join(STATE_DIR, "runs.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(report, ensure_ascii=False) + "\n")
    with open(os.path.join(STATE_DIR, "last_report.json"), "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)


def write_ticket(report, detail=""):
    tp = os.path.join(STATE_DIR, "tickets")
    os.makedirs(tp, exist_ok=True)
    rid = datetime.now(CST).strftime("%Y%m%dT%H%M%S")
    t = {"ticket_id": "P1GIT-A-TICKET-%s" % rid,
         "created_at": datetime.now(CST).strftime("%Y-%m-%dT%H:%M:%S+08:00"),
         "repo": "%s/%s" % (OWNER, REPO), "branch": BRANCH,
         "task_id": report.get("task_id"), "state": report.get("state"),
         "failure_reason": report.get("failure_reason"), "detail": detail,
         "escalate_to": "CODEX_APP_SERVER"}
    with open(os.path.join(tp, "%s.json" % t["ticket_id"]), "w", encoding="utf-8") as f:
        json.dump(t, f, ensure_ascii=False, indent=2)
    log("TICKET %s" % t["ticket_id"])


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        log("FATAL %s" % traceback.format_exc())
        write_report({"state": "ERROR", "failure_reason": "FATAL: %s" % e,
                      "planned_at": now_cst().strftime("%Y-%m-%dT%H:%M:%S+08:00")})
        write_ticket({"state": "ERROR", "failure_reason": "FATAL: %s" % e}, traceback.format_exc())
        sys.exit(9)
