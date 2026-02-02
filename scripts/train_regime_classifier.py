#!/usr/bin/env python3
"""
Train ML-based Regime Classifier.

Trains Random Forest and XGBoost classifiers to predict market regimes
(risk_on, risk_off, transition) based on:
- Aggregated sentiment features
- ECB CISS stress index
- VIX levels
- Cross-asset sentiment divergence

Ground truth labels derived from CISS thresholds:
- calm (CISS < 0.15) -> risk_on
- moderate (0.15 <= CISS < 0.35) -> transition  
- elevated/crisis (CISS >= 0.35) -> risk_off

Author: Jonathan Rocha
Date: February 2, 2026
"""

import asyncio
import json
import pickle
import sys
from datetime import date, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import TimeSeriesSplit, cross_val_score, GridSearchCV
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.preprocessing import StandardScaler
import warnings

warnings.filterwarnings('ignore')

# Try to import xgboost
try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    print("XGBoost not installed. Using GradientBoosting as alternative.")

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


# ============================================================================
# Database Connection
# ============================================================================

def get_database_url() -> str:
    """Get database URL from environment or default."""
    import os
    return os.environ.get(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:password@localhost:5432/sentiment_db"
    )


async def get_session() -> AsyncSession:
    """Create async database session."""
    engine = create_async_engine(get_database_url(), echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return async_session()


# ============================================================================
# Data Loading Functions
# ============================================================================

async def load_ciss_data(
    session: AsyncSession,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load ECB CISS stress index data."""
    result = await session.execute(text("""
        SELECT date, value as ciss
        FROM stress_indices
        WHERE source = 'ecb_ciss'
        AND region = 'ea'
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'ciss'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


async def load_vix_data(
    session: AsyncSession,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load VIX data."""
    result = await session.execute(text("""
        SELECT date, close as vix, high as vix_high, low as vix_low
        FROM market_data
        WHERE symbol = '^VIX'
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'vix', 'vix_high', 'vix_low'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


async def load_market_returns(
    session: AsyncSession,
    symbol: str,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load market data and calculate returns."""
    result = await session.execute(text("""
        SELECT date, close, adj_close, volume
        FROM market_data
        WHERE symbol = :symbol
        AND date BETWEEN :start AND :end
        ORDER BY date
    """), {"symbol": symbol, "start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'close', 'adj_close', 'volume'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    
    # Calculate returns
    df['returns'] = np.log(df['adj_close'] / df['adj_close'].shift(1))
    df['returns_5d'] = df['returns'].rolling(5).sum()
    df['volatility_20d'] = df['returns'].rolling(20).std() * np.sqrt(252)
    
    return df


async def load_sentiment_by_asset(
    session: AsyncSession,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load daily aggregated sentiment by asset class."""
    result = await session.execute(text("""
        SELECT 
            DATE(rt.content_created_at) as date,
            rt.asset_class,
            AVG(ss.compound) as sentiment,
            STDDEV(ss.compound) as sentiment_std,
            COUNT(*) as text_count
        FROM sentiment_scores ss
        JOIN raw_texts rt ON ss.text_id = rt.id
        WHERE rt.content_created_at BETWEEN :start AND :end
        AND rt.asset_class IS NOT NULL
        GROUP BY DATE(rt.content_created_at), rt.asset_class
        ORDER BY date
    """), {"start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=['date', 'asset_class', 'sentiment', 'sentiment_std', 'text_count'])
    df['date'] = pd.to_datetime(df['date'])
    
    # Pivot to wide format
    sentiment_pivot = df.pivot(index='date', columns='asset_class', values='sentiment')
    std_pivot = df.pivot(index='date', columns='asset_class', values='sentiment_std')
    count_pivot = df.pivot(index='date', columns='asset_class', values='text_count')
    
    # Rename columns
    sentiment_pivot.columns = [f'sentiment_{col}' for col in sentiment_pivot.columns]
    std_pivot.columns = [f'sentiment_std_{col}' for col in std_pivot.columns]
    count_pivot.columns = [f'count_{col}' for col in count_pivot.columns]
    
    result_df = pd.concat([sentiment_pivot, std_pivot, count_pivot], axis=1)
    return result_df


async def load_aggregate_sentiment(
    session: AsyncSession,
    start_date: date,
    end_date: date,
) -> pd.DataFrame:
    """Load overall daily aggregate sentiment."""
    result = await session.execute(text("""
        SELECT 
            DATE(rt.content_created_at) as date,
            AVG(ss.compound) as sentiment_mean,
            STDDEV(ss.compound) as sentiment_std,
            AVG(ss.positive) as sentiment_pos,
            AVG(ss.negative) as sentiment_neg,
            COUNT(*) as total_texts
        FROM sentiment_scores ss
        JOIN raw_texts rt ON ss.text_id = rt.id
        WHERE rt.content_created_at BETWEEN :start AND :end
        GROUP BY DATE(rt.content_created_at)
        ORDER BY date
    """), {"start": start_date, "end": end_date})
    
    rows = result.fetchall()
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows, columns=[
        'date', 'sentiment_mean', 'sentiment_std', 
        'sentiment_pos', 'sentiment_neg', 'total_texts'
    ])
    df['date'] = pd.to_datetime(df['date'])
    df = df.set_index('date')
    return df


# ============================================================================
# Feature Engineering
# ============================================================================

def engineer_features(df: pd.DataFrame, use_lagged_ciss: bool = True) -> pd.DataFrame:
    """
    Engineer features for regime classification.
    
    Features:
    - Sentiment: mean, std, momentum, acceleration
    - CISS: level, change, rolling stats (LAGGED to prevent leakage)
    - VIX: level, change, term structure proxy
    - Cross-asset: divergence, correlation
    - Market: returns, volatility
    
    Args:
        df: Raw data DataFrame
        use_lagged_ciss: If True, lag CISS features by 1 day to prevent leakage
                         when predicting CISS-based regime labels
    """
    features = pd.DataFrame(index=df.index)
    
    # === CISS Features (LAGGED to prevent data leakage) ===
    # Since labels are derived from CISS, we use previous day's CISS to predict today's regime
    if 'ciss' in df.columns:
        lag = 1 if use_lagged_ciss else 0
        ciss = df['ciss'].shift(lag) if lag > 0 else df['ciss']
        
        features['ciss_lag1'] = ciss
        features['ciss_change'] = ciss.diff()
        features['ciss_change_5d'] = ciss.diff(5)
        features['ciss_ma5'] = ciss.rolling(5).mean()
        features['ciss_ma20'] = ciss.rolling(20).mean()
        features['ciss_above_ma20'] = (ciss > features['ciss_ma20']).astype(int)
        features['ciss_std_20d'] = ciss.rolling(20).std()
        # Trend: Is CISS rising or falling?
        features['ciss_trend'] = (ciss - ciss.shift(5)).apply(lambda x: 1 if x > 0 else (-1 if x < 0 else 0))
    
    # === VIX Features (current - VIX is forward looking, not leakage) ===
    if 'vix' in df.columns:
        features['vix'] = df['vix']
        features['vix_change'] = df['vix'].diff()
        features['vix_change_pct'] = df['vix'].pct_change()
        features['vix_ma5'] = df['vix'].rolling(5).mean()
        features['vix_ma20'] = df['vix'].rolling(20).mean()
        features['vix_above_ma20'] = (df['vix'] > features['vix_ma20']).astype(int)
        # VIX spike detection
        features['vix_spike'] = (df['vix'] > df['vix'].rolling(20).mean() + 2 * df['vix'].rolling(20).std()).astype(int)
    
    # VIX range (intraday volatility proxy)
    if 'vix_high' in df.columns and 'vix_low' in df.columns:
        features['vix_range'] = df['vix_high'] - df['vix_low']
    
    # === Sentiment Features ===
    if 'sentiment_mean' in df.columns:
        features['sentiment'] = df['sentiment_mean']
        features['sentiment_change'] = df['sentiment_mean'].diff()
        features['sentiment_momentum_5d'] = df['sentiment_mean'].diff(5)
        features['sentiment_momentum_20d'] = df['sentiment_mean'].diff(20)
        features['sentiment_ma5'] = df['sentiment_mean'].rolling(5).mean()
        features['sentiment_ma20'] = df['sentiment_mean'].rolling(20).mean()
        features['sentiment_acceleration'] = features['sentiment_change'].diff()
        
    if 'sentiment_std' in df.columns:
        features['sentiment_dispersion'] = df['sentiment_std']
    
    if 'sentiment_pos' in df.columns and 'sentiment_neg' in df.columns:
        features['sentiment_spread'] = df['sentiment_pos'] - df['sentiment_neg']
    
    # === Cross-Asset Sentiment Divergence ===
    sentiment_cols = [c for c in df.columns if c.startswith('sentiment_') and 'equity' in c.lower() or 'crypto' in c.lower()]
    if len(sentiment_cols) >= 2:
        # Max divergence between asset classes
        sentiment_matrix = df[sentiment_cols].values
        if not np.all(np.isnan(sentiment_matrix)):
            valid_mask = ~np.isnan(sentiment_matrix).all(axis=1)
            features.loc[valid_mask, 'cross_asset_divergence'] = np.nanmax(sentiment_matrix, axis=1)[valid_mask] - np.nanmin(sentiment_matrix, axis=1)[valid_mask]
    
    # === Market Returns & Volatility ===
    if 'returns' in df.columns:
        features['returns'] = df['returns']
        features['returns_5d'] = df['returns'].rolling(5).sum()
        features['returns_20d'] = df['returns'].rolling(20).sum()
        
    if 'volatility_20d' in df.columns:
        features['realized_vol'] = df['volatility_20d']
        features['vol_change'] = df['volatility_20d'].diff()
    
    # === Interaction Features (use lagged CISS) ===
    if 'ciss_lag1' in features.columns and 'vix' in df.columns:
        features['ciss_vix_ratio'] = features['ciss_lag1'] / (df['vix'] / 100 + 0.01)
    
    if 'sentiment' in features.columns and 'vix' in df.columns:
        features['sentiment_vix_interaction'] = features['sentiment'] * (1 / (df['vix'] + 1))
    
    return features


def create_regime_labels(ciss: pd.Series) -> pd.Series:
    """
    Create regime labels from CISS values.
    
    Based on ECB CISS documentation and historical analysis:
    - risk_on: Low stress (CISS < 0.15)
    - transition: Moderate stress (0.15 <= CISS < 0.35)
    - risk_off: High stress (CISS >= 0.35)
    """
    labels = pd.Series(index=ciss.index, dtype=str)
    labels[ciss < 0.15] = 'risk_on'
    labels[(ciss >= 0.15) & (ciss < 0.35)] = 'transition'
    labels[ciss >= 0.35] = 'risk_off'
    return labels


# ============================================================================
# Model Training
# ============================================================================

def train_random_forest(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
) -> Tuple[RandomForestClassifier, Dict]:
    """Train Random Forest classifier with hyperparameter tuning."""
    
    print("\n" + "="*60)
    print("Training Random Forest Classifier")
    print("="*60)
    
    # Parameter grid
    param_grid = {
        'n_estimators': [100, 200],
        'max_depth': [5, 10, 15],
        'min_samples_split': [5, 10],
        'min_samples_leaf': [2, 5],
        'class_weight': ['balanced', 'balanced_subsample'],
    }
    
    # Time series cross-validation
    tscv = TimeSeriesSplit(n_splits=3)
    
    rf = RandomForestClassifier(random_state=42, n_jobs=-1)
    
    print("Performing grid search...")
    grid_search = GridSearchCV(
        rf, param_grid, cv=tscv, scoring='f1_weighted', 
        n_jobs=-1, verbose=1
    )
    grid_search.fit(X_train, y_train)
    
    best_rf = grid_search.best_estimator_
    
    # Evaluate on validation set
    y_pred = best_rf.predict(X_val)
    
    metrics = {
        'accuracy': accuracy_score(y_val, y_pred),
        'f1_weighted': f1_score(y_val, y_pred, average='weighted'),
        'precision_weighted': precision_score(y_val, y_pred, average='weighted'),
        'recall_weighted': recall_score(y_val, y_pred, average='weighted'),
        'best_params': grid_search.best_params_,
        'feature_importance': dict(zip(X_train.columns, best_rf.feature_importances_)),
    }
    
    print(f"\nBest Parameters: {grid_search.best_params_}")
    print(f"\nValidation Results:")
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  F1 (weighted): {metrics['f1_weighted']:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_val, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_val, y_pred))
    
    # Feature importance
    print("\nTop 10 Feature Importances:")
    importance_sorted = sorted(
        metrics['feature_importance'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:10]
    for feat, imp in importance_sorted:
        print(f"  {feat}: {imp:.4f}")
    
    return best_rf, metrics


def train_xgboost(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    X_val: pd.DataFrame,
    y_val: pd.Series,
) -> Tuple[object, Dict]:
    """Train XGBoost or GradientBoosting classifier."""
    
    print("\n" + "="*60)
    if HAS_XGBOOST:
        print("Training XGBoost Classifier")
    else:
        print("Training GradientBoosting Classifier (XGBoost not available)")
    print("="*60)
    
    # Encode labels
    label_map = {'risk_on': 0, 'transition': 1, 'risk_off': 2}
    y_train_encoded = y_train.map(label_map)
    y_val_encoded = y_val.map(label_map)
    
    if HAS_XGBOOST:
        # XGBoost parameter grid
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [3, 5, 7],
            'learning_rate': [0.01, 0.1],
            'subsample': [0.8, 1.0],
            'colsample_bytree': [0.8, 1.0],
        }
        
        model = xgb.XGBClassifier(
            objective='multi:softmax',
            num_class=3,
            random_state=42,
            use_label_encoder=False,
            eval_metric='mlogloss',
        )
    else:
        # GradientBoosting as fallback
        param_grid = {
            'n_estimators': [100, 200],
            'max_depth': [3, 5],
            'learning_rate': [0.01, 0.1],
            'subsample': [0.8, 1.0],
        }
        
        model = GradientBoostingClassifier(random_state=42)
    
    # Time series cross-validation
    tscv = TimeSeriesSplit(n_splits=3)
    
    print("Performing grid search...")
    grid_search = GridSearchCV(
        model, param_grid, cv=tscv, scoring='f1_weighted',
        n_jobs=-1, verbose=1
    )
    grid_search.fit(X_train, y_train_encoded)
    
    best_model = grid_search.best_estimator_
    
    # Evaluate
    y_pred_encoded = best_model.predict(X_val)
    
    # Decode predictions
    reverse_map = {v: k for k, v in label_map.items()}
    y_pred = pd.Series(y_pred_encoded).map(reverse_map)
    
    metrics = {
        'accuracy': accuracy_score(y_val, y_pred),
        'f1_weighted': f1_score(y_val, y_pred, average='weighted'),
        'precision_weighted': precision_score(y_val, y_pred, average='weighted'),
        'recall_weighted': recall_score(y_val, y_pred, average='weighted'),
        'best_params': grid_search.best_params_,
        'label_map': label_map,
    }
    
    # Get feature importance
    if HAS_XGBOOST:
        metrics['feature_importance'] = dict(zip(X_train.columns, best_model.feature_importances_))
    else:
        metrics['feature_importance'] = dict(zip(X_train.columns, best_model.feature_importances_))
    
    print(f"\nBest Parameters: {grid_search.best_params_}")
    print(f"\nValidation Results:")
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  F1 (weighted): {metrics['f1_weighted']:.4f}")
    print(f"\nClassification Report:")
    print(classification_report(y_val, y_pred))
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_val, y_pred))
    
    # Feature importance
    print("\nTop 10 Feature Importances:")
    importance_sorted = sorted(
        metrics['feature_importance'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    for feat, imp in importance_sorted:
        print(f"  {feat}: {imp:.4f}")
    
    return best_model, metrics


# ============================================================================
# Main Training Pipeline
# ============================================================================

async def main():
    """Main training pipeline."""
    
    print("="*60)
    print("REGIME CLASSIFIER TRAINING PIPELINE")
    print("="*60)
    print(f"\nStarted: {pd.Timestamp.now()}")
    
    # Configuration
    START_DATE = date(2010, 1, 1)  # Start from when we have good data overlap
    END_DATE = date(2026, 1, 31)
    TRAIN_END = date(2023, 12, 31)  # Train up to end of 2023
    VAL_START = date(2024, 1, 1)   # Validate on 2024-2026
    
    print(f"\nData range: {START_DATE} to {END_DATE}")
    print(f"Training: {START_DATE} to {TRAIN_END}")
    print(f"Validation: {VAL_START} to {END_DATE}")
    
    # Connect to database
    print("\nConnecting to database...")
    session = await get_session()
    
    try:
        # Load all data
        print("\nLoading data from PostgreSQL...")
        
        ciss_df = await load_ciss_data(session, START_DATE, END_DATE)
        print(f"  CISS: {len(ciss_df)} records")
        
        vix_df = await load_vix_data(session, START_DATE, END_DATE)
        print(f"  VIX: {len(vix_df)} records")
        
        spy_df = await load_market_returns(session, 'SPY', START_DATE, END_DATE)
        print(f"  SPY: {len(spy_df)} records")
        
        sentiment_agg = await load_aggregate_sentiment(session, START_DATE, END_DATE)
        print(f"  Sentiment (aggregate): {len(sentiment_agg)} records")
        
        sentiment_by_asset = await load_sentiment_by_asset(session, START_DATE, END_DATE)
        print(f"  Sentiment (by asset): {len(sentiment_by_asset)} records")
        
        # Merge all data
        print("\nMerging datasets...")
        
        # Start with CISS as base (it's the label source)
        merged = ciss_df.copy()
        merged = merged.join(vix_df, how='left')
        
        # Only add SPY data if available
        if len(spy_df) > 0 and 'returns' in spy_df.columns:
            merged = merged.join(spy_df[['returns', 'volatility_20d']], how='left')
        else:
            print("  (SPY data not available, skipping market returns)")
            
        merged = merged.join(sentiment_agg, how='left')
        merged = merged.join(sentiment_by_asset, how='left')
        
        print(f"Merged dataset: {len(merged)} records")
        print(f"Date range: {merged.index.min()} to {merged.index.max()}")
        
        # Create labels
        print("\nCreating regime labels from CISS...")
        labels = create_regime_labels(merged['ciss'])
        
        label_counts = labels.value_counts()
        print(f"\nLabel distribution:")
        for label, count in label_counts.items():
            print(f"  {label}: {count} ({count/len(labels)*100:.1f}%)")
        
        # Engineer features
        print("\nEngineering features...")
        features = engineer_features(merged)
        
        # Drop rows with NaN (from rolling calculations) - use any valid features
        valid_cols = features.columns[features.notna().any()]
        features = features[valid_cols]
        
        # Require at least these core features
        core_features = ['ciss', 'vix', 'sentiment']
        available_core = [f for f in core_features if f in features.columns]
        
        if len(available_core) < 2:
            print(f"WARNING: Only {len(available_core)} core features available")
        
        # Fill missing values with forward fill then backward fill
        features = features.ffill().bfill()
        
        valid_mask = features.notna().all(axis=1) & labels.notna()
        features_clean = features[valid_mask]
        labels_clean = labels[valid_mask]
        
        print(f"Clean dataset: {len(features_clean)} records ({len(features_clean)/len(features)*100:.1f}%)")
        print(f"Features: {list(features_clean.columns)}")
        
        # Train/validation split (temporal)
        train_mask = features_clean.index <= pd.Timestamp(TRAIN_END)
        val_mask = features_clean.index >= pd.Timestamp(VAL_START)
        
        X_train = features_clean[train_mask]
        y_train = labels_clean[train_mask]
        X_val = features_clean[val_mask]
        y_val = labels_clean[val_mask]
        
        print(f"\nTrain set: {len(X_train)} samples")
        print(f"Validation set: {len(X_val)} samples")
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train),
            index=X_train.index,
            columns=X_train.columns
        )
        X_val_scaled = pd.DataFrame(
            scaler.transform(X_val),
            index=X_val.index,
            columns=X_val.columns
        )
        
        # Train models
        rf_model, rf_metrics = train_random_forest(X_train_scaled, y_train, X_val_scaled, y_val)
        xgb_model, xgb_metrics = train_xgboost(X_train_scaled, y_train, X_val_scaled, y_val)
        
        # Compare models
        print("\n" + "="*60)
        print("MODEL COMPARISON")
        print("="*60)
        print(f"\n{'Metric':<25} {'Random Forest':<15} {'XGBoost/GB':<15}")
        print("-"*55)
        print(f"{'Accuracy':<25} {rf_metrics['accuracy']:<15.4f} {xgb_metrics['accuracy']:<15.4f}")
        print(f"{'F1 (weighted)':<25} {rf_metrics['f1_weighted']:<15.4f} {xgb_metrics['f1_weighted']:<15.4f}")
        print(f"{'Precision (weighted)':<25} {rf_metrics['precision_weighted']:<15.4f} {xgb_metrics['precision_weighted']:<15.4f}")
        print(f"{'Recall (weighted)':<25} {rf_metrics['recall_weighted']:<15.4f} {xgb_metrics['recall_weighted']:<15.4f}")
        
        # Select best model
        if rf_metrics['f1_weighted'] >= xgb_metrics['f1_weighted']:
            best_model = rf_model
            best_metrics = rf_metrics
            best_model_name = 'random_forest'
        else:
            best_model = xgb_model
            best_metrics = xgb_metrics
            best_model_name = 'xgboost' if HAS_XGBOOST else 'gradient_boosting'
        
        print(f"\n✓ Best Model: {best_model_name} (F1: {best_metrics['f1_weighted']:.4f})")
        
        # Save models and artifacts
        models_dir = project_root / "models"
        models_dir.mkdir(exist_ok=True)
        
        print(f"\nSaving models to {models_dir}...")
        
        # Save Random Forest
        with open(models_dir / "regime_classifier_rf.pkl", 'wb') as f:
            pickle.dump({
                'model': rf_model,
                'scaler': scaler,
                'feature_names': list(X_train.columns),
                'label_map': {'risk_on': 0, 'transition': 1, 'risk_off': 2},
                'metrics': rf_metrics,
                'train_end_date': str(TRAIN_END),
            }, f)
        print("  ✓ regime_classifier_rf.pkl")
        
        # Save XGBoost/GB
        with open(models_dir / "regime_classifier_xgb.pkl", 'wb') as f:
            pickle.dump({
                'model': xgb_model,
                'scaler': scaler,
                'feature_names': list(X_train.columns),
                'label_map': xgb_metrics['label_map'],
                'metrics': xgb_metrics,
                'train_end_date': str(TRAIN_END),
            }, f)
        print("  ✓ regime_classifier_xgb.pkl")
        
        # Save best model separately
        with open(models_dir / "regime_classifier_best.pkl", 'wb') as f:
            pickle.dump({
                'model': best_model,
                'model_type': best_model_name,
                'scaler': scaler,
                'feature_names': list(X_train.columns),
                'label_map': best_metrics.get('label_map', {'risk_on': 0, 'transition': 1, 'risk_off': 2}),
                'metrics': best_metrics,
                'train_end_date': str(TRAIN_END),
            }, f)
        print("  ✓ regime_classifier_best.pkl")
        
        # Save training summary
        summary = {
            'training_date': str(pd.Timestamp.now()),
            'data_range': f"{START_DATE} to {END_DATE}",
            'train_samples': len(X_train),
            'val_samples': len(X_val),
            'features': list(X_train.columns),
            'best_model': best_model_name,
            'random_forest': {
                'accuracy': rf_metrics['accuracy'],
                'f1_weighted': rf_metrics['f1_weighted'],
                'best_params': rf_metrics['best_params'],
            },
            'xgboost': {
                'accuracy': xgb_metrics['accuracy'],
                'f1_weighted': xgb_metrics['f1_weighted'],
                'best_params': xgb_metrics['best_params'],
            },
        }
        
        with open(models_dir / "training_summary.json", 'w') as f:
            json.dump(summary, f, indent=2, default=str)
        print("  ✓ training_summary.json")
        
        print("\n" + "="*60)
        print("TRAINING COMPLETE")
        print("="*60)
        print(f"\nBest Model: {best_model_name}")
        print(f"Validation F1: {best_metrics['f1_weighted']:.4f}")
        print(f"Validation Accuracy: {best_metrics['accuracy']:.4f}")
        print(f"\nModels saved to: {models_dir}")
        
    finally:
        await session.close()


if __name__ == "__main__":
    asyncio.run(main())
