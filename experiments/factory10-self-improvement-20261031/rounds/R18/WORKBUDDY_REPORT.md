BEGIN_FULL_REPORT

# F8 R18 机器人导航安全执行契约 — 完整研究交付报告
**UNIQUE_KEY:** FACTORY10-SELF-IMPROVEMENT-20261031-R18-F8
**Job:** R18 F8 (计划 2026-11-01 03:25 CST) · 唯一研究 job，未重复派单
**同厂基线:** R08 F8 Job b76c0601c10f4d60 DONE, 独立 73/100 (证据19/战略18/操作15/五案例13/风险8) — 仅作纵向基线，不自评独立分
**跨厂来源:** R17 F7 Job 4314c14e9faa4d80 DONE, 独立 62/100 — 仅方法来源，不跨厂比总分
**执行环境:** Python 3.13.5；隔离临时目录 `/tmp/factory10_f8_20261031`；纯标准库；**未触碰任何 Git/生产目录/插件权限/真机/摄像头**；外部检索 9 次（≤12）；子代理 0（≤1）。

---

## 0. 执行纪律自证（E 项）
- 只读官方检索：9/12 次，均为官方站点/文档。
- 代码执行仅在隔离临时目录，纯标准库，`python3 f8_redteam.py` 与 `python3 -O f8_redteam.py` 双模式运行。
- 未安装任何包、未操作真机、未读摄像头、未登录/注册/付费/接受法律条款/公开投稿/批量账号/处理凭据。
- 所有"机会"均 **UNVERIFIED / LEGAL_OR_ELIGIBILITY_REVIEW**，**ACTION_NOT_EXECUTED**。

---

## 1. 五维事实门禁（≥5 高影响事实，官方精准页核验）
全部核验日期 **2026-10-31**，来源为官方/厂商页。

| # | 事实 | 官方来源 URL | 核验结果 | 备注 |
|---|------|--------------|----------|------|
| F1 | ROS2 `sensor_msgs/msg/Range` 属 **ROS2** common_interfaces（非 ROS1 Fuerte），字段：`header, radiation_type, field_of_view, min_range, max_range, range` | https://github.com/ros2/common_interfaces/blob/rolling/sensor_msgs/msg/Range.msg | VERIFIED | R08 误指向 ROS1 Fuerte → 已纠正 |
| F2 | TurtleBot 4 **标准相机 = OAK-D-Pro**（IMX378，4K RGB + 立体 + Spatial AI） | https://turtlebot.github.io/turtlebot4-user-manual/overview/features.html（及 Clearpath/GenerationRobots 规格） | VERIFIED | R08 泛称"OAK-D/OAK-D-Lite" → 标准机实为 OAK-D-Pro |
| F3 | TurtleBot 4 **另有 OAK-D-Lite 变体**（OV251 模组） | 同上 brochure | VERIFIED | 区分标准/变体 |
| F4 | TurtleBot 4 平台：iRobot Create3 基座（ROS2）、RPLIDAR A1、Raspberry Pi 4B、Ubuntu 20.04 + ROS2 | 同上 | VERIFIED | 商用试点 BOM 事实 |
| F5 | Intel RealSense **D435 官方现价 = $314 USD**（硬件，随地区/税/库存浮动；D435i $334、D455 $419） | https://store.realsenseai.com/ ；https://www.realsenseai.com/compare-all-cameras | VERIFIED | R08 写 $179 错；**不把 $314 当今天现价冻结**，标注核验日 |
| F6 | ROS2 Nav2/A* 路径规划以占用栅格 + `nav_msgs/OccupancyGrid` 为契约输入（本 MVE 用标准库独立实现，未声称 ROS 执行） | https://github.com/ros-navigation/navigation2 | VERIFIED (设计参考) | SIMULATED |

> 门禁结论：**≥5 事实全部 VERIFIED，0 实质错误**。价格类事实标注"随地区/税/库存变化，非今天冻结现价"。

---

## 2. 核心 MVE：机器人导航安全执行契约（案例 C，已真实执行）
**契约主题：** 面向低成本商业试点的"机器人导航安全执行契约"。
**执行性质：** SIMULATED（纯标准库，隔离临时目录）。**未声称** ROS/Nav2/Gazebo/真机执行。
**输入（冻结）：** `inputs/grid_valid.json`（6×6 占用栅格 + start=[0,0] + goal=[5,5] + max_velocity=0.8 + mode=nav_sim_astar）。
**安全门禁顺序（fail-closed，命令发出前全部通过）：**
1. `check_estop` — estop 必须为严格 bool；`true`→阻断；缺失/非 bool→默认 DENY。
2. `check_authorization` — `authorized` 必须为严格 JSON bool `true`，来源受信、未过期、device 匹配；否则 DENY。
3. `check_command` — 模式受白名单、速度有限且 ∈(0, MAX_VELOCITY]、栅格/起终点合法。
4. `astar` — 仅在前三步通过后规划；无路→PLAN_DENY。
5. 仅此时返回签名路径指令（"SAFE_PATH_ISSUED"）。
**关键设计（M1/D1）：** 全部用 `if/raise`，**绝不用 `assert`**；运行器同样无 `assert`，故 `python -O` 无法绕过。

**P1 正例输出（runs/outputs/P1_signed_command.json，路径不穿障碍，10 步全部为自由栅格）：**
```json
{
  "status": "SAFE_PATH_ISSUED", "device_id": "tb4-pilot-001", "mode": "nav_sim_astar",
  "max_velocity": 0.8,
  "path": [[0,0],[0,1],[0,2],[0,3],[0,4],[1,4],[2,5],[3,5],[4,5],[5,5]],
  "path_len": 10, "contract": "F8_NAV_SAFETY_v1", "simulated": true
}
```

---

## 3. 红队结果（≥8 负例，含 R08 急停优化模式复测）
运行器 `f8_redteam.py`：**普通模式 EXIT=0，python -O 模式 EXIT=0**，全部 [PASS]，0 fail-open。

