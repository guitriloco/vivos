from fastapi import FastAPI, Request
import time
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from rex_orchestrator import RexOrchestrator

app = FastAPI(title="REX The Siphon - Production Overlord")
orchestrator = RexOrchestrator()

@app.post("/siphon/start")
async def siphon_start(target: str = "default"):
    await orchestrator.run_cycle([target])
    return {"status": "SIPHON_COMPLETE", "timestamp": time.time()}

@app.post("/protocol/callback")
async def protocol_callback(payload: dict):
    event = payload.get("event")
    if event == "PROTOCOL_START":
        await orchestrator.run_cycle([payload.get("data", {}).get("reason", "protocol_init")])
    return {"status": "signal_received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
