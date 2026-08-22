"""
Model Versioning
Manage model versions and stages
"""

import json
import os
from datetime import datetime

class ModelVersion:
    """Manage model versions"""

    def __init__(self, base_path):
        self.base_path = base_path
        self.versions = {}

    def create_version(self, version_id, metrics, stage='Staging'):
        """Create model version"""
        version = {
            'version_id': version_id,
            'created_date': datetime.now().isoformat(),
            'stage': stage,
            'metrics': metrics,
            'status': 'Active',
        }
        self.versions[version_id] = version
        return version

    def transition_stage(self, version_id, new_stage):
        """Move version to different stage"""
        if version_id in self.versions:
            self.versions[version_id]['stage'] = new_stage
            self.versions[version_id]['updated_date'] = datetime.now().isoformat()
            return True
        return False

    def get_production_model(self):
        """Get current production model"""
        for version_id, version in self.versions.items():
            if version['stage'] == 'Production':
                return version
        return None

    def save_versions(self, output_path):
        """Save versions to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.versions, f, indent=2)

# Usage example
if __name__ == '__main__':
    versioning = ModelVersion('.')

    metrics = {'test_auc': 0.92, 'test_f1': 0.85}
    v1 = versioning.create_version('v1.0.0', metrics, stage='Production')

    print("Model version created successfully")
