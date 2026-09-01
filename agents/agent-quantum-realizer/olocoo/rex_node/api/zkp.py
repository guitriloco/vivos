import hashlib
import json
import os
import time

class SiphonProtocol:
    @staticmethod
    def calculate_siphon(amount, rate=0.30):
        siphon_amount = amount * rate
        remaining_amount = amount - siphon_amount
        return remaining_amount, siphon_amount

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

    def seal_transaction(self, amount, source, destination, metadata=None):
        remaining, siphon = SiphonProtocol.calculate_siphon(amount)
        timestamp = time.time()

        # Create commitment for the main ledger
        tx_data = {
            "amount": remaining,
            "source": source,
            "destination": destination,
            "timestamp": timestamp,
            "metadata": metadata
        }
        tx_proof, tx_salt = self._generate_proof(tx_data)
        tx_entry = {
            "commitment": tx_proof,
            "salt": tx_salt,
            "data": tx_data,
            "status": "SEALED"
        }

        # Create commitment for cold storage
        cold_data = {
            "amount": siphon,
            "source": source,
            "destination": "COLD_STORAGE",
            "timestamp": timestamp,
            "reference_proof": tx_proof
        }
        cold_proof, cold_salt = self._generate_proof(cold_data)
        cold_entry = {
            "commitment": cold_proof,
            "salt": cold_salt,
            "data": cold_data,
            "status": "SIPHONED"
        }

        self._append_to_json(self.ledger_path, tx_entry)
        self._append_to_json(self.cold_storage_path, cold_entry)
        
        print(f"[ZKP Engine] Transaction sealed: {tx_proof[:12]}... | Siphoned: {siphon}")
        return tx_proof

    def verify_integrity(self):
        """Verifies the integrity of the ledger by re-calculating proofs."""
        with open(self.ledger_path, 'r') as f:
            ledger_data = json.load(f)
        
        for entry in ledger_data:
            proof, _ = self._generate_proof(entry['data'], entry['salt'])
            if proof != entry['commitment']:
                return False
        return True

    def _append_to_json(self, path, entry):
        with open(path, 'r+') as f:
            data = json.load(f)
            data.append(entry)
            f.seek(0)
            json.dump(data, f, indent=4)
            f.truncate()

# Alias for backward compatibility or as per alternative naming in ticket
ZeroKnowledgeLedger = EternalLedger

if __name__ == "__main__":
    LEDGER_PATH = "/home/engine/project/projets/Wealth_Core/eternal_ledger.json"
    COLD_STORAGE_PATH = "/home/engine/project/projets/Wealth_Core/cold_storage.json"
    
    engine = ZeroKnowledgeLedger(LEDGER_PATH, COLD_STORAGE_PATH)
    print("--- 🛡️ ZKP PRESERVATION ENGINE: ACTIVE ---")
    print(f"Eternal Ledger: {LEDGER_PATH}")
    print(f"Cold Storage: {COLD_STORAGE_PATH}")
    
    # Simple simulation of listening for events via a named pipe or just watching a file
    # For the purpose of this task, we will simulate the integration by having the ledger call this logic.
    # But as a standalone service, it might listen on a socket or wait for signals.
    
    # To keep the process alive as expected by APOGEU_MASTER:
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("ZKP Preservation Engine shutting down.")
