import json
import requests
from datetime import datetime, timezone
from typing import Dict, List, Any


class EverMemOSClient:
    """
    Minimal EverMemOS client for Full-Memory Build.
    Competition-safe:
    - state persistence
    - event persistence
    - memory-aware signal retrieval
    - lightweight pattern consolidation stub
    """

    def __init__(self, base_url: str = "http://localhost:1995", user_id: str = "user_001", timeout: int = 10):
        self.base_url = base_url.rstrip("/")
        self.user_id = user_id
        self.timeout = timeout
        self.api = f"{self.base_url}/api/v1/memories"

    def _now(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def store_state(self, u_vector: List[float], action: str, delta_u: float, extra: Dict[str, Any] | None = None):
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
        Lightweight memory-aware retrieval.
        Returns:
        - U_con_memory
        - U_unc_memory
        - U_tel_memory
        """
        memories = []

        # try POST search first
        try:
            resp = requests.post(
                f"{self.api}/search",
                json={
                    "query": "telos cognitive state",
                    "user_id": self.user_id,
                    "limit": 20,
                },
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                memories = resp.json().get("result", {}).get("memories", [])
        except Exception:
            memories = []

        # fallback GET if needed
        if not memories:
            try:
                resp = requests.get(
                    f"{self.api}/search",
                    params={
                        "query": "telos cognitive state",
                        "user_id": self.user_id,
                        "limit": 20,
                    },
                    timeout=self.timeout,
                )
                if resp.status_code == 200:
                    memories = resp.json().get("result", {}).get("memories", [])
            except Exception:
                memories = []

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
        Lightweight pattern-memory stub for demo.
        """
        print("[Pattern Memory] lightweight consolidation executed.")
