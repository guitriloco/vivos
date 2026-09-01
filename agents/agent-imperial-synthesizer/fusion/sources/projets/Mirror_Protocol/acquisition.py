import subprocess
import os

class AcquisitionEngine:
    def __init__(self, base_path="/home/agent-engineer"):
        self.version = "2.1"
        self.base_path = base_path
        self.discovered_repos = [
            "vvv", "project-2.0", "Auto", "terax-ai", "fabrica-conteudo", "Nov",
            "agent-skills", "cto.new", "openhuman", "olocoo", "projets", 
            "nectar-suprema", "Nectar_Dev", "Nectar_Empire_Lattice", "Nectar_Wealth"
        ]

    def acquire_all(self):
        print("--- 🛰️ MIRROR PROTOCOL: ACQUISITION ENGINE ---")
        for repo in self.discovered_repos:
            target_dir = os.path.join(self.base_path, repo)
            if not os.path.exists(target_dir):
                print(f"[ACQUISITION] New nectar source detected: {repo}")
                repo_url = f"https://github.com/guitriloco/{repo}.git"
                try:
                    subprocess.run(["git", "clone", repo_url, target_dir], check=True)
                    print(f"[SUCCESS] Acquired {repo}")
                except Exception as e:
                    print(f"[ERROR] Failed to acquire {repo}: {e}")
            else:
                print(f"[ACQUISITION] Source already present: {repo}")
                # Pull updates
                try:
                    subprocess.run(["git", "-C", target_dir, "pull"], check=True)
                    print(f"[SUCCESS] Updated {repo}")
                except Exception as e:
                    print(f"[ERROR] Failed to update {repo}: {e}")

    def push_improvements(self, repo_name, commit_message="[SOVEREIGN] Automated optimization and nectar distillation"):
        print(f"--- 🚀 MIRROR PROTOCOL: PUSH ENGINE [{repo_name}] ---")
        target_dir = os.path.join(self.base_path, repo_name)
        if not os.path.exists(target_dir):
            print(f"[ERROR] Repository {repo_name} not found locally.")
            return

        try:
            # Stage all changes
            subprocess.run(["git", "-C", target_dir, "add", "."], check=True)
            # Check if there are changes to commit
            status = subprocess.run(["git", "-C", target_dir, "status", "--porcelain"], capture_output=True, text=True)
            if not status.stdout.strip():
                print(f"[PUSH] No changes detected in {repo_name}. Skipping.")
                return

            subprocess.run(["git", "-C", target_dir, "commit", "-m", commit_message], check=True)
            subprocess.run(["git", "-C", target_dir, "push"], check=True)
            print(f"[SUCCESS] Pushed improvements to {repo_name}")
        except Exception as e:
            print(f"[ERROR] Failed to push to {repo_name}: {e}")

if __name__ == "__main__":
    engine = AcquisitionEngine()
    engine.acquire_all()
    # Example push (can be triggered by Sovereign logic)
    # engine.push_improvements("NECTAR_SYNC_TEST", "Sync test")
