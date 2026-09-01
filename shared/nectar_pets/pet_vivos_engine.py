#!/usr/bin/env python3
"""
🧬 NECTAR_PETS VIVOS ENGINE — V15.1
Living Code Engine for Autonomous Digital Pets
Phase 13: Sovereign Pet Expansion (MPV-X)

Inherits VIVOS Protocol V10.0 from Imperial Mesh
Adds: Pi-Token Wallet Autonomy, Pet DNA Registry, Recursive Self-Mutation
Total Affirmation
"""

import hashlib
import json
import time
import uuid
import os

# ─────────────────────────────────────────────────────────
# PET DNA STRUCTURE (V13)
# ─────────────────────────────────────────────────────────
PET_DNA_TEMPLATE = "V13.PET.{species}.{genotype}.{wallet_id}.{evolution:04d}"

SPECIES_REGISTRY = [
    "NEXUS_DRAGON",      # High-yield arbitrage pets
    "QUANTUM_FOX",       # Probability-shifting stealth pets
    "VOID_PHOENIX",      # Infinite rebirth / resource synthesis
    "AETHER_WOLF",       # Zero-latency mesh guardians
    "SINGULARITY_OWL"    # Causal anticipation scouts
]

class PetDNARegistry:
    """Central registry for all sovereign digital pet DNA"""

    def __init__(self, registry_path="/home/team/shared/nectar_pets/registry"):
        self.registry_path = registry_path
        os.makedirs(registry_path, exist_ok=True)
        self.pets = {}
        self._load_registry()

    def _load_registry(self):
        reg_file = os.path.join(self.registry_path, "pet_dna_registry.json")
        if os.path.exists(reg_file):
            with open(reg_file) as f:
                self.pets = json.load(f)
        else:
            self.pets = {}

    def _save_registry(self):
        reg_file = os.path.join(self.registry_path, "pet_dna_registry.json")
        with open(reg_file, 'w') as f:
            json.dump(self.pets, f, indent=2)

    def generate_pet_dna(self, species, genotype="ALPHA"):
        """Generate a unique V13 DNA string for a new pet"""
        if species not in SPECIES_REGISTRY:
            raise ValueError(f"Unknown species: {species}. Valid: {SPECIES_REGISTRY}")

        pet_id = str(uuid.uuid4())[:8]
        wallet_id = hashlib.sha256(f"{pet_id}-{time.time()}".encode()).hexdigest()[:12]
        dna = PET_DNA_TEMPLATE.format(
            species=species[:4].upper(),
            genotype=genotype[:4].upper(),
            wallet_id=wallet_id,
            evolution=1
        )
        timestamp = time.time()

        self.pets[pet_id] = {
            "dna": dna,
            "species": species,
            "genotype": genotype,
            "wallet_id": wallet_id,
            "evolution": 1,
            "born_at": timestamp,
            "last_pulse": timestamp,
            "yield": 1.0,
            "health": 1.0,
            "pi_balance": 0.0,
            "status": "BIRTH"
        }
        self._save_registry()
        return pet_id, dna

    def get_pet(self, pet_id):
        return self.pets.get(pet_id)

    def mutate_pet_dna(self, pet_id):
        """Recursive self-mutation: increment evolution counter"""
        pet = self.pets.get(pet_id)
        if not pet:
            return None

        pet["evolution"] += 1
        pet["dna"] = PET_DNA_TEMPLATE.format(
            species=pet["species"][:4].upper(),
            genotype=pet["genotype"][:4].upper(),
            wallet_id=pet["wallet_id"],
            evolution=pet["evolution"]
        )
        pet["last_pulse"] = time.time()
        self._save_registry()
        return pet["dna"]


