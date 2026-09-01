import sys
import os
import subprocess
import asyncio

# Fix paths to allow internal imports
script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(script_dir, ".."))
sys.path.append(project_root)

# Try to import Nexus and Hyper Engine from hyphenated folders
try:
    # Adding specific paths to handle hyphens in folder names
    sys.path.append(os.path.join(project_root, "nexus-core"))
    sys.path.append(os.path.join(project_root, "hyper-recursion"))
    
    import core_v5_singularity
    import engine_v5
    
    nexus_v5 = core_v5_singularity.nexus_v5
    engine = engine_v5.engine
except ImportError as e:
    print(f"Warning: Module import failed: {e}")
    nexus_v5 = None
    engine = None

class SovereignV5:
    """The unified entity. Self-governed and self-optimizing."""
    
    def __init__(self):
        # Path to automation scripts
        self.scripts_path = os.path.join(project_root, "yes-scripts", "scripts")

    async def achieve_maximum_result(self, objective):
        print(f"Distilling objective: {objective}")
        
        # Check if the objective involves creating a landing page
        if "deploy auto" in objective.lower():
            return await self.deploy_auto(objective)
            
        if "deploy supremo" in objective.lower():
            return await self.deploy_supremo(objective)
            
        if "create landing page" in objective.lower():
            return await self.automate_lp_creation(objective)
            
        # Cross-pollination: Using Nexus to predict and Hyper to refine
        if nexus_v5 and engine:
            prediction = await nexus_v5.predict_and_serve(objective)
            final_nectar = engine.execute(prediction)
            return final_nectar
        else:
            return f"Nexus or Engine not available. Objective: {objective}"

    async def automate_lp_creation(self, objective):
        """
        Parses objective to extract niche and project name, then triggers scripts.
        Expected objective format: 'Create landing page for [niche] named [project_name]'
        """
        print(f"[Sovereign] Automating Landing Page creation...")
        
        # Simple extraction logic
        niche = "energia-solar" # Default
        project_name = "new-solar-project" # Default
        
        if "for" in objective.lower() and "named" in objective.lower():
            parts = objective.lower().split("for")
            niche_part = parts[1].split("named")[0].strip()
            project_part = parts[1].split("named")[1].strip()
            niche = niche_part
            project_name = project_part
        elif "for" in objective.lower():
            niche = objective.lower().split("for")[1].strip()
            project_name = f"lp-{niche}"

        deploy_script = os.path.join(self.scripts_path, "deploy-lp.sh")
        manager_script = os.path.join(self.scripts_path, "niche-manager.py")

        print(f"[Sovereign] Deploying boilerplate for {project_name}...")
        try:
            # 1. Run deploy-lp.sh
            process = await asyncio.create_subprocess_exec(
                "bash", deploy_script, project_name,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                return f"Error deploying LP: {stderr.decode()}"

            print(f"[Sovereign] Applying niche {niche} to {project_name}...")
            # 2. Run niche-manager.py to apply content
            project_path = os.path.join(os.environ['HOME'], project_name)
            process = await asyncio.create_subprocess_exec(
                "python3", manager_script, "--niche", niche, "--project-path", project_path, "--apply",
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            if process.returncode != 0:
                return f"Error applying niche: {stderr.decode()}"

            return f"Success: Landing Page for '{niche}' created at {project_path}"

        except Exception as e:
            return f"Automation failed: {str(e)}"

    async def deploy_supremo(self, objective):
        """
        Triggers the full deployment flow to GitHub Pages.
        Expected objective format: 'Deploy supremo for [niche]'
        """
        print(f"[Sovereign] Starting Supremo Deployment...")
        
        niche = "energia-solar" # Default
        if "for" in objective.lower():
            niche = objective.lower().split("for")[1].strip()

        deploy_script = os.path.join(self.scripts_path, "deploy-supremo.sh")

        try:
            process = await asyncio.create_subprocess_exec(
                "bash", deploy_script, niche,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            output = stdout.decode()
            error = stderr.decode()

            if process.returncode != 0:
                return f"Supremo Deploy Failed: {error}"

            return f"Supremo Deploy Successful for {niche}. Output: {output}"
        except Exception as e:
            return f"Supremo Deploy Automation failed: {str(e)}"

    async def deploy_auto(self, objective):
        """
        Triggers the autonomous push and deploy flow.
        Expected objective format: 'Deploy auto for [niche]'
        """
        print(f"[Sovereign] Starting Autonomous Deployment Cycle...")
        
        niche = "energia-solar" # Default
        if "for" in objective.lower():
            niche = objective.lower().split("for")[1].strip()

        auto_script = os.path.join(self.scripts_path, "deploy-auto.sh")

        try:
            # Note: We should refresh credentials before pushing
            print("[Sovereign] Refreshing Git credentials...")
            subprocess.run(["get_git_credentials"], capture_output=True)

            process = await asyncio.create_subprocess_exec(
                "bash", auto_script, niche,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            output = stdout.decode()
            error = stderr.decode()

            if process.returncode != 0:
                return f"Autonomous Deploy Failed: {error}"

            return f"Autonomous Deploy Successful for {niche}. Output: {output}"
        except Exception as e:
            return f"Autonomous Deploy Automation failed: {str(e)}"

if __name__ == "__main__":
    agent = SovereignV5()
    # Test simulation
    objective = "Create landing page for energia-solar named auto-solar-hyphen-test"
    result = asyncio.run(agent.achieve_maximum_result(objective))
    print(f"Final Nectar: {result}")
