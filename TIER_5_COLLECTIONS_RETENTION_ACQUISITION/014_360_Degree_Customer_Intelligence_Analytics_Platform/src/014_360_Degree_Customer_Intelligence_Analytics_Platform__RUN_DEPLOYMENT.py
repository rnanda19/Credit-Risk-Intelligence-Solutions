#!/usr/bin/env python3
"""
ONE-STROKE DEPLOYMENT RUNNER
Fixes Unicode encoding issues and runs deployment
"""

base_path = r'C:\Users\rnand\Documents\home-credit-default-risk\Enterprise_AI_Workflows\PROBLEM_004_Customer_360_Analysis'

print("="*130)
print("🚀 STARTING ONE-STROKE DEPLOYMENT - PROBLEM_004")
print("="*130)

# STEP 1: Execute Master Deployment with UTF-8 encoding
print("\n[1/2] Running Master Deployment Executor...")
print("-"*130)

with open(f'{base_path}\\MASTER_DEPLOYMENT_EXECUTOR.py', 'r', encoding='utf-8') as f:
    exec(f.read())

# STEP 2: Update Documentation with UTF-8 encoding
print("\n[2/2] Running Documentation Update...")
print("-"*130)

with open(f'{base_path}\\UPDATE_CHUNK_DOCUMENTATION.py', 'r', encoding='utf-8') as f:
    exec(f.read())

print("\n" + "="*130)
print("✅ DEPLOYMENT COMPLETE - READY FOR PRODUCTION")
print("="*130)
