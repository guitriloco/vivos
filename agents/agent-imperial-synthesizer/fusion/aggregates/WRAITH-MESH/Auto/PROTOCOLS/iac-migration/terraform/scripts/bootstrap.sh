#!/bin/bash
set -e

# Update and install dependencies
apt-get update
apt-get install -y apt-transport-https ca-certificates curl software-properties-common gnupg-agent

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
      bash -c "echo 'hello from brutal scale' > index.js && node index.js"
    ports:
      - "3000:3000"
  node-exporter:
    image: prom/node-exporter:latest
    ports:
      - "9100:9100"
EOF

cd /opt/devops-squad
docker-compose up -d
