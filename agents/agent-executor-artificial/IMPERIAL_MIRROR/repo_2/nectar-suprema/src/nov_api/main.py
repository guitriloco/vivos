from fastapi import FastAPI, BackgroundTasks
import time
import json
import os
from typing import Dict, List

app = FastAPI(title="Sovereignty Dashboard API (Nov-API 2.0)")

# Storage paths
project_root = "/home/agent-ai-architect/nectar-suprema"
KNOWLEDGE_BASE = os.path.join(project_root, "src/sovereign-entity/AETHER_FLOW/Intelligence_Report/knowledge_base.json")
ROI_CONFIG = os.path.join(project_root, "src/sovereign-entity/AETHER_FLOW/Intelligence_Report/niche_roi.json")
MUTATION_LOG = os.path.join(project_root, "src/sovereign-entity/AETHER_FLOW/Intelligence_Report/mutation_log.jsonl")

@app.get("/")
async def root():
    return {"status": "ONLINE", "engine": "Sovereign Reality 2.0"}

@app.get("/stats")
async def get_stats():
    stats = {
        "active_expansions": 0,
        "total_niches": 0,
        "average_roi": 0.0,
        "mutations_count": 0
    }
    
    if os.path.exists(KNOWLEDGE_BASE):
        with open(KNOWLEDGE_BASE, "r") as f:
            kb = json.load(f)
            stats["active_expansions"] = len(kb.get("active_expansions", []))
            stats["total_niches"] = len(kb.get("predicted_niches", []))
            
    if os.path.exists(ROI_CONFIG):
        with open(ROI_CONFIG, "r") as f:
            roi_data = json.load(f)
            rois = [v["target_roi"] for v in roi_data.values()]
            if rois:
                stats["average_roi"] = sum(rois) / len(rois)
                
    if os.path.exists(MUTATION_LOG):
        with open(MUTATION_LOG, "r") as f:
            stats["mutations_count"] = sum(1 for _ in f)
            
    return stats

@app.get("/expansions")
async def list_expansions():
    if os.path.exists(KNOWLEDGE_BASE):
        with open(KNOWLEDGE_BASE, "r") as f:
            return json.load(f).get("active_expansions", [])
    return []

@app.post("/mirror/refine")
async def trigger_refine(payload: dict):
    print(f"🔄 [NOV-API] Refinement triggered: {payload.get('reason')}")
    # Logic to trigger Aether Expansion or Mutator Overlord
    return {"status": "refinement_initiated"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
