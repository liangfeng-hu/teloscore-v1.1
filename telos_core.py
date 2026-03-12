# telos_core.py
import time
import requests
from dataclasses import dataclass, asdict
from typing import List, Dict, Any

from evermemos_client import EverMemOSClient

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
    "clarify": {"uncertainty": -0.6},
    "patch": {"conflict": -0.8},
    "compress": {"entropy": -0.7},
    "respond": {"telos_distance": -0.4, "uncertainty": +0.1},
}

# EverMemOS integration
memory_client = EverMemOSClient(base_url="http://localhost:1995", user_id=USER_ID)

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
# 存储（保留本地回退）
# =========================
def store_event_local(content: str):
    local_memories.append({
        "content": content,
        "timestamp": time.time(),
        "weight": 1.0
    })

    # 保持旧接口兼容：本地 + 远端都尝试
    try:
        requests.post(
            f"{EVERMEMOS_API}/memories",
            json={"content": content, "user_id": USER_ID},
            timeout=2
        )
    except Exception:
        pass

def retrieve_context(query: str):
    # 旧检索保留为 fallback
    try:
        resp = requests.post(
            f"{EVERMEMOS_API}/memories/search",
            json={"query": query, "user_id": USER_ID},
            timeout=3
        )
        data = resp.json()
        return data.get("result", {}).get("memories", []) or data.get("memories", [])
    except Exception:
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

    if any(k in text for k in ["但是", "不过", "却", "相反", "一方面", "另一方面", "错", "不对劲"]):
        state.conflict = clamp01(state.conflict + 0.45)

    if any(k in text for k in ["也许", "不确定", "不知道", "可能", "大概"]):
        state.uncertainty = clamp01(state.uncertainty + 0.35)

    if any(k in text for k in ["目标", "计划", "想要", "打算", "决定", "健康", "坚持"]):
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
        return "我还不够确定。你更偏向哪一种：A) 继续当前想法 B) 改成相反做法？"
    if action == "patch":
        return "我检测到内部冲突。更像：A) 场景变了 B) 身体/状态变了？"
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
    # 1) 当前输入先写入本地回退记忆
    store_event_local(user_input)

    # 2) 当前输入更新信号
    update_signals(user_input)

    # 3) Full-Memory Build: memory-aware correction
    signals = memory_client.load_memory_signals()
    state.conflict = min(1.0, state.conflict + signals["U_con_memory"])
    state.uncertainty = min(1.0, state.uncertainty + signals["U_unc_memory"])
    state.telos_distance = min(1.0, state.telos_distance + signals["U_tel_memory"])

    print(
        f"[Memory Correction] U_con_memory={signals['U_con_memory']:.2f} | "
        f"U_unc_memory={signals['U_unc_memory']:.2f} | "
        f"U_tel_memory={signals['U_tel_memory']:.2f}"
    )

    # 4) 当前能量
    comps_before = energy_components(state)

    # 5) 纯反应式决策（用于对比展示）
    action_before, delta_before = choose_action(state)

    # 6) 最终动作（当前版本 memory correction 已进入状态，因此 choose_action 已是 memory-aware）
    action, delta = choose_action(state)

    # 7) 应用动作
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

    # 8) Persist state + events to EverMemOS
    u_vec = [state.uncertainty, state.conflict, state.entropy, state.telos_distance]
    try:
        memory_client.store_state(
            u_vec,
            action,
            delta,
            extra={
                "phase": state.phase,
                "context_size": len(ctx),
                "plasticity_triggered": triggered,
            },
        )
        print("[EverMemOS] state persisted.")
    except Exception as e:
        print(f"[EverMemOS] state persistence skipped: {e}")

    try:
        if action == "patch":
            memory_client.store_event("conflict_event", user_input)
            print("[EverMemOS] conflict_event persisted.")
        elif action == "clarify":
            memory_client.store_event("clarify_event", user_input)
            print("[EverMemOS] clarify_event persisted.")
        elif state.telos_distance > 0.6:
            memory_client.store_event("goal_event", user_input, {"telos": state.telos_distance})
            print("[EverMemOS] goal_event persisted.")
    except Exception as e:
        print(f"[EverMemOS] event persistence skipped: {e}")

    memory_client.consolidate_pattern()

    print(f"[Decision] Pure Reactive: {action_before} -> Memory-Aware: {action}")

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
