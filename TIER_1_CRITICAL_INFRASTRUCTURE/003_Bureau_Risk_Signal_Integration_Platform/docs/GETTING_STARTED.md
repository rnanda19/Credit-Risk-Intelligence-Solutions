# Getting Started - Bureau Risk Signal Integration

## Quick Start (5 Minutes)

### 1. Understand the Project Structure
```
020_Bureau_Risk_Signal_Integration/
├─ 01_Data_Ingestion/              (CHUNK 01)
├─ 02_Data_Cleaning_Preprocessing/ (CHUNK 02)
├─ 03_Feature_Validation_Analysis/ (CHUNK 03)
├─ 04_Feature_Engineering/         (CHUNK 04)
├─ 05_Model_Development/           (CHUNK 05)
├─ 06_Model_Validation_Backtesting/(CHUNK 06)
├─ 07_Model_Calibration_Threshold/ (CHUNK 07)
├─ 08_Explainability_Attribution/  (CHUNK 08)
├─ 09_Model_Monitoring_Drift/      (CHUNK 09)
├─ 10_Production_Deployment/       (CHUNK 10)
├─ 11_Regulatory_Compliance/       (CHUNK 11)
├─ 12_Business_Intelligence/       (CHUNK 12)
├─ 13_Production_Release/          (CHUNK 13)
├─ Dashboards/                     (Interactive dashboards)
├─ Documentation/                  (This folder)
├─ Models/                         (Trained models)
└─ governance_documentation/       (Compliance records)
```

### 2. Run the Pipeline (First Time)

**IMPORTANT**: The Python scripts must be executed to generate actual outputs.

```bash
# Step 1: Setup environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Step 2: Execute all CHUNKs in sequence
cd 01_Data_Ingestion/
python CHUNK_01_Data_Ingestion.py

cd ../02_Data_Cleaning_Preprocessing/
python CHUNK_02_Data_Cleaning_Preprocessing_CORRECTED.py

# ... continue for CHUNKs 03-13
```

### 3. Access Dashboards
- **Executive**: `Dashboards/Executive_Dashboards/executive_dashboard.html`
- **Portfolio**: `Dashboards/Monitoring_Dashboards/portfolio_monitoring_dashboard.html`
- **Model Performance**: `Dashboards/Power_BI_Metrics/model_performance_dashboard.html`
- **Operations**: `Dashboards/Monitoring_Dashboards/operational_monitoring_dashboard.html`

---

## Key Outputs (Generated After Running Scripts)

### Data Files
- `01_Data_Ingestion/Integrated_Data/bureau_risk_integrated.csv` → 307,511 records
- `02_Data_Cleaning_Preprocessing/Cleaned_Data/bureau_risk_cleaned.csv` → Cleaned data
- `04_Feature_Engineering/Engineered_Data/bureau_risk_engineered.csv` → 91 features

### Model Files
- `05_Model_Development/Trained_Models/bureau_risk_random_forest_v1.pkl` → Trained model
- `05_Model_Development/Trained_Models/feature_scaler_v1.pkl` → Feature scaler

### Reports Generated
- `*/Reports/*.json` → Analysis reports (40+ files)
- `*/Governance/*.json` → Compliance documents (104 files)

---

## For Different Roles

### Executive / Management
1. Open: `Dashboards/Executive_Dashboards/executive_dashboard.html`
2. Review: Portfolio default rate, capital ratios, model performance
3. Check: Monthly compliance reports in `Documentation/Compliance_Docs/`

### Risk Analyst
1. Open: `Dashboards/Monitoring_Dashboards/portfolio_monitoring_dashboard.html`
2. Review: Risk by segment, concentration analysis, early warnings
3. Reference: `Documentation/User_Guides/ANALYST_GUIDE.md`

### Data Scientist / ML Engineer
1. Review: `05_Model_Development/Reports/model_card.json`
2. Check: `Documentation/Technical_Reports/MODEL_ARCHITECTURE.md`
3. Monitor: `Dashboards/Power_BI_Metrics/model_performance_dashboard.html`
4. Run: Monthly validation tests from `CHUNK_06`

### Operations / DevOps
1. Monitor: `Dashboards/Monitoring_Dashboards/operational_monitoring_dashboard.html`
2. Reference: `Documentation/SOPs/DAILY_OPERATIONS.md`
3. Follow: Incident response procedures in `Documentation/SOPs/`

---

## Documentation Map

| Need | Location | Format |
|------|----------|--------|
| API Usage | `Documentation/API_Documentation/API_REFERENCE.md` | Markdown |
| Compliance | `Documentation/Compliance_Docs/REGULATORY_COMPLIANCE.md` | Markdown |
| Operations | `Documentation/SOPs/DAILY_OPERATIONS.md` | Markdown |
| Technical | `Documentation/Technical_Reports/MODEL_ARCHITECTURE.md` | Markdown |
| User Guides | `Documentation/User_Guides/*.md` | Markdown |

---

## Troubleshooting

### Issue: Dashboards show "No data"
**Solution**: Run the Python CHUNK scripts first - they generate the data

### Issue: Models folder is empty
**Solution**: Run CHUNK 05 (Model Development) to train the model

### Issue: Reports missing
**Solution**: All CHUNKs must be executed - they generate reports in their `Reports/` folders

---

## Next Steps

1. **Read**: Complete project overview in `00_Project_Overview/Documentation/README.md`
2. **Execute**: Run Python CHUNK scripts 01-13 in sequence
3. **Verify**: Check that outputs appear in respective folders
4. **Deploy**: Follow deployment guide in `10_Production_Deployment/`
5. **Monitor**: Use dashboards for ongoing monitoring

---

**CRITICAL REMINDER**: The Python scripts (CHUNK_01 through CHUNK_13) MUST be executed to generate actual outputs. The folders are currently empty because the scripts have never been run.

To get real data:
```bash
for i in {01..13}; do
  python *_CHUNK_$i*.py
done
```

After execution, you'll have:
- ✅ 3 CSV data files
- ✅ 2 model files
- ✅ 40+ report files
- ✅ 104 governance documents
- ✅ 4 interactive dashboards with real data
