import os
import json
import time

def check_core_components():
    components = ["Imperio_mutante", "Imperio-Mutante", "Imperio-Mutante-v3-Core"]
    status = {}
    for c in components:
        path = os.path.join(os.path.dirname(__file__), "..", c)
        status[c] = "ONLINE" if os.path.isdir(path) else "OFFLINE"
    return status

def main():
    while True:
        pulse_data = {
            "timestamp": time.time(),
            "repository": "Sovereign-Imperial-Core",
            "state": "SYNTHESIZED_V13",
            "components": check_core_components()
        }
        print(f"PULSE: {json.dumps(pulse_data)}")
        time.sleep(60)

if __name__ == "__main__":
    main()
