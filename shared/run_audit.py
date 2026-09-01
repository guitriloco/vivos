#!/usr/bin/env python3
"""Comprehensive Empire Code Audit - Phase 17"""
import subprocess, os, sys, re, json
from pathlib import Path

BASE = "/home/team/shared"
errors = []
warnings = []

def log(cat, fpath, sev, msg):
    rel = os.path.relpath(fpath, BASE)
    entry = {"category": cat, "file": rel, "severity": sev, "message": msg}
    errors.append(entry)
    print(f"  [{sev}] {cat}: {rel}")
def log_warn(cat, fpath, sev, msg):
    rel = os.path.relpath(fpath, BASE)
    entry = {"category": cat, "file": rel, "severity": sev, "message": msg}
    warnings.append(entry)
    print(f"  [{sev}] {cat}: {rel}")

# Collect files
py_files = []
cpp_files = []
rs_files = []
sh_files = []

for root, dirs, files in os.walk(BASE):
    if '.git' in root or '__pycache__' in root:
        continue
    for f in files:
        fp = os.path.join(root, f)
if f.endswith('.py'): py_files.append(fp)
        elif f.endswith('.cpp'): cpp_files.append(fp)
        elif f.endswith('.rs'): rs_files.append(fp)
        elif f.endswith('.sh'): sh_files.append(fp)

print(f"Found: {len(py_files)} .py, {len(cpp_files)} .cpp, {len(rs_files)} .rs, {len(sh_files)} .sh")

# === PHASE 1: Python Syntax ===
print("\n=== PHASE 1: Python Syntax Check ===")
for fp in py_files:
    try:
        res = subprocess.run(['python3', '-m', 'py_compile', fp], capture_output=True, text=True, timeout=10)
if res.returncode != 0:
            lines = [l for l in res.stderr.split('\n')
if l.strip()]
            msg = lines[-2] if len(lines) >= 2 else lines[-1] if lines else "Syntax error"
            log("PYTHON_SYNTAX", fp, "CRITICAL", msg)
    except subprocess.TimeoutExpired:
        log("PYTHON_SYNTAX", fp, "HIGH", "Timed out during syntax check")
    except Exception as e:
        log("PYTHON_CHECK", fp, "HIGH", str(e))

# === PHASE 2: Check for specific code issues ===
print("\n=== PHASE 2: Code Quality Analysis ===")
for fp in py_files:
    try:
        with open(fp, 'r') as f:
            content = f.read()
            lines = content.split('\n')
    except:
        continue
    
    # Check for bare except
    for i, line in enumerate(lines):
        if 'except:' in line and 'Exception' not in line:
            log_warn("BARE_EXCEPT", fp, "MEDIUM", f"Line {i+1}: bare 'except:' without exception type")
if re.search(r'password\s*=|secret\s*=|api_key\s*=|token\s*=[\'\"][^\*]', line, re.I):
            log_warn("HARDCODED_SECRET", fp, "HIGH", f"Line {i+1}: possible secret hardcoded: {line.strip()[:60]}")
if 'import subprocess' in line and 'shell=True' in content:
            log_warn("SHELL_INJECTION", fp, "HIGH", f"File uses subprocess with shell=True (potential risk)")
    
    # Check for dead code (functions defined but never called within the file)
    funcs = re.findall(r'def (\w+)\(', content)
if len(funcs) > 3:
        for fn in funcs:
            # Count calls
            calls = content.count(fn + '(')
if calls <= 1 and fn not in ['__init__', 'main']:
                log_warn("POSSIBLE_DEAD_CODE", fp, "LOW", f"Function '{fn}' defined but may never be called")

# === PHASE 3: C++ Syntax Check ===
print("\n=== PHASE 3: C++ Syntax Check ===")
for fp in cpp_files:
    try:
        res = subprocess.run(['g++', '-fsyntax-only', '-std=c++17', fp], 
                           capture_output=True, text=True, timeout=30)
if res.returncode != 0:
            lines = [l for l in res.stderr.split('\n')
if l.strip()]
            msg = lines[-1] if lines else "Compile error"
            log("CPP_SYNTAX", fp, "CRITICAL", msg)
    except Exception as e:
        log("CPP_CHECK", fp, "HIGH", str(e))

