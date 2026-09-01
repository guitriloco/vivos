import requests
import time
import subprocess
import os
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# Default Configuration
DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_APP_DIR = "/opt/devops-squad"
DEFAULT_SERVICE_NAME = "active-asset"
SYNTHESIS_REPORT = "/home/team/shared/synthesis/synthesis_report.json"

# Thresholds for decision making (Arbitrage logic)
LATENCY_UPPER_THRESHOLD = 0.2  # 200ms - Scale up if higher
LATENCY_LOWER_THRESHOLD = 0.05 # 50ms - Scale down if lower
AVAILABILITY_THRESHOLD = 0.9999 # Updated to 99.99% per EMPIRE_SLO.md
LOW_REQUEST_RATE = 5.0        # requests/sec - Scale down if lower

# Cache for synthesis priority to avoid redundant file I/O
synthesis_cache = {
    "data": None,
    "last_read": 0
}

def query_prometheus(url, query):
    try:
        response = requests.get(f"{url}/api/v1/query", params={'query': query}, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get('data', {}).get('result', [])
        if results:
            return float(results[0]['value'][1])
        return None
    except Exception as e:
        # Suppress logging for invalid URLs in profiling
        if "invalid-url" not in url:
            print(f"Error querying Prometheus at {url} for '{query}': {e}")
        return None

def get_current_scale(service_name):
    try:
        cmd = f"docker ps --filter name={service_name} --format '{{{{.ID}}}}' | wc -l"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return int(output)
    except Exception as e:
        # print(f"Error getting current scale for {service_name}: {e}")
        return 0

def set_scale(app_dir, service_name, replicas):
    if replicas < 1:
        replicas = 1
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scaling {service_name} to {replicas} replicas...")
        cmd = f"docker-compose -f {app_dir}/docker-compose.yml up -d --scale {service_name}={replicas}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"Successfully scaled to {replicas}.")
    except Exception as e:
        print(f"Error scaling: {e}")

def get_synthesis_priority(service_name):
    """
    Checks if the service has high synthesis value based on the report.
    Uses caching to reduce disk I/O.
    """
    now = time.time()
    # Cache for 60 seconds
    if synthesis_cache["data"] is None or now - synthesis_cache["last_read"] > 60:
        try:
            if os.path.exists(SYNTHESIS_REPORT):
                with open(SYNTHESIS_REPORT, "r") as f:
                    synthesis_cache["data"] = json.load(f)
                    synthesis_cache["last_read"] = now
        except:
            pass
    
    if synthesis_cache["data"]:
        for node in synthesis_cache["data"].get("top_priority_nodes", []):
            if service_name in node["node_id"]:
                return True
    return False

def run_arbitrage_cycle(prometheus_url, app_dir, service_name):
    log_msg = f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Optimized Arbitrage Engine V2.1 Cycle for {service_name}..."
    print(log_msg)
    
    # 1. Gather Metrics in Parallel (Latency Reduction)
    queries = {
        "availability": "empire_asset:availability:ratio_1m",
        "latency": "empire_asset:latency_p95:seconds_1m",
        "req_rate": f'sum(rate(http_requests_total{{job="{service_name}"}}[1m]))'
    }
    
    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        future_to_key = {executor.submit(query_prometheus, prometheus_url, q): k for k, q in queries.items()}
        for future in as_completed(future_to_key):
            key = future_to_key[future]
            try:
                results[key] = future.result()
            except Exception:
                results[key] = None
            
    availability = results.get("availability")
    latency = results.get("latency")
    req_rate = results.get("req_rate")
    
    current_scale = get_current_scale(service_name)
    is_high_priority = get_synthesis_priority(service_name)

    metrics_log = (
        f"Metrics: Avail={availability}, Latency={latency}, Rate={req_rate}, Scale={current_scale}, Priority={is_high_priority}"
    )
    print(metrics_log)

    # 2. Decision Logic
    action_taken = "Optimal."
    
    if (latency is not None and latency > LATENCY_UPPER_THRESHOLD) or \
       (availability is not None and availability < AVAILABILITY_THRESHOLD):
        
        # Priority scaling: Scale up by 2 if high synthesis value
        increment = 2 if is_high_priority else 1
        target_scale = current_scale + increment
        action_taken = f"SCALING UP (+{increment}) - Priority={is_high_priority}"
        set_scale(app_dir, service_name, target_scale)
        
    elif latency is not None and latency < LATENCY_LOWER_THRESHOLD and \
         req_rate is not None and req_rate < LOW_REQUEST_RATE and \
         current_scale > 1:
        
        target_scale = current_scale - 1
        action_taken = "SCALING DOWN"
        set_scale(app_dir, service_name, target_scale)
        
    print(f"Action: {action_taken}")

    # Log
    log_file = f"/home/team/shared/scripts/arbitrage_v2_1_{service_name}.log"
    try:
        with open(log_file, "a") as f:
            f.write(f"{log_msg}\n{metrics_log}\nAction: {action_taken}\n")
    except:
        pass

def main():
    parser = argparse.ArgumentParser(description="Empire Arbitrage Engine V2.1 (Optimized)")
    parser.add_argument("--prometheus", default=DEFAULT_PROMETHEUS_URL)
    parser.add_argument("--app-dir", default=DEFAULT_APP_DIR)
    parser.add_argument("--service", default=DEFAULT_SERVICE_NAME)
    parser.add_argument("--interval", type=int, default=15) # 15s interval for sub-60s failover
    args = parser.parse_args()

    while True:
        run_arbitrage_cycle(args.prometheus, args.app_dir, args.service)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
