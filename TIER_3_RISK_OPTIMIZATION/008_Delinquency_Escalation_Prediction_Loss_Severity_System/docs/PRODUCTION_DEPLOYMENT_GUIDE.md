# PROBLEM_001: PRODUCTION DEPLOYMENT GUIDE
## Probability of Default (PD) Prediction - Complete Deployment Instructions

**Project:** PROBLEM_001 - Probability of Default Prediction  
**Version:** 2.1.0  
**Status:** 100% DEPLOYMENT-READY  
**Last Updated:** 2026-08-14

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [System Requirements](#system-requirements)
3. [Pre-Deployment Checklist](#pre-deployment-checklist)
4. [Deployment Steps](#deployment-steps)
5. [Production Configuration](#production-configuration)
6. [Monitoring & Alerts](#monitoring--alerts)
7. [Troubleshooting](#troubleshooting)
8. [Rollback Procedures](#rollback-procedures)

---

## Quick Start

### One-Command Deployment (Docker Compose)

```bash
cd /path/to/019_Delinquency_Escalation_Prediction

# Execute unified orchestrator (validates all systems)
python UNIFIED_DEPLOYMENT_ORCHESTRATOR.py

# If approved, deploy with Docker Compose
docker-compose up -d

# Verify API is running
curl http://localhost:8000/health
```

---

## System Requirements

### Hardware
- **CPU:** Minimum 2 cores (recommended 4+)
- **Memory:** Minimum 4GB RAM (recommended 8GB+)
- **Storage:** 5GB for Docker images + models
- **Network:** Stable internet connection

### Software
- **Docker:** 20.10+ with Docker Compose 1.29+
- **Python:** 3.10+ (if running without Docker)
- **OS:** Linux (Ubuntu 20.04+ recommended), macOS, or Windows with WSL2

### Dependencies
All dependencies are listed in `requirements.txt` and automatically installed in Docker image.

---

## Pre-Deployment Checklist

Before deployment, ensure all items are completed:

### ✓ Model & Configuration
- [ ] Trained model file exists: `Models/Trained_Models/tuned_xgboost_model.pkl`
- [ ] Deployment configuration complete: `10_Production_Deployment/Deployment_Config/`
- [ ] Monitoring configuration ready: `10_Production_Deployment/monitoring_configuration.json`
- [ ] API serving script available: `MODEL_SERVING_API.py`

### ✓ Infrastructure
- [ ] Docker installed and running
- [ ] Docker Compose installed (version 1.29+)
- [ ] Sufficient disk space available (5GB minimum)
- [ ] Network ports available (8000 for API, 9090 for Prometheus, 3000 for Grafana)

### ✓ Documentation
- [ ] Model documentation complete
- [ ] Deployment guide reviewed
- [ ] Runbook for operators prepared
- [ ] Escalation procedures defined

### ✓ Testing
- [ ] All deployment scripts tested
- [ ] QA tests passed (6/6 tests)
- [ ] Compliance verified (4/4 frameworks)
- [ ] BI dashboards configured (3 dashboards)

### ✓ Approval
- [ ] Go-live approval obtained
- [ ] Stakeholder sign-off complete
- [ ] Operations team notified
- [ ] On-call rotation updated

---

## Deployment Steps

### Step 1: Validate Environment

```bash
# Navigate to project directory
cd /path/to/019_Delinquency_Escalation_Prediction

# Run unified orchestrator (validates all systems)
python UNIFIED_DEPLOYMENT_ORCHESTRATOR.py
```

**Expected Output:**
```
✓ PROBLEM_001 IS 100% DEPLOYMENT-READY

Status Summary:
  ✓ Deployment Automation: COMPLETE
  ✓ Compliance Verification: PASSED
  ✓ Business Intelligence: CONFIGURED
  ✓ Production Readiness: CERTIFIED

Go-Live Decision: APPROVED FOR PRODUCTION
```

### Step 2: Build Docker Image

```bash
# Build Docker image
docker build -t problem-001-pd-api:2.1.0 .

# Verify build
docker images | grep problem-001
```

### Step 3: Start Services

```bash
# Start all services (API, Prometheus, Grafana)
docker-compose up -d

# Verify services are running
docker-compose ps

# Check API logs
docker-compose logs -f pd-api
```

### Step 4: Verify API Health

```bash
# Check API health
curl http://localhost:8000/health

# Expected response:
# {"status":"healthy","model_loaded":true,"model_version":"v2.1.0",...}

# View API documentation
# Open browser: http://localhost:8000/docs
```

### Step 5: Test Predictions

```bash
# Test single prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": "CUST_001",
    "features": [0.5, 0.6, 0.7, ...],  # 80 features required
    "scenario": "moderate"
  }'

# View metrics
curl http://localhost:8000/metrics

# Access Grafana dashboards
# Open browser: http://localhost:3000 (default: admin/admin)
```

---

## Production Configuration

### Environment Variables

```bash
# Create .env file
cat > .env << 'EOL'
# Logging
LOG_LEVEL=INFO

# Model
MODEL_VERSION=v2.1.0

# API
API_PORT=8000
API_WORKERS=4

# Monitoring
PROMETHEUS_PORT=9090
GRAFANA_PORT=3000

# Database (if applicable)
# DB_CONNECTION_STRING=...
EOL
```

### Resource Limits

```yaml
# In docker-compose.yml, add resource limits:
services:
  pd-api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Network Configuration

```bash
# Create production network
docker network create problem-001-prod

# Connect services to production network
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

---

## Monitoring & Alerts

### Key Metrics to Monitor

```
Model Performance:
  - Prediction accuracy (baseline: >90%)
  - Average latency (target: <200ms)
  - P99 latency (target: <500ms)
  - Error rate (target: <0.5%)

System Health:
  - CPU utilization (target: <70%)
  - Memory usage (target: <80%)
  - API uptime (target: 99.9%)
  - Request volume per minute

Data Quality:
  - Feature drift detection (weekly)
  - Data quality score (target: >95%)
  - Model retraining frequency
```

### Prometheus Alerts

```yaml
# Example alert rules (prometheus.yml)
groups:
  - name: problem_001_alerts
    rules:
      - alert: HighPredictionLatency
        expr: histogram_quantile(0.99, prediction_latency_ms) > 500
        for: 5m
        
      - alert: HighErrorRate
        expr: error_rate > 0.01
        for: 5m
        
      - alert: ModelAccuracyDrop
        expr: model_accuracy < 0.90
        for: 1h
```

### Grafana Dashboards

Access Grafana at `http://localhost:3000`:

1. **Executive Dashboard** (C-Suite metrics)
2. **Operational Dashboard** (System health)
3. **Analytics Dashboard** (Model performance)

---

## Troubleshooting

### API Won't Start

```bash
# Check logs
docker-compose logs pd-api

# Verify model file exists
ls -lah Models/Trained_Models/tuned_xgboost_model.pkl

# Rebuild image
docker-compose build --no-cache
```

### High Latency

```bash
# Check resource utilization
docker stats

# Increase container resources
# Edit docker-compose.yml and adjust deploy.resources

# Restart service
docker-compose restart pd-api
```

### Model Loading Error

```bash
# Verify model file integrity
file Models/Trained_Models/tuned_xgboost_model.pkl

# Check Python compatibility
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt
```

### Database Connection Issues

```bash
# Verify database connectivity
docker-compose exec pd-api python -c "import psycopg2; print('OK')"

# Check environment variables
docker-compose config | grep DB_
```

---

## Rollback Procedures

### Quick Rollback (< 5 minutes)

```bash
# Stop current deployment
docker-compose down

# Restart previous version
docker-compose -f docker-compose.backup.yml up -d

# Verify rollback
curl http://localhost:8000/health
```

### Blue-Green Rollback

```bash
# If using blue-green deployment:

# Check current active environment
curl http://lb.example.com/health

# Switch to backup environment
./scripts/switch-to-backup.sh

# Verify
curl http://lb.example.com/health
```

### Database Rollback

```bash
# Restore from backup (if applicable)
docker exec problem-001-db psql -U postgres < backup.sql

# Verify data integrity
docker-compose exec pd-api python scripts/verify_data.py
```

---

## Performance Optimization

### Caching Strategy

```python
# Enable response caching
# In MODEL_SERVING_API.py:
from fastapi_cache2 import FastAPICache2
from fastapi_cache2.backends.redis import RedisBackend

# Results cached for 5 minutes
@app.get("/predict", tags=["cache"])
async def predict_cached(request: PredictionRequest):
    ...
```

### Load Balancing

```yaml
# docker-compose.yml with load balancer
services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - pd-api-1
      - pd-api-2
```

### Auto-Scaling

```bash
# Kubernetes deployment (optional)
kubectl apply -f k8s/deployment.yaml
kubectl autoscale deployment problem-001-pd-api --min=2 --max=5
```

---

## Support & Escalation

### For Support Issues

1. Check logs: `docker-compose logs -f`
2. Review monitoring dashboards
3. Verify data quality
4. Contact on-call engineer

### Critical Issues (Down/Error)

1. Execute rollback immediately
2. Notify stakeholders
3. Page on-call engineer
4. Document incident

### Non-Critical Issues (Performance/Quality)

1. Gather metrics and logs
2. Create support ticket
3. Schedule maintenance window
4. Implement fix during window

---

## Maintenance Schedule

| Task | Frequency | Owner |
|------|-----------|-------|
| Log rotation | Daily | Ops |
| Model retraining | Monthly | ML Team |
| Security patches | Quarterly | DevOps |
| Compliance audit | Quarterly | Compliance |
| Full backup | Weekly | Ops |
| Disaster recovery drill | Quarterly | DevOps |

---

**Questions?** Contact: `ml-ops@company.com`  
**Escalation:** Page on-call engineer via PagerDuty

