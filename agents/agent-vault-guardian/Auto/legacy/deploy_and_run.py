"""
Deployment and Execution Script
Prepare the system for deployment and run a sample document processing workflow
"""

import os
import sys
import json
import shutil
from datetime import datetime

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

from Document_Classifier_GUI.classifier import DocumentClassifier
from Configurable_Document_Processor.config_processor import ConfigurableProcessor
from Classification_History_Tracker.database import HistoryDatabase
from Classification_History_Tracker.analytics import AnalyticsEngine
from Local_Model_Trainer.trainer import ModelTrainer
from Document_Backup_Manager.backup_manager import BackupManager


def setup_deployment_environment():
    """
    Setup the deployment environment with required directories and configurations
    """
    print("Setting up deployment environment...")

    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # Create all required directories
    directories = config.get('directories', {})

    for dir_name, dir_path in directories.items():
        os.makedirs(dir_path, exist_ok=True)
        print(f"  OK Created {dir_name} directory: {dir_path}")

    # Initialize all components
    print("\nInitializing system components...")

    # Initialize backup manager
    backup_manager = BackupManager(directories['backup_location'])
    print("  OK Backup manager initialized")

    # Initialize history database
    history_db = HistoryDatabase(os.path.join(directories['logs'], 'classification_history.db'))
    analytics = AnalyticsEngine(history_db)
    print("  OK History tracker initialized")

    # Initialize document processor
    processor = ConfigurableProcessor(config)
    print("  OK Document processor initialized")

    # Initialize classifier
    classifier = DocumentClassifier()
    print("  OK Document classifier initialized")

    # Initialize model trainer
    model_trainer = ModelTrainer(directories['models'])
    print("  OK Model trainer initialized")

    print("\nOK Deployment environment setup complete!")
    return config, backup_manager, history_db, analytics, processor, classifier, model_trainer


def process_sample_workflow():
    """
    Run a sample document processing workflow
    """
    print("\nRunning sample document processing workflow...")

    # Setup the environment
    config, backup_manager, history_db, analytics, processor, classifier, model_trainer = setup_deployment_environment()

    # Get input directory
    input_dir = config['directories']['documents_input']

    # Create a sample document if none exist
    sample_doc_path = os.path.join(input_dir, 'sample_document.txt')
    if not os.path.exists(sample_doc_path):
        os.makedirs(input_dir, exist_ok=True)
        with open(sample_doc_path, 'w', encoding='utf-8') as f:
            f.write("""
            Sample Financial Document
            ========================

            This document contains financial information related to quarterly earnings.
            It includes revenue reports, profit margins, and budget forecasts.

            The company's financial performance has improved significantly this quarter
            with increased sales and reduced operational costs.
            """)
        print(f"  OK Created sample document: {sample_doc_path}")

    # Step 1: Create backup of the document
    print(f"\nStep 1: Creating backup of {os.path.basename(sample_doc_path)}")
    backup_info = backup_manager.create_backup(
        sample_doc_path,
        backup_name=f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_sample.txt"
    )
    print(f"  OK Backup created: {backup_info['backup_path']}")

    # Step 2: Classify the document
    print(f"\nStep 2: Classifying document")
    classification_result = classifier.classify_document(sample_doc_path)
    print(f"  OK Document classified as: {classification_result}")

    # Step 3: Record classification in history
    print(f"\nStep 3: Recording classification in history")
    record_id = history_db.add_classification(
        document_path=sample_doc_path,
        assigned_category=classification_result,
        classifier_model=classifier.model
    )
    print(f"  OK Classification recorded with ID: {record_id}")

    # Step 4: Process document according to configuration
    print(f"\nStep 4: Processing document with configurable processor")
    results = processor.process_documents(
        input_directory=input_dir,
        profile_name='default'
    )
    print(f"  OK Processing completed: {len(results['processed'])} processed, {len(results['failed'])} failed")

    # Step 5: Generate analytics report
    print(f"\nStep 5: Generating analytics report")
    report = analytics.generate_comprehensive_report()
    print(f"  OK Analytics generated - Total classifications: {report['summary_statistics']['total_classifications']}")

    # Step 6: Train/update model with new data (if sufficient data exists)
    print(f"\nStep 6: Checking if model training is needed")

    # Get recent classifications for potential model retraining
    recent_classifications = history_db.get_recent_classifications(limit=10)

    if len(recent_classifications) >= 5:  # Need minimum data for training
        print("  INFO Sufficient data available for model training")
        # In a real scenario, we would train the model with this data
        # trainer.train_from_history(history_db_path, min_confidence=0.7)
    else:
        print(f"  INFO Insufficient data for model training ({len(recent_classifications)} records)")

    print("\nOK Sample workflow completed successfully!")

    return {
        'backup_info': backup_info,
        'classification_result': classification_result,
        'record_id': record_id,
        'processing_results': results,
        'analytics_report': report
    }


def create_system_summary():
    """
    Create a summary of the deployed system
    """
    print("\nCreating system summary...")

    summary = f"""System Deployment Summary
========================

Deployment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
System Status: Operational
Components Deployed: 5/5

Component Status:
- Document Classifier GUI: Ready
- Configurable Document Processor: Ready
- Classification History Tracker: Ready
- Local Model Trainer: Ready
- Document Backup Manager: Ready

Directories Configured:
- Input: C:/Users/guilh/Desktop/projetos
- Output: C:/Users/guilh/Desktop/projetos/classificados
- Backups: C:/Users/guilh/Desktop/projetos/backups
- Logs: C:/Users/guilh/Desktop/projetos/logs
- Models: C:/Users/guilh/Desktop/projetos/models

Next Steps:
1. Begin processing real documents
2. Monitor classification accuracy
3. Provide feedback to improve models
4. Regularly review analytics reports
5. Retrain models as needed
"""

    summary_path = os.path.join(os.path.dirname(__file__), 'SYSTEM_SUMMARY.txt')
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary)

    print(f"OK System summary saved to: {summary_path}")
    return summary_path


if __name__ == "__main__":
    print("Documentos AI - Deployment and Execution")
    print("=" * 50)

    # Setup deployment environment
    setup_deployment_environment()

    # Run sample workflow
    results = process_sample_workflow()

    # Create system summary
    summary_path = create_system_summary()

    print(f"\nSUCCESS Deployment completed successfully!")
    print(f"REPORT System summary: {summary_path}")
    print(f"INFO Ready to process real documents!")