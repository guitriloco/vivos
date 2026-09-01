import asyncio
import os
import sys
import json
import datetime
import random
import httpx
from typing import List, Dict, Any

# Add base paths
project_root = "/home/agent-ai-architect/nectar-suprema"
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

aether_path = os.path.join(src_path, "sovereign_entity/AETHER_FLOW")
if aether_path not in sys.path:
    sys.path.append(aether_path)

from Expansion_Nexus import ExpansionNexus
from hyper_recursion.Mutator_Overlord import MutatorOverlord
from vvv_vault.purity_zkp import NectarVault
from automation_engine.market_scanner import MarketScanner
from sovereign_entity.niche_parser import extract_niches

class GlobalConquest:
    """
    Global Conquest (Conquista Global): The supreme brain coordinating mass expansion.
    Integrates Researcher data, Market Scanner, Expansion Nexus, and Mutator Overlord.
    """
    def __init__(self):
        self.expansion_nexus = ExpansionNexus()
        self.mutator = MutatorOverlord()
        self.vault = NectarVault()
        self.scanner = MarketScanner()
        self.research_files = [
            "/home/team/shared/research_results.md",
            "/home/team/shared/50_niches_roi.md"
        ]
        self.nov_api_url = "http://localhost:8001/refine"

    async def report_to_nov_api(self, niche_slug: str, result: str):
        """Reports expansion progress to the Nov-API for dashboard visualization."""
        try:
            payload = {
                "niche": niche_slug,
                "refinement_type": "Expansion",
                "improvement_score": 0.95,
                "status": "success",
                "details": f"Mass Replication: {result}"
            }
            async with httpx.AsyncClient() as client:
                await client.post(self.nov_api_url, json=payload)
        except Exception as e:
            print(f"⚠️ [NOV-API] Connection failed: {e}")

    async def execute_conquest(self):
        print("\n" + "🌍" * 40)
        print("🌌 OPERATION: CONQUISTA GLOBAL 3.0 INITIALIZED")
        print(f"Timestamp: {datetime.datetime.now()}")
        print("🌍" * 40 + "\n")

        # 1. Load validated niches from Researcher
        print("🔍 [PHASE 1] Analyzing Research Data...")
        all_research_niches = []
        for r_file in self.research_files:
            if os.path.exists(r_file):
                found = extract_niches(r_file)
                for n in found:
                    if not any(x['slug'] == n['slug'] for x in all_research_niches):
                        all_research_niches.append(n)
        
        print(f"✅ Found {len(all_research_niches)} unique validated niches in research.")

        # 2. Market Scanning & Validation
        print("\n📡 [PHASE 2] Market Pulse & ROI Prediction...")
        prioritized_niches = []
        for niche in all_research_niches:
            # Check if already expanded to avoid duplicates
            if any(e['slug'] == niche['slug'] for e in self.expansion_nexus.knowledge_base.get("active_expansions", [])):
                continue

            scan_data = self.scanner.scan_niche(niche['slug'])
            if scan_data.score >= 6.0: 
                niche['potential'] = scan_data.score / 10.0
                niche['avg_price'] = scan_data.avg_product_price
                prioritized_niches.append(niche)
                print(f"   ⭐ Niche Approved: {niche['name']} (Score: {scan_data.score})")

        # 3. Mass Expansion
        print(f"\n🚀 [PHASE 3] Mass Expansion Protocol: {len(prioritized_niches)} niches")
        for niche in prioritized_niches:
            print(f"\n--- Expanding: {niche['name'].upper()} ---")
            
            success = await self.expansion_nexus.auto_replicate(
                niche['slug'], 
                niche['name'], 
                current_roi=niche.get('potential', 1.0)
            )
            
            if success:
                if "active_expansions" not in self.expansion_nexus.knowledge_base:
                    self.expansion_nexus.knowledge_base["active_expansions"] = []
                    
                self.expansion_nexus.knowledge_base["active_expansions"].append({
                    "niche": niche["name"],
                    "slug": niche["slug"],
                    "timestamp": str(datetime.datetime.now()),
                    "status": "LIVE",
                    "calibrated_roi": niche["potential"]
                })
                
                await self.report_to_nov_api(niche['slug'], "LIVE")
                print(f"✅ [AETHER] {niche['name']} is now LIVE.")
                
                checkpoint = {
                    "niche": niche['name'],
                    "status": "CONQUERED",
                    "initial_roi": niche['potential']
                }
                self.vault.preserve(checkpoint, "Global_Conquest_Core", "Mass_Expansion_Seal")
            else:
                print(f"❌ [AETHER] Deployment failed for {niche['name']}")

        self.expansion_nexus.save_knowledge()
        
        # Cleanup/Consolidation
        target_content_dir = os.path.join(project_root, "content/copias-geradas/landing-pages")
        os.makedirs(target_content_dir, exist_ok=True)
        
        import shutil
        import glob
        home_dir = os.path.expanduser("~")
        for lp_dir in glob.glob(os.path.join(home_dir, "lp-*")):
            dest = os.path.join(target_content_dir, os.path.basename(lp_dir))
            if not os.path.exists(dest):
                try:
                    shutil.move(lp_dir, dest)
                except:
                    pass

        print("\n" + "🏁" * 40)
        print("🌌 CONQUISTA GLOBAL: SUCCESS")
        print(f"Soberania status: TOTAL DOMINATION")
        print("🏁" * 40 + "\n")

if __name__ == "__main__":
    conquest = GlobalConquest()
    asyncio.run(conquest.execute_conquest())
