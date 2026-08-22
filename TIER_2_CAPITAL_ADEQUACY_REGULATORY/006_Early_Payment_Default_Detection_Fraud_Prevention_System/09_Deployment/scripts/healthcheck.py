"""
Health Check Script
Verify API health and readiness
"""

import requests
import json
import sys

class HealthChecker:
    """Check API health"""

    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.timeout = 5

    def check_health(self):
        """Check API health"""
        try:
            response = requests.get(f'{self.base_url}/health', timeout=self.timeout)
            return response.status_code == 200
        except:
            return False

    def check_model(self):
        """Check model is loaded"""
        try:
            response = requests.get(f'{self.base_url}/info', timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                return 'model_type' in data
            return False
        except:
            return False

    def check_prediction(self):
        """Check prediction endpoint"""
        try:
            import numpy as np
            features = np.random.randn(130).tolist()
            data = {'features': features}
            response = requests.post(f'{self.base_url}/predict', json=data, timeout=self.timeout)
            return response.status_code == 200
        except:
            return False

    def run_all_checks(self):
        """Run all health checks"""
        checks = {
            'api_health': self.check_health(),
            'model_loaded': self.check_model(),
            'prediction_works': self.check_prediction(),
        }
        return checks

    def print_status(self):
        """Print health status"""
        checks = self.run_all_checks()

        for check, result in checks.items():
            status = 'PASS' if result else 'FAIL'
            print(f'{check}: {status}')

        all_pass = all(checks.values())
        return all_pass

if __name__ == '__main__':
    checker = HealthChecker()
    success = checker.print_status()
    sys.exit(0 if success else 1)
