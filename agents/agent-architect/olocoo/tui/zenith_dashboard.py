import os
import sys
import time

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        while True:
            clear_screen()
            print("====================================================")
            print("      ZENITH: SOVEREIGN EXTRACTION ENGINE         ")
            print("====================================================")
            print(f"Status: RUNNING")
            print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print("----------------------------------------------------")
            print("Real-time Extraction Feed:")
            print("[10:15:02] SHADOW_INFILTRATOR -> target_alpha -> 45KB [OK]")
            print("[10:15:05] SHADOW_INFILTRATOR -> target_beta  -> 12KB [OK]")
            print("[10:15:10] ZENITH_CORE -> Processing fragments...")
            print("----------------------------------------------------")
            print("Mesh Status: Wraith-Link CONNECTED")
            print("Throughput: 1.2 MB/s")
            print("Synergy Score: 0.88")
            print("====================================================")
            print("Press Ctrl+C to exit")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\nExiting Zenith TUI...")

if __name__ == "__main__":
    main()
