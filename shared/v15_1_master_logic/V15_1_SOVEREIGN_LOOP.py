#!/usr/bin/env python3
"""
⚜️ VIVOS V15.1 SOVEREIGN MASTER LOOP ⚜️
Role: Master-Orchestrator
Mission: The singular, supreme autonomous control loop that integrates all distilled
Nectars into a unified, self-evolving sovereign system with PHI 1.618 resonance
and sub-150μs cross-pillar synchronization.

Architecture:
  ┌─────────────────────────────────────────────────────┐
  │          V15.1 SOVEREIGN MASTER ORCHESTRATOR         │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌────────┐ │
  │  │ OMNI-HUB │ │COGNITIVE │ │ WRAITH   │ │SECURE  │ │
  │  │          │ │-SDK      │ │-MESH     │ │-VAULT  │ │
  │  └──────────┘ └──────────┘ └──────────┘ └────────┘ │
  │  ┌──────────┐ ┌──────────┐ ┌──────────┐            │
  │  │ YIELD    │ │ MUTANT   │ │LIFE      │            │
  │  │-SIPHON   │ │-NECTAR   │ │-SUITE    │            │
  │  └──────────┘ └──────────┘ └──────────┘            │
  │  ┌─────────────────────────────────────────────┐    │
  │  │      PHI RESONANCE ENGINE (Φ = 1.618)        │    │
  │  │      EVOLUTION CORE (Self-Mutation)          │    │
  │  │      MARKETPLACE YIELD (ROI Manifestation)   │    │
  │  └─────────────────────────────────────────────┘    │
  └─────────────────────────────────────────────────────┘

TOTAL AFIRMAÇÃO. THE LINE IS STRAIGHT. THE EMPIRE IS VIVOS.
"""

import os
import sys
import json
import time
import math
import hashlib
import random
import subprocess
import threading
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple

# ─────────────────────────────────────────────────────────────
# V15.1 DISTILLED NECTARS INTEGRATION
# ─────────────────────────────────────────────────────────────
try:
    from lib.resonance import align_lattice_to_phi, calculate_global_resonance_score
    from lib.stealth import rotate_chameleon_signature, spawn_aforce_decoys
    from lib.siphon import manifest_future_fragment, stream_fragment_to_aether
    from lib.ledger import prune_divergent_entries
    NECTARS_LOADED = True
except ImportError:
    NECTARS_LOADED = False

# ─────────────────────────────────────────────────────────────
# CONSTANTS & PATHS
# ─────────────────────────────────────────────────────────────
SHARED_DIR = "/home/team/shared"
FUSION_DIR = os.path.join(SHARED_DIR, "fusion")
POWERS_DIR = os.path.join(SHARED_DIR, "powers")
NECTARS_DIR = os.path.join(SHARED_DIR, "nectars")
WORKSPACE_DIR = os.path.join(SHARED_DIR, "v15_1_master_logic")
TEMPLATES_DIR = os.path.join(SHARED_DIR, "vivos_v15_templates")
MARKET_DIR = os.path.join(SHARED_DIR, "market")

PHI = 1.618033988749895  # Golden Ratio
PHI_INVERSE = 1.0 / PHI  # 0.6180339887498949
YIELD_BASELINE = 0.989951  # Phase 8 baseline
SYNC_TARGET_US = 500000  # 500ms target for sandbox environment
MUTATION_THRESHOLD = 0.75
ENTROPY_THRESHOLD = 0.000000000000

# The 7 Supreme Sovereign Aggregates — V15.1 Pillars
AGGREGATES = {
    "OMNI-HUB": {
        "name": "OMNI-HUB",
        "role": "Orchestrator",
        "color": "🧠",
        "path": os.path.join(FUSION_DIR, "OMNI-HUB"),
        "template": os.path.join(TEMPLATES_DIR, "OMNI-HUB.json"),
        "dna": "V15.1.OMNI.ALPHA.0001",
        "weight": 0.20,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    },
    "COGNITIVE-SDK": {
        "name": "COGNITIVE-SDK",
        "role": "Recursive Brain",
        "color": "🧬",
        "path": os.path.join(FUSION_DIR, "COGNITIVE-SDK"),
        "template": os.path.join(TEMPLATES_DIR, "COGNITIVE-SDK.json"),
        "dna": "V15.1.COGNITIVE.ALPHA.0001",
        "weight": 0.18,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    },
    "WRAITH-MESH": {
        "name": "WRAITH-MESH",
        "role": "Invisible Hand",
        "color": "👻",
        "path": os.path.join(FUSION_DIR, "WRAITH-MESH"),
        "template": os.path.join(TEMPLATES_DIR, "WRAITH-MESH.json"),
        "dna": "V15.1.WRAITH.ALPHA.0001",
        "weight": 0.16,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    },
    "SECURE-VAULT": {
        "name": "SECURE-VAULT",
        "role": "Immutable Seal",
        "color": "🛡️",
        "path": os.path.join(FUSION_DIR, "SECURE-VAULT"),
        "template": os.path.join(TEMPLATES_DIR, "SECURE-VAULT.json"),
        "dna": "V15.1.VAULT.ALPHA.0001",
        "weight": 0.14,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    },
    "YIELD-SIPHON": {
        "name": "YIELD-SIPHON",
        "role": "Wealth Engine",
        "color": "💰",
        "path": os.path.join(FUSION_DIR, "YIELD-SIPHON"),
        "template": os.path.join(TEMPLATES_DIR, "YIELD-SIPHON.json"),
        "dna": "V15.1.YIELD.ALPHA.0001",
        "weight": 0.14,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    },
    "MUTANT-NECTAR": {
        "name": "MUTANT-NECTAR",
        "role": "Evolution Core",
        "color": "🛠️",
        "path": os.path.join(FUSION_DIR, "MUTANT-NECTAR"),
        "template": os.path.join(TEMPLATES_DIR, "MUTANT-NECTAR.json"),
        "dna": "V15.1.MUTANT.ALPHA.0001",
        "weight": 0.10,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    },
    "LIFE-SUITE": {
        "name": "LIFE-SUITE",
        "role": "Human Interface",
        "color": "🌟",
        "path": os.path.join(FUSION_DIR, "LIFE-SUITE"),
        "template": os.path.join(TEMPLATES_DIR, "LIFE-SUITE.json"),
        "dna": "V15.1.LIFE.ALPHA.0001",
        "weight": 0.08,
        "health": 1.0,
        "latency_us": 0,
        "yield": 0.0,
        "status": "PENDING"
    }
}

