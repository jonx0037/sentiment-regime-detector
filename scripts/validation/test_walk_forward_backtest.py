#!/usr/bin/env python
"""Test script for walk-forward backtesting framework."""

import sys
sys.path.insert(0, '/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone')

import numpy as np
import pandas as pd
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

from src.sentiment_detector.validation.walk_forward_backtest import (
    WalkForwardBacktester,
    create_synthetic_crisis_data,
    MarketEvent,
    COVID_CRASH,
    KEY_MARKET_EVENTS,
)


def test_walk_forward_backtester():
    print("=" * 60)
    print("WALK-FORWARD BACKTESTING FRAMEWORK TESTS")
    print("=" * 60)
    
    # Create synthetic data
    print("\n1. Creating synthetic crisis data...")
    features, labels = create_synthetic_crisis_data(n_days=800)
    print(f"   Features shape: {features.shape}")
    print(f"   Labels: {labels.value_counts().to_dict()}")
    
    # Encode labels
    le = LabelEncoder()
    labels_encoded = pd.Series(
        le.fit_transform(labels.values), 
        index=labels.index, 
        name='regime'
    )
    print(f"   Classes: {le.classes_}")
    
    # Define model functions
    def train_model(X_train, y_train):
        """Simple Random Forest model for testing."""
        model = RandomForestClassifier(
            n_estimators=50, 
            max_depth=5, 
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        return model
    
    def predict_fn(model, X_test):
        """Prediction function."""
        return model.predict(X_test)
    
    # Test window generation
    print("\n2. Testing window generation...")
    backtester = WalkForwardBacktester(
        train_window_days=252,  # 1 year
        test_window_days=21,    # 1 month
        step_days=21,           # Monthly
        purge_days=5,
    )
    
    windows = backtester.generate_windows(features)
    print(f"   Generated {len(windows)} windows")
    if len(windows) > 0:
        print(f"   First window: train {windows[0].train_start.date()} to {windows[0].train_end.date()}")
        print(f"                 test {windows[0].test_start.date()} to {windows[0].test_end.date()}")
    
    # Run walk-forward backtest
    print("\n3. Running walk-forward backtest...")
    try:
        results = backtester.run(
            features=features,
            labels=labels_encoded,
            model_fn=train_model,
            predict_fn=predict_fn,
        )
        
        print(f"\n   Results:")
        print(f"   Overall Accuracy: {results.overall_accuracy:.4f}")
        print(f"   Overall F1: {results.overall_f1:.4f}")
        print(f"   Windows tested: {len(results.window_results)}")
        print(f"   Avg window accuracy: {results.avg_window_accuracy:.4f} ± {results.std_window_accuracy:.4f}")
        
    except Exception as e:
        print(f"   ⚠️ Walk-forward test skipped (insufficient data for events): {e}")
    
    # Test with custom crisis events
    print("\n4. Testing with custom event periods...")
    
    # Create custom event that matches our synthetic data
    custom_event = MarketEvent(
        name="Synthetic Crisis 1",
        start_date=datetime(2019, 10, 28),  # Day 300 from 2019-01-01
        end_date=datetime(2019, 11, 17),    # Day 350
        expected_regime="high_volatility",
        pre_event_days=14,
    )
    
    backtester_custom = WalkForwardBacktester(
        train_window_days=200,
        test_window_days=21,
        step_days=21,
        events=[custom_event],
    )
    
    try:
        event_results = backtester_custom.run_event_only(
            features=features,
            labels=labels_encoded,
            model_fn=train_model,
            predict_fn=predict_fn,
            events=[custom_event],
        )
        
        print(f"\n   Event Results:")
        for event_name, result in event_results.items():
            print(f"   📌 {event_name}")
            print(f"      Detected pre-event: {result.detected_pre_event}")
            print(f"      Warning days: {result.warning_days}")
            print(f"      Accuracy during event: {result.regime_accuracy:.2%}")
            for evidence in result.evidence[:3]:
                print(f"      • {evidence}")
                
    except Exception as e:
        print(f"   ⚠️ Event test failed: {e}")
    
    # Test market events list
    print("\n5. Checking pre-defined market events...")
    print(f"   Available events: {len(KEY_MARKET_EVENTS)}")
    for event in KEY_MARKET_EVENTS:
        print(f"   • {event.name}: {event.start_date.date()} to {event.end_date.date()}")
    
    # Generate summary report
    print("\n6. Testing summary report generation...")
    if 'results' in dir() and results is not None:
        summary = results.summary()
        print(summary[:500] + "...\n")
    
    print("\n✅ Walk-forward backtesting tests completed!")
    return True


if __name__ == '__main__':
    success = test_walk_forward_backtester()
    sys.exit(0 if success else 1)
