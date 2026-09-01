---
name: empire-runtime-audit
description: Systematic static syntax + runtime execution audit for VIVOS Empire scripts across Python, C++, and Rust.
---

# Empire Runtime Audit Protocol

## When to use
When performing FASE B2-style reverse engineering to verify scripts actually work at runtime.

## Procedure

### 1. Find all scripts
```bash
find /path -maxdepth 5 -type f \( -name "*.py" -o -name "*.sh" -o -name "*.rs" -o -name "*.cpp" \) | grep -v __pycache__ | grep -v node_modules | grep -v .git | sort
```

### 2. Static syntax check (Python)
```bash
for f in $(find /path -name "*.py" ! -path "*__pycache__*"); do
  python3 -m py_compile "$f" 2>&1 || echo "FAIL: $f"
done
```

### 3. Runtime execution test
Create batch script with timeout. Exit codes:
- 0 = ✅ PASS
- 1 + "Usage:" = expected (needs args)
- 124 = ⏰ TIMEOUT (has active loop)
- Other = ❌ FAIL (real bug)

### 4. Check compiled binaries
```bash
file <binary>    # verify ELF
timeout 2 ./<binary>  # test execution
```

### 5. Document findings
Report: pass rate, critical issues (permission errors, latency, divergences), recommendations.

### Gotchas
- Permission-denied across user dirs = env config, not code bug
- Scripts with CLI args exit(1) — expected
- Simulation loops timeout — use longer timeouts