import json
import os

MOCK_STATE_FILE = "/home/team/shared/inventory/global_inventory.json"
NICHES = ["bio-wealth", "financas", "e-commerce", "health-tech", "real-estate"]
PROVIDERS = {
    "AWS": ["us-east-1", "eu-west-1", "ap-southeast-1"],
    "DigitalOcean": ["nyc1", "ams3", "sgp1"],
    "GCP": ["us-central1", "europe-west1", "asia-southeast1"]
}
NODES_PER_REGION_PER_NICHE = 12

def update_inventory():
    print(f"--- /ENTIDADE_12: Updating Inventory to 540 Nodes ---")
    inventory = []
    
    for niche in NICHES:
        for provider, regions in PROVIDERS.items():
            for region in regions:
                for i in range(NODES_PER_REGION_PER_NICHE):
                    inventory.append({
                        "id": f"{niche}-{provider.lower()}-{region}-node-{i:02d}",
                        "niche": niche,
                        "provider": provider,
                        "region": region,
                        "type": "Standard",
                        "status": "Running"
                    })
    
    os.makedirs(os.path.dirname(MOCK_STATE_FILE), exist_ok=True)
    with open(MOCK_STATE_FILE, "w") as f:
        json.dump(inventory, f, indent=2)
    
    print(f"Inventory updated: {len(inventory)} nodes recorded.")

if __name__ == "__main__":
    update_inventory()
