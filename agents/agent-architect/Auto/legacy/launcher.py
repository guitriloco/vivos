#!/usr/bin/env python3
"""
Launcher script for HEDP-01 - High-Efficiency Data Processing Orchestrator
This script initializes the job queue and can be run as a background service
"""

import argparse
import sys
import os
import time
import signal
import logging
from core_orchestrator import HEDPOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('./hedp_service.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description='HEDP-01 Orchestrator Launcher')
    parser.add_argument('--module', type=str, required=True,
                        help='Transformation module name (without .py extension)')
    parser.add_argument('--dataset-path', type=str, required=True,
                        help='Path to the dataset file')
    parser.add_argument('--batch-size', type=int, default=1000,
                        help='Batch size for processing (default: 1000)')
    parser.add_argument('--checkpoint-dir', type=str, default='./checkpoints',
                        help='Directory for checkpoint files (default: ./checkpoints)')
    parser.add_argument('--plugins-dir', type=str, default='./plugins',
                        help='Directory for plugin modules (default: ./plugins)')
    parser.add_argument('--job-id', type=str, default=None,
                        help='Specific job ID (auto-generated if not provided)')

    args = parser.parse_args()

    logger.info(f"Starting HEDP-01 Orchestrator with parameters:")
    logger.info(f"  Module: {args.module}")
    logger.info(f"  Dataset: {args.dataset_path}")
    logger.info(f"  Batch size: {args.batch_size}")
    logger.info(f"  Checkpoint dir: {args.checkpoint_dir}")
    logger.info(f"  Plugins dir: {args.plugins_dir}")

    # Verify dataset exists
    if not os.path.exists(args.dataset_path):
        logger.error(f"Dataset file does not exist: {args.dataset_path}")
        sys.exit(1)

    # Initialize orchestrator
    orchestrator = HEDPOrchestrator(
        checkpoint_dir=args.checkpoint_dir,
        plugins_dir=args.plugins_dir
    )

    # Generate job ID if not provided
    job_id = args.job_id or f"hedp_job_{int(time.time())}"

    # Prepare job configuration
    job_config = {
        "job_id": job_id,
        "dataset_path": args.dataset_path,
        "module_name": args.module,
        "batch_size": args.batch_size,
        "output_path": "./output/",
        "start_time": time.time()
    }

    # Submit job
    logger.info(f"Submitting job: {job_id}")
    submitted_job_id = orchestrator.submit_job(job_config)

    # Process the job
    logger.info(f"Starting processing for job: {submitted_job_id}")
    try:
        result = orchestrator.resume_job_from_checkpoint(submitted_job_id)
        logger.info(f"Job completed successfully. Processed {result} records.")

        # Show final checkpoint info
        checkpoint = orchestrator.checkpoint_manager.load_checkpoint(submitted_job_id)
        if checkpoint:
            logger.info(f"Final state: {checkpoint.state.value}")
            logger.info(f"Processed records: {checkpoint.processed_records}")

    except Exception as e:
        logger.error(f"Error processing job: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    logger.info("HEDP-01 Orchestrator completed successfully")


if __name__ == "__main__":
    main()