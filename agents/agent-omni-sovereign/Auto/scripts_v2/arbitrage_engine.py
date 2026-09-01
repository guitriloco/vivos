import requests
import time
import subprocess
import os
import argparse

# Default Configuration
DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_APP_DIR = "/opt/devops-squad"
DEFAULT_SERVICE_NAME = "active-asset"

# Thresholds for decision making (Arbitrage logic)
LATENCY_UPPER_THRESHOLD = 0.2  # 200ms - Scale up if higher
LATENCY_LOWER_THRESHOLD = 0.05 # 50ms - Scale down if lower
AVAILABILITY_THRESHOLD = 0.999 # 99.9% - Scale up if lower
LOW_REQUEST_RATE = 5.0        # requests/sec - Scale down if lower

def query_prometheus(url, query):
    """
    Queries Prometheus for a single scalar value.
    """
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
    """
    Determines the current number of running replicas.
    """
    try:
        # Check for both docker compose and standalone docker naming patterns
        cmd = f"docker ps --filter name={service_name} --format '{{{{.ID}}}}' | wc -l"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return int(output)
    except Exception as e:
        print(f"Error getting current scale for {service_name}: {e}")
        return 1

def set_scale(app_dir, service_name, replicas):
    """
    Scales the docker-compose service.
    """
    if replicas < 1:
        replicas = 1
    
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scaling {service_name} to {replicas} replicas...")
        # Try both 'docker compose' and 'docker-compose'
        cmd = f"docker-compose -f {app_dir}/docker-compose.yml up -d --scale {service_name}={replicas}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"Successfully scaled to {replicas}.")
    except Exception as e:
        print(f"Error scaling: {e}")

def run_arbitrage_cycle(prometheus_url, app_dir, service_name):
    """
    A single cycle of monitoring and adjustment.
    """
    log_msg = f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Starting Arbitrage Cycle for {service_name}..."
    print(log_msg)
    
    # 1. Gather Metrics (Try new Empire names first, then fallback to old sample_app names)
    availability = query_prometheus(prometheus_url, "empire_asset:availability:ratio_5m")
    if availability is None:
        availability = query_prometheus(prometheus_url, "sample_app:availability:ratio_5m")

    latency = query_prometheus(prometheus_url, "empire_asset:latency_p95:seconds_5m")
    if latency is None:
        latency = query_prometheus(prometheus_url, "sample_app:latency_p95:seconds_5m")

    req_rate = query_prometheus(prometheus_url, f'sum(rate(http_requests_total{{job="{service_name}"}}[5m]))')
    
    metrics_log = (
        f"Current Metrics:\n"
        f"  - Availability: {availability if availability is not None else 'N/A'}\n"
        f"  - Latency (p95): {latency if latency is not None else 'N/A'}s\n"
        f"  - Request Rate: {req_rate if req_rate is not None else 'N/A'} req/s"
    )
    print(metrics_log)
    
    # 1.5. Run Necromancy Audit (Cost Purge Integration)
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Triggering Lucrative Necromancy Audit...")
        subprocess.run(["python3", "/home/team/shared/scripts/lucrative_necromancy.py"], check=True, capture_output=True)
        print("Necromancy Audit completed.")
    except Exception as e:
        print(f"Warning: Necromancy Audit failed to run: {e}")

    current_scale = get_current_scale(service_name)
    print(f"  - Current Scale: {current_scale} replicas")

    # 2. Decision Logic (Arbitrage)
    action_taken = "No adjustments needed. Infrastructure is optimal."
    
    if (latency is not None and latency > LATENCY_UPPER_THRESHOLD) or \
       (availability is not None and availability < AVAILABILITY_THRESHOLD):
        
        target_scale = current_scale + 1
        action_taken = f"Condition detected (Latency > {LATENCY_UPPER_THRESHOLD}s or Availability < {AVAILABILITY_THRESHOLD}). Scaling up."
        print(f"Action: {action_taken}")
        set_scale(app_dir, service_name, target_scale)
        
    elif latency is not None and latency < LATENCY_LOWER_THRESHOLD and \
         req_rate is not None and req_rate < LOW_REQUEST_RATE and \
         current_scale > 1:
        
        target_scale = current_scale - 1
        action_taken = f"Underutilization detected (Latency < {LATENCY_LOWER_THRESHOLD}s and Rate < {LOW_REQUEST_RATE}). Scaling down."
        print(f"Action: {action_taken}")
        set_scale(app_dir, service_name, target_scale)
        
    else:
        print(f"Action: {action_taken}")

    # Log for visibility
    try:
        log_file = f"/home/team/shared/scripts/arbitrage_{service_name}.log"
        with open(log_file, "a") as f:
            f.write(f"{log_msg}\n{metrics_log}\nAction: {action_taken}\n")
    except Exception as e:
        print(f"Error writing to log file: {e}")

def main():
    parser = argparse.ArgumentParser(description="Empire Arbitrage Engine")
    parser.add_argument("--prometheus", default=DEFAULT_PROMETHEUS_URL, help="Prometheus URL")
    parser.add_argument("--app-dir", default=DEFAULT_APP_DIR, help="Application directory")
    parser.add_argument("--service", default=DEFAULT_SERVICE_NAME, help="Service name")
    parser.add_argument("--interval", type=int, default=60, help="Check interval in seconds")
    
    args = parser.parse_args()

    print(f"Empire Arbitrage Engine Initialized for {args.service}.")
    print(f"Prometheus URL: {args.prometheus}")
    
    try:
        while True:
            run_arbitrage_cycle(args.prometheus, args.app_dir, args.service)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nArbitrage Engine stopped by user.")

if __name__ == "__main__":
    main()
