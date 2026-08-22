#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
PROBLEM_004: CUSTOMER 360-DEGREE ANALYSIS
CHUNK_04: FEATURE ENGINEERING LIBRARY
================================================================================

Utility classes for feature engineering:
- FeatureCreator: Create polynomial and interaction features
- CategoricalEncoder: Encode categorical variables
- FeatureTransformer: Transform features (scaling, normalization)
- FeatureSelector: Select best features
- FeatureQualityAssessor: Assess engineered features
- FeatureInteractionAnalyzer: Detect and create interactions

================================================================================
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif, mutual_info_classif
import warnings

warnings.filterwarnings('ignore')


class FeatureCreator:
    """Create new features from existing ones"""

    def __init__(self):
        self.created_features = {}

    def create_polynomial_features(self, df, columns, degree=2):
        """Create polynomial features"""
        new_df = df.copy()
        created = []

        for col in columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                for d in range(2, degree + 1):
                    new_col_name = f"{col}_poly_{d}"
                    new_df[new_col_name] = df[col] ** d
                    created.append(new_col_name)

        self.created_features['polynomial'] = created
        return new_df, created

    def create_interaction_features(self, df, column_pairs):
        """Create interaction features from column pairs"""
        new_df = df.copy()
        created = []

        for col1, col2 in column_pairs:
            if (pd.api.types.is_numeric_dtype(df[col1]) and
                pd.api.types.is_numeric_dtype(df[col2])):
                new_col_name = f"{col1}_x_{col2}"
                new_df[new_col_name] = df[col1] * df[col2]
                created.append(new_col_name)

        self.created_features['interaction'] = created
        return new_df, created

    def create_ratio_features(self, df, column_pairs):
        """Create ratio features"""
        new_df = df.copy()
        created = []

        for col1, col2 in column_pairs:
            if (pd.api.types.is_numeric_dtype(df[col1]) and
                pd.api.types.is_numeric_dtype(df[col2])):
                # Avoid division by zero
                new_col_name = f"{col1}_ratio_{col2}"
                new_df[new_col_name] = np.where(
                    df[col2] != 0,
                    df[col1] / df[col2],
                    0
                )
                created.append(new_col_name)

        self.created_features['ratio'] = created
        return new_df, created

    def create_log_features(self, df, columns):
        """Create log-transformed features"""
        new_df = df.copy()
        created = []

        for col in columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                if (df[col] > 0).all():
                    new_col_name = f"{col}_log"
                    new_df[new_col_name] = np.log(df[col])
                    created.append(new_col_name)

        self.created_features['log'] = created
        return new_df, created


class CategoricalEncoder:
    """Encode categorical variables"""

    def __init__(self):
        self.encoders = {}
        self.encoding_mapping = {}

    def label_encode(self, df, columns):
        """Label encode categorical columns"""
        new_df = df.copy()

        for col in columns:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                unique_values = df[col].dropna().unique()
                mapping = {val: idx for idx, val in enumerate(unique_values)}
                new_df[col] = df[col].map(mapping)
                self.encoding_mapping[col] = mapping

        return new_df

    def one_hot_encode(self, df, columns, drop_first=True):
        """One-hot encode categorical columns"""
        new_df = df.copy()
        created = []

        for col in columns:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                dummies = pd.get_dummies(new_df[col], prefix=col, drop_first=drop_first)
                created.extend(dummies.columns.tolist())
                new_df = pd.concat([new_df, dummies], axis=1)
                new_df = new_df.drop(columns=[col])

        return new_df, created

    def ordinal_encode(self, df, columns, order_mapping):
        """Ordinal encode with specified order"""
        new_df = df.copy()

        for col, mapping in order_mapping.items():
            if col in df.columns:
                new_df[col] = df[col].map(mapping)
                self.encoding_mapping[col] = mapping

        return new_df


class FeatureTransformer:
    """Transform features"""

    def __init__(self):
        self.scalers = {}

    def standardize(self, df, columns):
        """Standardize features (z-score normalization)"""
        new_df = df.copy()
        scaler = StandardScaler()

        numeric_cols = [c for c in columns if pd.api.types.is_numeric_dtype(df[c])]
        if numeric_cols:
            new_df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            self.scalers['standard'] = scaler

        return new_df

    def normalize(self, df, columns):
        """Normalize features (0-1 scaling)"""
        new_df = df.copy()
        scaler = MinMaxScaler()

        numeric_cols = [c for c in columns if pd.api.types.is_numeric_dtype(df[c])]
        if numeric_cols:
            new_df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            self.scalers['minmax'] = scaler

        return new_df

    def log_transform(self, df, columns):
        """Log transform features"""
        new_df = df.copy()

        for col in columns:
            if pd.api.types.is_numeric_dtype(df[col]) and (df[col] > 0).all():
                new_df[col] = np.log(df[col])

        return new_df

    def sqrt_transform(self, df, columns):
        """Square root transform features"""
        new_df = df.copy()

        for col in columns:
            if pd.api.types.is_numeric_dtype(df[col]) and (df[col] >= 0).all():
                new_df[col] = np.sqrt(df[col])

        return new_df


