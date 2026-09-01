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
  - job_name: 'niche-${niche}-app'
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

# Create SLI/SLO rules
cat <<EOF > /opt/monitoring/prometheus/rules.yml
groups:
  - name: niche_slis
    rules:
      - record: sample_app:availability:ratio_5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
EOF

# Setup Arbitrage Engine on the Monitoring Node
cat <<'EOF' > /opt/monitoring/arbitrage_engine.py
import requests
import time
import subprocess

PROMETHEUS_URL = "http://prometheus:9090"
AVAILABILITY_THRESHOLD = 0.999

def query_prometheus(query):
    try:
        response = requests.get(f"{PROMETHEUS_URL}/api/v1/query", params={'query': query}, timeout=10)
        return float(response.json()['data']['result'][0]['value'][1])
    except:
        return None

def run_arbitrage():
    avail = query_prometheus("sample_app:availability:ratio_5m")
    if avail and avail < AVAILABILITY_THRESHOLD:
        print(f"Low availability detected: {avail}. Scalability action required.")
        # In a real setup, this would call cloud APIs or Ansible to scale
    else:
        print("System health optimal.")

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
      - "3000:3000"
  arbitrage-engine:
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
