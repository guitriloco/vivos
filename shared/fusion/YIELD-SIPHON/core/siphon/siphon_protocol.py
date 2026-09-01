import hashlib
import json
import os
import time

class SiphonProtocol:
    """
    Refined Siphon Protocol for Resource Redirection.
    Handles different rates and prioritization for the Sovereign Line.
    """
    RATES = {
        "CORE": 0.50,    # 50% for core system assets
        "STANDARD": 0.30, # 30% for standard data
        "LEAN": 0.10     # 10% for low-value telemetry
    }

    @staticmethod
    def calculate_siphon(amount, priority="STANDARD"):
        rate = SiphonProtocol.RATES.get(priority, 0.30)
        siphon_amount = amount * rate
        remaining_amount = amount - siphon_amount
        return remaining_amount, siphon_amount

    @staticmethod
    def tag_resource(data_type, value_score):
        """Tags resource based on value score for siphoning priority."""
        if value_score > 0.9:
            return "CORE"
        elif value_score > 0.5:
            return "STANDARD"
        return "LEAN"

class EternalLedger:
    def __init__(self, ledger_path, cold_storage_path):
        self.ledger_path = ledger_path
        self.cold_storage_path = cold_storage_path
        self._init_storage()

    def _init_storage(self):
        os.makedirs(os.path.dirname(self.ledger_path), exist_ok=True)
        for path in [self.ledger_path, self.cold_storage_path]:
            if not os.path.exists(path):
                with open(path, 'w') as f:
                    json.dump([], f)

    def _generate_proof(self, data, salt=None):
        if salt is None:
            salt = os.urandom(16).hex()
        payload = json.dumps(data, sort_keys=True) + salt
        proof = hashlib.sha256(payload.encode()).hexdigest()
        return proof, salt

    def seal_transaction(self, amount, source, destination, priority="STANDARD", metadata=None):
        remaining, siphon = SiphonProtocol.calculate_siphon(amount, priority)
        timestamp = time.time()

        tx_data = {
            "amount": remaining,
            "source": source,
            "destination": destination,
            "timestamp": timestamp,
            "priority": priority,
            "metadata": metadata
        }
        tx_proof, tx_salt = self._generate_proof(tx_data)
        
        cold_data = {
            "amount": siphon,
            "source": source,
            "destination": "COLD_STORAGE",
            "timestamp": timestamp,
            "reference_proof": tx_proof
        }
        cold_proof, cold_salt = self._generate_proof(cold_data)

        self._append_to_json(self.ledger_path, {
            "commitment": tx_proof, "salt": tx_salt, "data": tx_data, "status": "SEALED"
        })
        self._append_to_json(self.cold_storage_path, {
            "commitment": cold_proof, "salt": cold_salt, "data": cold_data, "status": "SIPHONED"
        })
        
        return tx_proof, siphon

    def _append_to_json(self, path, entry):
        with open(path, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()
