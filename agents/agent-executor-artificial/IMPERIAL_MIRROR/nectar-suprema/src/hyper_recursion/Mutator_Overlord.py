import time
import random
import json
import os
import sys
from typing import Dict, Any

# Add base paths
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)

from hyper_recursion.harvest_optimizer import HarvestOptimizer

class MutatorOverlord:
    """
    Mutator Overlord: The mutation engine for the sales funnel.
    Adjusts pricing and copy based on ROI signals.
    """
    def __init__(self):
        self.optimizer = HarvestOptimizer()
        self.mutation_log_path = os.path.join(project_root, "src/sovereign_entity/AETHER_FLOW/Intelligence_Report/mutation_log.jsonl")

    def mutate_funnel(self, niche_slug: str, current_roi: float, current_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Calculates and applies mutations to the funnel data.
        """
        print(f"🧬 [MUTATOR] Analyzing {niche_slug} | ROI: {current_roi}")
        
        mutated_data = current_data.copy()
        mutation_applied = False
        
        # 1. Price Mutation
        if current_roi < 0.7: # Low ROI: Decrease price to increase conversion
            old_price = float(mutated_data.get("pricing", "0").replace(",", "."))
            new_price = round(old_price * 0.85, 2)
            mutated_data["pricing"] = str(new_price).replace(".", ",")
            mutation_applied = True
            print(f"   📉 Price mutation: {old_price} -> {new_price}")
        elif current_roi > 1.5: # High ROI: Increase price to maximize profit
            old_price = float(mutated_data.get("pricing", "0").replace(",", "."))
            new_price = round(old_price * 1.15, 2)
            mutated_data["pricing"] = str(new_price).replace(".", ",")
            mutation_applied = True
            print(f"   📈 Price mutation: {old_price} -> {new_price}")

        # 2. Copy Mutation (using HarvestOptimizer logic)
        optimization = self.optimizer.optimize_logic(f"Copy_{niche_slug}", current_roi)
        if optimization["optimization_level"] > 1.2:
            # Shift headline intensity
            if "!" not in mutated_data["headline"]:
                mutated_data["headline"] += "!!!"
                mutation_applied = True
                print(f"   ✍️ Copy mutation: Increased urgency in headline.")

        if mutation_applied:
            self._log_mutation(niche_slug, current_roi, mutated_data)
        
        return mutated_data

    def _log_mutation(self, niche_slug: str, roi: float, data: Dict[str, Any]):
        log_entry = {
            "timestamp": time.time(),
            "niche": niche_slug,
            "roi": roi,
            "new_pricing": data.get("pricing"),
            "mutation_applied": True
        }
        os.makedirs(os.path.dirname(self.mutation_log_path), exist_ok=True)
        with open(self.mutation_log_path, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

if __name__ == "__main__":
    # Test
    overlord = MutatorOverlord()
    test_data = {"pricing": "97,00", "headline": "Aprenda a vender solar"}
    result = overlord.mutate_funnel("energia-solar", 0.6, test_data)
    print(f"Result: {result}")
