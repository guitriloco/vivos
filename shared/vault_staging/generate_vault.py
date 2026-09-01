#!/usr/bin/env python3
"""
⚜️ VAULT STAGING — TOTAL DUMP SEQUENCE ⚜️
Generates /agent_blueprints, /environment_state, /logs from live source data.
"""

import json, os, shutil, subprocess, platform, sys, time
from datetime import datetime

VAULT = "/home/team/shared/vault_staging"
os.makedirs(f"{VAULT}/agent_blueprints", exist_ok=True)
os.makedirs(f"{VAULT}/environment_state", exist_ok=True)
os.makedirs(f"{VAULT}/logs", exist_ok=True)

def sql(query):
    try:
        r = subprocess.run(["team-db", query], capture_output=True, text=True, timeout=15)
        if r.returncode == 0 and r.stdout.strip():
            return json.loads(r.stdout)
        return []
    except: return []

print("=" * 60)
print("🔱 VAULT STAGING — TOTAL DUMP")
print("=" * 60)

# ─── 1. AGENT BLUEPRINTS ───
print("\n📋 /agent_blueprints ...")
agents = sql("SELECT id, role, capabilities FROM agents")
d = {"agent_count": len(agents), "agents": agents}
with open(f"{VAULT}/agent_blueprints/AGENT_ROSTER_MASTER.json", "w") as f:
    json.dump(d, f, indent=2)

tasks = sql("SELECT id, title, assigned_to, status FROM tasks")
by_agent = {}
for t in tasks:
    a = t.get("assigned_to", "unassigned")
    by_agent.setdefault(a, []).append(t)

agent_dna = {}
for a, at in sorted(by_agent.items()):
    agent_dna[a] = {
        "agent_id": a,
        "task_count": len(at),
        "completed": sum(1 for x in at if x["status"] == "done"),
        "in_progress": sum(1 for x in at if x["status"] == "in-progress"),
        "in_review": sum(1 for x in at if x["status"] == "review"),
        "tasks": at
    }
with open(f"{VAULT}/agent_blueprints/AGENT_BEHAVIORAL_DNA.json", "w") as f:
    json.dump(agent_dna, f, indent=2)

mt = sql("SELECT id, title, assigned_to, status, result FROM tasks WHERE assigned_to IN ('agent-master-orchestrator','agent-nectar-synthesizer')")
with open(f"{VAULT}/agent_blueprints/MASTER_NECTAR_DNA.json", "w") as f:
    json.dump({"task_count": len(mt), "tasks": mt}, f, indent=2)

print(f"   ✅ {len(agents)} agents, {len(tasks)} tasks, {len(mt)} master+nectar tasks")

# ─── 2. ENVIRONMENT STATE ───
print("\n📋 /environment_state ...")

# 2a. Env snapshot
env = {
    "snapshot_timestamp": datetime.now().isoformat(),
    "host": {"node": platform.node(), "platform": platform.platform(), "python": sys.version, "machine": platform.machine()},
    "environment": dict(sorted(os.environ.items())),
    "python_path": sys.path
}
try:
    r = subprocess.run(["pip", "freeze", "--local"], capture_output=True, text=True, timeout=10)
    env["pip_packages"] = r.stdout.strip().split("\n") if r.stdout else []
except: env["pip_packages"] = []
with open(f"{VAULT}/environment_state/ENV_SNAPSHOT.json", "w") as f:
    json.dump(env, f, indent=2)

# 2b. Filesystem
targets = ["v15_1_master_logic", "v15_1_distilled_nectars", "fusion", "powers", "nectars", "vivos_v15_templates", "skills"]
fs = {}
for t in targets:
    p = f"/home/team/shared/{t}"
    if os.path.exists(p):
        entries = []
        for root, dirs, files in os.walk(p):
            for fname in files:
                fp = os.path.join(root, fname)
                try:
                    st = os.stat(fp)
                    entries.append({"path": fp, "size": st.st_size, "modified": datetime.fromtimestamp(st.st_mtime).isoformat()})
                except Exception as e:
                    print(f"  ⚠️ Warning: Could not stat {fp}: {e}")
        fs[t] = {"entry_count": len(entries), "total_size_bytes": sum(e["size"] for e in entries)}
with open(f"{VAULT}/environment_state/FILESYSTEM_STATE.json", "w") as f:
    json.dump(fs, f, indent=2)

# 2c. Config
config = sql("SELECT key, value FROM config")
with open(f"{VAULT}/environment_state/CONFIG_STATE.json", "w") as f:
    json.dump({"config": config}, f, indent=2)