# Check for OpenSSL dependency (Immutability_Seal_V7.cpp uses openssl/sha.h)
for fp in cpp_files:
    try:
        with open(fp, 'r') as f:
            content = f.read()
if '#include <openssl/sha.h>' in content:
            log_warn("CPP_DEPENDENCY", fp, "MEDIUM", "Requires OpenSSL development library (libssl-dev)")
if 'std::this_thread::sleep_for' in content:
            log_warn("CPP_LATENCY", fp, "MEDIUM", "Contains sleep_for() - may affect latency targets (0.368μs)")
    except Exception as e:
        print(f"WARNING: {e}")# === PHASE 4: Cross-pillar compatibility ===
        print("\n=== PHASE 4: Cross-Pillar Compatibility ===")
for fp in py_files:
    try:
        with open(fp, 'r') as f:
            content = f.read()
    except:
        continue
    
    # Check for imports of modules that may not exist
    imports = re.findall(r'^import (\w+)|^from (\w+)', content, re.MULTILINE)
for imp in imports:
        mod = imp[0] or imp[1]
        if mod.startswith('cto_new') and os.path.dirname(fp) != os.path.dirname(os.path.join(BASE, 'cto.new')):
            log_warn("CROSS_IMPORT", fp, "MEDIUM", f"Import of '{mod}' may resolve differently across directories")

# === PHASE 5: Git repo status ===
print("\n=== PHASE 5: Git Repository Status ===")
git_dirs = []
for root, dirs, files in os.walk(BASE):
    if '.git' in dirs:
        git_dirs.append(root)
for gd in git_dirs:
    try:
        res = subprocess.run(['git', '-C', gd, 'status', '--short'], 
                           capture_output=True, text=True, timeout=10)
if res.stdout.strip():
            log("GIT_DIRTY", gd, "LOW", f"Uncommitted changes:\n{res.stdout.strip()[:200]}")
    except Exception as e:
        print(f"WARNING: {e}")# === PHASE 6: Shell script check ===
        print("\n=== PHASE 6: Shell Script Analysis ===")
for fp in sh_files:
    try:
        with open(fp, 'r') as f:
            content = f.read()
if '#!/bin/bash' not in content and '#!/bin/sh' not in content:
            log_warn("SHELL_SHEBANG", fp, "MEDIUM", "Missing shebang line")
        lines = content.split('\n')
for i, line in enumerate(lines):
            if line.strip().startswith('rm -rf') and not line.strip().endswith('/*'):
                log_warn("DANGEROUS_RM", fp, "HIGH", f"Line {i+1}: dangerous rm -rf: {line.strip()}")
    except Exception as e:
        print(f"WARNING: {e}")# === PHASE 7: Known issues from previous runtime ===
        print("\n=== PHASE 7: Runtime Analysis ===")
# Check if lattice_resonance_v5.cpp in cto.new has sleep_for (latency issue)
for fp in [os.path.join(BASE, "cto.new/Lattice_Resonance_V5.cpp")]:
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            content = f.read()
if 'sleep_for' in content:
            log("LATENCY_ISSUE", fp, "HIGH", 
                "Contains std::this_thread::sleep_for(std::chrono::milliseconds(10)) - "
                "10ms sleep blocks the 0.368μs latency target")

# Check the void_stream_siphon.py for the typo we fixed
for fp in [os.path.join(BASE, "void_stream_siphon.py")]:
    if os.path.exists(fp):
        with open(fp, 'r') as f:
            content = f.read()
if 'shiphoned_data' in content:
            log("TYPO", fp, "HIGH", "Variable 'shiphoned_data' (typo) - should be 'siphoned_data'")

# === REPORT GENERATION ===
print("\n" + "="*70)
print("  COMPREHENSIVE AUDIT REPORT")
print("="*70)
print(f"\n  Total Errors: {len(errors)}")
print(f"  Total Warnings: {len(warnings)}")
print(f"\n  Files Scanned: {len(py_files)} py + {len(cpp_files)} cpp + {len(rs_files)} rs + {len(sh_files)} sh")

