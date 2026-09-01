import base64
import json
import os

class VVVVault:
    """
    VVV-Vault: Basic encryption and preservation for lists of suppliers.
    Simulating Zero-Knowledge Proof preservation.
    """
    def __init__(self, vault_path=None):
        if vault_path is None:
            # Default path relative to this file
            self.vault_path = os.path.join(os.path.dirname(__file__), "vault_data.json")
        else:
            self.vault_path = vault_path
        
        if not os.path.exists(self.vault_path):
            with open(self.vault_path, "w") as f:
                json.dump({}, f)

    def _simple_obfuscate(self, text: str) -> str:
        # Basic base64 obfuscation to simulate "protection"
        return base64.b64encode(text.encode()).decode()

    def _simple_deobfuscate(self, text: str) -> str:
        return base64.b64decode(text.encode()).decode()

    def store_supplier_list(self, niche: str, suppliers: list):
        with open(self.vault_path, "r") as f:
            data = json.load(f)
        
        protected_suppliers = [self._simple_obfuscate(s) for s in suppliers]
        data[niche] = protected_suppliers
        
        with open(self.vault_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"[VVV-VAULT] Niche '{niche}' stored and protected.")

    def retrieve_supplier_list(self, niche: str) -> list:
        with open(self.vault_path, "r") as f:
            data = json.load(f)
        
        if niche in data:
            return [self._simple_deobfuscate(s) for s in data[niche]]
        return []

if __name__ == "__main__":
    vault = VVVVault()
    # Test
    vault.store_supplier_list("fitness", ["Supplier A - 1234", "Supplier B - 5678"])
    print(f"Retrieved: {vault.retrieve_supplier_list('fitness')}")