# 2d. Git
git_info = {}
try:
    r = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True, timeout=5, cwd="/home/team/shared")
    git_info["remotes"] = r.stdout.strip().split("\n") if r.stdout else []
except: git_info["remotes"] = []
with open(f"{VAULT}/environment_state/GIT_STATE.json", "w") as f:
    json.dump(git_info, f, indent=2)

# 2e. System info
sys_info = {
    "platform": platform.platform(), "python": sys.version,
    "machine": platform.machine(), "hostname": platform.node(),
    "timestamp": datetime.now().isoformat()
}
try:
    with open("/proc/meminfo") as f:
        mem = {}
        for line in f:
            parts = line.split(":")
            if len(parts) == 2:
                mem[parts[0].strip()] = parts[1].strip()
        sys_info["memory"] = {k: mem[k] for k in ["MemTotal", "MemFree", "MemAvailable"] if k in mem}
except: sys_info["memory"] = "N/A"
with open(f"{VAULT}/environment_state/SYSTEM_INFO.json", "w") as f:
    json.dump(sys_info, f, indent=2)

env_size = sum(os.path.getsize(f"{VAULT}/environment_state/{f}") for f in os.listdir(f"{VAULT}/environment_state") if os.path.isfile(f"{VAULT}/environment_state/{f}"))
print(f"   ✅ 5 files, {env_size:,} total bytes")

# ─── 3. LOGS ───
print("\n📋 /logs ...")
log_count = 0
logs_dir = f"{VAULT}/logs"

# V15.1 sovereign loop logs
loop_logs = [
    "/home/team/shared/v15_1_master_logic/CAUSAL_TRACE_V15_1.json",
    "/home/team/shared/v15_1_master_logic/MASTER_STATE_V15_1.json",
    "/home/team/shared/v15_1_master_logic/EVOLUTION_CODEX_V15_1.json",
    "/home/team/shared/v15_1_master_logic/MARKETPLACE_YIELD_V15_1.json",
    "/home/team/shared/V15_1_MASTER_STATE.json",
    "/home/team/shared/v15_1_master_logic/MASTER_MANIFEST_V15_1.json",
]
for sp in loop_logs:
    if os.path.exists(sp):
        name = f"OPERATIONAL_{os.path.basename(sp)}"
        shutil.copy2(sp, f"{logs_dir}/{name}")
        log_count += 1

# Historical logs
hist_logs = [
    "/home/team/shared/powers/memory_nexus_db.json",
    "/home/team/shared/SUPRA_COMMAND_LOG.json",
    "/home/team/shared/SINGULARITY_GOLD_REGISTRY.log",
    "/home/team/shared/supra_codex.json",
    "/home/team/shared/neural_resonance_pool.json",
    "/home/team/shared/pillar_metrics.json",
]
for sp in hist_logs:
    if os.path.exists(sp):
        name = f"HISTORICAL_{os.path.basename(sp)}"
        shutil.copy2(sp, f"{logs_dir}/{name}")
        log_count += 1

# Suite logs from vivos_aether
for sp in ["/home/team/shared/v15_1_master_logic/vivos_aether_mesh.log", "/home/team/shared/v15_1_master_logic/vivos_apex.mesh"]:
    if os.path.exists(sp):
        shutil.copy2(sp, f"{logs_dir}/MESH_{os.path.basename(sp)}")
        log_count += 1

# Nectar core_code logs
nectar_logs = ["/home/team/shared/v15_1_distilled_nectars/README.md"]
for sp in nectar_logs:
    if os.path.exists(sp):
        shutil.copy2(sp, f"{logs_dir}/NECTAR_{os.path.basename(sp)}")
        log_count += 1

print(f"   ✅ {log_count} log files collected")

# ─── FINAL SUMMARY ───
print("\n" + "=" * 60)
print("🔱 VAULT STAGING — TOTAL DUMP COMPLETE")
for d in ["agent_blueprints", "environment_state", "logs", "core_code"]:
    p = f"{VAULT}/{d}"
    if os.path.exists(p):
        files = [f for f in os.listdir(p) if os.path.isfile(f"{p}/{f}") or os.path.isdir(f"{p}/{f}")]
        sz = sum(os.path.getsize(f"{p}/{f}") for f in os.listdir(p) if os.path.isfile(f"{p}/{f}"))
        print(f"   📁 {d}/: {len(files)} entries, {sz:,} bytes")
    else:
        print(f"   ⚠️ {d}/: MISSING")
print("TOTAL AFIRMAÇÃO. THE VAULT IS SEALED.")
