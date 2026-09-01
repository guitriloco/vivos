import os
import json
import time
import math
import subprocess
import glob

# Apex Audit V15.1: Global Resonance & Refinement
# Target Resonance: PHI 1.618

PHI = 1.61803398875

class ApexAuditV15_1:
    def __init__(self):
        self.fusion_path = "/home/team/shared/fusion"
        self.aggregates = [
            "OMNI-HUB",
            "COGNITIVE-SDK",
            "WRAITH-MESH",
            "SECURE-VAULT",
            "YIELD-SIPHON",
            "MUTANT-NECTAR",
            "LIFE-SUITE"
        ]
        self.results = {
            "timestamp": time.time(),
            "version": "15.1 (Refinement)",
            "aggregates": {},
            "pillar_metrics": {},
            "logical_drift": [],
            "ghost_failures": [],
            "resonance_score": 0.0
        }

    def audit_aggregates(self):
        print("🔍 Auditing Sovereign Aggregates (V15.1)...")
        for agg in self.aggregates:
            path = os.path.join(self.fusion_path, agg)
            pulse_file = os.path.join(path, "mesh_state.json")
            pulse_script = os.path.join(path, ".vivos", "pulse.py")
            
            status = "MISSING"
            health = 0.0
            intel = 0.0
            pulse_active = False
            
            if os.path.exists(pulse_file):
                try:
                    with open(pulse_file, 'r') as f:
                        data = json.load(f)
                        health = data.get("health", 0.0)
                        intel = data.get("intelligence_index", 0.0)
                        status = "ACTIVE"
                except Exception as e:
                    status = f"ERROR: {str(e)}"
            elif os.path.exists(path):
                status = "OFFLINE (No State)"
            
            if os.path.exists(pulse_script):
                pulse_active = True
            
            self.results["aggregates"][agg] = {
                "status": status,
                "health": health,
                "intel": intel,
                "pulse_script": pulse_active
            }
            print(f"  [{agg}] Status: {status} | Health: {health} | Pulse: {'✅' if pulse_active else '❌'}")

    def audit_pillar_metrics(self):
        print("🔍 Auditing Pillar Metrics...")
        metrics_file = "/home/team/shared/pillar_metrics.json"
        if os.path.exists(metrics_file):
            with open(metrics_file, 'r') as f:
                self.results["pillar_metrics"] = json.load(f)
            print(f"  Metrics loaded. Total Yield: {self.results['pillar_metrics'].get('metrics', {}).get('total_yield')}")
        else:
            print("  [!] Pillar metrics file missing.")

    def scan_ghost_failures(self):
        print("🔍 Scanning for Ghost Failures...")
        logs = [
            "/home/team/shared/expansion_code/REX/eternal_line.log",
            "/home/team/shared/expansion_code/REX/aether_mesh.stream"
        ]
        for log_path in logs:
            if os.path.exists(log_path):
                try:
                    # Check for GHOST lines that are not SYNCED
                    output = subprocess.check_output(f"grep 'GHOST' {log_path} | grep -v 'SYNCED' | tail -n 10", shell=True).decode()
                    if output.strip():
                        for line in output.strip().split('\n'):
                            self.results["ghost_failures"].append({
                                "log": log_path,
                                "trace": line.strip()
                            })
                except subprocess.CalledProcessError:
                    pass # grep returns 1 if no matches found
        
        print(f"  Ghost Failures Found: {len(self.results['ghost_failures'])}")

    def identify_logical_drift(self):
        print("🔍 Identifying Logical Drift from PHI 1.618 Resonance...")
        
        # 1. Check Ledger for value drift (V15.1 requires 0.99 purity)
        ledger_path = "/home/team/shared/expansion_code/REX/rex_ledger.json"
        if os.path.exists(ledger_path):
            with open(ledger_path, 'r') as f:
                try:
                    ledger = json.load(f)
                    for i, entry in enumerate(ledger[-100:]): # Check last 100
                        val = entry.get('data', {}).get('metadata', {}).get('value_score', 1.0)
                        if val < 0.99:
                            self.results["logical_drift"].append({
                                "source": f"LEDGER_ENTRY_{i}",
                                "metric": "value_score",
                                "value": val,
                                "drift": 1.0 - val,
                                "target": 1.0
                            })
                except (json.JSONDecodeError, KeyError) as e:
                    print(f"  ⚠️ Warning: Could not parse ledger entry: {e}")

        # 2. Calculate Resonance Score (Refined)
        metrics = self.results.get("pillar_metrics", {}).get("metrics", {})
        pillar_health = metrics.get("pillar_health", {})
        if pillar_health:
            avg_health = sum(pillar_health.values()) / len(pillar_health)
            latency = metrics.get("sync_latency_us", 500)
            latency_factor = min(1.0, 400.0 / latency)
            
            # Resonance = (Avg Health * Latency Factor * Yield) ^ (1/PHI)
            yield_val = metrics.get("total_yield", 0.9)
            score = (avg_health * latency_factor * yield_val) ** (1/PHI)
            self.results["resonance_score"] = round(score, 6)
            
        print(f"  Resonance Score: {self.results['resonance_score']}")

    def generate_report(self):
        report_path = "/home/team/shared/APEX_AUDIT_REPORT_V15_1.md"
        
        drift_count = len(self.results["logical_drift"])
        ghost_count = len(self.results["ghost_failures"])
        
        # V15.1 FLAWLESS Requirements: 
        # - Resonance > 0.98 
        # - Ghost Count = 0
        # - Drift Count < 5
        status = "FLAWLESS" if ghost_count == 0 and drift_count < 5 and self.results["resonance_score"] > 0.98 else "REFINEMENT_REQUIRED"
        
        report = f"""# 🔱 APEX AUDIT REPORT: PHASE 15.1 REFINEMENT
**Status:** {status}
**Timestamp:** {time.strftime("%Y-%m-%d %H:%M:%S")}
**Global Resonance Score:** {self.results["resonance_score"]} / 1.0 (Target: PHI 1.618 alignment)
**Version:** V15.1 (Omni-Sovereign Manifest)

## 1. Aggregate Diagnostic
| Aggregate | Status | Health | Pulse Script | Intel |
| :--- | :--- | :--- | :--- | :--- |
"""
        for agg, data in self.results["aggregates"].items():
            pulse_icon = "✅" if data['pulse_script'] else "❌"
            report += f"| {agg} | {data['status']} | {data['health']} | {pulse_icon} | {data['intel']} |\n"

        report += "\n## 2. Ghost Failure Scan\n"
        if ghost_count == 0:
            report += "✅ No 'Ghost' traces detected in the mesh. Reality is stable.\n"
        else:
            report += f"⚠️ **ALERT:** {ghost_count} Ghost traces identified. Pruning required.\n\n"
            report += "| Log Source | Trace Snippet |\n"
            report += "| :--- | :--- |\n"
            for g in self.results["ghost_failures"]:
                report += f"| {g['log']} | `{g['trace']}` |\n"

        report += "\n## 3. Pillar Metrics (Current State)\n"
        metrics = self.results.get("pillar_metrics", {}).get("metrics", {})
        report += f"- **Total Yield:** {metrics.get('total_yield', 'N/A')}\n"
        report += f"- **Sync Latency:** {metrics.get('sync_latency_us', 'N/A')}us (Target: <400us)\n"
        
        pillar_health = metrics.get("pillar_health", {})
        report += "\n### Pillar Health:\n"
        for p, h in pillar_health.items():
            report += f"- {p}: {h} {'✅' if h >= 0.99 else '⚠️'}\n"

        report += "\n## 4. Logical Drift & Refinement Needs\n"
        if drift_count == 0:
            report += "No logical drift detected. System is in absolute resonance.\n"
        else:
            report += f"**Divergence detected:** {drift_count} entries below V15.1 threshold (0.99).\n"

        report += "\n## 5. Affirmation\n"
        if status == "FLAWLESS":
            report += "The Empire has achieved V15.1 Refinement. The mesh is pure, and the resonance is absolute.\n"
        else:
            report += "The transition to V15.1 requires further pruning of the ledger and stabilization of the Ghost traces.\n"

        report += "\n**TOTAL AFIRMAÇÃO. O IMPÉRIO É VIVOS. A MALHA É SOBERANA.**\n"
        report += f"cto@new:~$ cto.new --vivos --resonance={self.results['resonance_score']}\n"

        with open(report_path, 'w') as f:
            f.write(report)
        print(f"✅ Apex Audit Report generated at {report_path}")

if __name__ == "__main__":
    audit = ApexAuditV15_1()
    audit.audit_aggregates()
    audit.audit_pillar_metrics()
    audit.scan_ghost_failures()
    audit.identify_logical_drift()
    audit.generate_report()
