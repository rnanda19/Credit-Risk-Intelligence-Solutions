"""
Flask REST API for Early Payment Default Detection
Problem 18: Home Credit Default Risk
Production-Ready Model Serving Application
"""

from flask import Flask, request, jsonify
import pickle
import json
import numpy as np
import pandas as pd
from datetime import datetime
import logging
import os
import sys

# ============================================================================
# INITIALIZATION
# ============================================================================

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# MODEL LOADING
# ============================================================================

MODEL_PATH = 'Logistic_Regression_model.pkl'
SCALER_PATH = 'scaler.pkl'
FEATURES_PATH = 'features.json'

model = None
scaler = None
features = None

def load_model():
    global model, scaler, features

    try:
        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)
        logger.info("[OK] Model loaded successfully")
    except FileNotFoundError:
        logger.error("[ERROR] Model file not found: " + MODEL_PATH)
    except Exception as e:
        logger.error("[ERROR] Failed to load model: " + str(e))

    try:
        with open(SCALER_PATH, 'rb') as f:
            scaler = pickle.load(f)
        logger.info("[OK] Scaler loaded successfully")
    except FileNotFoundError:
        logger.error("[ERROR] Scaler file not found: " + SCALER_PATH)
    except Exception as e:
        logger.error("[ERROR] Failed to load scaler: " + str(e))

    try:
        with open(FEATURES_PATH, 'r', encoding='utf-8') as f:
            features = json.load(f)
        logger.info("[OK] Features loaded successfully (" + str(len(features)) + " features)")
    except FileNotFoundError:
        logger.error("[ERROR] Features file not found: " + FEATURES_PATH)
    except Exception as e:
        logger.error("[ERROR] Failed to load features: " + str(e))

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def validate_features(feature_values):
    """Validate feature input"""
    if not isinstance(feature_values, list):
        return False, "Features must be a list"

    if len(feature_values) != len(features):
        return False, "Expected " + str(len(features)) + " features, got " + str(len(feature_values))

    try:
        feature_values = [float(x) for x in feature_values]
    except (ValueError, TypeError):
        return False, "All feature values must be numeric"

    return True, feature_values

def get_timestamp():
    """Get current timestamp"""
    return datetime.utcnow().isoformat() + 'Z'

# ============================================================================
# ENDPOINTS
# ============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    status = 'healthy' if (model and scaler and features) else 'unhealthy'
    http_code = 200 if status == 'healthy' else 503

    return jsonify({
        'status': status,
        'service': 'Early Payment Default Detection',
        'model_loaded': model is not None,
        'scaler_loaded': scaler is not None,
        'features_loaded': features is not None,
        'num_features': len(features) if features else 0,
        'timestamp': get_timestamp()
    }), http_code

@app.route('/info', methods=['GET'])
def api_info():
    """API information endpoint"""
    return jsonify({
        'service': 'Early Payment Default Detection API',
        'version': '1.0.0',
        'problem': 'Problem 18 - Home Credit Dataset',
        'model_type': 'Logistic Regression',
        'num_features': len(features) if features else 0,
        'endpoints': {
            'health': 'GET /health',
            'info': 'GET /info',
            'model_info': 'GET /model-info',
            'predict': 'POST /predict',
            'predict_batch': 'POST /predict-batch'
        }
    }), 200

@app.route('/model-info', methods=['GET'])
def model_info():
    """Model information endpoint"""
    if not all([model, scaler, features]):
        return jsonify({'status': 'error', 'message': 'Model not available'}), 503

    return jsonify({
        'status': 'success',
        'model_name': 'Logistic Regression',
        'input_features': len(features),
        'feature_list': features,
        'input_shape': [1, len(features)],
        'output_type': 'binary_classification',
        'output_classes': ['Class 0 (No Default)', 'Class 1 (Default)'],
        'probability_output': True
    }), 200

@app.route('/predict', methods=['POST'])
def predict_single():
    """Single prediction endpoint"""
    if not all([model, scaler, features]):
        return jsonify({'status': 'error', 'message': 'Model not available'}), 503

    try:
        data = request.get_json()

        if not data or 'features' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required field: features'}), 400

        feature_values = data['features']

        is_valid, result = validate_features(feature_values)
        if not is_valid:
            return jsonify({'status': 'error', 'message': result}), 400

        feature_values = result
        X = pd.DataFrame([feature_values], columns=features)
        X_scaled = scaler.transform(X)

        prediction = int(model.predict(X_scaled)[0])
        probability = model.predict_proba(X_scaled)[0]

        logger.info("Prediction made: class=" + str(prediction))

        return jsonify({
            'status': 'success',
            'prediction': prediction,
            'prediction_label': 'Default' if prediction == 1 else 'No Default',
            'confidence': float(probability[prediction]),
            'probabilities': {
                'no_default': float(probability[0]),
                'default': float(probability[1])
            },
            'timestamp': get_timestamp()
        }), 200

    except Exception as e:
        logger.error("Prediction error: " + str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/predict-batch', methods=['POST'])
def predict_batch():
    """Batch prediction endpoint"""
    if not all([model, scaler, features]):
        return jsonify({'status': 'error', 'message': 'Model not available'}), 503

    try:
        data = request.get_json()

        if not data or 'records' not in data:
            return jsonify({'status': 'error', 'message': 'Missing required field: records'}), 400

        records = data['records']

        if not isinstance(records, list) or len(records) == 0:
            return jsonify({'status': 'error', 'message': 'Records must be non-empty list'}), 400

        if len(records) > 1000:
            return jsonify({'status': 'error', 'message': 'Batch size exceeds limit of 1000'}), 400

        validated_records = []
        for idx, record in enumerate(records):
            is_valid, result = validate_features(record)
            if not is_valid:
                return jsonify({'status': 'error', 'message': 'Record ' + str(idx) + ': ' + result}), 400
            validated_records.append(result)

        X = pd.DataFrame(validated_records, columns=features)
        X_scaled = scaler.transform(X)

        predictions = model.predict(X_scaled)
        probabilities = model.predict_proba(X_scaled)

        logger.info("Batch prediction: " + str(len(records)) + " records")

        results = []
        for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
            results.append({
                'record_id': i,
                'prediction': int(pred),
                'prediction_label': 'Default' if pred == 1 else 'No Default',
                'confidence': float(prob[int(pred)]),
                'probabilities': {
                    'no_default': float(prob[0]),
                    'default': float(prob[1])
                }
            })

        return jsonify({
            'status': 'success',
            'num_records': len(records),
            'results': results,
            'timestamp': get_timestamp()
        }), 200

    except Exception as e:
        logger.error("Batch error: " + str(e))
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'status': 'error', 'message': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'status': 'error', 'message': 'Internal server error'}), 500

# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    logger.info("="*80)
    logger.info("Starting Early Payment Default Detection API")
    logger.info("="*80)

    load_model()

    if not all([model, scaler, features]):
        logger.error("[ERROR] Failed to load required files")
        sys.exit(1)

    logger.info("[OK] All files loaded")
    logger.info("[OK] Model: Logistic Regression")
    logger.info("[OK] Features: " + str(len(features)))
    logger.info("="*80)
    logger.info("API Server starting on http://0.0.0.0:5000")
    logger.info("="*80)

    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True, use_reloader=False)
