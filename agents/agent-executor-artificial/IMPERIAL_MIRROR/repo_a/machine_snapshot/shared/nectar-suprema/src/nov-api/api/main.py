from fastapi import FastAPI, Request, Depends, Header, HTTPException
import time
import sys
import httpx
import os

# Add project root to path
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../../.."))
sys.path.append(project_root)
sys.path.append(os.path.join(project_root, "src"))

try:
    from sovereign_entity.sovereign_v5 import SovereignV5
    from mirror_protocol.registry import registry
    from sovereign_security import verify_sovereign_token, SOVEREIGN_TOKEN
    sovereign = SovereignV5()
except ImportError as e:
    print(f"Warning: Module import failed: {e}")
    sovereign = None
    registry = None
    def verify_sovereign_token(): return True
    SOVEREIGN_TOKEN = "UNSECURE"

app = FastAPI(title="Nov Predictive Observer (SECURE)")

OI_URL = "http://localhost:8002"

@app.post("/observe", dependencies=[Depends(verify_sovereign_token)])
async def observe(data: dict):
    print(f"[NOV] Observing telemetry: {data}")
    
    telemetry_signal = f"Telemetry {data.get('name')}: {data.get('notes')} (Rating: {data.get('rating')})"
    
    prediction = "NORMAL"
    if sovereign:
        prediction = await sovereign.achieve_maximum_result(telemetry_signal)
        print(f"[NOV] Sovereign Prediction: {prediction}")

    # Broadcast via Mirror Protocol if it's an anomaly
    is_anomaly = data.get("rating", 5) < 3
    if registry and is_anomaly:
        await registry.broadcast("ANOMALY_DETECTED", {"data": data, "prediction": prediction})
    if "CRITICAL" in prediction or "DEGRADED" in prediction or is_anomaly:
        print(f"[NOV] TRIGGERING REFINEMENT based on: {prediction if not is_anomaly else 'LOW_RATING'}")
        async with httpx.AsyncClient() as client:
            try:
                # Trigger an emergency Mirror Protocol refinement via the Sovereignty API
                # Include the Sovereign Token in the request to the Command Center
                await client.post(f"{OI_URL}/refinement/trigger", 
                    json={
                        "reason": prediction, 
                        "is_anomaly": is_anomaly,
                        "data": data
                    },
                    headers={"X-Sovereign-Token": SOVEREIGN_TOKEN}
                )
            except Exception as e:
                print(f"[NOV] Failed to trigger refinement: {e}")

    return {
        "status": "observed", 
        "prediction": prediction,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
