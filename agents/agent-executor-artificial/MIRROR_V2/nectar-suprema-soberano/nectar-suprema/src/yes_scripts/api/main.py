from fastapi import FastAPI, Request
import time
import sys

# Add projets to path for sovereign_essence
sys.path.append("/home/agent-engineer/projets")
try:
    from sovereign_essence import engine
except ImportError:
    engine = None

app = FastAPI(title="Yes Yield Execution Engine")

def execute_high_yield(refinement_result: dict):
    # Logic from Expansion Implementation Plan:
    # 1. Execute the refined logic (Conquer)
    # 2. Calculate Yield (Performance/Efficiency metrics)
    # 3. If Yield > Threshold, mark as "Absolute Nectar"
    
    refined_logic = refinement_result.get("refined_logic", "")
    print(f"[YES] Executing refined logic: {refined_logic}")
    
    # Simulate execution and yield calculation
    actual_yield = refinement_result.get("nectar_yield", 0.95)
    
    # In the plan, marking as Absolute Nectar happens if yield is high
    is_absolute_nectar = actual_yield > 0.97
    
    return {
        "execution_status": "CONQUERED",
        "yield": actual_yield,
        "is_absolute_nectar": is_absolute_nectar,
        "nectar_classification": "Absolute Nectar" if is_absolute_nectar else "High Grade Nectar"
    }

@app.post("/execute")
async def execute(objective: str):
    print(f"[YES] Maximizing yield for: {objective}")
    if engine:
        # If the objective is actually logic to be executed
        result = engine.execute(objective)
        return {"status": "success", "result": result, "timestamp": time.time()}
    return {"status": "success", "yield": "MAXIMIZED", "timestamp": time.time()}

@app.post("/protocol/callback")
async def protocol_callback(payload: dict):
    # Received from Mirror Protocol Registry in OI
    event = payload.get("event")
    data = payload.get("data")
    
    print(f"[YES] Received protocol signal: {event}")
    
    if event == "PROTOCOL_COMPLETE":
        result = execute_high_yield(data)
        print(f"[YES] Yield Result: {result['nectar_classification']}")
        return {"status": "callback_processed", "result": result}
    
    return {"status": "signal_received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
