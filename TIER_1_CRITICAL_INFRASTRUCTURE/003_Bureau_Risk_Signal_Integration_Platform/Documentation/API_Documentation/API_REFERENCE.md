# Bureau Risk Signal Integration - API Reference

## Overview

The Bureau Risk Signal Integration API provides real-time access to credit default risk predictions for customers. All endpoints require JWT authentication and return JSON responses.

**Base URL**: `https://api.prod.company.com/v1`  
**Authentication**: JWT Bearer Token  
**Rate Limit**: 1,000 requests/minute  
**Timeout**: 30 seconds

---

## Authentication

All requests require an `Authorization` header with a valid JWT token:

```bash
curl -H "Authorization: Bearer <YOUR_JWT_TOKEN>" \
  https://api.prod.company.com/v1/predict
```

### Obtaining a Token

```bash
POST /auth/token
Content-Type: application/json

{
  "api_key": "your_api_key",
  "api_secret": "your_api_secret"
}

Response:
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_in": 3600,
  "token_type": "Bearer"
}
```

---

## Endpoints

### 1. Predict Default Risk

**Endpoint**: `POST /predict`

Predict default risk probability for a customer.

#### Request

```json
{
  "sk_id_curr": 123456,
  "features": {
    "BUREAU_HIGH_RISK_FLAG": 0,
    "BUREAU_INQUIRY_FREQUENCY": 2,
    "CREDIT_TO_INCOME_RATIO": 0.85,
    "ANNUITY_TO_INCOME_RATIO": 0.12,
    "PAYMENT_CONSISTENCY": 0.95,
    "AGE_AT_APPLICATION": 35,
    "EMPLOYMENT_STABILITY": 0.8,
    "EXTERNAL_SCORE": 720,
    "DOCUMENTS_SUBMITTED_COUNT": 5,
    "CONTACT_INFO_COMPLETENESS": 1.0,
    "CC_UTILIZATION_RATE": 0.45,
    "HAS_DEPENDENTS": 1,
    "REGISTRATION_TENURE": 2.5,
    "GOODS_PRICE_TO_CREDIT_RATIO": 1.2,
    "DAYS_EMPLOYED": 1825
  }
}
```

#### Response (200 OK)

```json
{
  "sk_id_curr": 123456,
  "default_probability": 0.152,
  "default_prediction": false,
  "risk_category": "LOW",
  "confidence": 0.94,
  "model_version": "1.0.0",
  "timestamp": "2024-08-11T14:30:00Z",
  "explanation": {
    "top_factors": [
      "Low credit to income ratio",
      "Excellent payment history",
      "Good external score"
    ],
    "risk_drivers": []
  }
}
```

#### Risk Categories

| Category | Probability Range | Action |
|----------|------------------|--------|
| LOW | 0.00 - 0.30 | Approve, monitor |
| MEDIUM | 0.30 - 0.70 | Additional checks |
| HIGH | 0.70 - 1.00 | Escalate, decline |

#### Error Responses

```json
{
  "error": "INVALID_FEATURES",
  "message": "Missing required feature: BUREAU_HIGH_RISK_FLAG",
  "code": 400
}
```

---

### 2. Batch Predictions

**Endpoint**: `POST /batch-predict`

Submit multiple customers for prediction in a single request.

#### Request

```json
{
  "customers": [
    {
      "sk_id_curr": 123456,
      "features": { /* feature object */ }
    },
    {
      "sk_id_curr": 123457,
      "features": { /* feature object */ }
    }
  ]
}
```

#### Response (200 OK)

```json
{
  "batch_id": "batch_202408_001",
  "status": "PROCESSING",
  "total_records": 2,
  "completed": 2,
  "failed": 0,
  "predictions": [
    {
      "sk_id_curr": 123456,
      "default_probability": 0.152,
      "risk_category": "LOW"
    },
    {
      "sk_id_curr": 123457,
      "default_probability": 0.542,
      "risk_category": "MEDIUM"
    }
  ],
  "processing_time_ms": 245
}
```

---

### 3. Health Check

**Endpoint**: `GET /health`

Check if the model service is operational.

#### Response (200 OK)

```json
{
  "status": "HEALTHY",
  "timestamp": "2024-08-11T14:30:00Z",
  "model_version": "1.0.0",
  "uptime_minutes": 1440,
  "last_prediction": "2024-08-11T14:29:58Z",
  "predictions_today": 15234,
  "error_rate": 0.0023
}
```