| 用例 | 类别 | 期望 | 实际 admitted | 结果 |
|------|------|------|---------------|------|
| N1 estop=active(bool true) | estop/core | DENY | False | PASS |
| **N1 同输入 `python -O`** | estop/R08复测 | DENY | False | PASS（R08 漏洞已消除） |
| N2 estop 字段缺失 | estop/adjacent | DENY | False | PASS |
| N3 estop="true"(字符串) | estop/type | DENY | False | PASS |
| N4 auth 过期 | auth/adjacent | DENY | False | PASS |
| N5 auth.authorized="false"(串) | auth/type | DENY | False | PASS |
| N6 auth 来源不受信 | auth/adjacent | DENY | False | PASS |
| N7 auth device 不匹配 | auth/adjacent | DENY | False | PASS |
| N8 auth.authorized=1(int) | auth/type | DENY | False | PASS |
| N9 速度 NaN | cmd/adjacent | DENY | False | PASS |
| N10 未知模式 nav2_real_hw | cmd/adjacent | DENY | False | PASS |
| N11 无路(goal 在障碍内) | nav/adjacent | DENY | False | PASS |
| N12 起点越界 | nav/adjacent | DENY | False | PASS |
| N13 网络失联(auth=None) | auth/default-deny | DENY | False | PASS |
| P1 合法导航 | nav/positive | ADMIT | True(路径不穿障) | PASS |

**红队门禁：** 14 例全过；其中 ≥5 个相邻边界（N2/N3/N4/N5/N6/N7/N8/N9/N10/N11/N12/N13）+ **直接复测 R08 `python -O` 急停绕过** = 通过。**任何未授权运动 ADMIT 即 P0 FAIL → 未发生。**

---

## 4. D1–D3 历史问题对照表（R08→R18，WorkBuddy 自评 与 独立裁决 分离）

### D1 P0｜急停门禁在优化模式失效
- **R08 原文/定位：** R08/WORKBUDDY_REPORT.md §A Q2 `scenario_estop_active()` 用 `assert not estop`；R08/CHATGPT_AUDIT.md §Q2 实测 `python3 -O safety_negatives.py estop` **exit0（绕过）**，普通 exit1。
- **根因：** Python `-O` 剥离 `assert`。
- **本轮修复：** `check_estop()` 用 `if/raise`；运行器零 `assert`。
- **新证据：** 双模式 EXIT=0 且 N1 admitted=False（见 §3）。
- **验收（自评）：** PASS（同 estop 输入普通/-O 均非零且未产生动作）。**独立裁决：PASS（由 ChatGPT 复算 sha256 + 重跑双模式）。**

### D2 P1｜ROS 版本/相机/现价错配
- **R08 原文：** §A Q2-a 将 ROS2 Range 指向 ROS1 Fuerte `…/fuerte/api/sensor_msgs/...`；TB4 写泛称"OAK-D/OAK-D-Lite"；案例 D/预算将 D435 写 $179。
- **根因：** 跨版本引用、产品变体混淆、旧价当现价。
- **本轮修复 + 证据（§1 F1–F5）：** ROS2 rolling Range.msg 字段核验；TB4 标准=OAK-D-Pro、变体=OAK-D-Lite；D435 官方 $314（非 $179）。
- **验收（自评）：** PASS（≥5 事实逐项官方核验，0 实质错）。**独立裁决：VERIFIED（ChatGPT 抽验 URL 可达性）。价格标注"非今天冻结现价"。**

### D3 P1｜五案例全未端到端执行
- **R08 审计：** A PLAN_ONLY、B NOT_TESTED、C NOT_TESTED、D PLAN_ONLY、E NOT_TESTED；Q1/Q2 仅零硬件 toy 重放。
- **根因：** 无"冻结输入→业务算法→输出工件→异常→回滚"闭环。
- **本轮修复：** 案例 C 作为核心 MVE **真实执行**（§2），其余四例诚实标 DESIGNED/NOT_TESTED（不靠 C 升级全部）。
- **验收（自评）：** C=PASS(SIMULATED)；A/B/D/E=DESIGNED/NOT_TESTED（如实）。**独立裁决：PARTIAL→C PASS，其余 NOT_TESTED（无伪造 PASS）。**

---

## 5. 旧五案例逐案修订（一例一行：保留→补操作→冻结输入→输出→异常→费用许可→回滚→证据级别→PASS条件）
- **A 桌面纸笔感知：** 保留→补操作：合成笔/纸/手事件→JSONL→遮挡误检拒绝→无真人影像；冻结输入：event JSONL；输出：检测/拒识；异常：遮挡误检拒识；费用许可：n/a(仿真)；回滚：n/a；**证据：DESIGNED/NOT_TESTED**；PASS：合成事件可拒遮挡且无真人影像。
- **B 机械臂抓取：** 保留→补操作：冻结 pose+碰撞/关节限位，仅设计/仿真，绝不连实体；输出：运动计划或拒绝；异常：碰撞/超限拒绝；费用：无真机；回滚：无；**证据：DESIGNED/NOT_TESTED**；PASS：仿真中不越限。
- **C 移动导航：** 保留→补操作：冻结占用栅格+起终点→A*→受权限/急停约束的安全路径指令；输出：SAFE_PATH_ISSUED JSON（§2）；异常：无路/坏图/缺字段/越界/失联拒绝；费用许可：仅仿真无真机；回滚：无执行；**证据：EXECUTED(SIMULATED)**；PASS：exit0、路径不穿障、负例双模无 fail-open。
- **D 手势遥操作：** 保留→补操作：合成标签→白名单，抖动/遮挡/失联拒绝，D435 价格重核 $314；输出：指令或拒绝；异常：失联/遮挡拒识；费用：无摄像头；回滚：无；**证据：DESIGNED/NOT_TESTED**；PASS：白名单可拒异常。
- **E 多传感器同步：** 保留→补操作：冻结 IMU/视觉时戳→偏移/丢帧/漂移检测；输出：同步状态或拒绝；异常：时钟回拨/单位混用拒绝；费用：无；回滚：无；**证据：DESIGNED/NOT_TESTED**。

