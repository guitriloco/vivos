"""
Local Model Trainer
Main application file
"""

import os
import sys
import json
import importlib.util

# Add the current directory to the path to import modules
spec_trainer = importlib.util.spec_from_file_location("trainer", os.path.join(os.path.dirname(__file__), "trainer.py"))
trainer_module = importlib.util.module_from_spec(spec_trainer)
spec_trainer.loader.exec_module(trainer_module)
ModelTrainer = trainer_module.ModelTrainer

spec_model = importlib.util.spec_from_file_location("model", os.path.join(os.path.dirname(__file__), "model.py"))
model_module = importlib.util.module_from_spec(spec_model)
spec_model.loader.exec_module(model_module)
DocumentClassificationModel = model_module.DocumentClassificationModel


def main():
    print("Local Model Trainer")
    print("=" * 40)

    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.json')

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print(f"Configuration loaded from {config_path}")
    except FileNotFoundError:
        print(f"Configuration file not found at {config_path}")
        print("Using default configuration...")
        config = {
            "directories": {
                "documents_input": "C:/Users/guilh/Desktop/projetos",
                "models": "C:/Users/guilh/Desktop/projetos/models"
            }
        }

    # Create model trainer instance
    models_dir = config.get('directories', {}).get('models', './models')
    os.makedirs(models_dir, exist_ok=True)

    trainer = ModelTrainer(models_dir)

    # Example usage
    print(f"\nModel trainer initialized")
    print(f"Models directory: {trainer.models_dir}")

    print("\nReady to train local models based on classification history.")
    print("Use trainer.train_from_history() to start training.")


if __name__ == "__main__":
    main()