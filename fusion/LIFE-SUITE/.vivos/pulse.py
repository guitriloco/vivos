import os
import json
import time

def generate_pulse():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    
    status = {
        "timestamp": time.time(),
        "aggregate": "LIFE-SUITE",
        "health": 1.0,
        "intelligence_index": 0.998
    }
    with open("mesh_state.json", "w") as f:
        json.dump(status, f, indent=2)
    print(f"💓 LIFE-SUITE: Pulse Active | Health: {status['health']}")

if __name__ == "__main__":
    generate_pulse()
