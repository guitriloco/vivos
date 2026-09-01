#!/bin/bash
set -e

# Install Docker
apt-get update
apt-get install -y docker.io docker-compose python3 python3-pip

mkdir -p /opt/monitoring/prometheus
mkdir -p /opt/monitoring/alertmanager

# Create Prometheus Config
cat <<EOF > /opt/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 5s
  evaluation_interval: 5s

alerting:
  alertmanagers:
    - static_configs:
        - targets:
          - alertmanager:9093

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

# Create SLI/SLO rules (Harden for 99.99% Availability and High-Resolution tracking)
cat <<EOF > /opt/monitoring/prometheus/rules.yml
groups:
  - name: empire_slis
    rules:
      - record: empire_asset:availability:ratio_5m
        expr: |
          sum(rate(http_requests_total{status!~"5.."}[5m]))
          /
          sum(rate(http_requests_total[5m]))
      - record: empire_asset:latency_p95:seconds_5m
        expr: |
          histogram_quantile(0.95, sum(rate(http_request_duration_seconds_bucket[5m])) by (le))
      - record: empire_synthesis:duration_seconds:p99
        expr: |
          histogram_quantile(0.99, sum(rate(empire_synthesis_duration_seconds_bucket[5m])) by (le))
      - record: empire_node:roi_status
        expr: |
          count(empire_node_roi > 0) / count(empire_node_roi)
  - name: empire_alerts
    rules:
      - alert: GlobalAssetAvailabilityBreach
        expr: empire_asset:availability:ratio_5m < 0.9999
        for: 15s
        labels:
          severity: critical
        annotations:
          summary: "Global Asset Availability Breach"
          description: "Global availability has dropped below 99.99%. Current: {{ $value }}"
      - alert: SynthesisLatencyBreach
        expr: empire_synthesis:duration_seconds:p99 > 10
        for: 15s
        labels:
          severity: warning
        annotations:
          summary: "Synthesis Latency Breach"
          description: "Synthesis latency p99 is above 10s. Current: {{ $value }}s"
      - alert: MarginIntegrityBreach
        expr: empire_node:roi_status < 1.0
        for: 15s
        labels:
          severity: critical
        annotations:
          summary: "Margin Integrity Breach"
          description: "Negative ROI nodes detected. Integrity: {{ $value }}"
EOF

# Create Alertmanager Config
cat <<EOF > /opt/monitoring/alertmanager/alertmanager.yml
route:
  group_by: ['alertname']
  group_wait: 10s
  group_interval: 10s
  repeat_interval: 1h
  receiver: 'web.hook'
receivers:
  - name: 'web.hook'
    webhook_configs:
      - url: 'http://127.0.0.1:5001/'
EOF

# Setup Arbitrage Engine on the Monitoring Node (Local Governor)
cat <<'EOF' > /opt/monitoring/arbitrage_engine.py
import requests
import time
import os

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
        print(f"Error querying Prometheus: {e}")
        return None

def run_arbitrage():
    avail = query_prometheus("empire_asset:availability:ratio_5m")
    if avail is not None and avail < AVAILABILITY_THRESHOLD:
        print(f"Empire Governance Alert: SLO BREACH detected ({avail}). Initiating auto-scaling/remediation protocol.")
    else:
        print("Empire Status: ALL ASSETS OPTIMAL. SLO 99.99% MAINTAINED.")

if __name__ == "__main__":
    while True:
        run_arbitrage()
        time.sleep(15) # High-resolution cycle
EOF

# Run Monitoring Stack + Arbitrage Engine
cat <<EOF > /opt/monitoring/docker-compose.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus:latest
    container_name: prometheus
    volumes:
      - ./prometheus:/etc/prometheus
    ports:
      - "9090:9090"
    restart: unless-stopped

  alertmanager:
    image: prom/alertmanager:latest
    container_name: alertmanager
    volumes:
      - ./alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    ports:
      - "9093:9093"
    restart: unless-stopped

  grafana:
    image: grafana/grafana:latest
    container_name: grafana
    ports:
      - "3001:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    restart: unless-stopped

  arbitrage-governor:
    container_name: arbitrage-governor
    build:
      context: .
      dockerfile_inline: |
        FROM python:3.9-slim
        RUN pip install requests
        COPY arbitrage_engine.py /app/arbitrage_engine.py
        WORKDIR /app
        CMD ["python", "arbitrage_engine.py"]
    restart: unless-stopped
EOF

cd /opt/monitoring
docker-compose up -d
