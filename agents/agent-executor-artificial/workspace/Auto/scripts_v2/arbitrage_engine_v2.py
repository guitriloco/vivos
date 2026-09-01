import requests
import time
import subprocess
import os
import argparse
import json

# Default Configuration
DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_APP_DIR = "/opt/devops-squad"
DEFAULT_SERVICE_NAME = "active-asset"
SYNTHESIS_REPORT = "/home/team/shared/synthesis/synthesis_report.json"

# Thresholds for decision making (Arbitrage logic)
LATENCY_UPPER_THRESHOLD = 0.2  # 200ms - Scale up if higher
LATENCY_LOWER_THRESHOLD = 0.05 # 50ms - Scale down if lower
AVAILABILITY_THRESHOLD = 0.999 # 99.9% - Scale up if lower
LOW_REQUEST_RATE = 5.0        # requests/sec - Scale down if lower

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
        print(f"Error querying Prometheus at {url} for '{query}': {e}")
        return None

def get_current_scale(service_name):
    try:
        cmd = f"docker ps --filter name={service_name} --format '{{{{.ID}}}}' | wc -l"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return int(output)
    except Exception as e:
        print(f"Error getting current scale for {service_name}: {e}")
        return 1

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
    """
    try:
        if os.path.exists(SYNTHESIS_REPORT):
            with open(SYNTHESIS_REPORT, "r") as f:
                report = json.load(f)
            # Find current node in top priority
            # For simplicity, we check niches here
            for node in report.get("top_priority_nodes", []):
                if service_name in node["node_id"]:
                    return True
    except:
        pass
    return False

def run_arbitrage_cycle(prometheus_url, app_dir, service_name):
    log_msg = f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Arbitrage Engine V2 Cycle for {service_name}..."
    print(log_msg)
    
    # 1. Run Necromancy (Purge)
    try:
        subprocess.run(["python3", "/home/team/shared/scripts/lucrative_necromancy.py"], check=True, capture_output=True)
    except:
        pass

    # 2. Run Synthesis Aggregation
    try:
        subprocess.run(["python3", "/home/team/shared/scripts/synthesis_aggregator.py"], check=True, capture_output=True)
    except:
        pass

    # 3. Gather Metrics
    availability = query_prometheus(prometheus_url, "empire_asset:availability:ratio_5m") or query_prometheus(prometheus_url, "sample_app:availability:ratio_5m")
    latency = query_prometheus(prometheus_url, "empire_asset:latency_p95:seconds_5m") or query_prometheus(prometheus_url, "sample_app:latency_p95:seconds_5m")
    req_rate = query_prometheus(prometheus_url, f'sum(rate(http_requests_total{{job="{service_name}"}}[5m]))')
    
    current_scale = get_current_scale(service_name)
    is_high_priority = get_synthesis_priority(service_name)

    metrics_log = (
        f"Metrics: Avail={availability}, Latency={latency}, Rate={req_rate}, Scale={current_scale}, Priority={is_high_priority}"
    )
    print(metrics_log)

    # 4. Decision Logic
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
    with open(f"/home/team/shared/scripts/arbitrage_v2_{service_name}.log", "a") as f:
        f.write(f"{log_msg}\n{metrics_log}\nAction: {action_taken}\n")

def main():
    parser = argparse.ArgumentParser(description="Empire Arbitrage Engine V2")
    parser.add_argument("--prometheus", default=DEFAULT_PROMETHEUS_URL)
    parser.add_argument("--app-dir", default=DEFAULT_APP_DIR)
    parser.add_argument("--service", default=DEFAULT_SERVICE_NAME)
    parser.add_argument("--interval", type=int, default=60)
    args = parser.parse_args()

    while True:
        run_arbitrage_cycle(args.prometheus, args.app_dir, args.service)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
