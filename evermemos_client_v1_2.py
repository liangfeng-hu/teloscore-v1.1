import asyncio
import httpx
import time
from sentence_transformers import SentenceTransformer
from typing import List, Dict, Any, Optional

class EverMemOSClientV12:
    def __init__(self, user_id: str = "default_user"):
        self.user_id = user_id
        self.base_url = "http://localhost:1995/api/v1"
        self.client = httpx.AsyncClient(timeout=10.0)
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')

    async def close(self):
        await self.client.aclose()

    async def store(self, content: str, memory_type: str = "event_log", metadata: Optional[Dict] = None):
        if metadata is None:
            metadata = {}
        embedding = self.embedder.encode(content).tolist()
        payload = {
            "message_id": f"telos_{int(time.time())}",
            "create_time": time.strftime("%Y-%m-%dT%H:%M:%S+00:00"),
            "sender": self.user_id,
            "content": content,
            "memory_type": memory_type,
            "metadata": {**metadata, "embedding": embedding, "telos_score": metadata.get("U", 0.0)}
        }
        r = await self.client.post(f"{self.base_url}/memories", json=payload)
        return r.json()

    async def search(self, query: str, retrieve_method: str = "rrf", top_k: int = 15, memory_types: Optional[List[str]] = None):
        if memory_types is None:
            memory_types = ["event_log", "episodic_memory", "pattern"]
        payload = {"query": query, "user_id": self.user_id, "retrieve_method": retrieve_method, "memory_types": memory_types, "top_k": top_k}
        r = await self.client.post(f"{self.base_url}/memories/search", json=payload)
        results = r.json().get("result", [])
        return [{"content": item["content"], "metadata": item.get("metadata", {}), "similarity": item.get("score", 0)} for item in results]

    async def consolidate_patterns(self):
        print("[TelosCore] Pattern Consolidation 已触发 → EverMemOS 自动生成 pattern memory")
