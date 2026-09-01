#!/bin/bash
set -e

# Install Docker
apt-get update
apt-get install -y docker.io docker-compose

mkdir -p /opt/monitoring/prometheus

# Create Prometheus Config
cat <<EOF > /opt/monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'node-exporter'
    static_configs:
      - targets:
%{ for ip in target_ips ~}
        - '${ip}:9100'
%{ endfor ~}

  - job_name: 'sample-app'
    static_configs:
      - targets:
%{ for ip in target_ips ~}
        - '${ip}:3000'
%{ endfor ~}
EOF

# Run Monitoring Stack
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
EOF

cd /opt/monitoring
docker-compose up -d
