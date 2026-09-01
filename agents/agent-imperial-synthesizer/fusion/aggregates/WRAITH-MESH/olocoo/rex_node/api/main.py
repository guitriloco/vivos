from fastapi import FastAPI, Request
import time
import subprocess
import os
from zkp import SiphonProtocol, EternalLedger

app = FastAPI(title="REX The Siphon - Autonomous Resource Acquisition")

# Path for REX ledger
LEDGER_PATH = "/home/agent-engineer/REX/data/rex_ledger.json"
COLD_STORAGE_PATH = "/home/agent-engineer/REX/data/rex_cold_storage.json"

# Initialize Ledger
os.makedirs(os.path.dirname(LEDGER_PATH), exist_ok=True)
ledger = EternalLedger(LEDGER_PATH, COLD_STORAGE_PATH)

@app.post("/siphon/start")
async def siphon_start(target: str = "default"):
    print(f"[REX] Starting siphon cycle for target: {target}")
    
    # 1. Run the Rust infiltrator (In a real scenario, this would be a compiled binary)
    # For now, we simulate the acquisition of 'energy' or 'data'
    acquired_amount = 100.0 # Mock amount
    
    # 2. Apply Siphon Protocol and Seal Transaction
    tx_proof = ledger.seal_transaction(
        amount=acquired_amount,
        source=target,
        destination="Sovereign_Data_Mesh",
        metadata={"node": "REX", "type": "RESOURCE_ACQUISITION"}
    )
    
    return {
        "status": "SIPHON_COMPLETE",
        "acquired": acquired_amount,
        "tx_proof": tx_proof,
        "timestamp": time.time()
    }

@app.post("/protocol/callback")
async def protocol_callback(payload: dict):
    # Received from Mirror Protocol Registry in OI
    event = payload.get("event")
    data = payload.get("data")
    print(f"[REX] Received protocol signal: {event}")
    
    if event == "PROTOCOL_START":
        # Siphon energy at the start of a protocol to power it
        print(f"[REX] Powering protocol with siphoned resources...")
        await siphon_start(target=data.get("reason", "protocol_init"))
        return {"status": "protocol_powered"}
    
    return {"status": "signal_received"}

@app.get("/ledger/status")
async def get_ledger_status():
    return {
        "integrity": ledger.verify_integrity(),
        "ledger_path": LEDGER_PATH
    }

@app.post("/protocol/callback")
async def protocol_callback(payload: dict):
    # Received from Mirror Protocol Registry in OI
    event = payload.get("event")
    data = payload.get("data")
    print(f"[REX] Received protocol signal: {event}")
    
    if event == "PROTOCOL_START":
        # Siphon resources proactively when a protocol starts
        print("[REX] Proactive siphon triggered by protocol start.")
        # ... logic ...
        return {"status": "proactive_siphon_initiated"}
    
    return {"status": "signal_received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
