import os
import time
import math
import asyncio
from dataclasses import dataclass
from typing import Dict, Any, List

from evermemos_client_v1.2 import EverMemOSClientV12


CLIENT = EverMemOSClientV12()


@dataclass
class TelosState:
    uncertainty: float = 0.0
    conflict: float = 0.0
    entropy: float = 0.3
    telos_distance: float = 0.6


WEIGHTS = {
    "uncertainty": 1.2,
    "conflict": 1.8,
    "entropy": 1.0,
    "telos": 1.4,
}


class TopologicalMemory:
    """
    轻量艾宾浩斯显著性层（v1.2 最小版）
    """
    def __init__(self, half_life: float = 86400.0):
        self.half_life = half_life

    def calculate_salience(self, memory_item: Dict[str, Any], current_time: float) -> float:
        initial_strength = memory_item.get("intensity", 1.0)
        timestamp = memory_item.get("timestamp", current_time)
        elapsed = current_time - timestamp
        return initial_strength * math.exp(-elapsed / self.half_life)


class IntentPredictor:
    """
    最小可运行的意图预测器
    """
    def __init__(self):
        self.threshold = 0.85

    def analyze(self, text: str) -> Dict[str, Any]:
        text_l = text.lower()
        if any(k in text_l for k in ["图", "画", "plot", "fig", "visual"]):
            return {"action": "auto_make_figs", "confidence": 0.92, "args": {"baseline": 1.0, "amplitude": 0.45}}
        return {"action": "wait", "confidence": 1.0, "args": {}}


