import json
import subprocess
import time
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

PORT = 5001
NECROMANCY_SCRIPT = "/home/agent-infrastructure-engineer/empire-infrastructure/scripts/lucrative_necromancy.py"

class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)

        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] Received alert from Alertmanager")
        
        alerts = data.get('alerts', [])
        for alert in alerts:
            alert_name = alert.get('labels', {}).get('alertname')
            severity = alert.get('labels', {}).get('severity')
            status = alert.get('status')

            print(f"Alert: {alert_name}, Severity: {severity}, Status: {status}")

            if status == 'firing' and alert_name in ['GlobalAssetAvailabilityBreach', 'MarginIntegrityBreach']:
                self.trigger_self_healing(alert_name)

        self.send_response(200)
        self.end_headers()

    def trigger_self_healing(self, alert_name):
        print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] TRIGGERING SELF-HEALING for {alert_name}")
        
        # 1. Run Lucrative Necromancy
        try:
            print(f"Running {NECROMANCY_SCRIPT}...")
            result = subprocess.run(["python3", NECROMANCY_SCRIPT], capture_output=True, text=True)
            print(result.stdout)
        except Exception as e:
            print(f"Error running necromancy: {e}")

        # 2. Trigger Spacelift Reconciliation (Simulated)
        print("Triggering Spacelift Reconciliation for all affected stacks...")
        # In a real environment, this would be: 
        # spacelift stack trigger --id <stack-id>
        # For now, we log the intent as per the architecture design
        with open("/home/team/shared/spacelift_reconciliation.log", "a") as f:
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] RECONCILIATION TRIGGERED by {alert_name}\n")

        print("Self-healing sequence completed.")

def run(server_class=HTTPServer, handler_class=WebhookHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Starting Incident Responder on port {PORT}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
