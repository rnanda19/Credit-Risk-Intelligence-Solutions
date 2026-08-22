"""
API Test Script - Early Payment Default Detection
Test all API endpoints
"""

import requests
import json
import numpy as np
import sys

BASE_URL = "http://localhost:5000"
TIMEOUT = 10

def test_health():
    """Test health endpoint"""
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_info():
    """Test info endpoint"""
    print("Testing /info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/info", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Service: {data.get('service')}")
        print(f"Model: {data.get('model_type')}")
        print(f"Features: {data.get('num_features')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_model_info():
    """Test model info endpoint"""
    print("Testing /model-info endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/model-info", timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        data = response.json()
        print(f"Model: {data.get('model_name')}")
        print(f"Input Features: {data.get('input_features')}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_single_prediction():
    """Test single prediction endpoint"""
    print("Testing /predict endpoint...")
    try:
        features = np.random.randn(130).tolist()
        data = {"features": features}

        response = requests.post(f"{BASE_URL}/predict", json=data, timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        result = response.json()

        if response.status_code == 200:
            print(f"Prediction: {result.get('prediction_label')}")
            print(f"Confidence: {result.get('confidence'):.4f}")

        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("Testing /predict-batch endpoint...")
    try:
        records = [np.random.randn(130).tolist() for _ in range(3)]
        data = {"records": records}

        response = requests.post(f"{BASE_URL}/predict-batch", json=data, timeout=TIMEOUT)
        print(f"Status Code: {response.status_code}")
        result = response.json()

        if response.status_code == 200:
            print(f"Records Processed: {result.get('num_records')}")

        return response.status_code == 200
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("API TEST SUITE")
    print("="*80 + "\n")

    tests = [
        ("Health Check", test_health),
        ("API Info", test_info),
        ("Model Info", test_model_info),
        ("Single Prediction", test_single_prediction),
        ("Batch Prediction", test_batch_prediction),
    ]

    results = {}
    for name, test_func in tests:
        print("\n" + name)
        print("-" * 40)
        try:
            results[name] = test_func()
        except Exception as e:
            print(f"Exception: {str(e)}")
            results[name] = False

    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80 + "\n")

    passed_count = sum(results.values())
    total_count = len(results)

    for name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"{name:<30} {status}")

    print(f"\nTotal: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\nAll tests passed!")

    sys.exit(0 if passed_count == total_count else 1)
