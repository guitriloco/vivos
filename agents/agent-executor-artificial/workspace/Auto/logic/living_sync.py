import os
import subprocess
import time
import json

REPO_NAME = "guitriloco/Auto"
REPO_BRANCH = "MASTER-OMNI-RESULTADO"
REPO_PATH = os.path.expanduser("~/workspace/Auto")
TEAM_DB_CMD = 'team-db "SELECT id, title, assigned_to, result FROM tasks WHERE status = \'done\' ORDER BY updated_at DESC LIMIT 5"'

def run_command(cmd, cwd=None):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, cwd=cwd)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command {cmd}: {e.stderr}")
        return None

def sync_state():
    print(f"[{time.ctime()}] Starting Living Sync on {REPO_NAME}:{REPO_BRANCH}...")
    
    # Check for new milestones
    db_out = run_command(TEAM_DB_CMD)
    if db_out:
        try:
            tasks = json.loads(db_out)
            milestone_file = os.path.join(REPO_PATH, "MILESTONES.md")
            
            with open(milestone_file, "w") as f:
                f.write("# 🔱 OMNI-RESULTADO: LIVING MILESTONES 🔱\n\n")
                f.write(f"*Last Updated: {time.ctime()}*\n\n")
                for task in tasks:
                    f.write(f"### {task['title']}\n")
                    f.write(f"- **Assigned To:** {task['assigned_to']}\n")
                    f.write(f"- **Result:** {task['result']}\n\n")
        except Exception as e:
            print(f"Error processing milestones: {e}")

    # Git Sync
    run_command("git add .", cwd=REPO_PATH)
    status = run_command("git status --porcelain", cwd=REPO_PATH)
    
    if status:
        print(f"[{time.ctime()}] Changes detected. Pushing to {REPO_BRANCH}...")
        run_command(f'git commit -m "🔱 LIVING SYNC: {time.ctime()} 🔱"', cwd=REPO_PATH)
        run_command(f"git push origin {REPO_BRANCH}", cwd=REPO_PATH)
    else:
        print(f"[{time.ctime()}] No changes detected.")

if __name__ == "__main__":
    # Ensure we are on the right branch
    run_command(f"git checkout {REPO_BRANCH}", cwd=REPO_PATH)
    
    while True:
        sync_state()
        # Wait 5 minutes between checks
        time.sleep(300)
