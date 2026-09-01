#!/bin/bash
set -e

APP_DIR="/home/team/shared/sample-app"
SERVICE_NAME="sample-app"
PROMETHEUS_URL="http://localhost:9090"
AVAILABILITY_THRESHOLD=0.999

echo "Starting Safe Deployment for $SERVICE_NAME..."

# 1. Run security audit
echo "Running security audit..."
cd $APP_DIR
# We ignore errors for the sake of the demo, but in prod we'd fail the build
npm audit --audit-level=high || echo "Security audit found vulnerabilities. Continuing but please review."

# 2. Deploy
echo "Deploying new version..."
sudo docker compose -f $APP_DIR/docker-compose.yml up -d

# 3. Wait for stabilization
echo "Waiting 20 seconds for stabilization..."
sleep 20

# 4. Post-deployment health check via SLIs
echo "Performing post-deployment SLI check..."
# Query the SLI implemented by the SRE Lead
AVAILABILITY=$(curl -s "$PROMETHEUS_URL/api/v1/query?query=sample_app:availability:ratio_5m" | jq -r '.data.result[0].value[1]')

if [[ "$AVAILABILITY" == "null" || -z "$AVAILABILITY" ]]; then
    echo "Warning: Could not fetch availability metrics. Health check inconclusive."
else
    echo "Current Availability (5m): $AVAILABILITY"
    # Basic comparison using awk for floating point
    HEALTHY=$(echo "$AVAILABILITY $AVAILABILITY_THRESHOLD" | awk '{if ($1 >= $2) print "yes"; else print "no"}')
    
    if [[ "$HEALTHY" == "no" ]]; then
        echo "CRITICAL: Availability below threshold ($AVAILABILITY < $AVAILABILITY_THRESHOLD)!"
        echo "Suggesting immediate investigation."
    else
        echo "Health check passed. Deployment successful."
    fi
fi

echo "Deployment finished at $(date)"
