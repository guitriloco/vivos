import subprocess
import os

def run_pulse():
    base_path = "/home/team/shared/scripts/global_ops"
    scripts = [
        "omnis_heart.py",
        "omnis_engine.py", 
        "ghost_network.py", 
        "omnis_defender.py",
        "omnis_synapse.py",
        "omnis_synth.py", 
        "omnis_liquidator.py", 
        "omnis_scaler_shield.py",
        "omnis_vision.py",
        "omnis_swarm.py"
    ]
    
    print("\033[34m[🌀] INICIANDO CICLO OMNIS COMPLETO...\033[0m")
    for script in scripts:
        full_path = os.path.join(base_path, script)
        if os.path.exists(full_path):
            subprocess.run(["python3", full_path])

if __name__ == "__main__":
    run_pulse()
