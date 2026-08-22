"""
MLflow Setup Script
Initialize MLflow tracking server
"""

import os
import json

class MLflowSetup:
    """Setup MLflow for experiment tracking"""

    def __init__(self, base_path):
        self.base_path = base_path
        self.config_path = os.path.join(base_path, 'mlflow_config.json')

    def load_config(self):
        """Load MLflow configuration"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def get_tracking_uri(self):
        """Get MLflow tracking URI"""
        config = self.load_config()
        return config['tracking_uri']

    def get_experiment_name(self):
        """Get experiment name"""
        config = self.load_config()
        return config['experiment_name']

    def initialize_tracking(self):
        """Initialize MLflow tracking"""
        try:
            config = self.load_config()
            print("MLflow configuration loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading MLflow configuration: {str(e)}")
            return False

    def log_model_metadata(self, metadata):
        """Log model metadata"""
        metadata_path = os.path.join(self.base_path, 'model_metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2)
        return metadata_path

# Setup
if __name__ == '__main__':
    setup = MLflowSetup('.')
    success = setup.initialize_tracking()

    if success:
        tracking_uri = setup.get_tracking_uri()
        experiment_name = setup.get_experiment_name()

        print(f"Tracking URI: {tracking_uri}")
        print(f"Experiment: {experiment_name}")
