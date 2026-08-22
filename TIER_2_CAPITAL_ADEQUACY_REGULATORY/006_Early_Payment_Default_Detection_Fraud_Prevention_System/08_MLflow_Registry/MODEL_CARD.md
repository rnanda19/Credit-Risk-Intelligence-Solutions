# Model Card: Early Payment Default Detection

## Model Details

**Model Name:** Early Payment Default Detector
**Model Version:** 1.0.0
**Framework:** scikit-learn
**Algorithm:** Logistic Regression
**Created:** 2026-08-10

## Model Purpose

Predict probability of early payment default for Home Credit customers using historical transaction data.

## Model Performance

**Test Metrics:**
- AUC-ROC: 0.7634
- Precision: 0.5462
- Recall: 0.0274
- F1-Score: 0.0522

**Cross-Validation (5-Fold):**
- Mean AUC: 0.7582
- Std Dev: 0.0049

## Training Data

**Dataset:** Home Credit Default Risk
**Records:** 307,511
**Features:** 129
**Train/Test Split:** 80/20

**Target Distribution:**
- Class 0 (No Default): 282,686
- Class 1 (Default): 24,825

## Input Features

Total: 129 numeric features

**Feature Categories:**
- Customer Demographics
- Income & Employment
- Credit History
- Transaction Patterns

## Model Usage

### API Endpoint
POST /predict
Content-Type: application/json

Request:
{
    "features": [value1, value2, ..., value130]
}

Response:
{
    "prediction": 0,
    "probability": 0.92,
    "confidence": 0.92
}

## Limitations

1. Model trained on historical data only
2. Performance may degrade with distribution shift
3. Requires 130 features for prediction
4. Best for binary classification tasks

## Deployment Requirements

- Python 3.8+
- scikit-learn >= 0.24.0
- pandas >= 1.3.0
- numpy >= 2.0.0
- Flask >= 2.3.0

## Monitoring & Maintenance

**Monitoring Metrics:**
- Model accuracy over time
- Feature distribution drift
- Prediction latency
- Error rates

**Retraining Schedule:** Monthly

**Maintenance:** Quarterly

## Support & Contact

For issues or questions, contact: rnanda19@gmail.com
