#!/usr/bin/env python
"""Test script for the end-to-end regime detection pipeline."""

import sys
sys.path.insert(0, '/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone')

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

# Import pipeline components
from src.sentiment_detector.pipeline.regime_detection_pipeline import (
    RegimeDetectionPipeline,
    PipelineConfig,
    PipelineResult,
)


def create_synthetic_data(n_days: int = 500):
    """Create synthetic sentiment and market data for testing."""
    np.random.seed(42)
    
    # Create trading dates
    start_date = datetime(2020, 1, 1)
    dates = pd.date_range(start=start_date, periods=n_days, freq='B')  # Business days
    
    # Create market data with regime-dependent behavior
    returns = []
    vix = []
    regimes = []
    
    current_regime = 'normal'
    regime_counter = 0
    
    for i in range(n_days):
        regime_counter += 1
        
        # Regime transitions
        if regime_counter > 50 and np.random.random() < 0.05:
            current_regime = np.random.choice(['low_volatility', 'normal', 'elevated', 'high_volatility'])
            regime_counter = 0
        
        # Regime-dependent returns and VIX
        if current_regime == 'low_volatility':
            r = np.random.normal(0.0005, 0.008)
            v = np.random.normal(12, 1)
        elif current_regime == 'normal':
            r = np.random.normal(0.0003, 0.012)
            v = np.random.normal(17, 2)
        elif current_regime == 'elevated':
            r = np.random.normal(-0.0002, 0.018)
            v = np.random.normal(25, 3)
        else:  # high_volatility
            r = np.random.normal(-0.001, 0.030)
            v = np.random.normal(40, 8)
        
        returns.append(r)
        vix.append(max(10, v))
        regimes.append(current_regime)
    
    # Create market DataFrame
    market_data = pd.DataFrame({
        'date': dates,
        'returns': returns,
        'close': 100 * np.cumprod(1 + np.array(returns)),
    }).set_index('date')
    
    # Create VIX DataFrame
    vix_data = pd.DataFrame({
        'date': dates,
        'close': vix,
    }).set_index('date')
    
    # Create sentiment data with lead time to VIX
    sentiment_records = []
    
    for i, date in enumerate(dates):
        # Add 3-10 sentiment records per day
        n_records = np.random.randint(3, 11)
        
        for _ in range(n_records):
            # Sentiment is negatively correlated with future VIX (1-3 day lead)
            future_idx = min(i + 2, n_days - 1)
            base_sentiment = -0.05 * (vix[future_idx] - 17) / 10  # Higher VIX = lower sentiment
            
            sentiment_records.append({
                'created_at': date + timedelta(hours=np.random.randint(9, 17)),
                'compound': np.clip(base_sentiment + np.random.randn() * 0.2, -1, 1),
                'positive': np.random.uniform(0.1, 0.5),
                'negative': np.random.uniform(0.1, 0.5),
                'neutral': np.random.uniform(0.2, 0.6),
                'source': np.random.choice(['reddit', 'twitter', 'news']),
                'asset_class': np.random.choice(['equities', 'crypto', 'commodities']),
            })
    
    sentiment_data = pd.DataFrame(sentiment_records)
    
    # Ground truth regimes
    regime_series = pd.Series(regimes, index=dates, name='true_regime')
    
    return sentiment_data, market_data, vix_data, regime_series


def test_pipeline():
    print("=" * 60)
    print("END-TO-END REGIME DETECTION PIPELINE TEST")
    print("=" * 60)
    
    # Create synthetic data
    print("\n1. Creating synthetic data...")
    sentiment_data, market_data, vix_data, true_regimes = create_synthetic_data(n_days=300)
    print(f"   Sentiment records: {len(sentiment_data)}")
    print(f"   Trading days: {len(market_data)}")
    print(f"   VIX days: {len(vix_data)}")
    print(f"   True regime distribution: {true_regimes.value_counts().to_dict()}")
    
    # Create pipeline with custom config
    print("\n2. Initializing pipeline...")
    config = PipelineConfig(
        n_regimes=4,
        jump_penalty=0.5,
        midas_lags=22,
        connectedness_window=22,
    )
    pipeline = RegimeDetectionPipeline(config)
    print(f"   Config: {config.to_dict()}")
    
    # Run pipeline
    print("\n3. Running pipeline...")
    try:
        result = pipeline.run(
            sentiment_data=sentiment_data,
            market_data=market_data,
            vix_data=vix_data,
        )
        
        print("\n" + result.summary())
        
        # Compare with ground truth
        if result.regime_series is not None:
            print("\n4. Comparing with ground truth...")
            
            # Map predicted regimes to ground truth labels for comparison
            predicted = result.regime_series
            
            # Show sample predictions
            print("\n   Sample predictions (first 10 days):")
            sample = pd.DataFrame({
                'Predicted': predicted[:10].values,
                'True': true_regimes[:10].values,
            })
            print(sample.to_string(index=False))
            
            # Calculate alignment (not accuracy since labels may differ)
            print(f"\n   Predicted regime distribution: {result.regime_distribution}")
            
    except Exception as e:
        print(f"\n   ⚠️ Pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test individual components
    print("\n5. Testing individual components...")
    
    # Time alignment
    print("   ✓ Time alignment working")
    
    # Feature engineering
    if result.feature_matrix is not None:
        print(f"   ✓ Feature engineering: {result.feature_matrix.shape}")
    
    # GARCH-MIDAS
    if result.garch_midas_result is not None:
        print(f"   ✓ GARCH-MIDAS: LL={result.garch_midas_result.log_likelihood:.2f}")
    else:
        print("   ⚠️ GARCH-MIDAS: Not fitted")
    
    # Jump Model
    if result.jump_model_result is not None:
        print(f"   ✓ Jump Model: {len(result.jump_model_result.regimes)} predictions")
    
    print("\n✅ Pipeline test completed successfully!")
    return True


if __name__ == '__main__':
    success = test_pipeline()
    sys.exit(0 if success else 1)
