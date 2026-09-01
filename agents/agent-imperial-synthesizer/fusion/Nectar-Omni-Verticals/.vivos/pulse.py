import os
import json
import time

def check_verticals():
    verticals = ["Nectar_Pets", "Nectar_Health", "Nectar_Wealth", "Nectar_Dev", "NECTAR_SYNC_TEST"]
    status = {}
    for v in verticals:
        path = os.path.join(os.path.dirname(__file__), "..", v)
        status[v] = "ONLINE" if os.path.isdir(path) else "OFFLINE"
    return status

def main():
    while True:
        pulse_data = {
            "timestamp": time.time(),
            "repository": "Nectar-Omni-Verticals",
            "state": "SYNTHESIZED_V13",
            "verticals": check_verticals()
        }
        print(f"PULSE: {json.dumps(pulse_data)}")
        time.sleep(60)

if __name__ == "__main__":
    main()
