import time
import math
import asyncio
from dataclasses import dataclass
from evermemos_client_v1_2 import EverMemOSClientV12
from typing import Dict, Any

CLIENT = EverMemOSClientV12()
state = None

@dataclass
class TelosState:
    uncertainty: float = 0.0
    conflict: float = 0.0
    entropy: float = 0.0
    telos_distance: float = 0.0

WEIGHTS = {"uncertainty": 1.2, "conflict": 1.8, "entropy": 1.0, "telos": 1.4}

class IntentPredictor:
    def __init__(self):
        self.threshold = 0.85

    def analyze(self, text: str):
        if any(k in text.lower() for k in ["图","画","plot","fig","visual"]):
            return {"action": "auto_make_figs", "confidence": 0.92, "args": {}}
        return {"action": "wait", "confidence": 1.0, "args": {}}

class ContextGuard:
    def __init__(self, max_tokens=8000):
        self.max_tokens = max_tokens
        self.context = []

    def safe_append(self, item: Dict):
        total_tokens = sum(len(str(m)) // 4 for m in self.context)
        if total_tokens > self.max_tokens:
            self.context = self.context[-int(len(self.context)*0.7):]
        self.context.append(item)

class TelosCore:
    def __init__(self):
        self.intent_predictor = IntentPredictor()
        self.context_guard = ContextGuard()
        self.active_tasks = []
        self.state = TelosState()

    async def process(self, user_input: str):
        now = time.time()
        # 1. 意图预测抢跑
        intent = self.intent_predictor.analyze(user_input)
        if intent["confidence"] >= self.intent_predictor.threshold and intent["action"] != "wait":
            task = asyncio.create_task(self._shadow_execute(intent["action"], intent["args"]))
            self.active_tasks.append(task)

        # 2. 历史记忆修正
        past = await CLIENT.search(user_input, top_k=10)
        con_score = sum(m["metadata"].get("conflict",0)*m["similarity"] for m in past)*0.45
        self.state.conflict = min(1.0, self.state.conflict+con_score)

        await CLIENT.store(user_input, memory_type="event_log",
            metadata={"conflict":1 if "错" in user_input else 0,
                      "intensity":2.0,"timestamp":now,"U":self.state.conflict})

        # 3. U向量计算 + 动作决策
        energy = 1.0 - (self.state.conflict * WEIGHTS["conflict"])
        action = "patch" if self.state.conflict>0.3 else "respond"

        # 4. Pattern consolidation
        await CLIENT.consolidate_patterns()

        # 5. 能量耗散闭环
        if action=="patch":
            self.state.conflict *= 0.2

        self.context_guard.safe_append({"role":"user","content":user_input})

        print(f"[Decision] Pure Reactive -> Memory-Aware action: {action}")
        return {"action":action,"energy":round(energy,3),"U_con_memory":round(con_score,2)}

    async def _shadow_execute(self, action: str, args: Dict):
        if action=="auto_make_figs":
            try:
                import auto_make_figs_v1_2
                await auto_make_figs_v1.2.run(args)
                print(f"[抢跑] {action} 跨模态渲染完毕，已落盘至 assets/")
            except Exception as e:
                print(f"[抢跑底层异常] {e}")
        else:
            await asyncio.sleep(0.3)
            print(f"[抢跑] {action} 未知动作已忽略")
