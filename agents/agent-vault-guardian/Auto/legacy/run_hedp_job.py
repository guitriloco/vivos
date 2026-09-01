#!/usr/bin/env python3
"""
Script to run the HEDP-01 orchestrator with specified parameters
"""
import subprocess
import sys

def run_hedp_job():
    """Run the HEDP orchestrator with the specified parameters"""
    cmd = [
        sys.executable, "launcher.py",
        "--module", "advanced_transformation_module",
        "--dataset-path", "./data/sample_audit.json",
        "--batch-size", "1000"
    ]

    print("Running HEDP-01 with parameters:")
    print("  Module: advanced_transformation_module")
    print("  Dataset: ./data/sample_audit.json")
    print("  Batch size: 1000")
    print(f"Command: {' '.join(cmd)}")
    print()

    try:
        result = subprocess.run(cmd, check=True)
        print(f"\nJob completed successfully with return code: {result.returncode}")
    except subprocess.CalledProcessError as e:
        print(f"\nJob failed with return code: {e.returncode}")
        sys.exit(e.returncode)

if __name__ == "__main__":
    run_hedp_job()