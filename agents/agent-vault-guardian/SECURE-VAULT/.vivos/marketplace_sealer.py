#!/usr/bin/env python3
import hashlib
import os
import json
from datetime import datetime

TEMPLATES_DIR = "/home/team/shared/vivos_v15_templates"

def hash_content(content):
    return hashlib.sha3_256(content.encode()).hexdigest()

def seal_templates():
    templates = [f for f in os.listdir(TEMPLATES_DIR) if f.endswith(".json")]
    print(f"[MARKETPLACE] Sealing {len(templates)} templates...")
    
    global_hashes = {}
    
    for template_file in sorted(templates):
        path = os.path.join(TEMPLATES_DIR, template_file)
        with open(path, 'r') as f:
            data = json.load(f)
            
        # Remove old seal if present for clean hash
        if "zkp_seal" in data:
            del data["zkp_seal"]
            
        content_hash = hash_content(json.dumps(data, sort_keys=True))
        data["zkp_seal"] = content_hash
        data["last_hardened"] = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
            
        global_hashes[template_file] = content_hash
        print(f"[MARKETPLACE] {template_file} sealed: {content_hash}")

    # Create Master Marketplace Seal
    master_content = "".join(global_hashes[k] for k in sorted(global_hashes.keys()))
    master_seal = hash_content(master_content)
    
    registry = {
        "vivos_version": "15.1",
        "type": "Marketplace Supreme Registry",
        "master_seal": master_seal,
        "template_seals": global_hashes,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    }
    
    registry_path = os.path.join(TEMPLATES_DIR, "MARKETPLACE_ZKP_REGISTRY.json")
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)
        
    print(f"[MARKETPLACE] Supreme Registry Created. Master Seal: {master_seal}")
    return master_seal

if __name__ == "__main__":
    seal_templates()
