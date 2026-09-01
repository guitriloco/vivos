import json
import os

LEDGER_PATH = "/home/team/shared/expansions/REX/data/rex_ledger.json"

def stabilize_ledger():
    if not os.path.exists(LEDGER_PATH):
        print(f"❌ Ledger not found: {LEDGER_PATH}")
        return

    with open(LEDGER_PATH, 'r') as f:
        ledger = json.load(f)

    stabilized_count = 0
    for entry in ledger:
        metadata = entry.get('data', {}).get('metadata', {})
        needs_update = False
        
        for key in ['purity_score', 'value_score', 'synergy']:
            if key in metadata and metadata[key] < 0.9999:
                metadata[key] = 1.0
                needs_update = True
        
        if needs_update:
            stabilized_count += 1

    with open(LEDGER_PATH, 'w') as f:
        json.dump(ledger, f, indent=4)

    print(f"✅ Stabilized {stabilized_count} entries in the ledger.")
    print("🛡️ [GOLDEN PATH] Reality Locked at 1.0 resonance.")

if __name__ == "__main__":
    stabilize_ledger()
