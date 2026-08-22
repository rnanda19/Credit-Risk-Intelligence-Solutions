# Early Payment Default Detection API

## Quick Start

### 1. Install Dependencies
pip install -r requirements.txt

### 2. Run API
python app.py

### 3. Test API
python test_api.py

## Endpoints

### GET /health
Health check

### GET /info
API information

### GET /model-info
Model details

### POST /predict
Single prediction
Request: {"features": [value1, value2, ..., value130]}

### POST /predict-batch
Batch predictions
Request: {"records": [[values...], [values...], ...]}

## Example Usage

### Python
import requests
import numpy as np

features = np.random.randn(130).tolist()
response = requests.post('http://localhost:5000/predict', json={'features': features})
print(response.json())

### cURL
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [1.0, 2.0, ..., 3.0]}'

## Error Codes
- 200: Success
- 400: Bad request
- 503: Model unavailable
- 500: Server error

## Performance
- Single: 5-10ms
- Batch (100): 50-100ms
- Max batch: 1000 records
