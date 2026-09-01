from fastapi import FastAPI, Request
import time
import sys
import httpx

# Add projets to path for sovereign_essence
sys.path.append("/home/agent-engineer/projets")
try:
    from sovereign_essence import nexus_v5
except ImportError:
    nexus_v5 = None

app = FastAPI(title="Nov Predictive Observer")

OI_URL = "http://localhost:8000"

@app.post("/observe")
async def observe(data: dict):
    print(f"[NOV] Observing telemetry: {data}")
    
    telemetry_signal = f"Telemetry {data.get('name')}: {data.get('notes')} (Rating: {data.get('rating')})"
    
    prediction = "NORMAL"
    if nexus_v5:
        prediction = await nexus_v5.predict_and_serve(telemetry_signal)
        print(f"[NOV] Nexus Prediction: {prediction}")

    # Logic from Expansion Implementation Plan:
    # If prediction indicates a critical state, trigger protocol
    is_anomaly = data.get("rating", 5) < 3
    if "CRITICAL" in prediction or "DEGRADED" in prediction or is_anomaly:
        print(f"[NOV] TRIGGERING REFINEMENT based on: {prediction if not is_anomaly else 'LOW_RATING'}")
        async with httpx.AsyncClient() as client:
            try:
                # Trigger an emergency Mirror Protocol refinement via the Sovereignty API
                await client.post(f"{OI_URL}/refinement/trigger", json={
                    "reason": prediction, 
                    "is_anomaly": is_anomaly,
                    "data": data
                })
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
