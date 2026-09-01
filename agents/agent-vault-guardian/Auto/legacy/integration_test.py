"""
Integration Test
Test that all components work together
"""

import os
import sys
import json

# Add the project root to the path
sys.path.append(os.path.join(os.path.dirname(__file__)))

def test_integration():
    print("Testing Integration of All Components")
    print("=" * 50)

    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print("OK Configuration loaded")
    except Exception as e:
        print(f"ERROR Configuration error: {e}")
        return False

    # Test Document Classifier GUI
    try:
        from Document_Classifier_GUI.classifier import DocumentClassifier
        classifier = DocumentClassifier()
        print("OK Document Classifier GUI module loaded")
    except Exception as e:
        print(f"ERROR Document Classifier GUI error: {e}")
        return False

    # Test Configurable Document Processor
    try:
        from Configurable_Document_Processor.config_processor import ConfigurableProcessor
        processor = ConfigurableProcessor(config)
        print("OK Configurable Document Processor module loaded")
    except Exception as e:
        print(f"ERROR Configurable Document Processor error: {e}")
        return False

    # Test Classification History Tracker
    try:
        from Classification_History_Tracker.database import HistoryDatabase
        from Classification_History_Tracker.analytics import AnalyticsEngine

        logs_dir = config.get('directories', {}).get('logs', './logs')
        os.makedirs(logs_dir, exist_ok=True)

        db_path = os.path.join(logs_dir, 'test_integration.db')
        history_db = HistoryDatabase(db_path)
        analytics = AnalyticsEngine(history_db)
        print("OK Classification History Tracker modules loaded")
    except Exception as e:
        print(f"ERROR Classification History Tracker error: {e}")
        return False

    # Test Local Model Trainer
    try:
        from Local_Model_Trainer.model import DocumentClassificationModel
        from Local_Model_Trainer.trainer import ModelTrainer

        models_dir = config.get('directories', {}).get('models', './models')
        os.makedirs(models_dir, exist_ok=True)

        trainer = ModelTrainer(models_dir)
        print("OK Local Model Trainer modules loaded")
    except Exception as e:
        print(f"ERROR Local Model Trainer error: {e}")
        return False

    # Test Document Backup Manager
    try:
        from Document_Backup_Manager.backup_manager import BackupManager

        backup_dir = config.get('directories', {}).get('backup_location', './backups')
        os.makedirs(backup_dir, exist_ok=True)

        backup_manager = BackupManager(backup_dir)
        print("OK Document Backup Manager module loaded")
    except Exception as e:
        print(f"ERROR Document Backup Manager error: {e}")
        return False

    print("\nOK All components loaded successfully!")
    print("Integration test passed!")
    return True

if __name__ == "__main__":
    success = test_integration()
    if success:
        print("\nALL SYSTEMS OPERATIONAL! The document processing suite is ready for use.")
    else:
        print("\nSOME COMPONENTS FAILED TO LOAD. Please check the errors above.")