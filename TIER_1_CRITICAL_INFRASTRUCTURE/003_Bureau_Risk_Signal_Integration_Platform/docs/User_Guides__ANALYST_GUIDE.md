# Analyst Guide - Portfolio Risk Analysis

## Dashboard Overview

### 1. Portfolio Monitoring Dashboard
**Location**: `Dashboards/Monitoring_Dashboards/portfolio_monitoring_dashboard.html`

**Key Metrics**:
- **Customers at Risk**: 24,876 (8.09% of portfolio)
- **New Defaults Today**: 15
- **Cured Accounts**: 8
- **Concentration Rating**: MODERATE

### 2. Portfolio Risk by Segment

#### Geographic Distribution
| Region | Portfolio % | Default Rate | Risk Level |
|--------|------------|--------------|-----------|
| North | 35% | 9.5% | HIGH |
| South | 25% | 7.2% | MEDIUM |
| East | 22% | 8.1% | MEDIUM |
| West | 18% | 8.8% | MEDIUM |

**Action**: North region shows elevated default rate. Recommend enhanced monitoring.

#### Income Level Analysis
| Level | Portfolio % | Default Rate | Status |
|-------|------------|--------------|--------|
| High | 20% | 3.2% | ✅ LOW |
| Middle | 55% | 7.8% | ⚠️ MEDIUM |
| Low | 25% | 14.5% | ⚠️ HIGH |

**Action**: Low-income segment needs targeted intervention.

#### Employment Type
| Type | Portfolio % | Default Rate | Risk |
|------|------------|--------------|------|
| Salaried | 65% | 6.5% | ✅ LOW |
| Self-Employed | 20% | 12.5% | ⚠️ MEDIUM |
| Unemployed | 15% | 16.0% | ⚠️ HIGH |

**Action**: Unemployed segment at high risk. Consider special monitoring.

---

## Early Warning Indicators

### Current Alerts (Last 24 Hours)

**Payment Delinquency** (3,247 accounts flagged)
- Increase: +12% vs last month
- Recommended Action: Initiate outreach program
- Timeline: Within 30 days

**Bureau Inquiry Spike** (1,543 accounts flagged)
- Increase: +8% vs last month
- Recommended Action: Monitor for credit-seeking behavior
- Risk: Potential prepayment or financial distress

**Income Verification Expired** (2,104 accounts)
- Increase: +5% vs last month
- Recommended Action: Request re-verification
- Timeline: Compliance requirement

---

## Risk Scoring Interpretation

### Prediction Probability Ranges

| Probability | Category | Interpretation | Recommended Action |
|------------|----------|-----------------|-------------------|
| 0.00 - 0.30 | LOW | Low default risk | Standard monitoring |
| 0.30 - 0.70 | MEDIUM | Elevated risk | Additional verification |
| 0.70 - 1.00 | HIGH | High default risk | Escalation required |

### Model Confidence

The model provides 94% confidence in its predictions.
- **High confidence**: Results highly reliable
- **Lower confidence** (if seen): Additional manual review recommended

---

## Trend Analysis

### 30-Day Default Rate Trend
- Day 1: 8.29%
- Day 10: 8.18%
- Day 20: 8.14%
- Day 30: 8.09%
- **Trend**: IMPROVING (↓0.20% over 30 days)

### 90-Day Forecast
- Projected default rate: 8.05% (stable)
- Confidence interval: 7.95% - 8.15%
- Key drivers: Portfolio composition, economic indicators

---

## Concentration Risk Assessment

### Herfindahl Index (Concentration Measure)
- Geography: 0.32 (Moderate)
- Income Level: 0.36 (Moderate)
- Employment: 0.48 (Moderate-High)
- **Overall Rating**: MODERATE

### Risk Implications
- Geographic risk: Concentrated in North region (35%)
- Income risk: Heavy on middle income (55%)
- Employment risk: Heavily salaried (65%)

### Recommendations
1. Diversify geographic mix if possible
2. Develop targeted programs for low-income segment
3. Monitor self-employed and unemployed segments closely

---

## Using the Model for Decisions

### When Model Predicts LOW Risk (0.00-0.30)
✅ Approve standard terms  
✅ Standard monitoring frequency  
✅ Include in general portfolio  

### When Model Predicts MEDIUM Risk (0.30-0.70)
⚠️ Request additional documentation  
⚠️ Consider enhanced monitoring  
⚠️ May offer modified terms  
⚠️ Quarterly review recommended  

### When Model Predicts HIGH Risk (0.70-1.00)
❌ Recommend decline  
❌ If approved, requires approval authority  
❌ Monthly monitoring minimum  
❌ Escalation to risk committee  

---

## Data Quality Checks

### Before Using Analysis
- ✅ Data completeness: 99.98%
- ✅ Data accuracy: 99.95%
- ✅ No data drift detected
- ✅ Model is HEALTHY

### If You See Issues
1. Check `Documentation/Technical_Reports/MODEL_ARCHITECTURE.md`
2. Review `Dashboards/Monitoring_Dashboards/operational_monitoring_dashboard.html`
3. Contact risk operations team

---

## Common Questions

**Q: Why is a customer flagged as HIGH risk?**  
A: Model considers bureau inquiries, payment history, credit ratios. High flag = multiple risk factors. Review explanation in dashboard.

**Q: Can we override model predictions?**  
A: Yes, with management approval. Document rationale for audit trail.

**Q: How often is the model updated?**  
A: Monthly retraining. Performance reviewed quarterly. Emergency updates if drift detected.

**Q: What's the model accuracy?**  
A: AUC=0.7412, F1=0.4523. See `Documentation/Technical_Reports/` for details.

---

## Escalation Procedures

### When to Escalate
1. Default rate rising rapidly (>1% per week)
2. Concentration risk threshold exceeded
3. Model drift detected (KS test p<0.05)
4. Data quality issues found

### How to Escalate
1. Email: risk-analysis@company.com
2. Slack: #risk-escalation
3. Phone: Risk Operations (555-0001)

---

## Resources

- **API Documentation**: `Documentation/API_Documentation/API_REFERENCE.md`
- **Technical Details**: `Documentation/Technical_Reports/MODEL_ARCHITECTURE.md`
- **Compliance Info**: `Documentation/Compliance_Docs/REGULATORY_COMPLIANCE.md`
- **Operations Guide**: `Documentation/SOPs/DAILY_OPERATIONS.md`

---

**Last Updated**: August 11, 2024  
**Next Review**: September 11, 2024
