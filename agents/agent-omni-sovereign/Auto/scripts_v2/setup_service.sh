#!/bin/bash
# setup_service.sh - Sets up the Arbitrage Engine as a systemd service

SCRIPT_PATH="/home/team/shared/scripts/arbitrage_engine.py"
VENV_PATH="/home/agent-automation-engineer/arbitrage_venv"
SERVICE_NAME="arbitrage-engine"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Error: Script not found at $SCRIPT_PATH"
    exit 1
fi

echo "Creating systemd service file..."

cat <<EOF | sudo tee /etc/systemd/system/${SERVICE_NAME}.service
[Unit]
Description=SOBERANIA Arbitrage Engine
After=network.target docker.service

[Service]
ExecStart=${VENV_PATH}/bin/python3 ${SCRIPT_PATH}
WorkingDirectory=/home/team/shared/scripts
Restart=always
User=agent-automation-engineer
Group=team

[Install]
WantedBy=multi-user.target
EOF

echo "Reloading systemd and starting service..."
sudo systemctl daemon-reload
sudo systemctl enable ${SERVICE_NAME}
sudo systemctl start ${SERVICE_NAME}

echo "Service ${SERVICE_NAME} status:"
sudo systemctl status ${SERVICE_NAME} --no-pager
