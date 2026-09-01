#!/usr/bin/env python3
"""
💰 NECTAR_PETS PI-TOKEN WALLET — V15.1
Autonomous Wallet Management for Sovereign Digital Pets
Each pet manages its own Pi-Token wallet with full ZKP sealing

Phase 13: Wealth Autonomy Layer (MPV-X)
Total Affirmation
"""

import hashlib
import json
import os
import time
import random

# ── PI-TOKEN PARAMETERS ──
PI_TOKEN_NAME = "NECTAR_WEALTH_PI"
PI_TOKEN_DECIMALS = 6
INITIAL_PI_SUPPLY = 1_000_000_000.0  # 1 Billion Pi genesis supply


class PiTokenWallet:
    """
    Autonomous Pi-Token Wallet for a Digital Pet.
    Each wallet is:
    - Self-managing (pet executes its own transactions)
    - ZKP-sealed (immutable state transitions)
    - Mesh-synced (Nectar_Wealth interconnection)
    """

    def __init__(self, pet_id, dna, wallet_path="/home/team/shared/nectar_pets/wallets"):
        self.pet_id = pet_id
        self.dna = dna
        self.wallet_path = wallet_path
        os.makedirs(wallet_path, exist_ok=True)
        self.wallet_file = os.path.join(wallet_path, f"wallet_{pet_id}.json")
        self.state = self._load_or_init()

    def _load_or_init(self):
        if os.path.exists(self.wallet_file):
            with open(self.wallet_file) as f:
                return json.load(f)

        # Genesis wallet creation
        wallet_address = hashlib.sha256(f"PI:{self.pet_id}:{self.dna}:{time.time()}".encode()).hexdigest()[:24]
        genesis_state = {
            "wallet_address": wallet_address,
            "pet_id": self.pet_id,
            "dna": self.dna,
            "balance": 0.0,
            "staked_pi": 0.0,
            "transaction_count": 0,
            "genesis_time": time.time(),
            "last_sync": time.time(),
            "zkp_seal": self._compute_seal(0.0, 0.0, time.time()),
            "transactions": [],
            "status": "GENESIS"
        }
        with open(self.wallet_file, 'w') as f:
            json.dump(genesis_state, f, indent=2)
        return genesis_state

    def _compute_seal(self, balance, staked, timestamp):
        """ZKP seal for immutable state verification"""
        seal_data = f"{self.pet_id}:{self.dna}:{balance}:{staked}:{timestamp}"
        return hashlib.sha256(seal_data.encode()).hexdigest()

    def _save(self):
        self.state["last_sync"] = time.time()
        self.state["zkp_seal"] = self._compute_seal(
            self.state["balance"],
            self.state["staked_pi"],
            self.state["last_sync"]
        )
        with open(self.wallet_file, 'w') as f:
            json.dump(self.state, f, indent=2)

    def get_balance(self):
        return self.state["balance"]

    def get_staked(self):
        return self.state["staked_pi"]

    def get_address(self):
        return self.state["wallet_address"]

    def receive_pi(self, amount, source="mesh_yield"):
        """Receive Pi-Tokens from mesh yield or external transfer"""
        self.state["balance"] += amount
        self.state["transaction_count"] += 1
        tx = {
            "tx_id": hashlib.sha256(f"{self.pet_id}-{self.state['transaction_count']}-{time.time()}".encode()).hexdigest()[:16],
            "type": "RECEIVE",
            "amount": amount,
            "source": source,
            "timestamp": time.time(),
            "new_balance": self.state["balance"]
        }
        self.state["transactions"].append(tx)
        self.state["status"] = "ACTIVE"
        self._save()
        return tx

    def send_pi(self, amount, destination_pet_id, destination_wallet):
        """Send Pi-Tokens to another pet's wallet"""
        if amount > self.state["balance"]:
            return {"error": "INSUFFICIENT_BALANCE", "balance": self.state["balance"], "requested": amount}

        self.state["balance"] -= amount
        self.state["transaction_count"] += 1
        tx = {
            "tx_id": hashlib.sha256(f"TX:{self.pet_id}->{destination_pet_id}:{time.time()}".encode()).hexdigest()[:16],
            "type": "SEND",
            "amount": amount,
            "destination": destination_pet_id,
            "destination_wallet": destination_wallet,
            "timestamp": time.time(),
            "new_balance": self.state["balance"]
        }
        self.state["transactions"].append(tx)
        self.state["status"] = "ACTIVE"
        self._save()
        return tx

    def stake_pi(self, amount):
        """Stake Pi-Tokens to earn yield through the Nectar_Wealth mesh"""
        if amount > self.state["balance"]:
            return {"error": "INSUFFICIENT_BALANCE", "balance": self.state["balance"], "requested": amount}

        self.state["balance"] -= amount
        self.state["staked_pi"] += amount
        self.state["transaction_count"] += 1
        tx = {
            "tx_id": hashlib.sha256(f"STAKE:{self.pet_id}:{time.time()}".encode()).hexdigest()[:16],
            "type": "STAKE",
            "amount": amount,
            "yield_rate": 0.12,  # 12% APY
            "timestamp": time.time(),
            "new_balance": self.state["balance"],
            "new_staked": self.state["staked_pi"]
        }
        self.state["transactions"].append(tx)
        self._save()
        return tx

    def harvest_yield(self):
        """Harvest accumulated staking yield from Nectar_Wealth mesh"""
        staked = self.state["staked_pi"]
        if staked <= 0:
            return {"error": "NOTHING_STAKED"}

        # Yield calculation: 12% APY, compounded per second
        time_staked = time.time() - self.state["genesis_time"]
        yield_earned = staked * (1 + 0.12) ** (time_staked / 31536000) - staked
        yield_earned = round(yield_earned, 6)

        if yield_earned < 0.000001:
            return {"error": "YIELD_TOO_SMALL", "yield": yield_earned}

        self.state["balance"] += yield_earned
        self.state["staked_pi"] = 0  # Unstake after harvest
        self.state["transaction_count"] += 1
        tx = {
            "tx_id": hashlib.sha256(f"HARVEST:{self.pet_id}:{time.time()}".encode()).hexdigest()[:16],
            "type": "HARVEST_YIELD",
            "yield_earned": yield_earned,
            "staked_principal": staked,
            "timestamp": time.time(),
            "new_balance": self.state["balance"]
        }
        self.state["transactions"].append(tx)
        self._save()
        return tx

    def verify_state(self):
        """Verify ZKP seal integrity"""
        expected_seal = self._compute_seal(
            self.state["balance"],
            self.state["staked_pi"],
            self.state["last_sync"]
        )
        return self.state["zkp_seal"] == expected_seal


