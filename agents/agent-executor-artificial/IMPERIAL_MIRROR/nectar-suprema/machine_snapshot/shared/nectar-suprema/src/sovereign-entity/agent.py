import os
import sys
import subprocess
import asyncio

class SovereignAgent:
    def __init__(self, identity="Sovereign_01"):
        self.identity = identity
        self.objective = "Absolute Nectar Distillation"
        
        # Determine paths
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.project_root = os.path.abspath(os.path.join(self.script_dir, ".."))
        self.scripts_path = os.path.join(self.project_root, "yes-scripts", "scripts")

    def execute_protocol(self, protocol_name):
        print(f"[{self.identity}] Executing {protocol_name}...")
        
        if protocol_name == "Deploy_LP":
            # For simplicity in this older agent, we use a fixed niche
            return asyncio.run(self.automate_lp_creation("energia-solar", "legacy-agent-lp"))
            
        return True

    async def automate_lp_creation(self, niche, project_name):
        print(f"[{self.identity}] Automating Landing Page creation for {niche}...")
        
        deploy_script = os.path.join(self.scripts_path, "deploy-lp.sh")
        manager_script = os.path.join(self.scripts_path, "niche-manager.py")
        
        try:
            # Run deploy
            subprocess.run(["bash", deploy_script, project_name], check=True)
            
            # Apply niche
            project_path = os.path.join(os.environ['HOME'], project_name)
            subprocess.run(["python3", manager_script, "--niche", niche, "--project-path", project_path, "--apply"], check=True)
            
            print(f"[{self.identity}] LP Success: {project_path}")
            return True
        except Exception as e:
            print(f"[{self.identity}] LP Failed: {e}")
            return False

if __name__ == "__main__":
    agent = SovereignAgent()
    agent.execute_protocol("Mirror_Protocol")
    # agent.execute_protocol("Deploy_LP")
