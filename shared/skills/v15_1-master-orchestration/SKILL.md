---
name: v15_1-master-orchestration
description: Deploy and run the VIVOS V15.1 Sovereign Master Loop — integrates distilled nectars into a self-evolving autonomous control loop with PHI 1.618 resonance.
---

# V15.1 Master Orchestration Loop

## Overview
The V15.1 Sovereign Master Loop is the singular autonomous control loop that integrates all 7 Supreme Aggregates (OMNI-HUB, COGNITIVE-SDK, WRAITH-MESH, SECURE-VAULT, YIELD-SIPHON, MUTANT-NECTAR, LIFE-SUITE) with the distilled atomic nectars from `/home/team/shared/v15_1_distilled_nectars/`.

## Procedure

### 1. Activate the Master Loop
```bash
cd /home/team/shared/v15_1_master_logic

# Single execution
python3 V15_1_SOVEREIGN_LOOP.py --mode=SINGLE

# Continuous self-evolving loop (recommended)
python3 V15_1_SOVEREIGN_LOOP.py --mode=CONTINUOUS --iterations=5 --interval=1.5

# Or use the deployment script
bash DEPLOY_V15_1.sh single
bash DEPLOY_V15_1.sh continuous 5 1.5
```

### 2. Verify the State
```bash
# Read the master state
python3 V15_1_SOVEREIGN_LOOP.py --mode=STATE

# Or check the exported state
cat /home/team/shared/V15_1_MASTER_STATE.json
```

### 3. Integration with Distilled Nectars
The loop imports atomic functions from:
- `/home/team/shared/v15_1_distilled_nectars/lib/resonance.py` — PHI lattice alignment
- `/home/team/shared/v15_1_distilled_nectars/lib/stealth.py` — Chameleon-II signatures
- `/home/team/shared/v15_1_distilled_nectars/lib/siphon.py` — Negative latency streaming
- `/home/team/shared/v15_1_distilled_nectars/lib/ledger.py` — Purity-based pruning

### 4. Architecture
The loop executes 6 phases:
- **Phase I**: Initialization — verifies all 7 aggregates and templates
- **Phase II**: Synchronization — zero-latency cross-pillar sync
- **Phase II.5**: Nectar Flow — stealth, siphon, and ledger operations
- **Phase III**: Resonance Analysis — PHI lattice alignment (nectar-enhanced)
- **Phase IV**: Yield Manifestation — marketplace ROI calculation
- **Phase V**: Evolution & Mutation — self-evolving parameter optimization
- **Phase VI**: State Vaulting — causal trace logging and state persistence

### 5. Key Files
| File | Purpose |
|------|---------|
| `V15_1_SOVEREIGN_LOOP.py` | Main sovereign loop orchestrator |
| `NECTAR_INTEGRATION_V15_1.py` | Integration layer for distilled nectars |
| `MASTER_MANIFEST_V15_1.json` | System manifest with KPIs |
| `DEPLOY_V15_1.sh` | Deployment command script |
| `MASTER_STATE_V15_1.json` | Latest master state snapshot |

## Gotchas
- The loop expects aggregates in `/home/team/shared/fusion/` with 7 directories
- Marketplace template JSONs should be in `/home/team/shared/vivos_v15_templates/`
- If nectars are unavailable, the loop falls back to the built-in resonance engine
- Rust compiler is optional — the Sovereign Core functions are ported to Python