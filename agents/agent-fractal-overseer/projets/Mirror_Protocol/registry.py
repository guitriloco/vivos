import httpx
import asyncio
from typing import Dict, List, Any

class ExpansionRegistry:
    def __init__(self):
        self.remote_callbacks: Dict[str, List[str]] = {
            "PROTOCOL_START": [],
            "PROTOCOL_COMPLETE": [],
            "ANOMALY_DETECTED": [],
            "NECTAR_DISTILLED": []
        }

    def register_remote(self, event: str, url: str):
        if event in self.remote_callbacks:
            if url not in self.remote_callbacks[event]:
                self.remote_callbacks[event].append(url)
                print(f"[REGISTRY] Remote callback registered for {event}: {url}")

    async def broadcast(self, event: str, data: Any):
        print(f"[REGISTRY] Broadcasting {event} to {len(self.remote_callbacks.get(event, []))} remote nodes.")
        async with httpx.AsyncClient() as client:
            tasks = []
            for url in self.remote_callbacks.get(event, []):
                tasks.append(client.post(url, json={"event": event, "data": data}))
            
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for i, res in enumerate(results):
                    if isinstance(res, Exception):
                        print(f"[REGISTRY] Error broadcasting to {self.remote_callbacks[event][i]}: {res}")

registry = ExpansionRegistry()
