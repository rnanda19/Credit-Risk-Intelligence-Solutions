"""
MODEL SERVING API - Production Ready
Problem 19: Delinquency Escalation Prediction
"""

import numpy as np
import pandas as pd
import joblib
from datetime import datetime
import logging
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DelinquencyPredictor:
    """Production-grade predictor for delinquency escalation"""

    def __init__(self, model_path: str, feature_names: List[str]):
        """Initialize predictor with model and features"""
        try:
            self.model = joblib.load(model_path)
            self.feature_names = feature_names
            self.model_loaded = True
            logger.info("Model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            self.model = None
            self.model_loaded = False

    def validate_input(self, data: pd.DataFrame) -> Tuple[bool, str]:
        """Validate input data before prediction"""
        if data.empty:
            return False, "Input data is empty"

        missing_features = set(self.feature_names) - set(data.columns)
        if missing_features:
            return False, f"Missing features: {missing_features}"

        if data.isnull().any().any():
            return False, "Input contains NaN values"

        return True, "Valid"

    def predict_single(self, sample: Dict) -> Dict:
        """Predict for single sample"""
        if not self.model_loaded:
            return {'error': 'Model not loaded', 'status': 'FAILED'}

        try:
            df = pd.DataFrame([sample])
            valid, msg = self.validate_input(df)
            if not valid:
                return {'error': msg, 'status': 'VALIDATION_FAILED'}

            df = df[self.feature_names]
            pred_class = self.model.predict(df)[0]
            pred_proba = self.model.predict_proba(df)[0][1]

            if pred_proba < 0.3:
                risk_level = 'LOW'
            elif pred_proba < 0.7:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'HIGH'

            return {
                'prediction_id': str(hash(str(sample)))[:8],
                'predicted_class': int(pred_class),
                'predicted_probability': float(pred_proba),
                'risk_level': risk_level,
                'timestamp': datetime.now().isoformat(),
                'model_version': '1.0.0',
                'status': 'SUCCESS'
            }

        except Exception as e:
            logger.error(f"Prediction error: {str(e)}")
            return {'error': str(e), 'status': 'FAILED'}

    def predict_batch(self, data: pd.DataFrame) -> pd.DataFrame:
        """Predict for batch of samples"""
        if not self.model_loaded:
            return pd.DataFrame({'error': ['Model not loaded']})

        try:
            valid, msg = self.validate_input(data)
            if not valid:
                logger.warning(f"Validation warning: {msg}")

            data_prepared = data[self.feature_names].fillna(data[self.feature_names].median())
            predictions = self.model.predict(data_prepared)
            probabilities = self.model.predict_proba(data_prepared)[:, 1]

            results = pd.DataFrame({
                'sample_id': range(len(data)),
                'predicted_class': predictions,
                'predicted_probability': probabilities,
                'risk_level': ['HIGH' if p > 0.7 else 'MEDIUM' if p > 0.3 else 'LOW' 
                              for p in probabilities],
                'timestamp': datetime.now().isoformat(),
            })

            logger.info(f"Batch prediction complete: {len(results)} samples")
            return results

        except Exception as e:
            logger.error(f"Batch prediction error: {str(e)}")
            return pd.DataFrame({'error': [str(e)]})
