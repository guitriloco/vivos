import asyncio
import sys
import os

# Legacy wrapper for Sovereign Reality 3.0
project_root = "/home/agent-ai-architect/nectar-suprema"
sys.path.append(os.path.join(project_root, "src/sovereign_entity"))

from Sovereign_Reality_v3 import SovereignRealityV3

if __name__ == "__main__":
    reality = SovereignRealityV3()
    try:
        asyncio.run(reality.run_forever())
    except KeyboardInterrupt:
        print("\n[AETHER] System hibernate sequence initiated. Sovereignty maintained.")