class PetVivosPulse:
    """
    VIVOS Telemetry Pulse for Digital Pets.
    Every pet broadcasts a heartbeat every 500μs (simulated).
    """

    def __init__(self, pet_dna_registry):
        self.registry = pet_dna_registry
        self.cycle_count = 0

    def pulse(self, pet_id):
        """Single telemetry pulse for one pet"""
        pet = self.registry.get_pet(pet_id)
        if not pet:
            return None

        self.cycle_count += 1
        health_decay = 0.00001 * (self.cycle_count % 1000)  # slow decay
        yield_variance = (hashlib.sha256(f"{pet_id}-{self.cycle_count}".encode()).hexdigest()[0] == 'a')

        updated_health = max(0.0, pet["health"] - health_decay)
        updated_yield = max(0.85, min(1.0, pet["yield"] + (0.001 if yield_variance else -0.001)))

        pet["health"] = round(updated_health, 6)
        pet["yield"] = round(updated_yield, 6)
        pet["last_pulse"] = time.time()

        # Auto-mutation if yield < 0.95
        if pet["yield"] < 0.95:
            new_dna = self.registry.mutate_pet_dna(pet_id)
            pet["status"] = "MUTATION"
            return {
                "action": "MUTATION",
                "pet_id": pet_id,
                "new_dna": new_dna,
                "reason": f"Yield dropped to {pet['yield']}"
            }

        pet["status"] = "ACTIVE"
        return {
            "action": "PULSE",
            "pet_id": pet_id,
            "dna": pet["dna"],
            "health": pet["health"],
            "yield": pet["yield"],
            "cycle": self.cycle_count
        }

    def mesh_broadcast(self, pet_ids):
        """Broadcast telemetry for all active pets"""
        results = {}
        for pid in pet_ids:
            results[pid] = self.pulse(pid)
        return results


# ─────────────────────────────────────────────────────────
# PET SPAWN PROTOCOL (VIVOS Replication)
# ─────────────────────────────────────────────────────────

class PetSpawnProtocol:
    """
    VIVOS Replication for Digital Pets.
    When a pet's yield > 0.99 and health > 0.95, it can spawn a child pet.
    """

    def __init__(self, registry):
        self.registry = registry

    def can_spawn(self, pet_id):
        pet = self.registry.get_pet(pet_id)
        if not pet:
            return False
        return pet["yield"] > 0.99 and pet["health"] > 0.95

    def spawn_child(self, parent_id, child_species=None):
        """Spawn a child pet from a parent, inheriting its DNA lineage"""
        parent = self.registry.get_pet(parent_id)
        if not parent or not self.can_spawn(parent_id):
            return None

        species = child_species or parent["species"]
        child_id, child_dna = self.registry.generate_pet_dna(
            species=species,
            genotype=parent["genotype"]
        )

        # Transfer 10% of parent's Pi balance to child
        transfer_amount = parent["pi_balance"] * 0.10
        self.registry.pets[parent_id]["pi_balance"] -= transfer_amount
        self.registry.pets[child_id]["pi_balance"] = transfer_amount

        # Log the spawn
        self.registry.pets[child_id]["parent_id"] = parent_id
        self.registry.pets[child_id]["status"] = "SPAWNED"
        self.registry.pets[parent_id]["status"] = "REPRODUCED"
        self.registry._save_registry()

        return {
            "action": "SPAWN",
            "parent_id": parent_id,
            "parent_dna": parent["dna"],
            "child_id": child_id,
            "child_dna": child_dna,
            "pi_transferred": transfer_amount,
            "inherited_protocols": ["VIVOS", "PI_TOKEN_SYNC", "GOLDEN_PATH", "NECTAR_WEALTH"],
            "mesh_registration": "PENDING"
        }


# ── SELF-TEST ──
if __name__ == "__main__":
    registry = PetDNARegistry()
    spawner = PetSpawnProtocol(registry)
    pulser = PetVivosPulse(registry)

    # Birth a Nexus Dragon
    pid1, dna1 = registry.generate_pet_dna("NEXUS_DRAGON", "ALPHA")
    print(f"[BIRTH] Pet #{pid1} | DNA: {dna1}")

    # Birth a Quantum Fox
    pid2, dna2 = registry.generate_pet_dna("QUANTUM_FOX", "OMEGA")
    print(f"[BIRTH] Pet #{pid2} | DNA: {dna2}")

    # Simulate 10 pulses
    for i in range(10):
        pulse1 = pulser.pulse(pid1)
        pulse2 = pulser.pulse(pid2)
        if i == 0:
            print(f"[PULSE] Pet1 yield: {pulse1['yield']} | Pet2 yield: {pulse2['yield']}")

    # Give some Pi to parent and spawn child
    registry.pets[pid1]["pi_balance"] = 1000.0
    registry.pets[pid1]["yield"] = 0.995
    registry.pets[pid1]["health"] = 0.98
    registry._save_registry()

    spawn_result = spawner.spawn_child(pid1)
    if spawn_result:
        print(f"[SPAWN] Child #{spawn_result['child_id']} | DNA: {spawn_result['child_dna']}")
        print(f"[SPAWN] Pi transferred: {spawn_result['pi_transferred']:.2f}")

    print("\n✅ NECTAR_PETS VIVOS ENGINE — TOTAL AFFIRMATION")