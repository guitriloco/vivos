import requests
import time
import os
import json

VAULT_URL = "http://localhost:8010"
LOG_FILE = "/home/team/shared/vvv/security_audit.log"

def audit_vault():
    print(f"[{time.ctime()}] Starting Security Audit...")
    try:
        # 1. Check Pulse
        pulse_resp = requests.get(f"{VAULT_URL}/vault/pulse")
        pulse_resp.raise_for_status()
        pulse = pulse_resp.json()
        
        status = pulse.get("status")
        integrity = pulse.get("integrity_score")
        
        log_msg = f"[{time.ctime()}] Pulse: {status} | Integrity: {integrity} | Entries: {pulse.get('total_sealed_entries')}\n"
        
        if status != "STABLE" or integrity < 1.0:
            log_msg += f"!!! ALERT: System integrity compromised! Corrupted entries detected: {pulse.get('corrupted_entries')}\n"
            
        # 2. Deep Integrity Scan
        scan_resp = requests.get(f"{VAULT_URL}/vault/verify_integrity")
        scan_resp.raise_for_status()
        scan = scan_resp.json()
        
        log_msg += f"[{time.ctime()}] Deep Scan: {json.dumps(scan.get('ledger_integrity'))}\n"
        
        print(log_msg)
        with open(LOG_FILE, "a") as f:
            f.write(log_msg)
            
    except Exception as e:
        err_msg = f"[{time.ctime()}] AUDIT FAILED: {str(e)}\n"
        print(err_msg)
        with open(LOG_FILE, "a") as f:
            f.write(err_msg)

if __name__ == "__main__":
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    while True:
        audit_vault()
        time.sleep(60) # Poll every minute
