import requests
import json
import time

# List of instance IPs or hostnames (would normally come from discovery or Terraform output)
# For this simulation, we'll assume a list or a range
INSTANCES = [
    "http://localhost:3000", # Local simulation
    # "http://instance-1:3000",
    # ...
]

def check_instance_arbitrage(url):
    """
    Checks if the arbitrage engine is active on an instance by looking for its metrics or status.
    In a real scenario, this might query a specific status endpoint or check Prometheus.
    """
    try:
        # Check if app is up
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            return "ACTIVE"
        return "INACTIVE"
    except Exception:
        return "UNREACHABLE"

def generate_global_report():
    print(f"--- SOBERANIA: Global Arbitrage Status Report ---")
    print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'Instance':<30} | {'Status':<15}")
    print("-" * 50)
    
    for instance in INSTANCES:
        status = check_instance_arbitrage(instance)
        print(f"{instance:<30} | {status:<15}")
    
    print("-" * 50)
    print("End of Report")

if __name__ == "__main__":
    generate_global_report()
