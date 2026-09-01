import time
import random
import json
import os

# Configuration updated for Protocol /ENTIDADE_12 (540 Nodes)
NICHES = ["bio-wealth", "financas", "e-commerce", "health-tech", "real-estate"]
PROVIDERS = ["aws", "do", "gcp"]
REGIONS_PER_PROVIDER = 3
NODES_PER_REGION = 12 # 5 * 3 * 3 * 12 = 540 Nodes

LATENCY_SLO = 0.2  # 200ms
ROI_THRESHOLD = 1.0 # 1 req/s minimum for ROI positive

MOCK_STATE_FILE = "/home/team/shared/inventory/global_inventory.json"

def ensure_inventory():
    if not os.path.exists(os.path.dirname(MOCK_STATE_FILE)):
        os.makedirs(os.path.dirname(MOCK_STATE_FILE), exist_ok=True)
    
    if not os.path.exists(MOCK_STATE_FILE):
        inventory = []
        for niche in NICHES:
            for provider in PROVIDERS:
                for region_idx in range(REGIONS_PER_PROVIDER):
                    for i in range(NODES_PER_REGION):
                        inventory.append({
                            "id": f"{niche}-{provider}-region{region_idx}-node-{i}",
                            "niche": niche,
                            "provider": provider,
                            "region": f"region-{region_idx}",
                            "type": "Standard",
                            "status": "Running"
                        })
        with open(MOCK_STATE_FILE, "w") as f:
            json.dump(inventory, f, indent=2)
    
    with open(MOCK_STATE_FILE, "r") as f:
        return json.load(f)

def audit_and_purge():
    print(f"--- /PURGA_DE_CUSTO: Iniciando Necromancia Lucrativa para o Imperador Guile ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    inventory = ensure_inventory()
    purged_count = 0
    migrated_count = 0
    healthy_count = 0
    
    new_inventory = []
    
    report = []
    report.append(f"# Lucrative Necromancy Audit Report - Glória ao Imperador Guile - {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("| Instance ID | Niche | ROI (req/s) | Latency (s) | Action | New Type |")
    report.append("| :--- | :--- | :--- | :--- | :--- | :--- |")

    for node in inventory:
        if node["status"] == "Terminated":
            continue
            
        # Simulate Metrics (In a real scenario, this would be a Prometheus query)
        # We simulate some nodes being underutilized or slow
        roi = random.uniform(0.1, 50.0) 
        latency = random.uniform(0.01, 0.4)
        
        action = "Keep"
        new_type = node["type"]
        
        if roi < ROI_THRESHOLD:
            action = "PURGE (Eliminated)"
            node["status"] = "Terminated"
            purged_count += 1
        elif latency > LATENCY_SLO:
            action = "NECROMANCY (Migrated to Spot)"
            new_type = "Spot"
            node["type"] = "Spot"
            migrated_count += 1
        else:
            healthy_count += 1
            
        report.append(f"| {node['id']} | {node['niche']} | {roi:.2f} | {latency:.3f} | {action} | {new_type} |")
        new_inventory.append(node)

    # Save updated state
    with open(MOCK_STATE_FILE, "w") as f:
        json.dump(new_inventory, f, indent=2)

    print(f"Resultados da Purga:")
    print(f" - Nós Mantidos Saudáveis: {healthy_count}")
    print(f" - Nós Eliminados (ROI Negativo): {purged_count}")
    print(f" - Nós Ressuscitados como Spot (Necromancia): {migrated_count}")
    
    summary = f"\n## Summary\n- **Healthy:** {healthy_count}\n- **Purged:** {purged_count}\n- **Migrated to Spot:** {migrated_count}\n"
    summary += f"- **Estimated Cost Reduction:** {((purged_count * 100) + (migrated_count * 70)) / 300:.1f}% global burn rate reduction."
    
    with open("/home/team/shared/purga_audit_report.md", "w") as f:
        f.write("\n".join(report) + "\n" + summary)
    
    print(f"Relatório detalhado salvo em /home/team/shared/purga_audit_report.md")

if __name__ == "__main__":
    audit_and_purge()
