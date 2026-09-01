import asyncio
import sys
import requests
import time
import random

# Add projets to path for sovereign_essence
sys.path.append("/home/agent-engineer/projets")
try:
    from sovereign_essence import nexus_v5
except ImportError:
    print("Warning: sovereign_essence not found. Insights will be limited.")
    nexus_v5 = None

class AetherCore:
    def __init__(self, api_url="http://localhost:8000"):
        self.api_url = api_url
        self.running = True

    async def distill_and_forward(self, raw_data):
        print(f"[AETHER_FLOW] Distilling Zenith data: {raw_data}...")
        
        # Use Nexus (Strategic Brain) to predict/extract insight
        insight = "Zenith Data Signal"
        if nexus_v5:
            # Simulate a request to the brain
            insight = await nexus_v5.predict_and_serve(raw_data)
        
        # Construct signal for Wraith (Mutation Pipeline)
        signal = {
            "source": "ZENITH_AETHER_MESH",
            "insight": insight,
            "efficiency_metric": random.uniform(0.7, 1.0),
            "bottleneck_detected": random.choice([True, False]),
            "optimization_hint": "Increase parallelism in fragment ingestion"
        }
        
        # Forward directly to Wraith (oi) via Sovereignty API
        try:
            # In a real environment, we'd use an async client like httpx
            # But for simplicity and matching the existing pattern:
            resp = requests.post(f"{self.api_url}/zenith/signal", json=signal, timeout=2)
            if resp.status_code == 200:
                print(f"[AETHER_FLOW] Zenith-Wraith Link active: Signal forwarded -> {insight}")
            else:
                print(f"[AETHER_FLOW] Signal forward failed with status: {resp.status_code}")
        except Exception as e:
            print(f"[AETHER_FLOW] Zenith-Wraith Link Error: {e}")

    async def run_forever(self):
        print("[AETHER_FLOW] Core initialized. Establishing Zenith-Wraith Link...")
        while self.running:
            # Simulate receiving data from the low-level FragmentedProcessor
            mock_data = f"Fragment-Signal-{random.randint(100, 999)}"
            await self.distill_and_forward(mock_data)
            await asyncio.sleep(5)

if __name__ == "__main__":
    core = AetherCore()
    try:
        asyncio.run(core.run_forever())
    except KeyboardInterrupt:
        print("[AETHER_FLOW] Shutting down.")
