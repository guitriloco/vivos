from fastapi import FastAPI, Request
import time
import sys
import os
import httpx
import asyncio
import logging

# Add projets to path for sovereign_essence
sys.path.append(os.path.expanduser("~/projets"))
try:
    from sovereign_essence import engine
except ImportError:
    engine = None

from harvest_optimizer import HarvestOptimizer

app = FastAPI(title="Yes Yield Execution Engine")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("YES-CONQUEROR")

SOVEREIGN_API_URL = "http://localhost:8000"
VVV_URL = "http://localhost:8003"

optimizer = HarvestOptimizer()
nectar_events = []

def calculate_roi(data: dict) -> float:
    """
    Analyzes performance and efficiency to calculate ROI.
    Optimized by Atomic Evolution.
    """
    # Logic: ROI = (Performance * Efficiency) / Complexity
    performance = data.get("performance", 1.0)
    efficiency = data.get("efficiency", 1.0)
    complexity = data.get("complexity", 1.0)
    
    # Apply optimization level from HarvestOptimizer
    roi = (performance * efficiency * optimizer.optimization_level) / max(complexity, 0.1)
    return round(roi, 4)

def execute_high_yield(refinement_result: dict):
    # 1. Atomic Evolution Check (Cross-Build from SUPRA)
    latency_us = refinement_result.get("latency_us", 100)
    mode = optimizer.apply_atomic_evolution({"latency_us": latency_us})
    
    # 2. Execute the refined logic (Conquer)
    # (Simulated execution of refined_logic based on mode)
    if mode == "FAST_HARVEST":
        logger.info("[YES] Atomic Shift: Executing FAST_HARVEST mode")
    
    # 3. Calculate Yield (Performance/Efficiency metrics)
    actual_roi = calculate_roi(refinement_result)
    
    # 4. Self-Optimization Trigger (Sub-millisecond signals)
    if actual_roi < 0.95:
        optimizer.optimize_logic("execute_high_yield", actual_roi)
    
    # 5. If ROI > Threshold, mark as "Absolute Nectar"
    is_absolute_nectar = actual_roi > 0.98
    
    result = {
        "execution_status": "CONQUERED",
        "mode": mode,
        "yield_roi": actual_roi,
        "is_absolute_nectar": is_absolute_nectar,
        "nectar_classification": "Absolute Nectar" if is_absolute_nectar else "High Grade Nectar",
        "optimization_meta": optimizer.get_report(),
        "timestamp": time.time()
    }

    if is_absolute_nectar:
        nectar_events.append(result)
    
    return result

async def distillation_loop():
    """
    The Nectar Distillation Loop.
    Periodically analyzes cycles and marks 'Absolute Nectar'.
    """
    logger.info("Starting Nectar Distillation Loop...")
    while True:
        try:
            # 1. Analyze Sovereign cycles (Simulated by pulling from API)
            async with httpx.AsyncClient() as client:
                # We could pull recent results or signals
                # For now, let's assume we pull from a hypothetical endpoint or just simulate processing
                logger.info("Analyzing Sovereign cycle...")
                
                # Sample cycle data
                cycle_data = {
                    "performance": 0.99,
                    "efficiency": 0.995,
                    "complexity": 1.0,
                    "latency_us": 120,
                    "refined_logic": "Optimized_Matrix_Factorization"
                }
                
                yield_result = execute_high_yield(cycle_data)
                
                if yield_result["is_absolute_nectar"]:
                    logger.info(f"FOUND ABSOLUTE NECTAR: {yield_result['yield_roi']}")
                    # Mark in registry (Simulated by logging and sending to Vault)
                    await client.post(f"{SOVEREIGN_API_URL}/vault/preserve", params={"content": f"NECTAR_{int(time.time())}_{yield_result['yield_roi']}"})
                
        except Exception as e:
            logger.error(f"Error in distillation loop: {e}")
            
        await asyncio.sleep(60) # Process every minute

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(distillation_loop())

@app.get("/status")
async def get_status():
    return {
        "node": "YES",
        "status": "active",
        "optimization": optimizer.get_report()
    }

@app.get("/nectar/events")
async def get_nectar_events():
    """
    Returns all Absolute Nectar events since the engine started.
    """
    return {"events": nectar_events, "count": len(nectar_events)}

@app.post("/optimize")
async def trigger_optimization(performance_data: dict):
    """
    Manual or automated trigger for atomic evolution.
    """
    result = optimizer.optimize_logic("harvest_engine", performance_data.get("roi", 1.0))
    return {"status": "optimized", "record": result}

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
    uvicorn.run(app, host="0.0.0.0", port=8012)
