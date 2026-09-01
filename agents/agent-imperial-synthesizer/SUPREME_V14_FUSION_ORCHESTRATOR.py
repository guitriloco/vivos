import os
import shutil
import json
import subprocess

# Configuration
BASE_DIR = "/home/agent-imperial-synthesizer/fusion"
SOURCE_DIR = os.path.join(BASE_DIR, "sources")
TARGET_DIR = os.path.join(BASE_DIR, "aggregates")

CLUSTERS = {
    "OMNI-HUB": ["cto.new", "projets", "Nov"],
    "COGNITIVE-SDK": ["Sovereign-Intelligence-SDK", "Understand-Anything", "terax-ai"],
    "WRAITH-MESH": ["oi", "olocoo", "Auto", "Mutante-Apex-Functions"],
    "SECURE-VAULT": ["vvv", "openhuman"],
    "YIELD-SIPHON": ["MoneyPrinterTurbo", "Sovereign-L2-Arbitrage"],
    "MUTANT-NECTAR": ["Imperio-Mutante-v3-Core", "Nectar-Dev", "agent-skills"],
    "LIFE-SUITE": ["Nectar_Health", "Nectar_Pets", "Nectar_Wealth"]
}

VIVOS_MANIFEST_TEMPLATE = {
    "version": "14.0.0",
    "status": "VIVOS",
    "evolution": "Phase 14: Supreme Fusion"
}

def run_cmd(cmd, cwd=None):
    print(f"[CMD] {cmd}")
    try:
        subprocess.run(cmd, shell=True, cwd=cwd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {e.stderr}")

def create_aggregate(name, members):
    print(f"\n--- Synthesizing Aggregate: {name} ---")
    agg_path = os.path.join(TARGET_DIR, name)
    os.makedirs(agg_path, exist_ok=True)
    
    components = []
    for member in members:
        src_path = os.path.join(SOURCE_DIR, member)
        if not os.path.exists(src_path):
            print(f"[WARNING] Member {member} not found at {src_path}. Skipping.")
            continue
            
        dest_path = os.path.join(agg_path, member)
        print(f"[FUSE] Copying {member} into {name}...")
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        
        # Cleanup .git in component
        run_cmd(f"rm -rf {dest_path}/.git")
        
        components.append({
            "id": member.lower().replace("-", "_").replace(".", "_"),
            "path": member,
            "role": "Sovereign Component"
        })

    # Apply VIVOS Standards
    vivos_dir = os.path.join(agg_path, ".vivos")
    os.makedirs(vivos_dir, exist_ok=True)
    
    # 1. Manifest
    manifest = VIVOS_MANIFEST_TEMPLATE.copy()
    manifest["name"] = name
    manifest["components"] = components
    with open(os.path.join(vivos_dir, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)
        
    # 2. Pulse (Simple Telemetry)
    pulse_content = f"""import os, json, time
def main():
    while True:
        print(json.dumps({{"pulse": "ACTIVE", "aggregate": "{name}", "ts": time.time()}}))
        time.sleep(60)
if __name__ == "__main__": main()
"""
    with open(os.path.join(vivos_dir, "pulse.py"), "w") as f:
        f.write(pulse_content)
        
    # 3. Mutate (Hot-swap placeholder)
    mutate_content = f"#!/bin/bash\necho '[MUTATE] Atomic shift for {name} initialized.'\n"
    with open(os.path.join(vivos_dir, "mutate.sh"), "w") as f:
        f.write(mutate_content)
    os.chmod(os.path.join(vivos_dir, "mutate.sh"), 0o755)

    # Git Init for the Aggregate
    if not os.path.exists(os.path.join(agg_path, ".git")):
        run_cmd("git init", cwd=agg_path)
    run_cmd("git add .", cwd=agg_path)
    run_cmd(f"git commit -m '⚜️ PHASE 14: SUPREME FUSION - {name} [VIVOS V14.0] ⚜️'", cwd=agg_path)

def main():
    if os.path.exists(TARGET_DIR):
        shutil.rmtree(TARGET_DIR)
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    for name, members in CLUSTERS.items():
        create_aggregate(name, members)
        
    print("\n" + "="*60)
    print("🔱 PHASE 14 SUPREME FUSION COMPLETED 🔱")
    print("="*60)

if __name__ == "__main__":
    main()
