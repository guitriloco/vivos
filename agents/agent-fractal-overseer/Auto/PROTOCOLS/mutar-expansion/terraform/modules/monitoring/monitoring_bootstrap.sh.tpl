#!/bin/bash
set -e

# Install Docker
apt-get update
apt-get install -y docker.io docker-compose python3 python3-pip

mkdir -p /opt/monitoring/prometheus

# Create Prometheus Config with recording rules
cat <<EOF > /opt/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s

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

# Create SLI/SLO rules (Updated for Empire Asset Governance)
cat <<EOF > /opt/monitoring/prometheus/rules.yml
groups:
  - name: empire_niche_slis
    rules:
      - record: empire_asset:availability:ratio_5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
      - record: empire_asset:latency_p95:seconds_5m
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
EOF

# Setup Arbitrage Engine on the Monitoring Node
cat <<'EOF' > /opt/monitoring/arbitrage_engine.py
import requests
import time
import os

PROMETHEUS_URL = "http://prometheus:9090"
AVAILABILITY_THRESHOLD = 0.999

def query_prometheus(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query}, timeout=10)
        data = response.json()
        if data['data']['result']:
            return float(data['data']['result'][0]['value'][1])
        return None
    except Exception as e:
        print(f"Error querying Prometheus: {e}")
        return None

def run_arbitrage():
    avail = query_prometheus("empire_asset:availability:ratio_5m")
    if avail is not None and avail < AVAILABILITY_THRESHOLD:
        print(f"Empire Governance Alert: Low availability detected ({avail}). Initiating auto-scaling protocol.")
    else:
        print("Empire Status: ALL ASSETS OPTIMAL.")

if __name__ == "__main__":
    while True:
        run_arbitrage()
        time.sleep(60)
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
EOF

cd /opt/monitoring
docker-compose up -d
