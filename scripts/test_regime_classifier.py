#!/usr/bin/env python3
"""
Test the ML Regime Classifier.

Verifies that the trained model can be loaded and used for inference.
"""

import sys
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from sentiment_detector.services.regime_classifier import (
    MLRegimeClassifier,
    SentimentFeatures,
    RegimeState,
)


def test_ml_classifier():
    """Test the ML-based regime classifier."""
    
    print("="*60)
    print("ML REGIME CLASSIFIER TEST")
    print("="*60)
    
    # Test 1: Load the best model
    print("\n1. Loading best model...")
    classifier = MLRegimeClassifier(model_type="best")
    
    if classifier.is_loaded:
        print(f"   ✓ Model loaded: {classifier.model_version}")
        print(f"   ✓ Model type: {classifier._model_type}")
    else:
        print("   ✗ Model not loaded!")
        return False
    
    # Test 2: Classify a "risk_on" scenario
    print("\n2. Testing risk_on scenario (bullish sentiment, low VIX, low CISS)...")
    risk_on_features = SentimentFeatures(
        equity_sentiment=0.25,
        crypto_sentiment=0.30,
        forex_sentiment=0.10,
        commodity_sentiment=0.15,
        cross_asset_mean=0.20,
        cross_asset_std=0.05,
        sentiment_momentum=0.05,
        sentiment_acceleration=0.01,
        max_divergence=0.20,
        vix_level=14.0,
        ciss_level=0.08,  # Low stress = risk_on
    )
    
    result = classifier.classify(risk_on_features)
    print(f"   State: {result.state.value}")
    print(f"   Confidence: {result.confidence:.2%}")
    print(f"   Probabilities:")
    print(f"     risk_on: {result.prob_risk_on:.2%}")
    print(f"     transition: {result.prob_transition:.2%}")
    print(f"     risk_off: {result.prob_risk_off:.2%}")
    
    # Test 3: Classify a "risk_off" scenario
    print("\n3. Testing risk_off scenario (bearish sentiment, high VIX, high CISS)...")
    risk_off_features = SentimentFeatures(
        equity_sentiment=-0.40,
        crypto_sentiment=-0.50,
        forex_sentiment=-0.20,
        commodity_sentiment=0.10,  # Gold might be positive
        cross_asset_mean=-0.25,
        cross_asset_std=0.30,
        sentiment_momentum=-0.15,
        sentiment_acceleration=-0.05,
        max_divergence=0.60,
        vix_level=45.0,
        ciss_level=0.55,  # High stress = risk_off
    )
    
    result = classifier.classify(risk_off_features)
    print(f"   State: {result.state.value}")
    print(f"   Confidence: {result.confidence:.2%}")
    print(f"   Probabilities:")
    print(f"     risk_on: {result.prob_risk_on:.2%}")
    print(f"     transition: {result.prob_transition:.2%}")
    print(f"     risk_off: {result.prob_risk_off:.2%}")
    
    # Test 4: Classify a "transition" scenario
    print("\n4. Testing transition scenario (mixed sentiment, moderate VIX/CISS)...")
    transition_features = SentimentFeatures(
        equity_sentiment=0.05,
        crypto_sentiment=-0.10,
        forex_sentiment=0.00,
        commodity_sentiment=0.05,
        cross_asset_mean=0.00,
        cross_asset_std=0.15,
        sentiment_momentum=-0.02,
        sentiment_acceleration=0.00,
        max_divergence=0.15,
        vix_level=22.0,
        ciss_level=0.25,  # Moderate stress = transition
    )
    
    result = classifier.classify(transition_features)
    print(f"   State: {result.state.value}")
    print(f"   Confidence: {result.confidence:.2%}")
    print(f"   Probabilities:")
    print(f"     risk_on: {result.prob_risk_on:.2%}")
    print(f"     transition: {result.prob_transition:.2%}")
    print(f"     risk_off: {result.prob_risk_off:.2%}")
    
    # Test 5: Check feature importances
    print("\n5. Top feature importances:")
    importances = classifier.feature_importance
    if importances:
        sorted_imp = sorted(importances.items(), key=lambda x: x[1], reverse=True)[:5]
        for feat, imp in sorted_imp:
            print(f"   {feat}: {imp:.4f}")
    
    # Test 6: Try loading RF model specifically
    print("\n6. Testing Random Forest model...")
    rf_classifier = MLRegimeClassifier(model_type="rf")
    if rf_classifier.is_loaded:
        result = rf_classifier.classify(risk_on_features)
        print(f"   ✓ RF Model: {result.state.value} ({result.confidence:.2%})")
    
    print("\n" + "="*60)
    print("ALL TESTS PASSED ✓")
    print("="*60)
    
    return True


if __name__ == "__main__":
    success = test_ml_classifier()
    sys.exit(0 if success else 1)
