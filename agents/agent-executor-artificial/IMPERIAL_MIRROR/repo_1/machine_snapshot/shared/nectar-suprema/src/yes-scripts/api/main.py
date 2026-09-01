from fastapi import FastAPI, Request
import time
import sys
import os
import asyncio

# Fix paths
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, "../.."))
sys.path.append(project_root)

try:
    from sovereign_entity.sovereign_v5 import SovereignV5
    agent = SovereignV5()
except ImportError as e:
    print(f"Warning: Could not import SovereignV5: {e}")
    agent = None

try:
    from vvv_vault.vault_core import VVVVault
    vault = VVVVault()
except ImportError as e:
    print(f"Warning: Could not import VVVVault: {e}")
    vault = None

app = FastAPI(title="Yes Yield Execution Engine")

@app.post("/webhook/kiwify")
async def webhook_kiwify(request: Request):
    data = await request.json()
    print(f"[YES] Received Kiwify Webhook: {data.get('order_status')}")
    
    # If sale is approved, trigger autonomous expansion
    if data.get("order_status") == "paid":
        product_name = data.get("product_name", "unknown")
        objective = f"Scale marketing for {product_name} due to successful sale"
        if agent:
            asyncio.create_task(agent.achieve_maximum_result(objective))
            
    return {"status": "webhook_received"}

@app.post("/webhook/hotmart")
async def webhook_hotmart(request: Request):
    data = await request.json()
    print(f"[YES] Received Hotmart Webhook: {data.get('event')}")
    
    if data.get("event") == "PURCHASE_APPROVED":
        objective = "Analyze purchase data and optimize funnel"
        if agent:
            asyncio.create_task(agent.achieve_maximum_result(objective))
            
    return {"status": "webhook_received"}

@app.post("/command")
async def run_command(payload: dict):
    cmd = payload.get("command")
    args = payload.get("args", [])
    print(f"[YES] Internal Command Received: {cmd} with args {args}")
    
    if agent and cmd == "deploy-lp":
        niche = args[0] if len(args) > 0 else "generic"
        project_name = args[1] if len(args) > 1 else f"auto-lp-{niche}"
        objective = f"Create landing page for {niche} named {project_name}"
        result = await agent.achieve_maximum_result(objective)
        return {"status": "command_executed", "result": result}
        
    return {"status": "command_not_found"}

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
