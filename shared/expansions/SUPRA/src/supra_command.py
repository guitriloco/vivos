import asyncio
from intelligence_fusion_v2 import IntelligenceFusionV2
from mutation_loop import MutationLoop

class SupraCommand:
    """
    Production-ready Command Overlord (SUPRA).
    Manages multi-model fusion and self-mutation.
    """
    def __init__(self):
        self.fusion = IntelligenceFusionV2()
        self.evolution = MutationLoop()
        print("[SUPRA] Production Module Initialized.")

    async def run_ascension_check(self, telemetry, yield_report):
        print(f"[SUPRA] Initiating Strategic Ascension Check...")
        
        # 1. Fuse Strategic Inputs
        strategy = self.fusion.fuse_sovereign_strategy(
            claude_input=telemetry.get('analysis', ""),
            gemini_input=yield_report.get('insights', "")
        )
        
        print(f"[SUPRA] Strategy Fusion Complete. Synergy: {strategy['synergy_score']:.2f}")
        
        # 2. Trigger Evolution if threshold met
        if strategy['mutation_required']:
            print("[SUPRA] System-wide Mutation Required. Engaging Evolution Engine...")
            target = "WRAITH_ENGINE" # Example target
            log_path = await self.evolution.execute_evolution(target, telemetry.get('bottlenecks', "NONE"))
            strategy['evolution_staged'] = log_path
        else:
            print("[SUPRA] Current architecture stable. No mutation needed.")
            
        return strategy

if __name__ == "__main__":
    # Simulated run
    supra = SupraCommand()
    dummy_telemetry = {
        "analysis": "Wraith engine is experiencing latency in mesh-sync operations.",
        "bottlenecks": "High memory allocation in signal.proto handling"
    }
    dummy_yield = {
        "insights": "Current data siphoning rate is 30%. Potential for 45% if mesh-sync is optimized."
    }
    asyncio.run(supra.run_ascension_check(dummy_telemetry, dummy_yield))
