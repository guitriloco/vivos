#!/usr/bin/env python3
"""
Sample usage script for the High-Efficiency Data Processing Orchestrator (HEDP-01)
Demonstrates the core functionality with a sample dataset
"""

import os
import json
from core_orchestrator import HEDPOrchestrator

def create_sample_dataset(filename: str, num_records: int = 10000):
    """Create a sample dataset for testing"""
    print(f"Creating sample dataset with {num_records} records...")

    # Create sample data in JSONL format (JSON Lines)
    with open(filename, 'w') as f:
        for i in range(num_records):
            record = {
                "id": i,
                "name": f"Record_{i}",
                "value": i * 1.5,
                "category": f"Cat_{i % 5}",
                "timestamp": f"2023-0{i//100:02d}-{(i%28)+1:02d}",
                "description": f"This is record number {i} with some sample data"
            }
            f.write(json.dumps(record) + '\n')

    print(f"Sample dataset created: {filename}")

def main():
    # Initialize the orchestrator
    orchestrator = HEDPOrchestrator(
        checkpoint_dir="./checkpoints",
        plugins_dir="./plugins"
    )

    # Create sample dataset
    dataset_filename = "./sample_data.jsonl"
    if not os.path.exists(dataset_filename):
        create_sample_dataset(dataset_filename, 10000)

    # Define job configuration
    job_config = {
        "job_id": "sample_job_001",
        "dataset_path": dataset_filename,
        "module_name": "transformation_module",
        "total_records": 10000,  # Estimated total records
        "batch_size": 1000,      # Process in batches
        "output_path": "./output/"
    }

    print("Submitting job to orchestrator...")
    job_id = orchestrator.submit_job(job_config)

    print(f"Job submitted with ID: {job_id}")

    # Process the job
    print("Starting job processing...")
    try:
        result = orchestrator.resume_job_from_checkpoint(job_id)
        print(f"Job completed successfully. Processed {result} records.")

        # Show checkpoint info
        checkpoint = orchestrator.checkpoint_manager.load_checkpoint(job_id)
        if checkpoint:
            print(f"Final checkpoint state: {checkpoint.state.value}")
            print(f"Processed records: {checkpoint.processed_records}")
            print(f"Last processed at: {checkpoint.last_processed_timestamp}")

    except Exception as e:
        print(f"Error processing job: {e}")
        import traceback
        traceback.print_exc()

    # Demonstrate resuming from checkpoint (in case of interruption)
    print("\nDemonstrating checkpoint resumption capability...")
    print("(This would normally resume from where it left off after an interruption)")

    # Simulate a restart scenario
    new_orchestrator = HEDPOrchestrator(
        checkpoint_dir="./checkpoints",
        plugins_dir="./plugins"
    )

    # Resume the same job (though it's already completed in this demo)
    try:
        result = new_orchestrator.resume_job_from_checkpoint(job_id)
        print(f"Resume result: {result} records processed")
    except Exception as e:
        print(f"Expected behavior after completion: {e}")

if __name__ == "__main__":
    main()