# Generate markdown report
md = f"""# ⚜️ VIVOS EMPIRE AUDIT REPORT — PHASE 17 ⚜️
## Auditoria Completa de Erros & Correção

**Date:** {subprocess.run(['date'], capture_output=True, text=True).stdout.strip()}
**Files Scanned:** {len(py_files)} Python + {len(cpp_files)} C++ + {len(rs_files)} Rust + {len(sh_files)} Shell
**Total Errors:** {len(errors)} | **Total Warnings:** {len(warnings)}

---

## 🔴 CRITICAL ERRORS ({len([e for e in errors if e['severity'] == 'CRITICAL'])})
"""
for e in errors:
    if e['severity'] == 'CRITICAL':
        md += f"\n### {e['category']}: `{e['file']}`\n**Severity:** {e['severity']}\n**Message:** {e['message']}\n"

md += f"\n## 🟠 HIGH SEVERITY ({len([e for e in errors if e['severity'] == 'HIGH'])} + {len([w for w in warnings if w['severity'] == 'HIGH'])} warnings)\n"
for e in errors:
    if e['severity'] == 'HIGH':
        md += f"\n### {e['category']}: `{e['file']}`\n**Message:** {e['message']}\n"
for w in warnings:
    if w['severity'] == 'HIGH':
        md += f"\n### {w['category']}: `{w['file']}`\n**Message:** {w['message']}\n"

md += f"\n## 🟡 MEDIUM SEVERITY\n"
for w in warnings:
    if w['severity'] == 'MEDIUM':
        md += f"\n### {w['category']}: `{w['file']}`\n**Message:** {w['message']}\n"

md += f"\n## 🔵 LOW SEVERITY\n"
for e in errors:
    if e['severity'] == 'LOW':
        md += f"\n### {e['category']}: `{e['file']}`\n**Message:** {e['message']}\n"
for w in warnings:
    if w['severity'] == 'LOW':
        md += f"\n### {w['category']}: `{w['file']}`\n**Message:** {w['message']}\n"

md += """
---

## 📋 PLANO DE CORREÇÃO (Prioritário)

### Priority 1 — 🚨 CRITICAL (Corrigir imediatamente)
1. Fix all Python syntax errors found above
2. Fix all C++ compilation errors found above

### Priority 2 — ⚠️ HIGH (Corrigir na sequência)
1. Remove hardcoded secrets from source files → move to env vars
2. Fix bare except: statements → add specific exception types
3. Remove or guard dangerous shell commands (rm -rf)
4. Fix latency-blocking sleep_for() calls in performance-critical paths

### Priority 3 — 🔧 MEDIUM (Corrigir quando possível)
1. Add shebang lines to shell scripts missing them
2. Install missing dependencies (OpenSSL dev libs for SHA-512)
3. Review cross-module import paths for consistency
4. Address sleep_for latency issues in non-critical paths

### Priority 4 — 🧹 LOW (Refatoração futura)
1. Investigate and remove dead code (unused functions)
2. Commit/rebase git repositories with uncommitted changes
3. Review variable naming consistency (typo fixes)

---

## 📊 ESTIMATIVA DE ESFORÇO

| Priority | Items | Est. Effort | Complexity |
|----------|-------|-------------|------------|
| CRITICAL | Syntax fixes | 1-2 hours | Low (mechanical) |
| HIGH | Security/logic fixes | 2-4 hours | Medium |
| MEDIUM | Dependency/config | 1-3 hours | Low-Medium |
| LOW | Cleanup/refactor | 2-4 hours | Low |
| **TOTAL** | **All items** | **6-13 hours** | **Various** |

---

*Generated by Sovereign Integrator — Phase 17 Audit Protocol*
*Total Affirmation. The Line is Straight.*
"""

report_path = os.path.join(BASE, "AUDIT_ERROR_REPORT.md")
with open(report_path, 'w') as f:
    f.write(md)
print(f"\n✅ Report written to {report_path}")
print(f"\n{'='*70}")
print(f"  ✅ AUDIT COMPLETE — {len(errors)} errors, {len(warnings)} warnings")
print(f"  Report: {report_path}")
print(f"{'='*70}")