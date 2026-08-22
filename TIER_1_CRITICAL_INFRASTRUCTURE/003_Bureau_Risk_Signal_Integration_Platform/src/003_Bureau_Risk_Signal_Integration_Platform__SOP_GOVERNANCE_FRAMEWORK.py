# ============================================================================
# ENTERPRISE SOP GOVERNANCE FRAMEWORK
# ============================================================================
# Standard Operating Procedures for Top-Tier Financial Institutions
# Compliance: BCBS 239, SOX 404, JP Morgan, Goldman Sachs, Bloomberg standards
# ============================================================================

import os
import json
import hashlib
import logging
import numpy as np
from datetime import datetime
from pathlib import Path

# ============================================================================
# CLASS: GOVERNANCE TRACKER
# ============================================================================

class GovernanceTracker:
    """
    Enterprise SOP compliance tracker for data processing workflows.
    Implements standards from: JP Morgan, Goldman Sachs, Bloomberg, Morgan Stanley
    """

    def __init__(self, chunk_name, problem_id, data_owner, sensitivity_level='CONFIDENTIAL'):
        """
        Initialize governance tracker.

        Args:
            chunk_name: CHUNK_XX name
            problem_id: Problem 20 (Bureau Risk Signal Integration)
            data_owner: Data ownership (e.g., 'Risk Analytics Team')
            sensitivity_level: CONFIDENTIAL | INTERNAL | PUBLIC
        """
        self.chunk_name = chunk_name
        self.problem_id = problem_id
        self.data_owner = data_owner
        self.sensitivity_level = sensitivity_level
        self.execution_id = self._generate_execution_id()
        self.start_time = datetime.now()
        self.governance_log = []
        self.quality_gates = {}
        self.data_lineage = {}
        self.version_manifest = {}
        self.field_changes = {}
        self.pii_fields = set()
        self.reconciliation_results = {}
        self.access_audit = []

    def _generate_execution_id(self):
        """Generate unique execution ID for auditability."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{self.chunk_name}_{timestamp}_{self.problem_id}"

    def log_governance_event(self, event_type, description, status='SUCCESS', details=None):
        """Log governance-related events for audit trail."""
        event = {
            'timestamp': datetime.now().isoformat(),
            'execution_id': self.execution_id,
            'event_type': event_type,
            'description': description,
            'status': status,
            'details': details or {},
        }
        self.governance_log.append(event)
        return event

    def set_quality_gate(self, gate_name, threshold, actual_value, unit='records', status='PENDING'):
        """
        Define and track quality gates (SLA thresholds).

        Standards from BCBS 239 (data quality):
        - Must pass all critical gates before proceeding
        - Gate failures must be logged and escalated
        """
        gate = {
            'gate_name': gate_name,
            'threshold': threshold,
            'actual_value': actual_value,
            'unit': unit,
            'pass': actual_value >= threshold if gate_name not in ['missing_percentage', 'error_rate'] else actual_value <= threshold,
            'status': 'PASS' if (actual_value >= threshold if gate_name not in ['missing_percentage', 'error_rate'] else actual_value <= threshold) else 'FAIL',
            'timestamp': datetime.now().isoformat(),
        }
        self.quality_gates[gate_name] = gate

        if not gate['pass']:
            self.log_governance_event(
                'QUALITY_GATE_FAILURE',
                f"Quality gate '{gate_name}' failed: {actual_value} {unit}",
                status='WARNING',
                details=gate
            )

        return gate

    def track_data_lineage(self, source_file, output_file, record_count, transformation_type):
        """
        Track data lineage for SOX 404 compliance (internal control verification).
        Full parent-child tracking of data transformations.
        """
        lineage_record = {
            'source': source_file,
            'output': output_file,
            'record_count': record_count,
            'transformation_type': transformation_type,
            'timestamp': datetime.now().isoformat(),
            'checksum': self._calculate_file_checksum(output_file) if os.path.exists(output_file) else 'N/A',
        }

        if source_file not in self.data_lineage:
            self.data_lineage[source_file] = []

        self.data_lineage[source_file].append(lineage_record)
        return lineage_record

    def _calculate_file_checksum(self, filepath, algorithm='sha256'):
        """Calculate file checksum for data integrity verification."""
        if not os.path.exists(filepath):
            return None

        hash_func = hashlib.new(algorithm)
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    def _convert_to_serializable(self, obj):
        """Helper to convert numpy/bool types to JSON-serializable Python types."""
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, (np.bool_, bool)):
            return bool(obj)
        return obj

    def create_version_manifest(self, dataset_name, version, record_count, column_count, changes_summary):
        """
        Create versioned dataset manifest (JP Morgan standard).
        Enables rollback and version tracking.
        """
        manifest = {
            'dataset_name': dataset_name,
            'version': version,
            'execution_id': self.execution_id,
            'timestamp': datetime.now().isoformat(),
            'record_count': record_count,
            'column_count': column_count,
            'data_owner': self.data_owner,
            'sensitivity_level': self.sensitivity_level,
            'changes_summary': changes_summary,
            'checksum': None,  # Will be filled after save
        }
        self.version_manifest[dataset_name] = manifest
        return manifest

    def track_field_changes(self, field_name, change_type, before_value, after_value, affected_records):
        """
        Track field-level changes for detailed change logs.
        Required for BCBS 239 (detailed data aggregation).
        """
        change = {
            'field': field_name,
            'change_type': change_type,  # MISSING_FILLED, OUTLIER_CAPPED, STANDARDIZED, etc.
            'before': before_value,
            'after': after_value,
            'affected_records': affected_records,
            'timestamp': datetime.now().isoformat(),
        }

        if field_name not in self.field_changes:
            self.field_changes[field_name] = []

        self.field_changes[field_name].append(change)
        return change

    def classify_pii_field(self, field_name, classification='SENSITIVE', masking_rule=None):
        """
        Classify and track PII (Personally Identifiable Information) fields.
        Standards: GDPR, CCPA, data protection regulations.
        """
        self.pii_fields.add(field_name)

        pii_classification = {
            'field_name': field_name,
            'classification': classification,  # SENSITIVE, INTERNAL, PUBLIC
            'masking_rule': masking_rule,
            'timestamp': datetime.now().isoformat(),
        }

        self.log_governance_event(
            'PII_CLASSIFICATION',
            f"Field '{field_name}' classified as {classification}",
            details=pii_classification
        )

        return pii_classification

    def record_reconciliation(self, rec_name, source_count, output_count, variance_tolerance=0.01):
        """
        Record reconciliation results (SOX 404 control testing).
        Validates data integrity through count verification.
        """
        variance = abs(source_count - output_count) / source_count if source_count > 0 else 0
        reconciliation = {
            'reconciliation_name': rec_name,
            'source_count': source_count,
            'output_count': output_count,
            'variance_percentage': variance * 100,
            'within_tolerance': variance <= variance_tolerance,
            'timestamp': datetime.now().isoformat(),
        }

        self.reconciliation_results[rec_name] = reconciliation

        if not reconciliation['within_tolerance']:
            self.log_governance_event(
                'RECONCILIATION_VARIANCE',
                f"Reconciliation '{rec_name}' variance exceeds tolerance",
                status='WARNING',
                details=reconciliation
            )

        return reconciliation

    def add_access_audit(self, user_id, action, resource, timestamp=None):
        """
        Track data access for audit compliance.
        Required for SOX 404 (access control verification).
        """
        audit_entry = {
            'user_id': user_id,
            'action': action,  # READ, WRITE, DELETE, EXPORT
            'resource': resource,
            'timestamp': timestamp or datetime.now().isoformat(),
            'execution_id': self.execution_id,
        }
        self.access_audit.append(audit_entry)
        return audit_entry

    def generate_rollback_procedure(self, previous_version, current_version, restoration_steps):
        """
        Generate rollback procedure for data recovery (disaster recovery SOP).
        """
        rollback_doc = {
            'from_version': current_version,
            'to_version': previous_version,
            'generated_timestamp': datetime.now().isoformat(),
            'restoration_steps': restoration_steps,
            'estimated_duration_minutes': len(restoration_steps) * 2,
            'risk_level': 'LOW' if len(restoration_steps) <= 3 else 'MEDIUM',
        }
        return rollback_doc

    def create_data_dictionary_entry(self, field_name, field_type, description, business_rule, sample_values):
        """
        Create comprehensive data dictionary with business rules (JP Morgan standard).
        """
        dictionary_entry = {
            'field_name': field_name,
            'field_type': field_type,
            'description': description,
            'business_rule': business_rule,
            'sample_values': sample_values[:5],  # First 5 samples
            'classification': 'PII' if field_name in self.pii_fields else 'NON-PII',
            'timestamp': datetime.now().isoformat(),
        }
        return dictionary_entry

    def generate_compliance_report(self):
        """
        Generate comprehensive compliance report for regulatory submission.
        Covers: BCBS 239, SOX 404, data governance standards.
        """
        # Calculate pass/fail for quality gates
        gates_passed = sum(1 for g in self.quality_gates.values() if g['status'] == 'PASS')
        gates_total = len(self.quality_gates)

        # Calculate pass/fail for reconciliation
        rec_passed = sum(1 for r in self.reconciliation_results.values() if r['within_tolerance'])
        rec_total = len(self.reconciliation_results)

        # Calculate execution time
        execution_time = (datetime.now() - self.start_time).total_seconds() / 60  # minutes

        compliance_report = {
            'timestamp': datetime.now().isoformat(),
            'execution_id': self.execution_id,
            'chunk': self.chunk_name,
            'problem': self.problem_id,
            'data_owner': self.data_owner,
            'sensitivity': self.sensitivity_level,
            'execution_duration_minutes': round(execution_time, 2),

            # Quality Gates (BCBS 239)
            'quality_gates': {
                'total': gates_total,
                'passed': gates_passed,
                'failed': gates_total - gates_passed,
                'pass_rate': f"{(gates_passed/gates_total*100):.1f}%" if gates_total > 0 else "N/A",
                'details': self.quality_gates,
            },

            # Reconciliation (SOX 404)
            'reconciliation': {
                'total': rec_total,
                'passed': rec_passed,
                'failed': rec_total - rec_passed,
                'pass_rate': f"{(rec_passed/rec_total*100):.1f}%" if rec_total > 0 else "N/A",
                'details': self.reconciliation_results,
            },

            # Data Lineage
            'data_lineage': {
                'sources': len(self.data_lineage),
                'transformations': sum(len(v) for v in self.data_lineage.values()),
            },

            # PII Protection
            'pii_fields_identified': len(self.pii_fields),
            'pii_fields': list(self.pii_fields),

            # Audit Trail
            'governance_events': len(self.governance_log),
            'access_audit_entries': len(self.access_audit),

            # Overall Compliance Status
            'overall_status': 'COMPLIANT' if (gates_passed == gates_total and rec_passed == rec_total) else 'NON-COMPLIANT',
        }

        return compliance_report

    def save_governance_package(self, output_dir):
        """
        Save complete governance package (all compliance documentation).
        """
        os.makedirs(output_dir, exist_ok=True)

        # Helper to convert booleans
        def convert_with_bools(obj):
            if isinstance(obj, bool):
                return obj
            elif isinstance(obj, np.bool_):
                return bool(obj)
            elif isinstance(obj, (np.integer, np.floating)):
                return self._convert_to_serializable(obj)
            elif isinstance(obj, dict):
                return {k: convert_with_bools(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_with_bools(v) for v in obj]
            return obj

        # 1. Governance Log
        governance_file = f'{output_dir}/governance_audit_trail.json'
        with open(governance_file, 'w') as f:
            json.dump(convert_with_bools(self.governance_log), f, indent=2)

        # 2. Quality Gates Report
        gates_file = f'{output_dir}/quality_gates_report.json'
        with open(gates_file, 'w') as f:
            json.dump(convert_with_bools(self.quality_gates), f, indent=2)

        # 3. Data Lineage
        lineage_file = f'{output_dir}/data_lineage_manifest.json'
        with open(lineage_file, 'w') as f:
            json.dump(convert_with_bools(self.data_lineage), f, indent=2)

        # 4. Version Manifest
        version_file = f'{output_dir}/version_manifest.json'
        with open(version_file, 'w') as f:
            json.dump(convert_with_bools(self.version_manifest), f, indent=2)

        # 5. Field Changes Log
        changes_file = f'{output_dir}/field_changes_log.json'
        with open(changes_file, 'w') as f:
            json.dump(convert_with_bools(self.field_changes), f, indent=2)

        # 6. Reconciliation Report
        reconciliation_file = f'{output_dir}/reconciliation_report.json'
        with open(reconciliation_file, 'w') as f:
            json.dump(convert_with_bools(self.reconciliation_results), f, indent=2)

        # 7. Access Audit Trail
        access_file = f'{output_dir}/access_audit_trail.json'
        with open(access_file, 'w') as f:
            json.dump(convert_with_bools(self.access_audit), f, indent=2)

        # 8. Compliance Report (Main Report)
        compliance_file = f'{output_dir}/compliance_report.json'
        with open(compliance_file, 'w') as f:
            json.dump(convert_with_bools(self.generate_compliance_report()), f, indent=2)

        return {
            'governance_audit_trail': governance_file,
            'quality_gates_report': gates_file,
            'data_lineage_manifest': lineage_file,
            'version_manifest': version_file,
            'field_changes_log': changes_file,
            'reconciliation_report': reconciliation_file,
            'access_audit_trail': access_file,
            'compliance_report': compliance_file,
        }

# ============================================================================
# QUICK START TEMPLATE FOR CHUNKS
# ============================================================================

def create_chunk_governance_template(chunk_name, problem_id, data_owner):
    """
    Quick template for initializing governance in any chunk.

    Usage:
        gov = create_chunk_governance_template('CHUNK_05', 'Problem 20', 'Risk Analytics Team')
        gov.set_quality_gate('missing_percentage', 1.0, 0.0)  # Must have < 1% missing
        gov.track_data_lineage('input.csv', 'output.csv', 100000, 'MODEL_TRAINING')
        gov.save_governance_package('governance_output')
    """
    return GovernanceTracker(chunk_name, problem_id, data_owner, sensitivity_level='CONFIDENTIAL')

# ============================================================================
# END OF FRAMEWORK
# ============================================================================
