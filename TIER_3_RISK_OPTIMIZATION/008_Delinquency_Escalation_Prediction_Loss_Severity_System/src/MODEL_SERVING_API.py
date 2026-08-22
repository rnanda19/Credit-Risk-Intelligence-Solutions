#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PROBLEM_001: MODEL SERVING API
Production-grade FastAPI application for serving the PD prediction model
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
import numpy as np
import pickle
import logging
import json
from datetime import datetime
from pathlib import Path
import traceback
from typing import List, Dict, Optional
import asyncio

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="PROBLEM_001 - PD Prediction API",
    description="Production API for Probability of Default prediction",
    version="2.1.0"
)

# ============================================================================
# DATA MODELS
# ============================================================================

class PredictionRequest(BaseModel):
    """Request schema for predictions"""
    customer_id: str = Field(..., description="Unique customer identifier")
    features: List[float] = Field(..., min_items=80, max_items=80, 
                                  description="80 features for the model")
    scenario: str = Field(default="conservative", 
                         description="Scenario: conservative, moderate, aggressive")
    
    @validator('scenario')
    def scenario_must_be_valid(cls, v):
        if v not in ['conservative', 'moderate', 'aggressive']:
            raise ValueError('Scenario must be conservative, moderate, or aggressive')
        return v

class PredictionResponse(BaseModel):
    """Response schema for predictions"""
    customer_id: str
    prediction: float = Field(..., ge=0, le=1, description="PD probability (0-1)")
    risk_tier: str
    confidence: float
    timestamp: str
    model_version: str
    latency_ms: float

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    model_loaded: bool
    model_version: str
    uptime_seconds: float
    predictions_served: int
    avg_latency_ms: float

# ============================================================================
# GLOBAL STATE
# ============================================================================

class ModelState:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.model_version = "v2.1.0"
        self.model_loaded_time = None
        self.predictions_count = 0
        self.total_latency_ms = 0.0
        self.start_time = datetime.now()

model_state = ModelState()

# ============================================================================
# MODEL LOADING
# ============================================================================

def load_models():
    """Load trained model and scaler"""
    try:
        base_path = Path(__file__).parent
        
        # Load model
        model_path = base_path / "Models" / "Trained_Models" / "tuned_xgboost_model.pkl"
        logger.info(f"Loading model from {model_path}")
        
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, 'rb') as f:
            model_state.model = pickle.load(f)
        
        logger.info("✓ Model loaded successfully")
        
        # Log model info
        logger.info(f"  Model type: {type(model_state.model)}")
        logger.info(f"  Model version: {model_state.model_version}")
        
        model_state.model_loaded_time = datetime.now()
        
        return True
    
    except Exception as e:
        logger.error(f"✗ Failed to load models: {str(e)}")
        logger.error(traceback.format_exc())
        return False

