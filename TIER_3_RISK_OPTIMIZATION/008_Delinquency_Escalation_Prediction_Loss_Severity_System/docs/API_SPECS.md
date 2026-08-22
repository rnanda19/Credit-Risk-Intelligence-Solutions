# Model Serving API - Specifications

## Endpoint: /predict
```
POST /predict
Content-Type: application/json

{
  "features": [list of 75 features],
  "customer_id": "customer_123"
}

Response:
{
  "prediction": 0.8523,  // probability of delinquency
  "class": 1,            // 0 = no delinquency, 1 = delinquency
  "confidence": 0.9512,  // model confidence
  "customer_id": "customer_123"
}
```

## Endpoint: /batch_predict
```
POST /batch_predict
Content-Type: application/json

{
  "data": "path/to/batch_data.csv"
}

Response:
{
  "predictions_file": "path/to/predictions.csv",
  "status": "success",
  "records_processed": 1000
}
```

## Endpoint: /health
```
GET /health

Response:
{
  "status": "healthy",
  "model_version": "v1.0.0",
  "uptime": 3600
}
```
