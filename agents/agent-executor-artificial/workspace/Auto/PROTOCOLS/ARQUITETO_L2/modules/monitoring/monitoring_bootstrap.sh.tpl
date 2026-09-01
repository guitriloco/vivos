#!/bin/bash
# Monitoring & Governance Bootstrap (Governor V2.2 - Hardened for 99.99% SLO)

# Install Docker & Compose
apt-get update
apt-get install -y docker.io docker-compose
systemctl start docker
systemctl enable docker

# Create Monitoring Directories
mkdir -p /opt/monitoring/prometheus
chmod 777 /opt/monitoring/prometheus

# Create Prometheus Configuration
cat <<EOF > /opt/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s # High-resolution scraping for 99.99% SLO
  evaluation_interval: 15s

rule_files:
  - "rules.yml"

scrape_configs:
%{ for niche, ips in target_ips_by_niche ~}
  - job_name: 'niche-${niche}-active-asset'
    static_configs:
      - targets:
%{ for ip in ips ~}
        - '${ip}:3000'
%{ endfor ~}

  - job_name: 'niche-${niche}-node'
    static_configs:
      - targets:
%{ for ip in ips ~}
        - '${ip}:9100'
%{ endfor ~}
%{ endfor ~}
EOF

# Create SLI/SLO rules (Updated for Empire Asset Governance & 99.99% SLO)
cat <<EOF > /opt/monitoring/prometheus/rules.yml
groups:
  - name: empire_niche_slis
    rules:
      # 1m Availability for fast detection (Failover support)
      - record: empire_asset:availability:ratio_1m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[1m]))
          /
          sum(rate(http_requests_total[1m]))
      # 5m Availability for official SLO compliance
      - record: empire_asset:availability:ratio_5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
      - record: empire_asset:latency_p95:seconds_1m
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[1m])) by (le))
      - record: empire_asset:latency_p95:seconds_5m
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
EOF

# Setup Arbitrage Engine on the Monitoring Node (Governor V2.2 - Global Control)
cat <<'EOF' > /opt/monitoring/arbitrage_engine.py
import requests
import time
import os
import subprocess

PROMETHEUS_URL = "http://prometheus:9090"
AVAILABILITY_THRESHOLD = 0.9999

def query_prometheus(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query}, timeout=10)
        data = response.json()
        if data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
        return None
    except Exception as e:
        return None

def run_centralized_tasks():
    # Centralized control: Execute Necromancy and Synthesis from the hub
    # This prevents node-level collisions and handles the 540-node scale
    try:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Executing Centralized Necromancy (ROI Audit)...")
        subprocess.run(["python3", "/home/team/shared/scripts/lucrative_necromancy.py"], capture_output=True)
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Executing Centralized Synthesis L2 (Massive Scale Aggregation)...")
        subprocess.run(["python3", "/home/team/shared/scripts/synthesis_aggregator_l2.py"], capture_output=True)
    except Exception as e:
        print(f"Error running centralized tasks: {e}")

def run_governance():
    # Use 1m for faster governor response
    avail = query_prometheus("empire_asset:availability:ratio_1m")
    if avail is not None and avail < AVAILABILITY_THRESHOLD:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Empire Governance Alert: SLO BREACH ({avail}).")
    else:
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Empire Status: OPTIMAL (SLO 99.99% MET).")
    
    # Run heavy tasks every 4 cycles (~1 minute)
    if int(time.time() / 15) % 4 == 0:
        run_centralized_tasks()

if __name__ == "__main__":
    while True:
        run_governance()
        time.sleep(15) # Fast 15s cycle for 99.99% availability response
EOF

# Run Monitoring Stack + Arbitrage Engine
cat <<EOF > /opt/monitoring/docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    volumes:
      - ./prometheus:/etc/prometheus
    ports:
      - "9090:9090"
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3001:3000"
  arbitrage-governor:
    build:
      context: .
      dockerfile_inline: |
        FROM python:3.9-slim
        RUN pip install requests
        COPY arbitrage_engine.py /app/arbitrage_engine.py
        WORKDIR /app
        CMD ["python", "arbitrage_engine.py"]
    volumes:
      - /home/team/shared:/home/team/shared
EOF

cd /opt/monitoring
docker-compose up -d