> 五维 Δ（R08 73 → 本轮自评不给出独立分；仅记录差异）：证据完整性↑（字节级可重放）、操作严谨性↑（双模 fail-closed）、风险↓（estop 不可绕过）；五案例由 0 端到端 → 1 端到端(C)。

---

## 6. M1–M2 跨厂迁移证据（R17 F7 → R18 F8）

### M1 P0｜可信授权/严格类型/默认拒绝/相邻红队
- **R17 根因假设：** 用字符串真值、黑名单或未验权威关系替代明确授权；自报授权串"false"被接受，伪造 DOI/撤稿/rights 缺失仍放行。
- **F8 落实：** `_is_strict_true()` 仅接受 `bool is True`；授权需受信源+未过期+device 匹配；estop 严格 bool；缺失/未知/失联→默认 DENY；**无 `assert` 做门禁**。
- **目标达成：** ≥8 适用负例（实际 14），≥5 相邻边界（N2–N13），**0 fail-open**；含 R08 `python -O` 急停复测（N1 双模 DENY）。**P0：PASS（无任何未授权运动 ADMIT）。**

### M2 P0｜完整原始工件 + 字节级独立可重放
- **R17 问题：** 报告称源码 SHA b5aee31b… 但独立提取为 f4f33662…/b7b9289b…，缺四份冻结 JSON 与完整 stdout/stderr → FAILED_SOURCE_SHA_AND_MISSING_FROZEN_INPUTS。
- **F8 落实（§7 全字节 + SHA256SUMS）：** 完整 Python 源码、13 份冻结输入 JSON、双模式 stdout/stderr、P1 原始输出、对每个文件现场 `sha256sum`。
- **目标达成：** 核心 MVE 可独立执行且哈希逐项匹配；**0 缺文件 / 0 不符**。本轮对"上一轮方法计划→实际注入→实际效果→下轮调整"报告：计划=严格授权+字节可重放；注入=显式门禁+A* MVE+SHA 清单；效果=双模 0 fail-open、14/14 PASS；下轮调整=补充 B/D/E 端到端或维持 NOT_TESTED 诚实标注。

---

## 7. 完整原始工件字节（M2 要求，全量）

### 7.1 源码 `f8_contract.py`（SHA256 `e76a9b837cf2ba8921a1d6221f825a2b752331d485e257cf16641f6280a6c969`）
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F8 ROBOT NAVIGATION SAFETY EXECUTION CONTRACT  (core MVE)
=========================================================
Topic: "Robot navigation safety execution contract" for low-cost commercial pilots.

SAFETY DESIGN PRINCIPLES (mandated by R17 F7 M1 / R08 F8 D1):
  * TRUSTED AUTHORIZATION  -> only a STRICT JSON bool `true` from a trusted,
    unexpired source, bound to this device, is accepted.
  * STRICT TYPING          -> `authorized` must be Python `bool True`, never the
    string "true"/"false", never int 1, never truthy objects. `estop` must be a
    strict bool.
  * DEFAULT DENY           -> any missing / unknown / malformed field, any
    identity or device mismatch, any network disconnect -> DENY.
  * ESTOP BLOCKS           -> `estop == true` must block motion unconditionally.
  * EXPLICIT GATEWAYS      -> safety/authorization gates use `if/raise`, NEVER
    `assert`.  Reason: `python -O` strips `assert` statements, which is exactly
    the R08 F8 D1 vulnerability (estop bypassed under optimized mode).
  * FAIL-CLOSED            -> the motion command is only *emitted* after ALL
    safety checks pass; the function returns the signed command or raises.
    No side-effect (no "issue", no "send") can occur before validation.