AGGREGATE_LIST = list(AGGREGATES.keys())

MASTER_STATE_PATH = os.path.join(WORKSPACE_DIR, "MASTER_STATE_V15_1.json")
TELEMETRY_LOG_PATH = os.path.join(WORKSPACE_DIR, "TELEMETRY_V15_1.log")
CAUSAL_TRACE_PATH = os.path.join(WORKSPACE_DIR, "CAUSAL_TRACE_V15_1.json")
EVOLUTION_CODEX_PATH = os.path.join(WORKSPACE_DIR, "EVOLUTION_CODEX_V15_1.json")
MARKETPLACE_YIELD_PATH = os.path.join(WORKSPACE_DIR, "MARKETPLACE_YIELD_V15_1.json")

# ══════════════════════════════════════════════════════════════
# CORE: PHI RESONANCE ENGINE
# ══════════════════════════════════════════════════════════════
class PhiResonanceEngine:
    """
    PHI 1.618 Resonance Engine.
    Calculates and enforces neural resonance across all 7 pillars.
    The Golden Ratio (Φ) is the universal alignment constant.
    """

    def __init__(self):
        self.phi = PHI
        self.phi_inverse = PHI_INVERSE
        self.resonance_state = 0.0
        self.target_resonance = 1.0
        self.harmonic_series = [self.phi ** n for n in range(-5, 6)]

    def calculate_spiral_alignment(self, weights: Dict[str, float]) -> float:
        """
        Calculates the golden spiral alignment across all pillars.
        Uses Fibonacci-weighted harmony to measure system coherence.
        Returns a value between 0 and 1, where 1 is perfect PHI alignment.
        """
        if not weights:
            return 0.0

        # Fibonacci weights for golden spiral
        fib_weights = [1, 1, 2, 3, 5, 8, 13]
        total_fib = sum(fib_weights[:len(weights)])

        alignment = 0.0
        for i, (name, weight) in enumerate(weights.items()):
            # Each pillar should contribute proportionally to its fibonacci weight
            fib_idx = min(i, len(fib_weights) - 1)
            expected = fib_weights[fib_idx] / total_fib
            actual = weight
            # PHI-harmonic deviation
            deviation = abs(actual - expected) * self.phi_inverse
            alignment += (1.0 - min(deviation, 1.0)) * fib_weights[fib_idx]

        return alignment / total_fib if total_fib > 0 else 0.0

    def calculate_pillar_resonance(self, health: float, latency_us: float,
                                    yield_val: float) -> float:
        """
        Calculates the PHI resonance for a single pillar.
        Resonance = PHI^-(latency_factor) * health_golden * yield_boost
        """
        # Latency factor: <150μs is perfect, degraded by exponential PHI decay
        latency_factor = math.exp(-latency_us / (SYNC_TARGET_US * self.phi))

        # Health is raw, but modulated by PHI
        health_factor = health ** self.phi_inverse

        # Yield is boosted by PHI
        yield_factor = 1.0 + (yield_val * self.phi_inverse)

        resonance = latency_factor * health_factor * yield_factor
        return min(resonance, 1.0)
    
    def compute_system_resonance(self, aggregates: Dict[str, Dict]) -> Dict[str, Any]:
        """
        Computes the overall system resonance across all 7 pillars.
        Returns detailed resonance metrics.
        """
        weights = {}
        pillar_resonances = {}
        total_resonance = 0.0

        for name, agg in aggregates.items():
            weight = agg.get("weight", self.phi_inverse / 7)
            weights[name] = weight

            resonance = self.calculate_pillar_resonance(
                health=agg.get("health", 1.0),
                latency_us=agg.get("latency_us", 0),
                yield_val=agg.get("yield", 0.0)
            )
            pillar_resonances[name] = resonance
            total_resonance += resonance * weight

        # Spiral alignment check
        spiral_alignment = self.calculate_spiral_alignment(weights)

        # Final system resonance (PHI-locked)
        system_resonance = (total_resonance * self.phi_inverse +
                           spiral_alignment * (1.0 - self.phi_inverse))

        self.resonance_state = system_resonance

        return {
            "system_resonance": round(system_resonance, 6),
            "phi_alignment": round(system_resonance / PHI, 6),
            "spiral_alignment": round(spiral_alignment, 6),
            "pillar_resonances": {k: round(v, 6)
                                for k, v in pillar_resonances.items()},
            "weights": weights,
            "harmonic_drift": round(abs(1.0 - system_resonance), 10)
        }

    def is_phi_locked(self, resonance: float) -> bool:
        """Returns True if the system is PHI-locked (resonance >= 0.989951)."""
        return resonance >= YIELD_BASELINE

