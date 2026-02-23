# telos_core.py  (TelosCore v1.1 - Stable Competition Build)

import time
import requests
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

# =========================
# 基础配置
# =========================

EVERMEMOS_API = "http://localhost:1995/api/v1"
USER_ID = "user_001"

WEIGHTS = {
    "uncertainty": 1.2,
    "conflict": 1.8,
    "entropy": 1.0,
    "telos": 1.4,
}

ACTION_EFFECT = {
    "clarify":  {"uncertainty": -0.6},
    "patch":    {"conflict": -0.8},
    "compress": {"entropy": -0.7},
    "respond":  {"telos_distance": -0.4, "uncertainty": +0.1},
}

# =========================
# v1.1 Plasticity 开关
# =========================

PLASTICITY = 1
PLASTICITY_TRIGGER_U = 0.8
ANNEAL_RATE = 0.15
REINFORCE_RATE = 0.05
MIN_WEIGHT_KEEP = 0.25
RECENT_WINDOW = 30

# =========================
# 状态
# =========================

@dataclass
class TelosState:
    uncertainty: float = 0.4
    conflict: float = 0.0
    entropy: float = 0.0
    telos_distance: float = 0.5
    phase: str = "initial"

state = TelosState()
energy_history: List[float] = []
component_history: List[Dict[str, float]] = []
local_memories: List[Dict[str, Any]] = []

def clamp01(x: float) -> float:
    return max(0.0, min(1.0, x))

# =========================
# 存储
# =========================

def store_event(content: str):
    local_memories.append({
        "content": content,
        "timestamp": time.time(),
        "weight": 1.0
    })

    try:
        requests.post(
            f"{EVERMEMOS_API}/memories",
            json={"content": content, "user_id": USER_ID},
            timeout=2
        )
    except:
        pass

def retrieve_context(query: str):
    try:
        resp = requests.post(
            f"{EVERMEMOS_API}/memories/search",
            json={"query": query, "user_id": USER_ID},
            timeout=3
        )
        return resp.json().get("memories", [])
    except:
        candidates = local_memories[-80:]
        filtered = [m for m in candidates if m["weight"] >= MIN_WEIGHT_KEEP]
        filtered.sort(key=lambda x: x["weight"], reverse=True)
        return filtered[:6]

# =========================
# 信号更新
# =========================

def update_signals(text: str):
    words = len(text.split())
    state.entropy = clamp01(state.entropy + words / 200.0)

    if any(k in text for k in ["但是", "不过", "却", "相反", "一方面", "另一方面"]):
        state.conflict = clamp01(state.conflict + 0.45)

    if any(k in text for k in ["也许", "不确定", "不知道", "可能", "大概"]):
        state.uncertainty = clamp01(state.uncertainty + 0.35)

    if any(k in text for k in ["目标", "计划", "想要", "打算", "决定"]):
        state.telos_distance = clamp01(state.telos_distance - 0.15)
    else:
        state.telos_distance = clamp01(state.telos_distance + 0.05)

# =========================
# 能量
# =========================

def energy_components(s: TelosState):
    u_unc = WEIGHTS["uncertainty"] * s.uncertainty
    u_con = WEIGHTS["conflict"] * s.conflict
    u_ent = WEIGHTS["entropy"] * s.entropy
    u_tel = WEIGHTS["telos"] * s.telos_distance
    total = u_unc + u_con + u_ent + u_tel
    return {
        "total": total,
        "uncertainty": u_unc,
        "conflict": u_con,
        "entropy": u_ent,
        "telos": u_tel,
    }

def apply_effect(s: TelosState, effect: dict):
    ns = TelosState(**asdict(s))
    for k, v in effect.items():
        if hasattr(ns, k):
            setattr(ns, k, clamp01(getattr(ns, k) + v))
    return ns

def choose_action(s: TelosState):
    current = energy_components(s)["total"]
    best_action = "respond"
    best_delta = 0.0

    for act, eff in ACTION_EFFECT.items():
        ns = apply_effect(s, eff)
        nxt = energy_components(ns)["total"]
        delta = nxt - current
        if delta < best_delta:
            best_delta = delta
            best_action = act

    return best_action, round(best_delta, 4)

def respond_text(action: str):
    if action == "clarify":
        return "我还不够确定。你更偏向哪一种：A) 继续当前想法  B) 改成相反做法？"
    if action == "patch":
        return "我检测到内部冲突。更像：A) 场景变了  B) 身体/状态变了？"
    if action == "compress":
        state.phase = "compressed"
        return "我先把近期信息整理压缩成更清晰的要点，再继续。"
    return "收到。我继续沿着当前目标给出下一步建议。"

# =========================
# Plasticity
# =========================

def plasticity_score():
    if not local_memories:
        return 1.0
    recent = local_memories[-10:]
    return round(sum(m["weight"] for m in recent) / len(recent), 3)

def anneal_memories(triggered: bool):
    if not PLASTICITY:
        return

    if state.telos_distance < 0.3:
        for m in local_memories[-12:]:
            m["weight"] = clamp01(m["weight"] + REINFORCE_RATE)

    if not triggered:
        return

    window = local_memories[-RECENT_WINDOW:]
    for m in window:
        decay = ANNEAL_RATE * (0.5 + 0.5 * max(state.conflict, state.entropy))
        m["weight"] = clamp01(m["weight"] - decay)

# =========================
# 主逻辑
# =========================

def telos_step(user_input: str):
    store_event(user_input)
    update_signals(user_input)

    comps_before = energy_components(state)
    action, delta = choose_action(state)

    new_state = apply_effect(state, ACTION_EFFECT[action])
    state.uncertainty = new_state.uncertainty
    state.conflict = new_state.conflict
    state.entropy = new_state.entropy
    state.telos_distance = new_state.telos_distance

    comps_after = energy_components(state)
    energy_history.append(round(comps_after["total"], 4))
    component_history.append(comps_after)

    triggered = comps_before["total"] >= PLASTICITY_TRIGGER_U
    anneal_memories(triggered)

    ctx = retrieve_context(user_input[:20])

    return {
        "response": respond_text(action),
        "action": action,
        "delta_U": delta,
        "energy": round(comps_after["total"], 4),
        "components": {k: round(v, 4) for k, v in comps_after.items()},
        "plasticity_enabled": PLASTICITY,
        "plasticity_score": plasticity_score(),
        "plasticity_triggered": triggered,
        "phase": state.phase,
        "context_size": len(ctx),
    }