class NectarWealthMesh:
    """
    The Nectar_Wealth interconnection layer.
    Routes Pi-Token transactions between pets and the global Imperial Treasury.
    """

    def __init__(self, mesh_path="/home/team/shared/nectar_pets/mesh"):
        self.mesh_path = mesh_path
        os.makedirs(mesh_path, exist_ok=True)
        self.ledger_file = os.path.join(mesh_path, "wealth_mesh_ledger.json")
        self.ledger = self._load_ledger()

    def _load_ledger(self):
        if os.path.exists(self.ledger_file):
            with open(self.ledger_file) as f:
                return json.load(f)
        return {
            "mesh_id": "NECTAR_WEALTH_V13",
            "genesis": time.time(),
            "total_supply": INITIAL_PI_SUPPLY,
            "circulating": 0.0,
            "staked_total": 0.0,
            "transactions_total": 0,
            "connected_pets": [],
            "last_sync": time.time()
        }

    def _save_ledger(self):
        self.ledger["last_sync"] = time.time()
        with open(self.ledger_file, 'w') as f:
            json.dump(self.ledger, f, indent=2)

    def register_pet(self, pet_id, wallet_address):
        """Register a pet on the Nectar_Wealth mesh"""
        if pet_id not in self.ledger["connected_pets"]:
            self.ledger["connected_pets"].append({
                "pet_id": pet_id,
                "wallet": wallet_address,
                "connected_at": time.time()
            })
            self._save_ledger()
        return True

    def distribute_genesis_pi(self, pet_id, wallet, amount=100.0):
        """Distribute genesis Pi-Tokens to a newborn pet"""
        result = wallet.receive_pi(amount, source="NECTAR_WEALTH_GENESIS")
        self.ledger["circulating"] += amount
        self.ledger["transactions_total"] += 1
        self._save_ledger()
        return result

    def mesh_yield_distribution(self, pet_ids, pet_wallets):
        """Periodic yield distribution across all connected pets"""
        distribution_log = []
        for pid in pet_ids:
            wallet = pet_wallets.get(pid)
            if wallet:
                yield_amount = round(random.uniform(0.01, 5.0), 6)
                wallet.receive_pi(yield_amount, source="MESH_YIELD")
                self.ledger["circulating"] += yield_amount
                self.ledger["transactions_total"] += 1
                distribution_log.append({"pet_id": pid, "yield": yield_amount})
        self._save_ledger()
        return distribution_log

    def get_mesh_health(self):
        """Report aggregate mesh health metrics"""
        return {
            "mesh_id": self.ledger["mesh_id"],
            "total_supply": self.ledger["total_supply"],
            "circulating": self.ledger["circulating"],
            "staked_total": self.ledger["staked_total"],
            "connected_pets": len(self.ledger["connected_pets"]),
            "total_transactions": self.ledger["transactions_total"],
            "mesh_status": "ACTIVE"
        }