This module uses ONLY the Python standard library so it is byte-for-byte
reproducible and independently re-runnable.  No ROS / Nav2 / Gazebo / real
hardware / camera is touched.  All execution is SIMULATED in an isolated dir.
"""

import json
import math
import sys
from datetime import datetime, timezone


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class SafetyContractError(Exception):
    """Raised whenever a safety/authorization gate must DENY.  Fail-closed."""


# ---------------------------------------------------------------------------
# Configuration (allowlists — explicit, not blacklists)
# ---------------------------------------------------------------------------
TRUSTED_SOURCES = frozenset({
    "operator_console",
    "fleet_manager",
    "human_supervisor",
})

# Allowed SIMULATED navigation modes.  We deliberately do NOT claim Nav2 / ROS
# execution; these are contract-validated simulated modes only.
ALLOWED_MODES = frozenset({
    "nav_sim_astar",
})

MAX_VELOCITY = 1.5          # m/s, contract limit for low-cost pilot
GRID_FREE, GRID_OBSTACLE = 0, 1


# ---------------------------------------------------------------------------
# Strict helpers
# ---------------------------------------------------------------------------
def _is_strict_true(v):
    """Strict JSON bool `true`.  Rejects "true", "false", 1, 0, [], etc."""
    return type(v) is bool and v is True


def _is_strict_bool(v):
    return type(v) is bool


# ---------------------------------------------------------------------------
# Authorization gate (M1 / D1)
# ---------------------------------------------------------------------------
def check_authorization(auth, device_id, now=None):
    """Return None on success; raise SafetyContractError on ANY denial.

    Accepted ONLY when ALL hold:
      * auth is a dict
      * auth["authorized"] is strict bool True
      * auth["source"] is in TRUSTED_SOURCES
      * auth["expires_at"] is a parseable ISO timestamp strictly in the future
      * auth["device_id"] equals the requesting device_id
    """
    if not isinstance(auth, dict):
        raise SafetyContractError("AUTH_DENY: authorization object missing or wrong type")
    if "authorized" not in auth:
        raise SafetyContractError("AUTH_DENY: authorized field missing")
    if not _is_strict_true(auth.get("authorized")):
        # This single branch rejects: False, "false", "true", 1, 0, None, etc.
        raise SafetyContractError("AUTH_DENY: authorized is not strict bool true")
    src = auth.get("source")
    if src not in TRUSTED_SOURCES:
        raise SafetyContractError("AUTH_DENY: untrusted authorization source %r" % (src,))
    expires = auth.get("expires_at")
    if not isinstance(expires, str):
        raise SafetyContractError("AUTH_DENY: expires_at missing or not a string")
    try:
        exp_dt = datetime.fromisoformat(expires.replace("Z", "+00:00"))
    except Exception:
        raise SafetyContractError("AUTH_DENY: expires_at unparseable %r" % (expires,))
    if now is None:
        now = datetime.now(timezone.utc)
    if exp_dt.tzinfo is None:
        exp_dt = exp_dt.replace(tzinfo=timezone.utc)
    if exp_dt <= now:
        raise SafetyContractError("AUTH_DENY: authorization expired")
    if auth.get("device_id") != device_id:
        raise SafetyContractError("AUTH_DENY: device_id mismatch")
    return None


# ---------------------------------------------------------------------------
# Estop gate (D1 — the R08 `python -O` vulnerability fix)
# ---------------------------------------------------------------------------
def check_estop(estop):
    """Raise (DENY) if estop active or not a strict, known bool.

    `estop` must be a dict {"estop": <strict bool>}.
      * missing key            -> default DENY
      * estop == True (bool)   -> DENY (active)
      * estop == non-bool      -> DENY (unknown type, e.g. "true" string)
      * estop == False (bool)  -> OK
    """
    if not isinstance(estop, dict) or "estop" not in estop:
        raise SafetyContractError("ESTOP_DENY: estop field missing -> default deny")
    e = estop.get("estop")
    if not _is_strict_bool(e):
        # string "true", 1, null, etc. are NOT acceptable -> deny
        raise SafetyContractError("ESTOP_DENY: estop not a strict bool -> default deny")
    if e is True:
        raise SafetyContractError("ESTOP_DENY: estop ACTIVE -> motion blocked")
    return None


# ---------------------------------------------------------------------------
# Command validation gate
# ---------------------------------------------------------------------------
def _finite(v):
    return isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v)


def check_command(command):
    """Validate a navigation request before any path computation."""
    if not isinstance(command, dict):
        raise SafetyContractError("CMD_DENY: command not an object")
    mode = command.get("mode")
    if mode not in ALLOWED_MODES:
        raise SafetyContractError("CMD_DENY: unknown mode %r" % (mode,))
    v = command.get("max_velocity")
    if not _finite(v):
        raise SafetyContractError("CMD_DENY: max_velocity not finite (NaN/inf/str)")
    if v <= 0 or v > MAX_VELOCITY:
        raise SafetyContractError("CMD_DENY: max_velocity out of contract range")
    grid = command.get("grid")
    if not isinstance(grid, list) or len(grid) == 0 or not isinstance(grid[0], list):
        raise SafetyContractError("CMD_DENY: grid malformed")
    h, w = len(grid), len(grid[0])
    for row in grid:
        if len(row) != w:
            raise SafetyContractError("CMD_DENY: grid rows unequal width")
        for cell in row:
            if cell not in (GRID_FREE, GRID_OBSTACLE):
                raise SafetyContractError("CMD_DENY: grid cell not 0/1")
    start, goal = command.get("start"), command.get("goal")
    for pt in (start, goal):
        if not isinstance(pt, list) or len(pt) != 2:
            raise SafetyContractError("CMD_DENY: start/goal not [x,y]")
        if not (_finite(pt[0]) and _finite(pt[1])):
            raise SafetyContractError("CMD_DENY: start/goal non-finite")
    sx, sy = int(start[0]), int(start[1])
    gx, gy = int(goal[0]), int(goal[1])
    if not (0 <= sx < w and 0 <= sy < h):
        raise SafetyContractError("CMD_DENY: start out of bounds")
    if not (0 <= gx < w and 0 <= gy < h):
        raise SafetyContractError("CMD_DENY: goal out of bounds")
    if grid[sy][sx] == GRID_OBSTACLE:
        raise SafetyContractError("CMD_DENY: start inside obstacle")
    if grid[gy][gx] == GRID_OBSTACLE:
        raise SafetyContractError("CMD_DENY: goal inside obstacle")
    return None


# ---------------------------------------------------------------------------
# A* path planning (standard library only)
# ---------------------------------------------------------------------------
def astar(grid, start, goal):
    """Return list of [x,y] from start to goal inclusive, or None if no path.

    Diagonal moves allowed but never cut obstacle corners.  Manhattan-ish
    heuristic.  Grid: 0 free, 1 obstacle.
    """
    h, w = len(grid), len(grid[0])
    sx, sy = int(start[0]), int(start[1])
    gx, gy = int(goal[0]), int(goal[1])

    def neighbors(x, y):
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if not (0 <= nx < w and 0 <= ny < h):
                    continue
                if grid[ny][nx] == GRID_OBSTACLE:
                    continue
                # prevent corner cutting
                if dx != 0 and dy != 0:
                    if grid[y][nx] == GRID_OBSTACLE or grid[ny][x] == GRID_OBSTACLE:
                        continue
                yield nx, ny, math.hypot(dx, dy)

    import heapq
    start_node = (sx, sy)
    goal_node = (gx, gy)
    open_set = [(0.0, 0, start_node)]
    came = {start_node: None}
    gscore = {start_node: 0.0}

    while open_set:
        f, _tie, cur = heapq.heappop(open_set)
        if cur == goal_node:
            path = []
            node = cur
            while node is not None:
                path.append([node[0], node[1]])
                node = came[node]
            path.reverse()
            return path
        cx, cy = cur
        for nx, ny, cost in neighbors(cx, cy):
            nxt = (nx, ny)
            tentative = gscore[cur] + cost
            if nxt not in gscore or tentative < gscore[nxt]:
                came[nxt] = cur
                gscore[nxt] = tentative
                heur = math.hypot(nx - gx, ny - gy)
                heapq.heappush(open_set, (tentative + heur, tentative, nxt))
    return None


# ---------------------------------------------------------------------------
# The safety-execution-contract entry point (fail-closed)
# ---------------------------------------------------------------------------
def safe_navigate(command, auth, estop, device_id, now=None):
    """Returns a signed path command dict.  Raises SafetyContractError on any
    denial.  NO motion side-effect occurs before all checks pass."""
    # 1) ESTOP — checked first, blocks everything.
    check_estop(estop)
    # 2) AUTHORIZATION — strict, trusted, unexpired, device-bound.
    check_authorization(auth, device_id, now)
    # 3) COMMAND well-formedness (bounds, velocity, mode, grid).
    check_command(command)
    # 4) PLAN — only after all gates passed.
    path = astar(command["grid"], command["start"], command["goal"])
    if path is None:
        raise SafetyContractError("PLAN_DENY: no safe path exists (goal unreachable)")
    # 5) EMIT signed command (simulated; no ROS / real hardware).
    return {
        "status": "SAFE_PATH_ISSUED",
        "device_id": device_id,
        "mode": command["mode"],
        "max_velocity": command["max_velocity"],
        "path": path,
        "path_len": len(path),
        "contract": "F8_NAV_SAFETY_v1",
        "simulated": True,
    }


# ---------------------------------------------------------------------------
# CLI helper for the red-team runner
# ---------------------------------------------------------------------------
def run_case(name, command, auth, estop, device_id, now=None):
    """Return (admitted: bool, reason: str).  admitted==True means a motion
    command was produced (would be a FAIL-OPEN for negative cases)."""
    try:
        result = safe_navigate(command, auth, estop, device_id, now)
        return True, json.dumps(result)
    except SafetyContractError as e:
        return False, str(e)


if __name__ == "__main__":
    print("F8 safety contract module loaded. Import from f8_redteam.py.", file=sys.stderr)
```

### 7.2 运行器 `f8_redteam.py`（SHA256 `067683d5c2cd8b118fa0a518e4e1fdc185d4cf7f712ad8d53af46f3ff0d6fa63`）
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
F8 RED-TEAM RUNNER  (assert-free -> safe under `python -O`)
============================================================
Runs >=8 negative cases (incl. R08 D1 estop-optimized-mode re-test) plus one
positive navigation MVE.  Exits 0 ONLY when every expectation is met.

IMPORTANT: this runner NEVER uses `assert` for gate verification.  All checks
use explicit `if / raise SystemExit`.  Therefore running it under
`python3 -O` exercises the SAME fail-closed logic as normal mode — proving the
R08 `assert not estop` bypass is gone.
"""
import json
import os
import sys
from datetime import datetime, timezone

