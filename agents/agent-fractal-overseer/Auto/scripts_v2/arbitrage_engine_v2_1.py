import requests
import time
import subprocess
import os
import argparse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── CENTRAL CONFIGURATION ──────────────────────────────────────────────────
CONFIG_PATH = "/home/team/shared/empire_config.json"
if os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "r") as config_file:
        empire_config = json.load(config_file)
else:
    empire_config = {
        "thresholds": {"latency_slo_sec": 0.1, "availability_target": 0.9999},
        "paths": {"synthesis_report": "/home/team/shared/synthesis/synthesis_report_l2.json"}
    }

DEFAULT_PROMETHEUS_URL = "http://localhost:9090"
DEFAULT_APP_DIR = "/opt/devops-squad"
DEFAULT_SERVICE_NAME = "active-asset"
SYNTHESIS_REPORT = empire_config["paths"]["synthesis_report"]

# Dynamic Thresholds based on Global SLO
LATENCY_UPPER_THRESHOLD = empire_config["thresholds"]["latency_slo_sec"] * 2  # 0.2s
LATENCY_LOWER_THRESHOLD = empire_config["thresholds"]["latency_slo_sec"] / 2  # 0.05s
AVAILABILITY_THRESHOLD = empire_config["thresholds"]["availability_target"]
LOW_REQUEST_RATE = 5.0  # requests/sec

synthesis_cache = {"data": None, "last_read": 0}

# ── CORE FUNCTIONS ──────────────────────────────────────────────────────────

def query_prometheus(url, query):
    try:
        response = requests.get(f"{url}/api/v1/query", params={'query': query}, timeout=10)
        response.raise_for_status()
        data = response.json()
        results = data.get('data', {}).get('result', [])
        return float(results[0]['value'][1]) if results else None
    except Exception as e:
        if "invalid-url" not in url:
            print(f"Error querying Prometheus: {e}")
        return None

def get_current_scale(service_name):
    try:
        cmd = f"docker ps --filter name={service_name} --format '{{{{.ID}}}}' | wc -l"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return int(output)
    except:
        return 0

def set_scale(app_dir, service_name, replicas):
    replicas = max(1, replicas)
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Scaling {service_name} to {replicas}...")
        cmd = f"docker-compose -f {app_dir}/docker-compose.yml up -d --scale {service_name}={replicas}"
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
    except Exception as e:
        print(f"Error scaling: {e}")

def get_synthesis_priority(service_name):
    global synthesis_cache
    now = time.time()
    if synthesis_cache["data"] is None or now - synthesis_cache["last_read"] > 60:
        try:
            if os.path.exists(SYNTHESIS_REPORT):
                with open(SYNTHESIS_REPORT, "r") as f:
                    synthesis_cache["data"] = json.load(f)
                    synthesis_cache["last_read"] = now
        except: pass
    
    if synthesis_cache["data"]:
        for node in synthesis_cache["data"].get("top_priority_nodes", []):
            if service_name in node["node_id"]: return True
    return False

def run_arbitrage_cycle(prometheus_url, app_dir, service_name):
    print(f"\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Cycle for {service_name}...")
    queries = {
        "availability": "empire_asset:availability:ratio_1m",
        "latency": "empire_asset:latency_p95:seconds_1m",
        "req_rate": f'sum(rate(http_requests_total{{job="{service_name}"}}[1m]))'
    }
    results = {}
    with ThreadPoolExecutor(max_workers=3) as executor:
        f_to_k = {executor.submit(query_prometheus, prometheus_url, q): k for k, q in queries.items()}
        for f in as_completed(f_to_k):
            try: results[f_to_k[f]] = f.result()
            except: results[f_to_k[f]] = None

    avail, lat, rate = results.get("availability"), results.get("latency"), results.get("req_rate")
    scale = get_current_scale(service_name)
    priority = get_synthesis_priority(service_name)
    
    print(f"Metrics: Avail={avail}, Lat={lat}, Rate={rate}, Scale={scale}, Priority={priority}")

    if (lat and lat > LATENCY_UPPER_THRESHOLD) or (avail and avail < AVAILABILITY_THRESHOLD):
        inc = 2 if priority else 1
        set_scale(app_dir, service_name, scale + inc)
    elif lat and lat < LATENCY_LOWER_THRESHOLD and rate and rate < LOW_REQUEST_RATE and scale > 1:
        set_scale(app_dir, service_name, scale - 1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--prometheus", default=DEFAULT_PROMETHEUS_URL)
    parser.add_argument("--app-dir", default=DEFAULT_APP_DIR)
    parser.add_argument("--service", default=DEFAULT_SERVICE_NAME)
    parser.add_argument("--interval", type=int, default=15)
    args = parser.parse_args()
    while True:
        run_arbitrage_cycle(args.prometheus, args.app_dir, args.service)
        time.sleep(args.interval)

if __name__ == "__main__":
    main()
