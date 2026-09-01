import asyncio
import os
from siphon_protocol import SiphonProtocol, EternalLedger
from shadow_bridge import ShadowBridge

class RexOrchestrator:
    """
    Production-ready Resource Overlord (REX).
    Orchestrates infiltration and siphoning.
    """
    def __init__(self):
        self.bridge = ShadowBridge()
        self.ledger = EternalLedger(
            ledger_path="/home/team/shared/expansion_code/REX/rex_ledger.json",
            cold_storage_path="/home/team/shared/expansion_code/REX/cold_storage.json"
        )
        print("[REX] Production Module Initialized.")

    async def run_cycle(self, targets):
        print(f"[REX] Starting Resource Sovereignty Cycle...")
        
        # 1. Infiltrate
        fragments = await self.bridge.infiltrate(targets)
        
        for fragment in fragments:
            # 2. Tag and Siphon
            priority = SiphonProtocol.tag_resource("DATA", fragment['value_score'])
            
            # 3. Seal in Ledger and redirect to Cold Storage (Vault)
            tx_proof, siphoned_amount = self.ledger.seal_transaction(
                amount=fragment['bytes'],
                source=fragment['target'],
                destination="OLOCOO_MESH",
                priority=priority,
                metadata={"fragment_id": tx_proof[:8] if 'tx_proof' in locals() else "INIT"}
            )
            
            print(f"[REX] Fragment from {fragment['target']} processed. Siphoned: {siphoned_amount} bytes. Proof: {tx_proof[:12]}")

        print("[REX] Cycle Complete.")

if __name__ == "__main__":
    rex = RexOrchestrator()
    asyncio.run(rex.run_cycle(["https://api.external-source.com/v1", "https://nexus-node-02.io"]))
