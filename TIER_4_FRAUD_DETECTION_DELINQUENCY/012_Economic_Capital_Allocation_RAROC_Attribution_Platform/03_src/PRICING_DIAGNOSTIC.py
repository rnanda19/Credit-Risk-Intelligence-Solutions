# ============================================================================
# PRICING DIAGNOSTIC - Understand why revenue is decreasing
# ============================================================================

import pandas as pd
import numpy as np

print("\n" + "="*100)
print("PRICING OPTIMIZATION DIAGNOSTIC - ROOT CAUSE ANALYSIS")
print("="*100 + "\n")

# STEP 1: Check pricing algorithm outputs
print("STEP 1: PRICING ALGORITHM COMPONENTS\n")

print("Current Price Rate Statistics:")
print(f"  Mean: {df_master['current_price_rate'].mean():.4f}")
print(f"  Median: {df_master['current_price_rate'].median():.4f}")
print(f"  Min: {df_master['current_price_rate'].min():.4f}")
print(f"  Max: {df_master['current_price_rate'].max():.4f}")

print("\nRecommended Price Statistics:")
print(f"  Mean: {df_master['price_recommended'].mean():.4f}")
print(f"  Median: {df_master['price_recommended'].median():.4f}")
print(f"  Min: {df_master['price_recommended'].min():.4f}")
print(f"  Max: {df_master['price_recommended'].max():.4f}")

# STEP 2: Check the three pricing methods
print("\n\nSTEP 2: INDIVIDUAL PRICING METHODS")
print("\nCost-Plus Price:")
print(f"  Mean: {df_master['price_costplus'].mean():.4f}")
print(f"  Range: {df_master['price_costplus'].min():.4f} to {df_master['price_costplus'].max():.4f}")

print("\nValue-Based Price:")
print(f"  Mean: {df_master['price_valuebased'].mean():.4f}")
print(f"  Range: {df_master['price_valuebased'].min():.4f} to {df_master['price_valuebased'].max():.4f}")

print("\nRisk-Adjusted Price:")
print(f"  Mean: {df_master['price_riskadjusted'].mean():.4f}")
print(f"  Range: {df_master['price_riskadjusted'].min():.4f} to {df_master['price_riskadjusted'].max():.4f}")

# STEP 3: Check revenue impact
print("\n\nSTEP 3: REVENUE IMPACT")
print(f"\nTotal Current Revenue: ${df_master['revenue_current'].sum()/1e9:.2f}B")
print(f"Total Recommended Revenue: ${df_master['revenue_recommended'].sum()/1e9:.2f}B")
print(f"Total Revenue Impact: ${df_master['revenue_impact_usd'].sum()/1e9:.2f}B")

print(f"\nRevenue Impact Statistics:")
print(f"  Mean per customer: ${df_master['revenue_impact_usd'].mean():,.2f}")
print(f"  Positive impact: {(df_master['revenue_impact_usd'] > 0).sum():,} customers")
print(f"  Negative impact: {(df_master['revenue_impact_usd'] < 0).sum():,} customers")

# STEP 4: Sample comparison
print("\n\nSTEP 4: SAMPLE COMPARISON (Top 5 by EAD)")
sample = df_master.nlargest(5, 'TOTAL_EAD_USD')[['SK_ID_CURR', 'TOTAL_EAD_USD', 'RAROC_PCT',
                                                    'current_price_rate', 'price_recommended',
                                                    'price_change_pct', 'revenue_current', 'revenue_recommended']]
print(sample.to_string())

# STEP 5: ROOT CAUSE - Compare current vs recommended for same EAD
print("\n\nSTEP 5: ROOT CAUSE ANALYSIS")
print("\nFor same EAD, how does price impact revenue?")
print("Example: If EAD=$1,000,000")
print(f"  Current Price: {df_master['current_price_rate'].mean():.4f} → Revenue: ${1000000 * df_master['current_price_rate'].mean():,.0f}")
print(f"  Recommended Price: {df_master['price_recommended'].mean():.4f} → Revenue: ${1000000 * df_master['price_recommended'].mean():,.0f}")
print(f"  Loss per $1M EAD: ${1000000 * (df_master['current_price_rate'].mean() - df_master['price_recommended'].mean()):,.0f}")

# STEP 6: Price change distribution
print("\n\nSTEP 6: PRICE CHANGE DISTRIBUTION")
print(df_master['price_change_pct'].describe())

print("\n\nWHERE IS THE PROBLEM?")
if df_master['price_recommended'].mean() < df_master['current_price_rate'].mean():
    diff = (df_master['current_price_rate'].mean() - df_master['price_recommended'].mean()) / df_master['current_price_rate'].mean() * 100
    print(f"\n🚨 ISSUE FOUND: Recommended prices are {diff:.1f}% LOWER than current prices")
    print("   This is why revenue is decreasing!")
    print("\nLikely causes:")
    print("  1. Pricing algorithms using COST as ceiling instead of FLOOR")
    print("  2. Not properly valuing high-RAROC customers")
    print("  3. Over-applying discounts for risk")

print("\n" + "="*100)