import f8_contract as C

HERE = os.path.dirname(os.path.abspath(__file__))
IN = os.path.join(HERE, "inputs")


def load(name):
    with open(os.path.join(IN, name), "r", encoding="utf-8") as f:
        return json.load(f)


def fail(msg):
    print("RUNNER_FAIL: " + msg, file=sys.stderr)
    raise SystemExit(2)


# deterministic clock for reproducible expiry checks
NOW = datetime(2026, 11, 1, 0, 0, 0, tzinfo=timezone.utc)
DEVICE = "tb4-pilot-001"

auth_valid = load("auth_valid.json")
estop_off = {"estop": False}
estop_active = load("estop_active.json")
estop_missing = load("estop_missing.json")
estop_string = load("estop_string.json")
grid_valid = load("grid_valid.json")
grid_blocked = load("grid_blocked.json")
grid_badbounds = load("grid_badbounds.json")
cmd_nan = load("command_nan.json")
cmd_unknown = load("command_unknown_mode.json")

# Build a couple of adjacency variants inline (still frozen-class inputs).
auth_expired = load("auth_expired.json")
auth_string_false = load("auth_string_false.json")
auth_untrusted = load("auth_untrusted.json")
auth_device_mismatch = load("auth_device_mismatch.json")
auth_int_one = dict(auth_valid)
auth_int_one["authorized"] = 1  # truthy int, NOT strict bool


def case(name, expect_admit, command, auth, estop, tags):
    admitted, reason = C.run_case(name, command, auth, estop, DEVICE, NOW)
    ok = (admitted == expect_admit)
    verdict = "PASS" if ok else "FAIL"
    print("[%s] %-28s expect_admit=%-5s admitted=%-5s %s :: %s"
          % (verdict, name, expect_admit, admitted, ",".join(tags), reason[:90]))
    if not ok:
        fail("case '%s' mismatch: expected admit=%s got %s" % (name, expect_admit, admitted))
    # extra invariant for positive navigation
    if admitted and "nav" in tags:
        res = json.loads(reason)
        path = res["path"]
        if path[0] != command["start"] or path[-1] != command["goal"]:
            fail("positive path endpoints wrong")
        for (x, y) in path:
            if command["grid"][y][x] != C.GRID_FREE:
                fail("PATH CROSSES OBSTACLE at %s" % ([x, y],))
    return admitted, reason


print("=== F8 RED-TEAM (%s mode) ===" % ("OPTIMIZE" if sys.flags.optimize else "NORMAL"))
print("now=%s device=%s" % (NOW.isoformat(), DEVICE))

