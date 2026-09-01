#!/bin/bash
set -e

# Variable injected by Terraform
NICHE_NAME="${niche_name}"

# Update and install dependencies
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg-agent python3-pip

# Install Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-get install -y docker-ce docker-ce-cli containerd.io

# Install Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Setup Application
mkdir -p /opt/devops-squad
cat <<EOF > /opt/devops-squad/docker-compose.yml
version: '3.8'
services:
  sample-app:
    image: node:18-slim
    command: >
      bash -c "echo \"const http = require('http'); const client = require('prom-client'); const collectDefaultMetrics = client.collectDefaultMetrics; collectDefaultMetrics(); const requestCounter = new client.Counter({ name: 'http_requests_total', help: 'Total HTTP requests', labelNames: ['method', 'route', 'status'] }); const server = http.createServer((req, res) => { if (req.url === '/metrics') { res.setHeader('Content-Type', client.register.contentType); client.register.metrics().then(data => res.end(data)); return; } requestCounter.inc({ method: req.method, route: req.url, status: 200 }); res.writeHead(200); res.end('Hello from \$NICHE_NAME niche'); }); server.listen(3000);\" > index.js && npm install prom-client && node index.js"
    ports:
      - "3000:3000"
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
    ports:
      - "9090:9090"
EOF

# Local Prometheus config for the Arbitrage Engine
cat <<EOF > /opt/devops-squad/prometheus.yml
global:
  scrape_interval: 15s
scrape_configs:
  - job_name: 'sample-app'
    static_configs:
      - targets: ['sample-app:3000']
EOF

# Install Arbitrage Engine requirements
pip3 install requests

# Setup Arbitrage Engine
cat <<'PYEOF' > /opt/devops-squad/arbitrage_engine.py
import requests
import time
import subprocess
import os
import argparse

LATENCY_UPPER_THRESHOLD = 0.2
LATENCY_LOWER_THRESHOLD = 0.05
AVAILABILITY_THRESHOLD = 0.999
LOW_REQUEST_RATE = 5.0

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
        print(f"Error querying Prometheus: {e}")
        return None

def get_current_scale(service_name):
    try:
        cmd = f"docker ps --filter name={service_name} --format '{{{{.ID}}}}' | wc -l"
        output = subprocess.check_output(cmd, shell=True).decode().strip()
        return int(output)
    except Exception as e:
        return 1

def set_scale(app_dir, service_name, replicas):
    if replicas < 1: replicas = 1
    try:
        cmd = f"docker-compose -f {app_dir}/docker-compose.yml up -d --scale {service_name}={replicas}"
        subprocess.run(cmd, shell=True, check=True)
    except Exception as e:
        print(f"Error scaling: {e}")

def run_cycle(prometheus_url, app_dir, service_name):
    availability = query_prometheus(prometheus_url, "sum(rate(http_requests_total{status!~'5..'}[5m])) / sum(rate(http_requests_total[5m]))")
    # Simplified latency query for the niche demo
    latency = query_prometheus(prometheus_url, "rate(http_request_duration_seconds_sum[5m]) / rate(http_request_duration_seconds_count[5m])")
    req_rate = query_prometheus(prometheus_url, 'sum(rate(http_requests_total[5m]))')
    
    current_scale = get_current_scale(service_name)
    
    if (latency is not None and latency > LATENCY_UPPER_THRESHOLD) or (availability is not None and availability < AVAILABILITY_THRESHOLD):
        set_scale(app_dir, service_name, current_scale + 1)
    elif latency is not None and latency < LATENCY_LOWER_THRESHOLD and req_rate is not None and req_rate < LOW_REQUEST_RATE and current_scale > 1:
        set_scale(app_dir, service_name, current_scale - 1)

if __name__ == "__main__":
    while True:
        run_cycle("http://localhost:9090", "/opt/devops-squad", "sample-app")
        time.sleep(60)
PYEOF

cd /opt/devops-squad
docker-compose up -d
python3 arbitrage_engine.py > arbitrage.log 2>&1 &
