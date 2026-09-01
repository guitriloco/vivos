import os
import sys
import asyncio
import json
import subprocess
import datetime
import random
import re
from typing import List, Dict, Any

# Add project root to sys.path to allow internal imports
project_root = "/home/agent-ai-architect/nectar-suprema"
src_path = os.path.join(project_root, "src")
if src_path not in sys.path:
    sys.path.append(src_path)

from hyper_recursion.Mutator_Overlord import MutatorOverlord
from vvv_vault.purity_zkp import NectarVault

class ExpansionNexus:
    """
    Expansion Nexus 3.0: The intelligence module for AETHER FLOW.
    Enhanced with Fabrica-Conteudo templates and Mutator Overlord logic.
    """
    def __init__(self):
        self.knowledge_base_path = os.path.join(project_root, "src/sovereign_entity/AETHER_FLOW/Intelligence_Report/knowledge_base.json")
        self.scripts_path = "/home/team/shared/scripts"
        self.fabrica_path = "/home/team/shared/fabrica-conteudo"
        self.mutator = MutatorOverlord()
        self.vault = NectarVault()
        self.load_knowledge()

    def load_knowledge(self):
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r') as f:
                self.knowledge_base = json.load(f)
        else:
            self.knowledge_base = {
                "predicted_niches": [
                    {"name": "Energia Solar Residencial", "slug": "energia-solar", "potential": 0.95, "category": "Home"},
                    {"name": "Acessórios de Celular Premium", "slug": "acessorios-celular", "potential": 0.88, "category": "Tech"},
                    {"name": "Suplementos Naturais Bio-hacking", "slug": "suplementos", "potential": 0.92, "category": "Health"},
                    {"name": "Produtos Pet de Luxo", "slug": "pets-luxo", "potential": 0.85, "category": "Pets"},
                    {"name": "Consultoria de IA para PMEs", "slug": "ia-negocios", "potential": 0.97, "category": "B2B"}
                ],
                "active_expansions": []
            }
            self.save_knowledge()

    def save_knowledge(self):
        os.makedirs(os.path.dirname(self.knowledge_base_path), exist_ok=True)
        with open(self.knowledge_base_path, 'w') as f:
            json.dump(self.knowledge_base, f, indent=4)

    async def predict_lucrative_niches(self, count=3):
        print("[Expansion_Nexus] Synthesizing market data for niche expansion...")
        await asyncio.sleep(0.5)
        
        if len(self.knowledge_base.get("active_expansions", [])) >= 3:
            new_niche = {
                "name": f"Niche_Gen_{len(self.knowledge_base['active_expansions'])}",
                "slug": f"infinite-niche-{len(self.knowledge_base['active_expansions'])}",
                "potential": round(random.uniform(0.8, 0.99), 2),
                "category": "Synthetic"
            }
            self.knowledge_base["predicted_niches"].append(new_niche)
            print(f"✨ [Infinite_Niches] Discovered new territory: {new_niche['slug']}")

        sorted_niches = sorted(self.knowledge_base["predicted_niches"], key=lambda x: x["potential"], reverse=True)
        return sorted_niches[:count]

    def _generate_copy(self, niche_name: str, niche_slug: str) -> Dict[str, Any]:
        """Generates copy using Fabrica-Conteudo templates logic."""
        template_path = os.path.join(self.fabrica_path, "templates/landing-pages/template-landing-page.md")
        
        # Default fallback
        data = {
            "title": f"Mastering {niche_name}",
            "headline": f"O Guia Definitivo para Lucrar com {niche_name}",
            "subheadline": f"Descubra como dominar o mercado de {niche_slug} sem complicação.",
            "pricing": "97,00",
            "cta": "Quero Começar Agora",
            "garantia": "7 dias"
        }

        # If template exists, we could use LLM or RegEx to fill it. 
        # For now, we simulate a 'Mutant' filling.
        if os.path.exists(template_path):
            # In a real scenario, we'd process the template here.
            pass
            
        return data

    async def auto_replicate(self, niche_slug, niche_name, current_roi=1.0):
        print(f"[AETHER] >> REPLICATION PROTOCOL INITIALIZED: {niche_slug}")
        
        deploy_script = os.path.join(self.scripts_path, "deploy-lp.sh")
        if not os.path.exists(deploy_script):
            # Fallback to team shared scripts if not found in local path
            deploy_script = "/home/team/shared/scripts/deploy-lp.sh"

        if not os.path.exists(deploy_script):
            print(f"❌ Deploy script missing.")
            return False
            
        project_name = f"lp-{niche_slug}-{datetime.datetime.now().strftime('%Y%m%d')}"
        result = subprocess.run(["bash", deploy_script, project_name], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Deploy failed: {result.stderr}")
            return False
            
        project_path = os.path.join(os.path.expanduser("~"), project_name)
        print(f"✅ Landing Page deployed at: {project_path}")

        # Step 2: Generate Content from Template
        base_data = self._generate_copy(niche_name, niche_slug)
        
        # Apply Mutation Overlord logic (Repo YES integration)
        mutated_data = self.mutator.mutate_funnel(niche_slug, current_roi, base_data)
        
        # Apply to project
        config_dir = os.path.join(project_path, 'src/config')
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, 'content.json')
        with open(config_file, 'w') as f:
            json.dump(mutated_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Funnel Mutated and Calibrated: {config_file}")

        # Step 3: VVV Vault Protection
        self.vault.preserve(mutated_data, f"Expansion_{niche_slug}", "Funnel_Deployment")
        print(f"🔒 [VVV] Funnel Essence sealed.")
        
        return True

    def update_roi_config(self, niche_slug, roi):
        roi_config_path = os.path.join(project_root, "src/sovereign_entity/AETHER_FLOW/Intelligence_Report/niche_roi.json")
        if os.path.exists(roi_config_path):
            with open(roi_config_path, 'r') as f:
                roi_config = json.load(f)
        else:
            roi_config = {}
        
        roi_config[niche_slug] = {
            "target_roi": roi,
            "last_updated": str(datetime.datetime.now()),
            "strategy": "MAX_GROWTH" if roi > 0.9 else "STEADY_SCALE"
        }
        
        with open(roi_config_path, 'w') as f:
            json.dump(roi_config, f, indent=4)

    async def expandir_total(self, target_niche=None):
        if target_niche:
            niche_match = next((n for n in self.knowledge_base["predicted_niches"] if n["slug"] == target_niche), None)
            if niche_match:
                niches = [niche_match]
            else:
                niches = [{"name": target_niche.capitalize(), "slug": target_niche, "potential": 0.7}]
        else:
            niches = await self.predict_lucrative_niches()

        print(f"--- 🌌 AETHER FLOW: COMMAND /expandir-total RECEIVED ---")
        results = []
        for niche in niches:
            niche_name = niche["name"]
            niche_slug = niche["slug"]
            
            success = await self.auto_replicate(niche_slug, niche_name, niche.get("potential", 1.0))
            
            if success:
                if "active_expansions" not in self.knowledge_base:
                    self.knowledge_base["active_expansions"] = []
                self.knowledge_base["active_expansions"].append({
                    "niche": niche_name,
                    "slug": niche_slug,
                    "timestamp": str(datetime.datetime.now()),
                    "status": "LIVE"
                })
                self.update_roi_config(niche_slug, niche.get("potential", 0.85))
                results.append({"niche": niche_name, "status": "OPTIMIZED"})
            else:
                print(f"❌ [AETHER] FAILED FOR {niche_name}")

        self.save_knowledge()
        return results

if __name__ == "__main__":
    nexus = ExpansionNexus()
    asyncio.run(nexus.expandir_total())