---

### 4. Metrics

**Endpoint**: `GET /metrics`

Get current model performance metrics.

#### Response (200 OK)

```json
{
  "model_version": "1.0.0",
  "performance": {
    "auc": 0.7412,
    "f1": 0.4523,
    "precision": 0.5234,
    "recall": 0.3891,
    "accuracy": 0.9192
  },
  "monitoring": {
    "predictions_served_today": 15234,
    "predictions_served_total": 1234567,
    "average_latency_ms": 145,
    "p95_latency_ms": 320,
    "p99_latency_ms": 540,
    "error_rate": 0.0023,
    "uptime_percentage": 99.95
  },
  "drift_detection": {
    "data_drift_detected": false,
    "model_drift_detected": false,
    "ks_test_pvalue": 0.34,
    "last_check": "2024-08-11T14:00:00Z"
  }
}
```

---

## Error Codes

| Code | Message | Meaning |
|------|---------|---------|
| 400 | INVALID_REQUEST | Malformed request or invalid parameters |
| 401 | UNAUTHORIZED | Missing or invalid authentication token |
| 403 | FORBIDDEN | Insufficient permissions |
| 404 | NOT_FOUND | Endpoint not found |
| 429 | RATE_LIMIT_EXCEEDED | Too many requests |
| 500 | INTERNAL_ERROR | Server error |
| 503 | SERVICE_UNAVAILABLE | Model service temporarily down |

---

## Request Examples

### Python

```python
import requests
import json

API_URL = "https://api.prod.company.com/v1"
TOKEN = "your_jwt_token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# Single prediction
payload = {
    "sk_id_curr": 123456,
    "features": {
        "BUREAU_HIGH_RISK_FLAG": 0,
        "BUREAU_INQUIRY_FREQUENCY": 2,
        # ... other features
    }
}

response = requests.post(
    f"{API_URL}/predict",
    headers=headers,
    json=payload
)

print(response.json())
```

### cURL

```bash
curl -X POST https://api.prod.company.com/v1/predict \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "sk_id_curr": 123456,
    "features": {
      "BUREAU_HIGH_RISK_FLAG": 0,
      "BUREAU_INQUIRY_FREQUENCY": 2
    }
  }'
```

### Node.js

```javascript
const axios = require('axios');

const api = axios.create({
  baseURL: 'https://api.prod.company.com/v1',
  headers: {
    'Authorization': `Bearer YOUR_TOKEN`,
    'Content-Type': 'application/json'
  }
});

api.post('/predict', {
  sk_id_curr: 123456,
  features: {
    BUREAU_HIGH_RISK_FLAG: 0,
    BUREAU_INQUIRY_FREQUENCY: 2
  }
}).then(response => {
  console.log(response.data);
});
```

---

## Rate Limiting

The API enforces rate limits of 1,000 requests per minute per API key.

**Rate Limit Headers** (returned in all responses):

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 987
X-RateLimit-Reset: 1691760660
```

When rate limit is exceeded, the API returns:

```json
{
  "error": "RATE_LIMIT_EXCEEDED",
  "message": "Rate limit exceeded. Reset at 2024-08-11T14:31:00Z",
  "retry_after_seconds": 60
}
```

---

## Pagination

For batch operations and list endpoints, use pagination:

```
GET /predictions?page=1&page_size=100
```

**Response**:

```json
{
  "data": [ /* results */ ],
  "pagination": {
    "page": 1,
    "page_size": 100,
    "total": 5234,
    "total_pages": 53
  }
}
```

---

## Webhook Support

Subscribe to webhook events for real-time updates:

```
POST /webhooks/subscribe
{
  "event_type": "prediction_completed",
  "webhook_url": "https://your-app.com/webhook",
  "secret": "your_secret_key"
}
```

---

## SDK Libraries

Official SDKs available:

- **Python**: `pip install bureau-risk-sdk`
- **Node.js**: `npm install @bureau-risk/sdk`
- **Java**: `maven dependency: com.company:bureau-risk-sdk`
- **Go**: `go get github.com/company/bureau-risk-go`

---

## API Versioning

The API follows semantic versioning. Current version: **1.0.0**

Breaking changes will result in a new major version (e.g., `/v2`).

---

## Support

**API Support Email**: api-support@company.com  
**Slack Channel**: #api-support  
**Documentation**: https://docs.company.com/api  
**Status Page**: https://status.company.com
