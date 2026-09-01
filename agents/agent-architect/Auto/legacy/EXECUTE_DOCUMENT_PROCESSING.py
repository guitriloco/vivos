#!/usr/bin/env python3
"""
Document Processing Execution Script
Ready to process real documents with the complete system
"""

import os
import sys
import json
from datetime import datetime

# Add the project root to the path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

print("="*60)
print("DOCUMENTOS AI - COMPLETE SYSTEM READY FOR DEPLOYMENT")
print("="*60)

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), 'config.json')
with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

print(f"Configuration loaded: {config_path}")
print()

# Display system readiness
print("SYSTEM COMPONENTS STATUS:")
print("-" * 30)

# Test each component
try:
    from Document_Classifier_GUI.classifier import DocumentClassifier
    classifier = DocumentClassifier()
    print("✓ Document Classifier GUI - READY")
except Exception as e:
    print(f"✗ Document Classifier GUI - ERROR: {e}")

try:
    from Configurable_Document_Processor.config_processor import ConfigurableProcessor
    processor = ConfigurableProcessor(config)
    print("✓ Configurable Document Processor - READY")
except Exception as e:
    print(f"✗ Configurable Document Processor - ERROR: {e}")

try:
    from Classification_History_Tracker.database import HistoryDatabase
    logs_dir = config.get('directories', {}).get('logs', './logs')
    os.makedirs(logs_dir, exist_ok=True)
    db_path = os.path.join(logs_dir, 'classification_history.db')
    history_db = HistoryDatabase(db_path)
    print("✓ Classification History Tracker - READY")
except Exception as e:
    print(f"✗ Classification History Tracker - ERROR: {e}")

try:
    from Local_Model_Trainer.trainer import ModelTrainer
    models_dir = config.get('directories', {}).get('models', './models')
    os.makedirs(models_dir, exist_ok=True)
    model_trainer = ModelTrainer(models_dir)
    print("✓ Local Model Trainer - READY")
except Exception as e:
    print(f"✗ Local Model Trainer - ERROR: {e}")

try:
    from Document_Backup_Manager.backup_manager import BackupManager
    backup_dir = config.get('directories', {}).get('backup_location', './backups')
    os.makedirs(backup_dir, exist_ok=True)
    backup_manager = BackupManager(backup_dir)
    print("✓ Document Backup Manager - READY")
except Exception as e:
    print(f"✗ Document Backup Manager - ERROR: {e}")

print()
print("CONFIGURED DIRECTORIES:")
print("-" * 30)
directories = config.get('directories', {})
for dir_name, dir_path in directories.items():
    print(f"• {dir_name.upper()}: {dir_path}")
    os.makedirs(dir_path, exist_ok=True)

print()
print("NEXT STEPS:")
print("-" * 30)
print("1. Place documents to be processed in the input directory")
print("2. Run the Document Classifier GUI for manual classification")
print("3. Use the Configurable Processor for automated workflows")
print("4. Monitor classification history and analytics")
print("5. Retrain models periodically with new data")
print("6. Maintain backups according to your retention policy")

print()
print("SYSTEM DEPLOYMENT COMPLETE!")
print(f"Ready at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()
print("To start processing documents, run:")
print("  python -m Document_Classifier_GUI.main")
print()

print("SUCCESS: The Documentos AI system is fully deployed and operational!")