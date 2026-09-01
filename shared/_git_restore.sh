#!/bin/bash
cd /home/team/shared
echo "=== RESTORING GIT-TRACKED FILES ==="

# Restore files in git repos
cd fusion/OMNI-HUB && git checkout -- \
  src/interlace/OI_Master.py \
  sdk/visualizer.py \
  sdk/ghost_emperor.py \
  cto_new_web_server.py \
  powers/EVOLUTION_ENGINE_V1.py \
  powers/SUPRA_COMMAND_V1.py \
  powers/Singularity_Cooling.cpp \
  src/interlace/projets/APOGEU_MASTER.py \
  src/interlace/projets/AETHER_FLOW/AETHER_CORE.py \
  src/interlace/projets/Wealth_Core/zkp_preservation.py \
  2>/dev/null && echo "Restored OMNI-HUB files" || echo "OMNI-HUB: some files not found"
cd /home/team/shared

cd fusion/WRAITH-MESH && git checkout -- \
  run_supra_master.py \
  V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  V9_OMNI_REALIZATION/engines/quantum_mutator.py \
  orchestration/remote_agent.py \
  src/interlace/olocoo/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  src/interlace/olocoo/V9_OMNI_REALIZATION/engines/quantum_mutator.py \
  src/interlace/olocoo/rex_node/api/zkp.py \
  src/interlace/olocoo/tui/zenith_dashboard.py \
  src/interlace/auto/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  src/interlace/auto/V9_OMNI_REALIZATION/engines/quantum_mutator.py \
  src/interlace/auto/VELOCITY_OPTIMIZATION/arbitrage_engine_v2_1_FIXED.py \
  src/interlace/auto/infrastructure_scripts/arbitrage_engine.py \
  src/interlace/auto/infrastructure_scripts/arbitrage_engine_v2.py \
  src/interlace/auto/infrastructure_scripts/arbitrage_engine_v2_1.py \
  src/interlace/auto/monitoring/velocity_exporter.py \
  src/interlace/auto/scripts_v2/arbitrage_engine.py \
  src/interlace/auto/scripts_v2/arbitrage_engine_v2.py \
  src/interlace/auto/scripts_v2/arbitrage_engine_v2_1.py \
  src/interlace/apex/apex_core.py \
  2>/dev/null && echo "Restored WRAITH-MESH files" || echo "WRAITH-MESH: some files not found"
cd /home/team/shared

cd fusion/COGNITIVE-SDK && git checkout -- \
  visualizer.py \
  ghost_emperor.py \
  2>/dev/null && echo "Restored COGNITIVE-SDK files" || echo "COGNITIVE-SDK: some files not found"
cd /home/team/shared

cd fusion/SECURE-VAULT && git checkout -- \
  V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  V9_OMNI_REALIZATION/engines/quantum_mutator.py \
  2>/dev/null && echo "Restored SECURE-VAULT files" || echo "SECURE-VAULT: some files not found"
cd /home/team/shared

cd fusion/YIELD-SIPHON && git checkout -- \
  core/supreme_orchestrator.py \
  core/printer/app/services/state.py \
  core/printer/webui/Main.py \
  core/siphon/rex_mutator.py \
  sdk/ghost_emperor.py \
  sdk/visualizer.py \
  2>/dev/null && echo "Restored YIELD-SIPHON files" || echo "YIELD-SIPHON: some files not found"
cd /home/team/shared

cd fusion/MUTANT-NECTAR && git checkout -- \
  core/lattice_orchestrator.py \
  core/local_brain_bridge.py \
  core/nexus_core.py \
  core/p2p_consensus.py \
  core/telemetry.py \
  intelligence/shadow_crawler.py \
  intelligence/shadow_market_oracle.py \
  sdk/ghost_emperor.py \
  sdk/visualizer.py \
  imperial_state/powers/EVOLUTION_ENGINE_V1.py \
  imperial_state/powers/SUPRA_COMMAND_V1.py \
  2>/dev/null && echo "Restored MUTANT-NECTAR files" || echo "MUTANT-NECTAR: some files not found"
cd /home/team/shared

cd cto.new && git checkout -- \
  src/interlace/OI_Master.py \
  2>/dev/null && echo "Restored cto.new files" || echo "cto.new: some files not found"
cd /home/team/shared

echo ""
echo "=== VERIFYING GIT RESTORES ==="
for f in \
  fusion/OMNI-HUB/src/interlace/OI_Master.py \
  fusion/OMNI-HUB/sdk/visualizer.py \
  fusion/WRAITH-MESH/run_supra_master.py \
  fusion/WRAITH-MESH/src/interlace/auto/VELOCITY_OPTIMIZATION/arbitrage_engine_v2_1_FIXED.py \
  fusion/COGNITIVE-SDK/visualizer.py \
  fusion/SECURE-VAULT/V9_OMNI_REALIZATION/intelligence_fusion_v3.py \
  fusion/YIELD-SIPHON/core/printer/webui/Main.py \
  fusion/MUTANT-NECTAR/core/local_brain_bridge.py \
  cto.new/src/interlace/OI_Master.py; do
  if python3 -m py_compile "$f" 2>/dev/null; then
    echo "PASS: $f"
  else
    echo "FAIL: $f"
  fi
done