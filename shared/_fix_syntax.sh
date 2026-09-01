#!/bin/bash
cd /home/team/shared
echo "=== FIXING MASS-REWRITE REGEX DAMAGE ==="
total=0
pass=0
fail=0

for f in \
  expansion_code/SUPRA/intelligence_fusion_v3.py \
  interlace_matrix/src/interlace/OI_Master.py \
  cto.new/src/interlace/OI_Master.py \
  fusion/OMNI-HUB/src/interlace/OI_Master.py \
  fusion/WRAITH-MESH/run_supra_master.py \
  fusion/WRAITH-MESH/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  fusion/WRAITH-MESH/src/interlace/olocoo/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  fusion/WRAITH-MESH/src/interlace/auto/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  fusion/WRAITH-MESH/src/interlace/auto/VELOCITY_OPTIMIZATION/arbitrage_engine_v2_1_FIXED.py \
  fusion/SECURE-VAULT/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  fusion/YIELD-SIPHON/core/printer/webui/Main.py \
  fusion/MUTANT-NECTAR/core/local_brain_bridge.py \
  fusion/MUTANT-NECTAR/core/telemetry.py \
  fusion/MUTANT-NECTAR/imperial_state/powers/EVOLUTION_ENGINE_V1.py \
  fusion/MUTANT-NECTAR/imperial_state/powers/SUPRA_COMMAND_V1.py \
  v15_1_master_logic/V15_1_SOVEREIGN_LOOP.py; do
  
  total=$((total+1))
  if [ -f "$f" ]; then
    python3 -m py_compile "$f" 2>/dev/null
    if [ $? -eq 0 ]; then
      echo "PASS: $f"
      pass=$((pass+1))
    else
      echo "FAIL: $f -- fixing..."
      # Fix: the regex merged lines — restore newlines before def/class/for
      sed -i 's/")def /")\ndef /g; s/")class /")\nclass /g; s/")for /")\nfor /g; s/")async /")\nasync /g; s/")while /")\nwhile /g' "$f"
      python3 -m py_compile "$f" 2>/dev/null
      if [ $? -eq 0 ]; then
        echo "  -> FIXED: $f"
        pass=$((pass+1))
      else
        echo "  -> STILL FAILS: $f"
        fail=$((fail+1))
      fi
    fi
  fi
done

echo ""
echo "SUMMARY: $total checked | $pass pass | $fail fail"