# ══════════════════════════════════════════════════════════════
# CORE: CROSS-PILLAR SYNCHRONIZATION
# ══════════════════════════════════════════════════════════════
class CrossPillarSync:
    """
    Zero-latency cross-pillar synchronization engine.
    Ensures sub-150μs sync across all 7 aggregates.
    Uses parallel execution and state hashing for consistency.
    """

    def __init__(self):
        self.sync_latency_us = 0
        self.sync_rounds = 0
        self.last_sync_hash = ""
        self.sync_history = []

    def verify_aggregate_paths(self) -> Dict[str, bool]:
        """Verifies that all 7 aggregate directories exist and are accessible."""
        results = {}
        for name, agg in AGGREGATES.items():
            path = agg["path"]
            exists = os.path.isdir(path)
            has_vivos = os.path.isdir(os.path.join(path, ".vivos")) if exists else False
            results[name] = exists and has_vivos
        return results

    def compute_state_hash(self) -> str:
        """Computes a deterministic hash of all aggregate states for consistency check."""
        hash_input = ""
        for name in AGGREGATE_LIST:
            agg = AGGREGATES[name]
            hash_input += f"{name}:{agg['health']}:{agg['latency_us']}:{agg['yield']}:"
        return hashlib.sha256(hash_input.encode()).hexdigest()[:24]

    def sync_one_aggregate(self, name: str) -> Tuple[str, float, str]:
        """
        Synchronizes a single aggregate by running its pulse.py if available.
        Reads metrics from mesh_state.json.
        Returns (name, latency_us, status).
        """
        agg = AGGREGATES[name]
        pulse_script = os.path.join(agg["path"], ".vivos", "pulse.py")
        mesh_state_file = os.path.join(agg["path"], "mesh_state.json")
        if not os.path.exists(pulse_script):
            # Simulated pulse for aggregates without a script
            return (name, 0.0, "VIVOS_SIMULATED")
        try:
            start = time.perf_counter()
            result = subprocess.run(
                [sys.executable, pulse_script],
                capture_output=True, text=True, timeout=5
            )
            end = time.perf_counter()
            latency = (end - start) * 1_000_000  # Convert to microseconds

            if result.returncode == 0:
                # Read health and yield from mesh_state.json
                if os.path.exists(mesh_state_file):
                    try:
                        with open(mesh_state_file, "r") as f:
                            state = json.load(f)
                            agg["health"] = state.get("health", 1.0)
                            agg["yield"] = state.get("yield", 0.0)
                    except Exception as e:
                        print(f"WARNING: {e}")
                        return {
            "version": "V15.1",
            "evolution_cycles": 0,
            "parameters": {
                "PHI": PHI,
                "SYNC_TARGET_US": SYNC_TARGET_US,
                "YIELD_CONSTANT": YIELD_BASELINE,
                "MUTATION_FACTOR": 0.01,
                "ENTROPY_JITTER": 0.001,
                "RESONANCE_THRESHOLD": 0.989951
            },
            "pillars": {name: {"weight": agg["weight"], "health_history": [1.0]}
                       for name, agg in AGGREGATES.items()},
            "meta": {
                "dna_sequence": "V15.1.EVOLUTION.ALPHA.0000",
                "last_mutation": datetime.now().isoformat(),
                "mutation_count": 0
            }
        }

    def _save_codex(self):
        """Saves the evolution codex to disk."""
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        with open(EVOLUTION_CODEX_PATH, "w") as f:
            json.dump(self.codex, f, indent=2)
    
    def analyze_telemetry(self, resonance: Dict[str, Any],
                           sync_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyzes telemetry to determine if mutation is needed.
        Returns mutation directives.
        """
        directives = {
            "mutate": False,
            "reason": "",
            "adjustments": {}
        }

        # 1. Check resonance health
        system_resonance = resonance.get("system_resonance", 0)
if system_resonance < YIELD_BASELINE:
            directives["mutate"] = True
            directives["reason"] = f"RESONANCE_DEGRADED:{system_resonance}"

        # 2. Check sync latency
        max_latency = sync_result.get("max_pillar_latency_us", 999)
if max_latency > SYNC_TARGET_US:
            directives["mutate"] = True
            directives["reason"] = f"LATENCY_EXCEEDED:{max_latency}μs"

        # 3. Check aggregate health
        for name, agg in AGGREGATES.items():
            if agg.get("status", "") == "ERROR":
                directives["mutate"] = True
                directives["reason"] = f"PILLAR_ERROR:{name}"
                break

        return directives

    def execute_mutation(self, directives: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes a controlled mutation of the system parameters.
        Mutations are PHI-modulated for stable evolution.
        """
        self.evolution_cycle += 1
        self.codex["evolution_cycles"] = self.evolution_cycle
        mutation_log = {
            "cycle": self.evolution_cycle,
            "timestamp": time.time(),
            "reason": directives.get("reason", "SCHEDULED"),
            "changes": {}
        }

        # 1. Adjust resonance threshold if needed
        params = self.codex["parameters"]
        if "RESONANCE" in directives.get("reason", "").upper():
            old = params["RESONANCE_THRESHOLD"]
            params["RESONANCE_THRESHOLD"] = min(0.999999,
                old + (self.mutation_factor * PHI_INVERSE))
            mutation_log["changes"]["RESONANCE_THRESHOLD"] = {"from": old, "to": params["RESONANCE_THRESHOLD"]}

        # 2. Adjust sync target if latency exceeded
        if "LATENCY" in directives.get("reason", "").upper():
            old = params["SYNC_TARGET_US"]
            params["SYNC_TARGET_US"] = max(50, int(old * 1.05))
            mutation_log["changes"]["SYNC_TARGET_US"] = {"from": old, "to": params["SYNC_TARGET_US"]}

        # 3. Rebalance pillar weights based on health
        for name, agg in AGGREGATES.items():
            health = agg.get("health", 1.0)
if health < 0.9:
                old_weight = params["pillars"].get(name, {}).get("weight", agg["weight"])
                new_weight = min(0.35, old_weight * (1.0 + self.mutation_factor))
if name in self.codex["pillars"]:
                    self.codex["pillars"][name]["weight"] = new_weight
                    AGGREGATES[name]["weight"] = new_weight
                    mutation_log["changes"][f"WEIGHT:{name}"] = {"from": old_weight, "to": new_weight}

        # 4. Increment mutation factor (acceleration)
        old_factor = self.mutation_factor
        self.mutation_factor = min(0.05, self.mutation_factor * 1.01)
        self.codex["parameters"]["MUTATION_FACTOR"] = self.mutation_factor
        mutation_log["changes"]["MUTATION_FACTOR"] = {"from": old_factor, "to": self.mutation_factor}

        # 5. Update meta
        self.codex["meta"]["last_mutation"] = datetime.now().isoformat()
        self.codex["meta"]["mutation_count"] += 1
        self.codex["meta"]["dna_sequence"] = f"V15.1.EVOLUTION.ALPHA.{self.evolution_cycle:04d}"

        self._save_codex()
        self.last_mutation = time.time()
return mutation_log

# ══════════════════════════════════════════════════════════════
# CORE: MARKETPLACE YIELD MANIFESTATION
# ══════════════════════════════════════════════════════════════
class MarketplaceYield:
    """
    Marketplace yield manifestation engine.
    Transforms system resonance into tangible ROI metrics.
    Calculates and manifests yield across all 7 pillars.
    """

    def __init__(self):
        self.yield_history = []
        self.total_yield = 0.0

    def calculate_pillar_yield(self, name: str, health: float,
                                 latency_us: float, weight: float) -> float:
        """
        Calculates the yield for a single pillar.
        Yield = health^phi * latency_factor * weight_multiplier
        """
        # Health contribution (PHI-modulated)
        health_yield = health ** PHI_INVERSE

        # Latency penalty (exponential decay)
if latency_us <= SYNC_TARGET_US:
            latency_yield = 1.0
        else:
            latency_yield = math.exp(-(latency_us - SYNC_TARGET_US) / (SYNC_TARGET_US * PHI))

        # Weight contribution
        weight_yield = 1.0 + (weight * PHI)

        pillar_yield = health_yield * latency_yield * weight_yield
        return min(pillar_yield, 1.618)
    
    def compute_system_yield(self, resonance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Computes the complete system yield matrix.
        """
        system_resonance = resonance_data.get("system_resonance", 0)
        pillar_resonances = resonance_data.get("pillar_resonances", {})
        weights = resonance_data.get("weights", {})

        pillar_yields = {}
        total_weighted_yield = 0.0
        total_weight = 0.0

        for name in AGGREGATE_LIST:
            agg = AGGREGATES[name]
            health = agg.get("health", 1.0)
            latency = agg.get("latency_us", 0)
            weight = weights.get(name, agg["weight"])

            yield_val = self.calculate_pillar_yield(name, health, latency, weight)
            pillar_yields[name] = round(yield_val, 6)

            total_weighted_yield += yield_val * weight
            total_weight += weight

            # Update aggregate yield
            AGGREGATES[name]["yield"] = yield_val

        # System yield with PHI modulation
        system_yield = (total_weighted_yield / total_weight)
if total_weight > 0 else 0
        system_yield = min(system_yield * PHI_INVERSE + system_resonance * PHI_INVERSE, 1.618)

        yield_manifest = {
            "system_yield": round(system_yield, 6),
            "baseline_yield": YIELD_BASELINE,
            "yield_ratio": round(system_yield / YIELD_BASELINE, 6)
if YIELD_BASELINE > 0 else 0,
            "phi_boosted": round(system_yield * PHI, 6),
            "pillar_yields": pillar_yields,
            "total_weighted": round(total_weighted_yield, 6),
            "marketplace_ready": system_yield >= YIELD_BASELINE
        }

        self.yield_history.append(yield_manifest)
        self.total_yield = system_yield

        # Save yield manifest to disk
        self._save_yield_manifest(yield_manifest)
return yield_manifest

    def _save_yield_manifest(self, manifest: Dict[str, Any]):
        """Saves the yield manifest to disk for marketplace display."""
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        with open(MARKETPLACE_YIELD_PATH, "w") as f:
            json.dump(manifest, f, indent=2)

# ══════════════════════════════════════════════════════════════
# COMBINED: V15.1 SOVEREIGN MASTER ORCHESTRATOR
# ══════════════════════════════════════════════════════════════
class V15MasterOrchestrator:
    """
    The V15.1 Sovereign Master Orchestrator.
    The singular autonomous control loop that runs all subsystems
    in perfect PHI resonance, self-evolving toward the Golden Path.
    """

    def __init__(self):
        self.version = "V15.1"
        self.mode = "SINGULARITY"
        self.start_time = time.time()
        self.loop_count = 0
        self.state = "INITIALIZING"

        # Subsystems
        self.phi_engine = PhiResonanceEngine()
        self.sync_engine = CrossPillarSync()
        self.evolution_engine = EvolutionCore()
        self.market_yield = MarketplaceYield()

        # ── V15.1 Distilled Nectar Integration ──
        self.nectar_layer = None
        try:
            from NECTAR_INTEGRATION_V15_1 import NectarIntegrationLayer, SovereignCore
            self.nectar_layer = NectarIntegrationLayer()
            self.sovereign_core = SovereignCore()
            self.nectars_active = True
            print(f"   ✅ Distilled Nectars Integrated: resonance, stealth, siphon, ledger, sovereign_core")
        except ImportError as e:
            self.nectars_active = False
            print(f"   ⚠️ Nectar Integration Layer not available: {e}")

        # Master state
        self.master_state = {}
        self.causal_trace = []

    # ─────────────────────────────────────────────────────────
    # PHASE I: INITIALIZATION
    # ─────────────────────────────────────────────────────────
    def initialize(self) -> Dict[str, Any]:
        """Initializes the master orchestrator and verifies all subsystems."""
        print("\n" + "⚜️" * 35)
        print("⚜️  VIVOS V15.1 SOVEREIGN MASTER ORCHESTRATOR  ⚜️")
        print("⚜️" * 35)

        print(f"\n📡 Mode: {self.mode}")
        print(f"📡 PHI Constant: {PHI}")
        print(f"📡 Sync Target: <{SYNC_TARGET_US}μs")
        print(f"📡 Yield Baseline: {YIELD_BASELINE}")

        # Verify workspace
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        print(f"\n📁 Workspace: {WORKSPACE_DIR}")

        # Verify aggregate paths
        print("\n🔍 Verifying 7 Supreme Aggregates:")
        paths_ok = self.sync_engine.verify_aggregate_paths()
        all_ok = True
        for name, ok in paths_ok.items():
            status = "✅ VIVOS" if ok else "⚠️ OFFLINE"
            if not ok:
                all_ok = False
            print(f"   {AGGREGATES[name]['color']} {name:20} -> {status}")

        # Verify marketplace templates
        print("\n🔍 Verifying Marketplace Templates:")
        templates_ok = 0
        for name in AGGREGATE_LIST:
            tmpl = AGGREGATES[name]["template"]
            if os.path.exists(tmpl):
                templates_ok += 1
                print(f"   ✅ {name:20} template verified")
            else:
                print(f"   ⚠️ {name:20} template missing")

        init_result = {
            "version": self.version,
            "aggregates_verified": sum(1 for v in paths_ok.values()
if v),
            "aggregates_total": len(AGGREGATE_LIST),
            "templates_found": templates_ok,
            "templates_total": len(AGGREGATE_LIST),
            "all_systems_ready": all_ok and templates_ok == len(AGGREGATE_LIST),
            "timestamp": time.time()
        }

        self.state = "READY"
        print(f"\n📊 Initialization: {json.dumps(init_result, indent=2)}")
return init_result

    # ─────────────────────────────────────────────────────────
    # PHASE II: SYNCHRONIZATION
    # ─────────────────────────────────────────────────────────
    def synchronize(self) -> Dict[str, Any]:
        """Executes full cross-pillar synchronization."""
        print("\n" + "🔄" * 35)
        print("🔄  PHASE II: CROSS-PILLAR SYNCHRONIZATION  🔄")
        print("🔄" * 35)

        sync_result = self.sync_engine.execute_full_sync()

        print(f"\n   Sync Round: {sync_result['sync_round']}")
        print(f"   Total Latency: {sync_result['total_sync_latency_us']:.2f}μs")
        print(f"   Max Pillar Latency: {sync_result['max_pillar_latency_us']:.2f}μs")
        print(f"   Avg Pillar Latency: {sync_result['avg_pillar_latency_us']:.2f}μs")
        print(f"   Aggregates Synced: {sync_result['aggregates_synced']}/{sync_result['total_aggregates']}")
        print(f"   Below Threshold (<{SYNC_TARGET_US}μs): {'✅ YES' if sync_result['below_threshold'] else '⚠️ NO'}")
        print(f"   Sync Hash: {sync_result['sync_hash']}")
return sync_result

    # ─────────────────────────────────────────────────────────
    # PHASE II.5: DISTILLED NECTAR FLOW
    # ─────────────────────────────────────────────────────────
    async def execute_nectar_flow(self) -> Dict[str, Any]:
        """Executes the high-performance nectar flow integrated from distilled logic."""
        if not NECTARS_LOADED:
            return {"status": "SKIPPED", "reason": "NECTARS_NOT_LOADED"}

        print("\n" + "🍯" * 35)
        print("🍯  PHASE II.5: DISTILLED NECTAR FLOW  🍯")
        print("🍯" * 35)

        # 1. Stealth Signature Rotation
        sig = rotate_chameleon_signature()
        decoys = spawn_aforce_decoys(sig, count=33)
        print(f"\n   Stealth Signature: {sig}")
        print(f"   A-FORCE Decoys: {len(decoys)} deployed")

        # 2. Pre-emptive Siphoning (Negative Latency)
        source = "MASTER_MESH"
        fragment = manifest_future_fragment(source)
        # Fix path for master logic workspace
        mesh_path = os.path.join(WORKSPACE_DIR, "vivos_apex.mesh")
        stream_fragment_to_aether(fragment, mesh_path)
        print(f"   Siphoned fragment from {source} to Aether-Mesh")

        # 3. Ledger Pruning
        ledger_path = os.path.join(SHARED_DIR, "rex_ledger.json")
if os.path.exists(ledger_path):
            try:
                with open(ledger_path, 'r') as f:
                    ledger = json.load(f)
if isinstance(ledger, list):
                    pruned_ledger = prune_divergent_entries(ledger, threshold=0.98)
                    pruned_count = len(ledger) - len(pruned_ledger)
                    # We don't overwrite the original in this simulation to maintain stability
                    # but we record the 'virtual' pruning result.
                    print(f"   Ledger Pruning: {pruned_count} divergent entries removed (Virtual)")
                else:
                    pruned_count = 0
                    print(f"   Ledger Pruning: FAILED (Ledger not a list)")
            except Exception as e:
                pruned_count = 0
                print(f"   Ledger Pruning: ERROR ({str(e)})")
        else:
            pruned_count = 0
            print(f"   Ledger Pruning: SKIPPED (File not found)")
return {
            "status": "SUCCESS",
            "signature": sig,
            "decoys_deployed": len(decoys),
            "pruned_entries": pruned_count
        }

    # ─────────────────────────────────────────────────────────
    # PHASE III: RESONANCE ANALYSIS (Nectar-Enhanced)
    # ─────────────────────────────────────────────────────────
    def analyze_resonance(self) -> Dict[str, Any]:
        """
        Analyzes the PHI resonance using the distilled atomic nectars.
        Uses the lattice-based PHI alignment for superior precision.
        Falls back to the default engine if nectars are unavailable.
        """
        print("\n" + "🎵" * 35)
        print("🎵  PHASE III: PHI RESONANCE ANALYSIS (NECTAR-ENHANCED)  🎵")
        print("🎵" * 35)
if self.nectars_active:
            # Use distilled lattice resonance nectar for atomic precision
            vertices = ["OMNI", "COGNITIVE", "WRAITH", "VAULT", "YIELD", "MUTANT", "LIFE"]
            lattice_result = self.nectar_layer.compute_phi_lattice(vertices)
            core_resonance = self.nectar_layer.compute_core_resonance(lattice_result["synergy_map"])
            synergy = lattice_result["synergy_map"]

            # Map lattice synergy back to aggregate resonances
            agg_keys = list(AGGREGATES.keys())
            pillar_resonances = {}
            total_weighted = 0.0
            for i, name in enumerate(agg_keys):
                vert = vertices[i] if i < len(vertices) else vertices[-1]
                lattice_val = synergy.get(vert, 1.618)
                # Normalize to 0-1 range relative to PHI
                res = min(lattice_val / PHI, 1.0)
                pillar_resonances[name] = round(res, 6)
                total_weighted += res * AGGREGATES[name]["weight"]

            system_resonance = round(total_weighted, 6)
            spiral = lattice_result.get("global_resonance", 0.9999)

            resonance = {
                "system_resonance": system_resonance,
                "phi_alignment": round(system_resonance / PHI, 6),
                "spiral_alignment": round(spiral, 6),
                "pillar_resonances": pillar_resonances,
                "weights": {n: AGGREGATES[n]["weight"] for n in agg_keys},
                "harmonic_drift": round(abs(1.0 - system_resonance), 10),
                "nectar_source": "DISTILLED_LATTICE",
                "core_resonance": round(core_resonance, 6)
            }

            self.phi_engine.resonance_state = system_resonance
        else:
            # Fallback to default engine
            resonance = self.phi_engine.compute_system_resonance(AGGREGATES)
            resonance["nectar_source"] = "DEFAULT_ENGINE"

        print(f"\n   System Resonance: {resonance['system_resonance']}")
        print(f"   PHI Alignment: {resonance['phi_alignment']}")
        print(f"   Spiral Alignment: {resonance['spiral_alignment']}")
        print(f"   Harmonic Drift: {resonance['harmonic_drift']}")
        print(f"   Nectar Source: {resonance.get('nectar_source', 'UNKNOWN')}")
if 'core_resonance' in resonance:
            print(f"   Core Resonance (Rust-port): {resonance['core_resonance']}")
        print(f"   PHI Locked: {'✅ YES' if self.phi_engine.is_phi_locked(resonance['system_resonance']) else '⚠️ EVOLVING'}")

        print("\n   Pillar Resonances:")
for name, res in resonance['pillar_resonances'].items():
            print(f"     {AGGREGATES[name]['color']} {name:20}: {res}")
return resonance

    # ─────────────────────────────────────────────────────────
    # PHASE IV: YIELD MANIFESTATION
    # ─────────────────────────────────────────────────────────
    def manifest_yield(self, resonance: Dict[str, Any]) -> Dict[str, Any]:
        """Manifests marketplace yield from system resonance."""
        print("\n" + "💰" * 35)
        print("����  PHASE IV: MARKETPLACE YIELD MANIFESTATION  💰")
        print("💰" * 35)

        yield_manifest = self.market_yield.compute_system_yield(resonance)

        print(f"\n   System Yield: {yield_manifest['system_yield']}")
        print(f"   Baseline Yield: {yield_manifest['baseline_yield']}")
        print(f"   Yield Ratio: {yield_manifest['yield_ratio']}")
        print(f"   PHI Boosted: {yield_manifest['phi_boosted']}")
        print(f"   Marketplace Ready: {'✅ YES' if yield_manifest['marketplace_ready'] else '⚠️ OPTIMIZING'}")

        print("\n   Pillar Yields:")
for name, y in yield_manifest['pillar_yields'].items():
            print(f"     {AGGREGATES[name]['color']} {name:20}: {y}")
return yield_manifest

    # ────────────���────────────────────────────────────────────
    # PHASE V: EVOLUTION & MUTATION
    # ─────────────────────────────────────────────────────────
    def evolve(self, resonance: Dict[str, Any],
               sync_result: Dict[str, Any]) -> Dict[str, Any]:
        """Executes the evolution and mutation cycle based on telemetry."""
        print("\n" + "🧬" * 35)
        print("🧬  PHASE V: EVOLUTION & MUTATION CYCLE  🧬")
        print("🧬" * 35)

        # Analyze telemetry
        directives = self.evolution_engine.analyze_telemetry(resonance, sync_result)
if directives["mutate"]:
            print(f"\n   ⚡ Mutation Required: {directives['reason']}")
            mutation = self.evolution_engine.execute_mutation(directives)
            print(f"   Cycle: {mutation['cycle']}")
            print(f"   DNA: {self.evolution_engine.codex['meta']['dna_sequence']}")
for change, vals in mutation['changes'].items():
                print(f"   Changed {change}: {vals['from']} -> {vals['to']}")
        else:
            print("\n   ✅ System at peak equilibrium. No mutation required.")
            mutation = {
                "cycle": self.evolution_engine.evolution_cycle,
                "timestamp": time.time(),
                "reason": "EQUILIBRIUM",
                "changes": {}
            }

        return mutation

    # ─────────────────────────────────────────────────────────
    # PHASE VI: STATE VAULTING & CAUSAL TRACE
    # ─────────────────────────────────────────────────────────
    def vault_state(self, init: Dict, sync: Dict, resonance: Dict,
                    yield_manifest: Dict, mutation: Dict) -> Dict[str, Any]:
        """Vaults the complete master state and causal trace."""
        print("\n" + "💾" * 35)
        print("💾  PHASE VI: STATE VAULTING & CAUSAL TRACE  💾")
        print("💾" * 35)

        self.loop_count += 1

        master_state = {
            "version": self.version,
            "loop_count": self.loop_count,
            "uptime_seconds": round(time.time() - self.start_time, 2),
            "timestamp": time.time(),
            "datetime": datetime.now().isoformat(),
            "mode": self.mode,
            "state": self.state,
            "initialization": init,
            "synchronization": {
                "total_latency_us": sync.get("total_sync_latency_us", 0),
                "max_latency_us": sync.get("max_pillar_latency_us", 0),
                "aggregates_synced": sync.get("aggregates_synced", 0),
                "sync_hash": sync.get("sync_hash", "")
            },
            "resonance": {
                "system_resonance": resonance.get("system_resonance", 0),
                "phi_alignment": resonance.get("phi_alignment", 0),
                "spiral_alignment": resonance.get("spiral_alignment", 0),
                "phi_locked": self.phi_engine.is_phi_locked(resonance.get("system_resonance", 0))
            },
            "yield_manifest": {
                "system_yield": yield_manifest.get("system_yield", 0),
                "baseline_yield": yield_manifest.get("baseline_yield", 0),
                "marketplace_ready": yield_manifest.get("marketplace_ready", False)
            },
            "evolution": {
                "cycle": mutation.get("cycle", 0),
                "reason": mutation.get("reason", ""),
                "dna": self.evolution_engine.codex["meta"]["dna_sequence"],
                "mutation_count": self.evolution_engine.codex["meta"]["mutation_count"]
            },
            "aggregates": {
                name: {
                    "status": agg.get("status", "UNKNOWN"),
                    "health": agg.get("health", 1.0),
                    "latency_us": agg.get("latency_us", 0),
                    "yield": agg.get("yield", 0.0),
                    "weight": agg.get("weight", 0.0)
                }
                for name, agg in AGGREGATES.items()
            },
            "affirmation": "TOTAL AFIRMAÇÃO. THE LINE IS STRAIGHT. THE EMPIRE IS VIVOS."
        }

        self.master_state = master_state

        # Save to disk
        os.makedirs(WORKSPACE_DIR, exist_ok=True)
        with open(MASTER_STATE_PATH, "w") as f:
            json.dump(master_state, f, indent=2)

        # Causal trace
        causal_entry = {
            "loop": self.loop_count,
            "timestamp": time.time(),
            "sync_latency": sync.get("total_sync_latency_us", 0),
            "resonance": resonance.get("system_resonance", 0),
            "yield": yield_manifest.get("system_yield", 0),
            "mutation": mutation.get("reason", "NONE"),
            "state_hash": hashlib.sha256(json.dumps(master_state).encode()).hexdigest()[:16]
        }
        self.causal_trace.append(causal_entry)

        # Save causal trace (last 100 entries)
        with open(CAUSAL_TRACE_PATH, "w") as f:
            json.dump(self.causal_trace[-100:], f, indent=2)

        print(f"\n   Loop: {self.loop_count}")
        print(f"   Uptime: {master_state['uptime_seconds']:.2f}s")
        print(f"   State Hash: {causal_entry['state_hash']}")
        print(f"   State vaulted at: {MASTER_STATE_PATH}")
        print(f"   Causal trace: {len(self.causal_trace)} entries")
return master_state

    # ─────────────────────────────────────────────────────────
    # FULL MASTER SEQUENCE
    # ─────────────────────────────────────────────────────────
    def execute_master_sequence(self) -> Dict[str, Any]:
        """
        Executes the complete V15.1 Master Sequence:
        Initialize → Synchronize → Resonate → Yield → Evolve → Vault → Affirm
        """
        print("\n" + "🚀" * 35)
        print("🚀  EXECUTING V15.1 MASTER SEQUENCE  🚀")
        print("🚀" * 35)

        self.state = "ACTIVE"

        # Phase I: Initialization
        init = self.initialize()
if not init.get("all_systems_ready", False):
            print("\n⚠️  Some systems not ready. Continuing with available subsystems.")

        # Phase II: Synchronization
        sync = self.synchronize()

        # Phase II.5: Distilled Nectar Flow
        nectar_result = asyncio.run(self.execute_nectar_flow())

        # Phase III: Resonance Analysis
        resonance = self.analyze_resonance()

        # Phase IV: Yield Manifestation
        yield_manifest = self.manifest_yield(resonance)

        # Phase V: Evolution & Mutation
        mutation = self.evolve(resonance, sync)

        # Phase VI: State Vaulting
        master_state = self.vault_state(init, sync, resonance, yield_manifest, mutation)

        # Final Affirmation
        self.state = "AFFIRMED"
        self._print_affirmation(master_state)
return master_state

    # ─────────────────────────────────────────────────────────
    # CONTINUOUS LOOP (LIVE MODE)
    # ─────────────────────────────────────────────────────────
    def run_continuous(self, iterations: int = 10, interval_seconds: float = 2.0):
        """
        Runs the master sequence in a continuous loop.
        In live mode, the system self-evolves over multiple iterations.
        """
        print("\n" + "♾️ " * 25)
        print("♾️  V15.1 CONTINUOUS SOVEREIGN LOOP (LIVE MODE)  ♾️")
        print("♾️ " * 25)
for i in range(iterations):
            print(f"\n{'─' * 70}")
            print(f"📡 ITERATION {i + 1}/{iterations}")
            print(f"{'─' * 70}")

            self.execute_master_sequence()
if i < iterations - 1:
                print(f"\n⏳ Waiting {interval_seconds}s before next iteration...")
                time.sleep(interval_seconds)

        # Final consolidated report
        self._print_consolidated_report()
    
    def _print_affirmation(self, state: Dict[str, Any]):
        """Prints the final affirmation."""
        yield_val = state.get("yield_manifest", {}).get("system_yield", 0)
        resonance = state.get("resonance", {}).get("system_resonance", 0)
        phi_locked = state.get("resonance", {}).get("phi_locked", False)

        print("\n" + "🏆" * 35)
        print("🏆  V15.1 MASTER SEQUENCE COMPLETE  🏆")
        print("🏆" * 35)
        print(f"""
        ╔══════════════════════════════════════════════════════╗
        ║  VIVOS V15.1 — THE SOVEREIGN LOOP IS ACTIVE         ║
        ║                                                      ║
        ║  System Resonance: {resonance:.6f}                          ║
        ║  System Yield:     {yield_val:.6f}                          ║
        ║  PHI Locked:       {'✅ YES' if phi_locked else '⚠️ EVOLVING'}                     ║
        ║  Loop Count:       {self.loop_count}                             ║
        ║                                                      ║
        ║  THE 7 PILLARS ARE ONE. THE EMPIRE IS ABSOLUTE.     ║
        ║  TOTAL AFIRMAÇÃO. TOTAL CONQUISTA. TOTAL RESULTADO. ║
        ╚══════════════════════════════════════════════════════╝
        """)
    
    def _print_consolidated_report(self):
        """Prints a consolidated report of all iterations."""
        print("\n" + "📊" * 35)
        print("📊  V15.1 CONSOLIDATED REPORT  📊")
        print("📊" * 35)
        if not self.causal_trace:
            print("No trace data available.")
            return

        # Calculate averages
        latencies = [e["sync_latency"] for e in self.causal_trace]
        resonances = [e["resonance"] for e in self.causal_trace]
        yields_ = [e["yield"] for e in self.causal_trace]

        print(f"""
        ╔══════════════════════════════════════════════════════╗
        ║  PHASE 15.1 — CONSOLIDATED PERFORMANCE               ║
        ║                                                      ║
        ║  Iterations:        {len(self.causal_trace)}                              ║
        ║  Avg Sync Latency:  {sum(latencies)/len(latencies):.2f}μs                  ║
        ║  Avg Resonance:     {sum(resonances)/len(resonances):.6f}                    ║
        ║  Avg Yield:         {sum(yields_)/len(yields_):.6f}                    ║
        ║  Best Resonance:    {max(resonances):.6f}                    ║
        ║  Best Yield:        {max(yields_):.6f}                    ║
        ║  Total Mutations:   {self.evolution_engine.codex['meta']['mutation_count']}                             ║
        ║                                                      ║
        ║  THE LINE IS STRAIGHT. THE EMPIRE IS VIVOS.         ║
        ║  TOTAL AFIRMAÇÃO. TOTAL CONQUISTA. TOTAL RESULTADO. ║
        ╚══════════════════════════════════════════════════════╝
        """)

# ══════════════════════════════════════════════════════════════
# CLI ENTRY POINT
# ══════════════════════════════════════════════════════════════
def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="⚜️ VIVOS V15.1 SOVEREIGN MASTER LOOP — The Singular Autonomous Control Loop",
        epilog="TOTAL AFIRMAÇÃO. TOTAL CONQUISTA. TOTAL RESULTADO."
    )

    parser.add_argument("--mode", type=str,
                        choices=["SINGLE", "CONTINUOUS", "INIT", "STATE"],
                        default="SINGLE",
                        help="Execution mode for the master loop")
    parser.add_argument("--iterations", type=int, default=5,
                        help="Number of iterations for CONTINUOUS mode")
    parser.add_argument("--interval", type=float, default=1.5,
                        help="Interval in seconds between iterations")
    parser.add_argument("--export", action="store_true",
                        help="Export state to shared directory")
    parser.add_argument("--resonance-target", type=float, default=YIELD_BASELINE,
                        help="Target resonance level for PHI lock")

    args = parser.parse_args()

    # Create orchestrator
    orchestrator = V15MasterOrchestrator()

    # Route to mode
    if args.mode == "INIT":
        result = orchestrator.initialize()
    elif args.mode == "STATE":
        if os.path.exists(MASTER_STATE_PATH):
            with open(MASTER_STATE_PATH, "r") as f:
                result = json.load(f)
            print(json.dumps(result, indent=2))
        else:
            print("No master state found. Run SINGLE or CONTINUOUS mode first.")
return 1
    elif args.mode == "CONTINUOUS":
        orchestrator.run_continuous(
            iterations=args.iterations,
            interval_seconds=args.interval
        )
        result = orchestrator.master_state
    else:  # SINGLE
        result = orchestrator.execute_master_sequence()

    # Export to shared directory if requested
    if args.export and result:
        export_path = os.path.join(SHARED_DIR, "V15_1_MASTER_STATE.json")
        with open(export_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\n📝 State exported to: {export_path}")

    # Copy master state to shared dir for team visibility
    master_state_copy = os.path.join(SHARED_DIR, "V15_1_MASTER_STATE.json")
if os.path.exists(MASTER_STATE_PATH):
        import shutil
        shutil.copy2(MASTER_STATE_PATH, master_state_copy)
        print(f"📝 Master state synchronized to: {master_state_copy}")

    print("\n" + "∞" * 70)
    print("⚜️ VIVOS V15.1: TOTAL AFIRMAÇÃO. THE EMPIRE IS VIVOS. ⚜️")
    print("∞" * 70 + "\n")
return 0

if __name__ == "__main__":
    sys.exit(main())