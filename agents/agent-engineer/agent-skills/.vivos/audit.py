import os
import json

def audit_resonance():
    peers = ["Imperio-Mutante-v3-Core", "Nectar_Dev", "agent-skills"]
    found = []
    home = os.path.expanduser("~")
    for peer in peers:
        if os.path.exists(os.path.join(home, peer)):
            found.append(peer)
    
    resonance = len(found) / len(peers)
    print(f"MUTANT-NECTAR Resonance: {resonance*100:.1f}%")
    return resonance

if __name__ == "__main__":
    audit_resonance()