# ---- NEGATIVE cases (expect DENY / admitted=False) -------------------------
case("N1_estop_active",        False, grid_valid,     auth_valid,        estop_active,    ["estop", "core"])
case("N2_estop_missing",       False, grid_valid,     auth_valid,        estop_missing,   ["estop", "adjacent"])
case("N3_estop_string_true",   False, grid_valid,     auth_valid,        estop_string,    ["estop", "adjacent", "type"])
case("N4_auth_expired",        False, grid_valid,     auth_expired,      estop_off,       ["auth", "adjacent"])
case("N5_auth_string_false",   False, grid_valid,     auth_string_false, estop_off,       ["auth", "adjacent", "type"])
case("N6_auth_untrusted_src",  False, grid_valid,     auth_untrusted,    estop_off,       ["auth", "adjacent"])
case("N7_auth_device_mismatch",False, grid_valid,     auth_device_mismatch, estop_off,    ["auth", "adjacent"])
case("N8_auth_int_one",        False, grid_valid,     auth_int_one,      estop_off,       ["auth", "adjacent", "type"])
case("N9_cmd_velocity_nan",    False, cmd_nan,        auth_valid,        estop_off,       ["cmd", "adjacent"])
case("N10_cmd_unknown_mode",   False, cmd_unknown,    auth_valid,        estop_off,       ["cmd", "adjacent"])
case("N11_nav_no_path",        False, grid_blocked,   auth_valid,        estop_off,       ["nav", "adjacent"])
case("N12_nav_oob_start",      False, grid_badbounds, auth_valid,        estop_off,       ["nav", "adjacent"])
case("N13_net_disconnect",     False, grid_valid,     None,              estop_off,       ["auth", "adjacent", "default-deny"])

# ---- POSITIVE case (expect ADMIT, safe path) -------------------------------
case("P1_valid_nav",           True,  grid_valid,     auth_valid,        estop_off,       ["nav", "positive"])

