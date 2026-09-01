import json
import os

ASSETS_DIR = "/home/team/shared/vault_staging/marketplace_assets/"
TEMPLATES = [
    "OMNI-HUB.json", "COGNITIVE-SDK.json", "WRAITH-MESH.json",
    "SECURE-VAULT.json", "YIELD-SIPHON.json", "MUTANT-NECTAR.json", "LIFE-SUITE.json"
]

optimization_data = {
    "margin": "Infinite",
    "scaling": "Zero-Cost",
    "value_extraction": "Recursive"
}

for template in TEMPLATES:
    path = os.path.join(ASSETS_DIR, template)
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = json.load(f)
        
        data["optimization"] = optimization_data
        data["vivos_status"] = "VIVOS-ST"
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Updated {template}")
    else:
        print(f"Skipping {template} (not found)")
