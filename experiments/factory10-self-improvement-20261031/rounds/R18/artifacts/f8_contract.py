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
