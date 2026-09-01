import json
import os
import random
import time
from datetime import datetime

# Configuration
INVENTORY_FILE = "/home/team/shared/inventory/global_inventory.json"
OUTPUT_DIR = "/home/team/shared/synthesis/"
REPORT_FILE = os.path.join(OUTPUT_DIR, "synthesis_report.json")

def collect_node_data(node):
    """
    Simulates collecting rich data from a single node.
    In a real scenario, this would query a niche-specific API on the node.
    """
    niche = node.get("niche", "unknown")
    
    # Base synthesis value simulation
    base_value = random.uniform(10, 100)
    
    data = {
        "node_id": node["id"],
        "niche": niche,
        "region": node["region"],
        "timestamp": datetime.now().isoformat(),
        "operational_health": random.uniform(0.95, 1.0),
        "synthesis_value": base_value
    }
    
    if niche == "bio-wealth":
        data["revenue_usd"] = random.uniform(500, 5000)
        data["bio_insights_collected"] = random.randint(100, 1000)
        # Bio-wealth has higher synthesis priority
        data["synthesis_value"] *= 1.5 
    elif niche == "financas":
        data["revenue_usd"] = random.uniform(1000, 10000)
        data["transactions_processed"] = random.randint(1000, 50000)
        data["synthesis_value"] *= 1.2
    else:
        data["revenue_usd"] = random.uniform(100, 1000)
        
    return data

def run_synthesis_aggregation():
    print(f"--- /SINTESE: Starting Centralized AI Aggregation ---")
    
    if not os.path.exists(INVENTORY_FILE):
        print(f"Error: Inventory file {INVENTORY_FILE} not found. Run Necromancy script first.")
        return

    with open(INVENTORY_FILE, "r") as f:
        inventory = json.load(f)
    
    # Filter for active nodes in target niches
    target_niches = ["bio-wealth", "financas"]
    active_nodes = [n for n in inventory if n["status"] == "Running" and n["niche"] in target_niches]
    
    print(f"Aggregating data from {len(active_nodes)} nodes in niches: {target_niches}")
    
    aggregated_data = []
    total_revenue = 0
    total_synthesis_value = 0
    
    for node in active_nodes:
        node_data = collect_node_data(node)
        aggregated_data.append(node_data)
        total_revenue += node_data.get("revenue_usd", 0)
        total_synthesis_value += node_data["synthesis_value"]
        
    # Sort by synthesis value (prioritization)
    aggregated_data.sort(key=lambda x: x["synthesis_value"], reverse=True)
    
    report = {
        "summary": {
            "timestamp": datetime.now().isoformat(),
            "nodes_aggregated": len(active_nodes),
            "total_revenue_usd": total_revenue,
            "global_synthesis_index": total_synthesis_value / len(active_nodes) if active_nodes else 0,
            "status": "SUCCESS"
        },
        "top_priority_nodes": aggregated_data[:10],
        "full_data": aggregated_data
    }
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(REPORT_FILE, "w") as f:
        json.dump(report, f, indent=2)
        
    print(f"Synthesis Report generated: {REPORT_FILE}")
    print(f"Total Revenue Aggregated: ${total_revenue:,.2f}")
    print(f"Global Synthesis Index: {report['summary']['global_synthesis_index']:.2f}")

if __name__ == "__main__":
    run_synthesis_aggregation()
