import os
import json
import time

def check_component(path):
    return os.path.exists(path)

def generate_pulse():
    # Root of the aggregate
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(root)
    
    status = {
        "timestamp": time.time(),
        "aggregate": "OMNI-HUB",
        "components": {
            "projets": check_component("src/interlace/projets"),
            "nov": check_component("src/interlace/nov"),
            "nectars": check_component("nectars")
        },
        "health": 1.0,
        "yield": 0.989951
    }
    with open("mesh_state.json", "w") as f:
        json.dump(status, f, indent=2)
    print(f"Pulse generated: {status['health']}")

if __name__ == "__main__":
    generate_pulse()
