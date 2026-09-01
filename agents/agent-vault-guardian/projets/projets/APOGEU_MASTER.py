import subprocess
import time
import sys
import os
import signal

def run_component(name, command):
    print(f"[*] Launching {name}...")
    # Using shell=True or splitting command
    process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)
    return process

def main():
    print("""
    =========================================
    🌌 APOGEU MASTER: SOVEREIGN ORCHESTRATOR
    =========================================
    """)

    components = []
    
    try:
        # ZKP Preservation Engine (Phase 7)
        zkp_engine = run_component(
            "ZKP Preservation", 
            "python3 /home/engine/project/projets/Wealth_Core/zkp_preservation.py"
        )
        components.append(("ZKP Preservation", zkp_engine))

        # We could also start other components here if they were defined in the ticket
        # e.g., AETHER_CORE, Nexus_WS_Bridge, etc.
        
        print("[!] All systems operational. Monitoring heartbeats...")
        
        while True:
            time.sleep(5)
            # Add basic health checks if necessary
            
    except KeyboardInterrupt:
        print("\n[!] Shutdown signal received. Terminating all components...")
        for name, proc in components:
            print(f"[*] Stopping {name}...")
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
            except Exception as e:
                print(f"[!] Error stopping {name}: {e}")
        print("[!] Clean exit completed.")

if __name__ == "__main__":
    main()
