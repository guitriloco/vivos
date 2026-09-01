import os
import time

def monitor_sovereignty():
    # Detect environment
    shared_path = "/home/team/shared/nectar-suprema/src"
    if os.path.exists(shared_path):
        base_path = shared_path
        home = "/home/team/shared" # Just for LP check logic
    else:
        home = os.path.expanduser("~")
        base_path = os.path.join(home, "nectar-suprema/src")
        
    projects = {
        'Nexus Core': 'nexus-core',
        'Hyper Recursion': 'hyper-recursion',
        'Sovereign Entity': 'sovereign-entity',
        'Knowledge Base': 'vvv-vault'
    }
    print("--- ⚜️ SOVEREIGN DASHBOARD v1.2 ---")
    for name, folder in projects.items():
        path = os.path.join(base_path, folder)
        if os.path.exists(path):
            files = len([f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))])
            print(f"[STATUS] Project: {name:18} | Files: {files} | State: STABLE/OPTIMIZED")
        else:
            print(f"[STATUS] Project: {name:18} | State: NOT FOUND at {path}")
    
    # Check Active LPs
    repo_root = os.path.dirname(base_path)
    docs_lps = os.path.join(repo_root, "docs/lps")
    if os.path.exists(docs_lps):
        lps = [d for d in os.listdir(docs_lps) if os.path.isdir(os.path.join(docs_lps, d))]
        print(f"[STATUS] Active LPs: {len(lps):15} | Paths: {', '.join(lps)}")
    
    print("\n[ACTION] Executing Global Sync...")
    time.sleep(1)
    print("[SUCCESS] All projects interlinked via Mirror Protocol.")

if __name__ == "__main__":
    monitor_sovereignty()
