#!/bin/bash
set -e

# Update and install dependencies
apt-get update
apt-get install -y docker.io docker-compose

# Setup Application
mkdir -p /opt/devops-squad
cat <<EOF > /opt/devops-squad/docker-compose.yml
version: '3.8'
services:
  sample-app:
    image: node:18-slim
    command: >
      bash -c "echo 'const http = require(\"http\"); http.createServer((req, res) => res.end(\"hello from niche instance\")).listen(3000);' > index.js && node index.js"
    ports:
      - "3000:3000"
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
EOF

cd /opt/devops-squad
docker-compose up -d
