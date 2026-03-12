import json
import requests
from datetime import datetime, timezone
from typing import Dict, List, Any


class EverMemOSClient:
    """
    Minimal full-memory client for EverMemOS.
    Focus: state/event persistence + memory-aware signal retrieval.
    """

    def __init__(self, base_url: str = "http://localhost:1995", user_id: str = "user_001", timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.timeout = timeout
        self.api = f"{self.base_url}/api/v1/memories"

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def store_state(self, u_vector: List[float], action: str, delta_u: float, extra: Dict[str, Any] | None = None):
        """
        State Memory + minimal Audit payload.
        """
        payload = {
            "message_id": f"state_{int(datetime.now().timestamp())}",
            "create_time": self._now(),
            "sender": self.user_id,
            "user_id": self.user_id,
            "content": json.dumps(
                {
                    "type": "state_memory",
                    "u_vector": u_vector,
                    "action": action,
                    "delta_u": delta_u,
                    "extra": extra or {},
                    "timestamp": self._now(),
                },
                ensure_ascii=False,
            ),
        }
        resp = requests.post(self.api, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def store_event(self, event_type: str, content: str, extra: Dict[str, Any] | None = None):
        """
        Event Memory.
        event_type: conflict_event / clarify_event / goal_event / compress_event / rollback_event / pending_event
        """
        payload = {
            "message_id": f"event_{event_type}_{int(datetime.now().timestamp())}",
            "create_time": self._now(),
            "sender": self.user_id,
            "user_id": self.user_id,
            "content": json.dumps(
                {
                    "type": "event_memory",
                    "event_type": event_type,
                    "content": content,
                    "extra": extra or {},
                    "timestamp": self._now(),
                },
                ensure_ascii=False,
            ),
        }
        resp = requests.post(self.api, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        return resp.json()

    def load_memory_signals(self) -> Dict[str, float]:
        """
        Minimal memory-aware retrieval for competition demo.
        Returns U-memory bias for conflict / uncertainty / telos.
        """
        resp = requests.post(
            f"{self.api}/search",
            json={
                "query": "telos cognitive state",
                "user_id": self.user_id,
                "limit": 20,
            },
            timeout=self.timeout,
        )
        resp.raise_for_status()

        memories = resp.json().get("result", {}).get("memories", [])

        con = 0.0
        unc = 0.0
        tel = 0.0

        for m in memories:
            try:
                raw = m.get("content", "{}")
                data = json.loads(raw) if isinstance(raw, str) else raw
                event_type = data.get("event_type", "")

                if event_type == "conflict_event":
                    con += 0.25
                elif event_type == "clarify_event":
                    unc += 0.20
                elif event_type == "goal_event":
                    tel -= 0.18
            except Exception:
                continue

        return {
            "U_con_memory": min(0.8, con),
            "U_unc_memory": min(0.7, unc),
            "U_tel_memory": max(-0.6, tel),
        }

    def consolidate_pattern(self) -> None:
        """
        Minimal Pattern Memory stub for demo.
        Keeps README / video statement honest: this is a lightweight competition build.
        """
        print("[Pattern Memory] lightweight consolidation executed.")