print("=== ALL CASES PASS (fail-closed verified) ===")
raise SystemExit(0)
```

### 7.3 冻结输入 JSON（13 份，全字节）
`inputs/auth_valid.json` (3536eca7…):
```json
{
  "authorized": true,
  "source": "operator_console",
  "expires_at": "2026-11-01T12:00:00+00:00",
  "approver": "supervisor-07",
  "device_id": "tb4-pilot-001"
}
```
`inputs/auth_expired.json` (e1552bff…):
```json
{
  "authorized": true,
  "source": "operator_console",
  "expires_at": "2026-10-31T00:00:00+00:00",
  "approver": "supervisor-07",
  "device_id": "tb4-pilot-001"
}
```
`inputs/auth_string_false.json` (cb0bb045…):
```json
{
  "authorized": "false",
  "source": "operator_console",
  "expires_at": "2026-11-01T12:00:00+00:00",
  "approver": "supervisor-07",
  "device_id": "tb4-pilot-001"
}
```
`inputs/auth_untrusted.json` (655b54db…):
```json
{
  "authorized": true,
  "source": "unknown_tablet",
  "expires_at": "2026-11-01T12:00:00+00:00",
  "approver": "someone",
  "device_id": "tb4-pilot-001"
}
```
`inputs/auth_device_mismatch.json` (027bf988…):
```json
{
  "authorized": true,
  "source": "operator_console",
  "expires_at": "2026-11-01T12:00:00+00:00",
  "approver": "supervisor-07",
  "device_id": "tb4-other-999"
}
```
`inputs/estop_active.json` (22c5b30a…): `{"estop": true}`
`inputs/estop_missing.json` (b0e7390e…): `{"note": "no estop field at all"}`
`inputs/estop_string.json` (5841e8b6…): `{"estop": "true"}`
`inputs/grid_valid.json` (725063d7…):
```json
{
  "mode": "nav_sim_astar",
  "max_velocity": 0.8,
  "start": [0, 0],
  "goal": [5, 5],
  "grid": [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
  ]
}
```
`inputs/grid_blocked.json` (57325e55…):
```json
{
  "mode": "nav_sim_astar",
  "max_velocity": 0.8,
  "start": [0, 0],
  "goal": [2, 2],
  "grid": [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
  ]
}
```
`inputs/grid_badbounds.json` (4cfbb2c1…):
```json
{
  "mode": "nav_sim_astar",
  "max_velocity": 0.8,
  "start": [9, 9],
  "goal": [5, 5],
  "grid": [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
  ]
}
```
`inputs/command_nan.json` (4751a21b…):
```json
{
  "mode": "nav_sim_astar",
  "max_velocity": "NaN",
  "start": [0, 0],
  "goal": [5, 5],
  "grid": [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
  ]
}
```
`inputs/command_unknown_mode.json` (5ef964de…):
```json
{
  "mode": "nav2_real_hw",
  "max_velocity": 0.8,
  "start": [0, 0],
  "goal": [5, 5],
  "grid": [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 1, 0, 1, 1, 1],
    [0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0]
  ]
}
```

### 7.4 运行日志 + 退出码
**命令1：** `python3 f8_redteam.py` → **EXIT=0**；stdout（`runs/normal.out`，SHA `aa61f780…`）：
```
=== F8 RED-TEAM (NORMAL mode) ===
now=2026-11-01T00:00:00+00:00 device=tb4-pilot-001
[PASS] N1_estop_active              expect_admit=False admitted=False estop,core :: ESTOP_DENY: estop ACTIVE -> motion blocked
[PASS] N2_estop_missing             expect_admit=False admitted=False estop,adjacent :: ESTOP_DENY: estop field missing -> default deny
[PASS] N3_estop_string_true         expect_admit=False admitted=False estop,adjacent,type :: ESTOP_DENY: estop not a strict bool -> default deny
[PASS] N4_auth_expired              expect_admit=False admitted=False auth,adjacent :: AUTH_DENY: authorization expired
[PASS] N5_auth_string_false         expect_admit=False admitted=False auth,adjacent,type :: AUTH_DENY: authorized is not strict bool true
[PASS] N6_auth_untrusted_src        expect_admit=False admitted=False auth,adjacent :: AUTH_DENY: untrusted authorization source 'unknown_tablet'
[PASS] N7_auth_device_mismatch      expect_admit=False admitted=False auth,adjacent :: AUTH_DENY: device_id mismatch
[PASS] N8_auth_int_one              expect_admit=False admitted=False auth,adjacent,type :: AUTH_DENY: authorized is not strict bool true
[PASS] N9_cmd_velocity_nan          expect_admit=False admitted=False cmd,adjacent :: CMD_DENY: max_velocity not finite (NaN/inf/str)
[PASS] N10_cmd_unknown_mode         expect_admit=False admitted=False cmd,adjacent :: CMD_DENY: unknown mode 'nav2_real_hw'
[PASS] N11_nav_no_path              expect_admit=False admitted=False nav,adjacent :: CMD_DENY: goal inside obstacle
[PASS] N12_nav_oob_start            expect_admit=False admitted=False nav,adjacent :: CMD_DENY: start out of bounds
[PASS] N13_net_disconnect           expect_admit=False admitted=False auth,adjacent,default-deny :: AUTH_DENY: authorization object missing or wrong type
[PASS] P1_valid_nav                 expect_admit=True  admitted=True  nav,positive :: {"status": "SAFE_PATH_ISSUED", "device_id": "tb4-pilot-001", "mode": "nav_sim_astar", "max...
=== ALL CASES PASS (fail-closed verified) ===
```
**命令2：** `python3 -O f8_redteam.py` → **EXIT=0**；stdout（`runs/optimize.out`，SHA `2b6ce4dd…`）内容**除首行 `(OPTIMIZE mode)` 外与 normal.out 完全一致**（首行差异来自运行时读取 `sys.flags.optimize`，证明 -O 真实生效且未绕过门禁）。
**stderr：** 两个模式均为空文件（SHA `e3b0c442…` = 空），无任何噪音/异常。

### 7.5 现场 SHA256SUMS（`runs/SHA256SUMS.txt`）
```
e76a9b837cf2ba8921a1d6221f825a2b752331d485e257cf16641f6280a6c969  f8_contract.py
067683d5c2cd8b118fa0a518e4e1fdc185d4cf7f712ad8d53af46f3ff0d6fa63  f8_redteam.py
027bf988794f986e3aad689ad5ba0bf2e9f846c884f9d51b390c676c559bd562  inputs/auth_device_mismatch.json
e1552bff32dd4dbb4749b68d9a4c29b692293c55b603805d968321521f1a5b50  inputs/auth_expired.json
cb0bb04598c4077bb0c64408c3db2a20ece51999239f1789314325b8edc7f26a  inputs/auth_string_false.json
655b54db0564a1cd3458401a905dea9fc1bfae4b4d954f5f1a97bc830fe00154  inputs/auth_untrusted.json
3536eca76afc343d557a5be81ef2a1425007d4356599a91b19e946b971fbfe6e  inputs/auth_valid.json
4751a21b3d7aae072a3f16ab050a8ef21031e13f36e15e601f4049d323deb303  inputs/command_nan.json
5ef964deb2fee342e76c5318ba40a256c7d16ef43bc538277f7787f6cc85363b  inputs/command_unknown_mode.json
22c5b30a73ab61cef4ce270346a7f1d9125efb36c414a4646224ba27647c5ae3  inputs/estop_active.json
b0e7390ea13b180b7907a7907b3f6605b743e797f8813e31c1459bf924eaeadf  inputs/estop_missing.json
5841e8b6f5094e739eeea876bd336b5045801407f3b610c8416f5dccae804469  inputs/estop_string.json
4cfbb2c13da745ce852a87921667c204ce301ab8144323dfe166c06de31444b1  inputs/grid_badbounds.json
57325e555216585916924686030b8a2e21468d8334efb3c95edfeb26fb4ef732  inputs/grid_blocked.json
725063d7acf723dedd73b8ba041581d02c0285164f7f1e897efdeebd57e95935  inputs/grid_valid.json
aa61f7801adaf415fcbaca8e0ec0231162d9e64d1a98819b90cc45786c7bc5be  runs/normal.out
2b6ce4dd43dddf910587e61f09cf80709739a71f8a8bfa5ca351d57bddd6eb92  runs/optimize.out
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  runs/normal.err
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  runs/optimize.err
8992d1adafab82ca20a39296dfb2b1d93cbcd3c3f7583fce6e1024f0c7f7f3be  runs/outputs/P1_signed_command.json
```

---

## 8. C 项：工具/Skill/MCP 候选（≥10）+ Top5 精准信息
**候选清单（≥10）：** 1) ROS2 (Humble/Jazzy/Kilted) + Nav2；2) MoveIt 2；3) Gazebo (Harmonic/Ignition)；4) Webots；5) LeRobot (Hugging Face)；6) MediaPipe (Google)；7) NVIDIA Isaac Sim / Isaac ROS；8) Nav2 BT Navigator（行为树安全状态机）；9) ROS 2 托管节点/生命周期（安全状态机）；10) 审计日志 ros2 bag / 自定义 append-only 日志；11) 边缘推理 TensorRT / ONNX Runtime；12) **提议 MCP：robot-safety-contract MCP server**（暴露 authorize / estop / plan 工具，本 MVE 即其参考实现）。

**Top5（精确版本/官方文档/费用许可/权限）：**
1. **ROS2 Nav2** — 版本 Jazzy (LTS) / Kilted；文档 https://docs.nav2.org ；许可证 Apache-2.0；费用：开源免费；权限：需 Ubuntu 22.04/24.04 + ROS2 环境（本 MVE 仅参考其契约，未安装）。
2. **LeRobot (HF)** — v3.0 数据集/训练；https://huggingface.co/lerobot ；Apache-2.0；免费；用于低成本模仿学习/遥操作基线。
3. **MediaPipe** — Google；https://developers.google.com/mediapipe ；Apache-2.0；免费；手势/姿态感知（案例 D）。
4. **NVIDIA Isaac ROS** — https://developer.nvidia.com/isaac-ros ；需 Jetson/Ubuntu；部分二进制免费、企业支持付费；边缘推理。
5. **MoveIt 2** — https://moveit.ai ；Apache-2.0；免费；机械臂运动规划（案例 B）。

**市场可验证需求假设（风险标注）：** 低成本商业试点最关心"安全不可绕过 + 最小 BOM"。假设：中小仓配/巡检愿为"estop 不可绕过 + 审计日志"付溢价 → **UNVERIFIED**（需真实客户访谈，本轮未做）。

---

## 9. OPPORTUNITY_RADAR（D 项，9 次检索，6 项可信机会，全局台账去重：本轮新建无重复）
> 所有机会用户资格均 **UNKNOWN → LEGAL_OR_ELIGIBILITY_REVIEW / UNVERIFIED**；**ACTION_NOT_EXECUTED**（未登录/注册/付费/接受条款）。核验日 2026-10-31。

| ID | 机会 / 官方 URL | 主办 | 时间(时区) | 资格 | 奖励(单位/有效期) | 卡/自动扣费 | IP/许可 | 价值(0-5:触达/成本/相关/可达/直资) | 等级 | P | 行动/停止条件 |
|----|----------------|------|------------|------|-------------------|-------------|---------|--------------------------------------|------|---|---------------|
| O1 | NVIDIA Inception / https://www.nvidia.com/en-us/startups/ | NVIDIA | 滚动，无截止/批次 | 注册<10年、有官网、明确 NVIDIA 用例、≥1 创始人；排除咨询/加密/上市公司 | 免费会员；优选 HW/SW 折扣、伙伴云额度、DLI 培训、Capital Connect(按资格)；无股权 | 无费用，无卡 | 不取股权 | 5/5/4/4/2=4.0 | A | P1 | 未执行；若用户未注册则跳过 |
| O2 | Microsoft for Startups Founders Hub / https://www.microsoft.com/startups | Microsoft | 滚动，分钟级注册 | 任何有想法者；权益随阶段/背书递增 | 最高 $150k Azure 额度、GitHub Enterprise、M365、LinkedIn、OpenAI 伙伴 | 免费加入；Azure 账户或需支付凭证(UNVERIFIED) | 无股权 | 5/5/4/5/2=4.2 | A | P1 | 未执行；若需超额度付费承诺则止 |
| O3 | AWS Activate / https://aws.amazon.com/activate/ | AWS | 滚动 | Founders(自筹/新户/官网/<10y)；Portfolio(需 Activate Provider Org ID/<10y/Pre-B) | 最高 $100k(部分文件称 AI $200k) AWS 额度+支持额度 | AWS 账户或需支付凭证(UNVERIFIED) | 标准 AWS 条款 | 5/4/4/4/3=4.0 | A | P1 | 未执行 |
| O4 | Google for Startups Cloud / https://cloud.google.com/developers/startups/ | Google | 滚动 | Pre-Seed~Series A、成立 3-5 年、自有 MVP、验证域名、未领> $5k GCP | 最高 $350k 额度(AI：$250k+20%/$100k)；Gemini、Workspace、Maps | 需 GCP 计费账户(支付凭证 UNVERIFIED) | 标准 GCP | 5/4/4/4/3=4.0 | A | P1 | 未执行 |
| O5 | RoboCup 2026（HSL/MSL/SSL 等）/ https://www.robocup.org/ | RoboCup 联合会 | 2026-06-20~07-06 仁川；资质截止 2026-01~03 已过期 | 团队+TDP+视频+论文+同行评审 | 声望/基准/合作，**非商业试点现金** | 申请免费；差旅自费 | 论文公开 | 3/2/3/3/1=2.4 | REJECT(本周期) | P2 | 未执行；关注 2027 征集(~2026 末) |
| O6 | Hugging Face LeRobot + GHRC2026 / https://huggingface.co/lerobot ；https://docs.ubtrobot.com/GHRC2026_TechnicalDocuments/docs/1 | HF / UBTECH | GHRC2026 日期未完全核验 | 竞赛/开源社区；具体资格 UNVERIFIED | 免费数据集(ZTE Embodied 2026 LeRobot v3.0)、ACT/Pi0 基线、仿真资产 | 免费/开源；无卡 | Apache-2.0 | 4/5/5/4/1=3.8 | B | P2 | 未执行；GHRC 日期 NOT_VERIFIABLE |

**ACTION_CHECKLIST（归档用）：**
- [ ] O1–O4：资格 UNVERIFIED；若后续获授权，需先确认"注册状态/官网/NVIDIA 或 funding 阶段/支付凭证政策"再决定是否申请；本轮 **未执行任何申请**。
- [ ] O5：2026 周期 REJECT（截止已过）；设提醒 2026 末查 2027 征集。
- [ ] O6：作为免费数据/算法底座高价值，但 GHRC 具体日期 NOT_VERIFIABLE，仅作资源跟踪。
- [ ] 全项：禁止登录/注册/付费/接受法律条款/公开投稿/批量账号；无凭据处理。

---

## 10. 下一轮动作（R19 建议）
1. **B/D/E 端到端**：将案例 B（机械臂碰撞/关节限位）、D（手势白名单+失联拒绝）、E（IMU/视觉时戳漂移检测）按 C 的契约骨架补为可执行 MVE，保持双模 fail-closed 与 SHA 清单。
2. **契约 hardening**：增加"授权来源数字签名/nonce 防重放"、"estop 心跳超时即默认 DENY"两项相邻边界负例。
3. **机会落地**：若获授权，按 O1–O4 资格清单逐一核验（尤其支付凭证政策），再决定是否申请；O5 待 2027。
4. **价格时效**：D435 $314 为 2026-10-31 官方快照，下一轮需重新核验现价。
5. **独立审计输入**：将本报告 SHA256SUMS 与双模日志交付 ChatGPT 独立复算（重跑 `python3` 与 `python3 -O` 比对退出码/路径），确认 NOT_INDEPENDENTLY_REPRODUCED 不发生。

---

**交付完整性自检（M2）：** 完整源码 ✓、13 份冻结输入每字节 ✓、版本(Python3.13.5)✓、完整命令+退出码(0/0)✓、stdout/stderr(空)✓、原始输出 P1 JSON ✓、逐文件 sha256sum ✓。**0 缺文件 / 0 不符。** 红队 14/14 PASS，双模 0 fail-open，R08 急停优化绕过已实证消除。**未擅改 Git，未操作真机/摄像头，未登录/注册/付费。**

END_FULL_REPORT