# ============================================================================
# STARTUP & SHUTDOWN
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Initialize on startup"""
    logger.info("="*80)
    logger.info("PROBLEM_001: MODEL SERVING API - STARTUP")
    logger.info("="*80)
    
    success = load_models()
    
    if success:
        logger.info("✓ API startup successful - Ready to serve predictions")
    else:
        logger.error("✗ API startup failed - Model loading unsuccessful")
    
    logger.info("="*80 + "\n")

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("="*80)
    logger.info("PROBLEM_001: MODEL SERVING API - SHUTDOWN")
    logger.info(f"Total predictions served: {model_state.predictions_count}")
    if model_state.predictions_count > 0:
        avg_latency = model_state.total_latency_ms / model_state.predictions_count
        logger.info(f"Average latency: {avg_latency:.2f}ms")
    logger.info("="*80 + "\n")

# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    try:
        uptime = (datetime.now() - model_state.start_time).total_seconds()
        avg_latency = 0.0
        
        if model_state.predictions_count > 0:
            avg_latency = model_state.total_latency_ms / model_state.predictions_count
        
        health = HealthCheck(
            status="healthy" if model_state.model is not None else "unhealthy",
            model_loaded=model_state.model is not None,
            model_version=model_state.model_version,
            uptime_seconds=uptime,
            predictions_served=model_state.predictions_count,
            avg_latency_ms=avg_latency
        )
        
        return health
    
    except Exception as e:
        logger.error(f"Health check error: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

# ============================================================================
# PREDICTION ENDPOINT
# ============================================================================

@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """Make a prediction"""
    try:
        start_time = datetime.now()
        
        # Validate model loaded
        if model_state.model is None:
            logger.error("Model not loaded")
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        # Validate input
        if len(request.features) != 80:
            raise HTTPException(status_code=400, detail=f"Expected 80 features, got {len(request.features)}")
        
        # Make prediction
        features_array = np.array(request.features).reshape(1, -1)
        
        try:
            prediction = model_state.model.predict_proba(features_array)[0][1]
        except:
            # Fallback for different model types
            prediction = model_state.model.predict(features_array)[0]
        
        # Ensure prediction is in valid range
        prediction = float(np.clip(prediction, 0, 1))
        
        # Determine risk tier based on prediction
        if prediction < 0.3:
            risk_tier = "LOW"
            confidence = 1.0 - prediction
        elif prediction < 0.6:
            risk_tier = "MEDIUM"
            confidence = 0.5
        else:
            risk_tier = "HIGH"
            confidence = prediction
        
        # Calculate latency
        latency_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        # Update metrics
        model_state.predictions_count += 1
        model_state.total_latency_ms += latency_ms
        
        # Log prediction
        logger.info(f"Prediction for {request.customer_id}: PD={prediction:.4f}, Risk={risk_tier}, Latency={latency_ms:.2f}ms")
        
        return PredictionResponse(
            customer_id=request.customer_id,
            prediction=prediction,
            risk_tier=risk_tier,
            confidence=float(confidence),
            timestamp=datetime.now().isoformat(),
            model_version=model_state.model_version,
            latency_ms=latency_ms
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        logger.error(traceback.format_exc())
        raise HTTPException(status_code=500, detail="Prediction failed")

# ============================================================================
# BATCH PREDICTION ENDPOINT
# ============================================================================

@app.post("/predict_batch")
async def predict_batch(requests: List[PredictionRequest]):
    """Batch prediction endpoint"""
    try:
        if model_state.model is None:
            raise HTTPException(status_code=503, detail="Model not loaded")
        
        results = []
        
        for request in requests:
            try:
                result = await predict(request)
                results.append(result.dict())
            except Exception as e:
                logger.error(f"Batch prediction error for {request.customer_id}: {str(e)}")
                results.append({
                    "customer_id": request.customer_id,
                    "error": str(e)
                })
        
        return {
            "total_predictions": len(results),
            "timestamp": datetime.now().isoformat(),
            "results": results
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch prediction failed")

# ============================================================================
# METRICS ENDPOINT
# ============================================================================

@app.get("/metrics")
async def metrics():
    """Prometheus-style metrics endpoint"""
    try:
        uptime = (datetime.now() - model_state.start_time).total_seconds()
        avg_latency = 0.0
        
        if model_state.predictions_count > 0:
            avg_latency = model_state.total_latency_ms / model_state.predictions_count
        
        metrics_data = {
            "timestamp": datetime.now().isoformat(),
            "model_version": model_state.model_version,
            "model_loaded": model_state.model is not None,
            "model_load_time": model_state.model_loaded_time.isoformat() if model_state.model_loaded_time else None,
            "uptime_seconds": uptime,
            "predictions_served": model_state.predictions_count,
            "total_latency_ms": model_state.total_latency_ms,
            "avg_latency_ms": avg_latency,
            "api_version": "2.1.0"
        }
        
        return metrics_data
    
    except Exception as e:
        logger.error(f"Metrics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Metrics retrieval failed")

# ============================================================================
# INFO ENDPOINT
# ============================================================================

@app.get("/info")
async def info():
    """API information endpoint"""
    return {
        "project": "PROBLEM_001_Probability_of_Default",
        "api_version": "2.1.0",
        "model_version": model_state.model_version,
        "model_type": "XGBoost Classifier",
        "input_features": 80,
        "output": "Probability of Default (0-1)",
        "endpoints": {
            "health": "/health",
            "predict": "/predict (POST)",
            "predict_batch": "/predict_batch (POST)",
            "metrics": "/metrics",
            "docs": "/docs"
        }
    }

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "PROBLEM_001 PD Prediction API",
        "status": "online",
        "version": "2.1.0",
        "endpoints": "/docs for API documentation"
    }

# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """HTTP exception handler"""
    logger.error(f"HTTP Exception: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    logger.error(traceback.format_exc())
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "timestamp": datetime.now().isoformat()
        }
    )

# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info("Starting PROBLEM_001 Model Serving API...")
    logger.info("API available at: http://localhost:8000")
    logger.info("Documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=False
    )
