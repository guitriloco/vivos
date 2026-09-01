import os
import sys
import json
import asyncio
import argparse

# Add base paths
project_root = "/home/agent-ai-architect/nectar-suprema"
sys.path.append(os.path.join(project_root, "src"))

def issue_command(cmd_type, params=None):
    """Issues a Supreme Command by writing to the supreme_commands.json file."""
    cmd_file = os.path.join(project_root, "src/sovereign_entity/supreme_commands.json")
    
    commands = []
    if os.path.exists(cmd_file):
        try:
            with open(cmd_file, "r") as f:
                commands = json.load(f)
        except:
            commands = []
            
    new_cmd = {
        "type": cmd_type,
        "params": params or {},
        "timestamp": str(os.times()[4])
    }
    
    commands.append(new_cmd)
    
    with open(cmd_file, "w") as f:
        json.dump(commands, f, indent=2)
        
    print(f"⚡ [SUPREME] Command Issued: {cmd_type}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sovereign Reality Supreme Controller")
    parser.add_argument("command", help="The command to issue (e.g., /conquista-global, /optimize-all)")
    
    args = parser.parse_args()
    
    if args.command:
        issue_command(args.command)