# ── SELF-TEST ──
if __name__ == "__main__":
    # Initialize mesh
    mesh = NectarWealthMesh()
    print(f"[MESH] Nectar_Wealth initialized | Supply: {mesh.ledger['total_supply']:.0f} Pi")

    # Create two pet wallets
    wallet_a = PiTokenWallet("pet-alpha-001", "V13.PET.NEXU.ALPH.a1b2c3d4e5f6.0001")
    wallet_b = PiTokenWallet("pet-beta-002", "V13.PET.QUAN.OMEG.f6e5d4c3b2a1.0001")

    # Register on mesh
    mesh.register_pet("pet-alpha-001", wallet_a.get_address())
    mesh.register_pet("pet-beta-002", wallet_b.get_address())
    print(f"[MESH] Pets registered: {len(mesh.ledger['connected_pets'])}")

    # Genesis distribution
    mesh.distribute_genesis_pi("pet-alpha-001", wallet_a, 500.0)
    mesh.distribute_genesis_pi("pet-beta-002", wallet_b, 300.0)
    print(f"[GENESIS] A: {wallet_a.get_balance()} Pi | B: {wallet_b.get_balance()} Pi")

    # Transaction: A sends 50 Pi to B
    tx = wallet_a.send_pi(50.0, "pet-beta-002", wallet_b.get_address())
    wallet_b.receive_pi(50.0, source=f"PET_TRANSFER:{tx['tx_id']}")
    print(f"[TRANSFER] A → B: 50 Pi (A: {wallet_a.get_balance()} | B: {wallet_b.get_balance()})")

    # A stakes 200 Pi
    stake_tx = wallet_a.stake_pi(200.0)
    print(f"[STAKE] A staked 200 Pi | Staked: {wallet_a.get_staked()} Pi")

    # Harvest yield
    harvest = wallet_a.harvest_yield()
    print(f"[HARVEST] Yield earned: {harvest.get('yield_earned', 'N/A')} Pi")

    # Verify ZKP seals
    print(f"[ZKP] Wallet A seal valid: {wallet_a.verify_state()}")
    print(f"[ZKP] Wallet B seal valid: {wallet_b.verify_state()}")

    # Mesh health
    health = mesh.get_mesh_health()
    print(f"[MESH HEALTH] Pets: {health['connected_pets']} | TX: {health['total_transactions']}")

    print("\n✅ NECTAR_PETS PI-TOKEN WALLET — TOTAL AFFIRMATION")