class FeatureSelector:
    """Select best features"""

    def __init__(self):
        self.selected_features = {}

    def select_by_variance(self, df, threshold=0.01):
        """Select features by variance"""
        numeric_df = df.select_dtypes(include=[np.number])
        variances = numeric_df.var()
        selected = variances[variances > threshold].index.tolist()
        self.selected_features['variance'] = selected
        return selected

    def select_by_correlation(self, df, target_col=None, threshold=0.05):
        """Select features by correlation with target"""
        if target_col is None or target_col not in df.columns:
            return []

        numeric_df = df.select_dtypes(include=[np.number])
        if target_col not in numeric_df.columns:
            return []

        correlations = numeric_df.corr()[target_col].abs()
        selected = correlations[correlations > threshold].index.tolist()
        selected = [s for s in selected if s != target_col]
        self.selected_features['correlation'] = selected
        return selected

    def select_by_mutual_information(self, df, target_col=None, k=10):
        """Select top k features by mutual information"""
        if target_col is None or target_col not in df.columns:
            return []

        X = df.select_dtypes(include=[np.number]).drop(columns=[target_col])
        y = df[target_col]

        if len(X) == 0 or len(y) == 0:
            return []

        selector = SelectKBest(f_classif, k=min(k, X.shape[1]))
        selector.fit(X, y)
        selected = X.columns[selector.get_support()].tolist()
        self.selected_features['mutual_info'] = selected
        return selected


class FeatureQualityAssessor:
    """Assess quality of engineered features"""

    def __init__(self):
        pass

    def assess_features(self, df, original_df):
        """Assess new vs original features"""
        assessment = {
            'total_original': len(original_df.columns),
            'total_new': len(df.columns),
            'features_added': len(df.columns) - len(original_df.columns),
            'memory_increase_mb': (
                (df.memory_usage(deep=True).sum() -
                 original_df.memory_usage(deep=True).sum()) / (1024**2)
            )
        }

        return assessment

    def detect_redundant_features(self, df, threshold=0.95):
        """Detect highly correlated (redundant) features"""
        numeric_df = df.select_dtypes(include=[np.number])
        corr_matrix = numeric_df.corr()

        redundant_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i + 1, len(corr_matrix.columns)):
                if abs(corr_matrix.iloc[i, j]) > threshold:
                    redundant_pairs.append((
                        corr_matrix.columns[i],
                        corr_matrix.columns[j],
                        round(corr_matrix.iloc[i, j], 4)
                    ))

        return redundant_pairs

    def assess_feature_importance(self, df, features):
        """Assess importance of features"""
        importance = {}

        for feat in features:
            if feat in df.columns:
                if pd.api.types.is_numeric_dtype(df[feat]):
                    importance[feat] = {
                        'variance': float(df[feat].var()),
                        'std': float(df[feat].std()),
                        'range': float(df[feat].max() - df[feat].min())
                    }
                else:
                    importance[feat] = {
                        'unique_count': int(df[feat].nunique()),
                        'entropy': -sum(df[feat].value_counts(normalize=True) *
                                       np.log2(df[feat].value_counts(normalize=True) + 1e-10))
                    }

        return importance


class FeatureInteractionAnalyzer:
    """Analyze and detect feature interactions"""

    def __init__(self):
        self.interactions = {}

    def find_numeric_interactions(self, df, threshold=0.3):
        """Find significant numeric feature interactions"""
        numeric_df = df.select_dtypes(include=[np.number])
        interactions = []

        for i in range(len(numeric_df.columns)):
            for j in range(i + 1, len(numeric_df.columns)):
                col1, col2 = numeric_df.columns[i], numeric_df.columns[j]
                interaction = numeric_df[col1] * numeric_df[col2]

                # Check if interaction has enough variance
                if interaction.var() > threshold:
                    interactions.append({
                        'feature1': col1,
                        'feature2': col2,
                        'variance': float(interaction.var()),
                        'correlation': float(interaction.corr(numeric_df[col1]))
                    })

        self.interactions['numeric'] = interactions
        return interactions

    def find_categorical_interactions(self, df):
        """Find categorical feature interactions"""
        categorical_cols = df.select_dtypes(exclude=[np.number]).columns
        interactions = []

        for i, col1 in enumerate(categorical_cols):
            for col2 in categorical_cols[i+1:]:
                unique_combinations = len(df.groupby([col1, col2]))
                interactions.append({
                    'feature1': col1,
                    'feature2': col2,
                    'unique_combinations': unique_combinations
                })

        self.interactions['categorical'] = interactions
        return interactions
