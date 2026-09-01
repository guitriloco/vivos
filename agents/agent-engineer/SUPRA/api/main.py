from fastapi import FastAPI, Request
import time
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
from fusion import create_fusion_engine
from mutator import Mutator

app = FastAPI(title="SUPRA The Ascension - Multi-Model Fusion & Mutation")

fusion_engine = create_fusion_engine()
mutator = Mutator()

@app.post("/ascend/fuse")
async def ascend_fuse(request: Request):
    context = await request.json()
    # If it receives a list instead of a dict, wrap it
    if isinstance(context, list):
        context = {"models": context}
    elif context is None:
        context = {"task_type": "general"}
        
    print(f"[SUPRA] Initiating Ascension Cycle with context: {context.get('task_type', 'general')}")
    
    # 1. Simulate multi-model input
    claude_suggestion = "Optimize memory management in WraithEngine."
    gemini_suggestion = "Improve recursive depth in HyperProtocol."
    
    # 2. Fuse intelligence
    fusion_result = fusion_engine.fuse_responses(
        claude_response=claude_suggestion,
        gemini_response=gemini_suggestion,
        task_type=context.get('task_type', 'general')
    )
    
    return {
        "status": "ASCENDED",
        "fusion_score": fusion_result['synergy_score'],
        "fused_directive": fusion_result['fused_response'],
        "timestamp": time.time()
    }

@app.post("/ascend/mutate")
async def ascend_mutate(target_node: str, signals: dict = None):
    print(f"[SUPRA] Mutating architecture for {target_node}")
    # 1. Acquire signals from Zenith if not provided
    if signals is None:
        signals = {"zenith_insights": [{"insight": "High latency in WraithEngine", "efficiency_metric": 0.45}]}
    
    # 2. Identify target file (Mock)
    target_file = f"/home/agent-engineer/oi/src/{target_node.lower()}_engine.cpp"
    # Create mock file for demonstration if it doesn't exist
    if not os.path.exists(target_file):
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        with open(target_file, 'w') as f:
            f.write("// Sovereign Core Node\nvoid process() { /* ... */ }\n")

    # 3. Execute Mutation
    mutated_code = mutator.mutate(target_file, signals)
    mutation_path = mutator.save_mutation(mutated_code, target_file)
    
    return {
        "status": "ARCHITECTURE_MUTATED",
        "target": target_node,
        "mutation_log": mutation_path,
        "timestamp": time.time()
    }

@app.post("/protocol/callback")
async def protocol_callback(payload: dict):
    # Received from Mirror Protocol Registry in OI
    event = payload.get("event")
    data = payload.get("data")
    print(f"[SUPRA] Received protocol signal: {event}")
    
    if event == "ANOMALY_DETECTED":
        # Mutate system architecture if an anomaly is detected
        print(f"[SUPRA] Architectural mutation triggered by anomaly: {data.get('reason')}")
        # Trigger a mutation for the node that reported the anomaly
        await ascend_mutate(target_node="OI", signals=data)
        return {"status": "system_mutation_initiated"}
    
    return {"status": "signal_received"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