class ContextGuard:
    """
    轻量上下文安全阀
    """
    def __init__(self, max_tokens: int = 8000):
        self.max_tokens = max_tokens
        self.context: List[Dict[str, Any]] = []

    def safe_append(self, item: Dict[str, Any]):
        est_total = sum(len(str(m)) // 4 for m in self.context)
        if est_total > self.max_tokens:
            self.context = self.context[-int(len(self.context) * 0.7):]
        self.context.append(item)


class TelosCore:
    def __init__(self):
        self.memory_index = TopologicalMemory()
        self.intent_predictor = IntentPredictor()
        self.context_guard = ContextGuard()
        self.active_tasks: List[asyncio.Task] = []
        self.state = TelosState()

    def _calculate_cognitive_energy(self) -> float:
        """
        U = 1.2 * uncertainty + 1.8 * conflict + 1.0 * entropy + 1.4 * telos_distance
        """
        s = self.state
        return (
            WEIGHTS["uncertainty"] * s.uncertainty
            + WEIGHTS["conflict"] * s.conflict
            + WEIGHTS["entropy"] * s.entropy
            + WEIGHTS["telos"] * s.telos_distance
        )

    def _pure_reactive_action(self) -> str:
        """
        不考虑历史记忆时的简单反应动作
        """
        U = self._calculate_cognitive_energy()
        if self.state.conflict > 0.30:
            return "patch"
        if self.state.uncertainty > 0.45:
            return "clarify"
        if self.state.entropy > 0.70:
            return "compress"
        if U < 0.9:
            return "respond"
        return "clarify"

    async def _load_memory_bias(self, user_input: str) -> Dict[str, float]:
        """
        从 EverMemOS 取回历史记忆并形成修正量
        """
        past = await CLIENT.search(user_input, retrieve_method="rrf", top_k=10)

        con_score = sum(m.get("metadata", {}).get("conflict", 0) * m.get("similarity", 0) for m in past) * 0.45
        unc_score = sum(m.get("metadata", {}).get("uncertainty", 0) * m.get("similarity", 0) for m in past) * 0.35
        tel_score = sum(m.get("metadata", {}).get("telos_bonus", 0) for m in past) * -0.18

        return {
            "U_con_memory": min(0.8, con_score),
            "U_unc_memory": min(0.7, unc_score),
            "U_tel_memory": max(-0.6, tel_score),
        }

    def _apply_current_input_signals(self, user_input: str):
        """
        当前输入的快速规则/启发式更新（保留最小版）
        """
        txt = user_input.lower()

        if any(k in user_input for k in ["错", "不行", "不对劲", "冲突"]) or "wrong" in txt:
            self.state.conflict = min(1.0, self.state.conflict + 0.35)

        if any(k in user_input for k in ["也许", "不确定", "可能"]) or "maybe" in txt or "unsure" in txt:
            self.state.uncertainty = min(1.0, self.state.uncertainty + 0.25)

        if any(k in user_input for k in ["目标", "计划", "恢复", "原计划"]) or "goal" in txt or "plan" in txt:
            self.state.telos_distance = max(0.0, self.state.telos_distance - 0.15)
        else:
            self.state.telos_distance = min(1.0, self.state.telos_distance + 0.03)

        self.state.entropy = min(1.0, self.state.entropy + len(user_input.split()) / 100.0)

    def _memory_aware_action(self) -> str:
        """
        考虑 U 修正后的动作
        """
        U = self._calculate_cognitive_energy()

        if self.state.conflict > 0.30:
            return "patch"
        if self.state.uncertainty > 0.45:
            return "clarify"
        if self.state.entropy > 0.75:
            return "compress"
        if U < 0.9:
            return "respond"
        return "clarify"

    async def process(self, user_input: str) -> Dict[str, Any]:
        now = time.time()

        # 1. 当前输入先更新
        self._apply_current_input_signals(user_input)

        # 2. 纯反应动作（用于对照）
        action_before = self._pure_reactive_action()

        # 3. 意图预测 + 抢跑
        intent = self.intent_predictor.analyze(user_input)
        if intent["confidence"] >= self.intent_predictor.threshold and intent["action"] != "wait":
            task = asyncio.create_task(self._shadow_execute(intent["action"], intent["args"]))
            self.active_tasks.append(task)

        # 4. 历史记忆修正
        signals = await self._load_memory_bias(user_input)
        self.state.conflict = min(1.0, self.state.conflict + signals["U_con_memory"])
        self.state.uncertainty = min(1.0, self.state.uncertainty + signals["U_unc_memory"])
        self.state.telos_distance = max(0.0, min(1.0, self.state.telos_distance + signals["U_tel_memory"]))

        print(
            f"[Memory Correction] "
            f"U_con_memory={signals['U_con_memory']:.2f} | "
            f"U_unc_memory={signals['U_unc_memory']:.2f} | "
            f"U_tel_memory={signals['U_tel_memory']:.2f}"
        )

        # 5. 记忆感知动作
        action = self._memory_aware_action()
        energy = self._calculate_cognitive_energy()

        # 6. 持久化当前输入到 EverMemOS
        await CLIENT.store(
            user_input,
            memory_type="event_log",
            metadata={
                "conflict": 1 if any(k in user_input for k in ["错", "不行", "不对劲", "冲突"]) else 0,
                "uncertainty": 1 if any(k in user_input for k in ["也许", "不确定", "可能"]) else 0,
                "telos_bonus": -0.15 if any(k in user_input for k in ["目标", "计划", "恢复", "原计划"]) else 0.05,
                "intensity": 2.0,
                "timestamp": now,
                "U": energy,
            },
        )

        print("[EverMemOS] state persisted.")

        # 7. Pattern consolidation
        await CLIENT.consolidate_patterns()

        # 8. 终极补丁：能量耗散（避免 patch 后永远高冲突卡死）
        if action == "patch":
            self.state.conflict *= 0.2

        self.context_guard.safe_append({"role": "user", "content": user_input})

        print(f"[Decision] Pure Reactive: {action_before} -> Memory-Aware: {action}")

        return {
            "action": action,
            "energy": round(energy, 3),
            "U_con_memory": round(signals["U_con_memory"], 2),
            "U_unc_memory": round(signals["U_unc_memory"], 2),
            "U_tel_memory": round(signals["U_tel_memory"], 2),
        }

    async def _shadow_execute(self, action: str, args: Dict[str, Any]):
        """
        真正的后台抢跑：动态调起跨模态/图表生成器
        """
        if action == "auto_make_figs":
            try:
                import auto_make_figs_v1.2
                await auto_make_figs_v1.2.run(args)
                print(f"[抢跑] {action} 跨模态渲染完毕，已落盘至 assets/。")
            except Exception as e:
                print(f"[抢跑底层异常] {e}")
        else:
            await asyncio.sleep(0.3)
            print(f"[抢跑] {action} 未知动作已忽略")
