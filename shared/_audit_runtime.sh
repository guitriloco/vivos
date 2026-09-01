#!/bin/bash
cd /home/team/shared
echo "================================================"
echo "  RUNTIME AUDIT — FASE B2 ENGENHARIA REVERSA"
echo "================================================"
echo ""

run_test() {
  local script=$1
  local timeout=$2
  echo "--- TEST: $script ---"
  timeout $timeout python3 "$script" 2>&1
  local code=$?
  echo "EXIT CODE: $code"
  if [ $code -eq 0 ]; then echo "RESULT: ✅ PASS"; else echo "RESULT: ❌ FAIL"; fi
  echo ""
}

# Test 1: STABILIZE_V15_1
run_test "STABILIZE_V15_1.py" 5

# Test 2: sovereign_terminal.py
run_test "sovereign_terminal.py" 5

# Test 3: generate_causal_log.py
run_test "generate_causal_log.py" 5

# Test 4: log_nectar.py
run_test "log_nectar.py" 5

# Test 5: void_stream_siphon.py
run_test "void_stream_siphon.py" 5

# Test 6: jogada_de_mestre.py  
run_test "jogada_de_mestre.py" 5

echo "=== RUNTIME AUDIT COMPLETE ==="