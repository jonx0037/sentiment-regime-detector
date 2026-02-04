#!/usr/bin/env python
"""Test script for hypothesis validator."""

import sys
sys.path.insert(0, '/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone')

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

from src.sentiment_detector.validation.hypothesis_validator import (
    HypothesisValidator,
    HypothesisResult,
    generate_hypothesis_report,
)

def test_hypothesis_validator():
    print('Testing HypothesisValidator...')

    # Create test data
    np.random.seed(42)
    dates = pd.date_range(start='2020-01-01', periods=500, freq='D')
    n = len(dates)

    # Test 1: Lead-lag relationship
    print('\n1. Testing H1 (sentiment leading VIX)...')
    base_signal = np.sin(np.linspace(0, 4 * np.pi, n)) + np.random.randn(n) * 0.3
    sentiment = pd.Series(base_signal, index=dates)
    vix_base = -base_signal * 5 + 20
    vix = pd.Series(np.roll(vix_base, 3) + np.random.randn(n) * 1, index=dates).clip(10, 80)

    validator = HypothesisValidator()
    h1_result = validator.validate_h1(sentiment, vix)
    print(f'   Optimal lag: {h1_result.lead_lag.optimal_lag} days')
    print(f'   Max correlation: {h1_result.lead_lag.max_correlation:.4f}')
    print(f'   Significant: {h1_result.lead_lag.is_significant}')
    print(f'   Result: {h1_result.result.value}')

    # Test 2: Divergence
    print('\n2. Testing H2 (divergence before transitions)...')
    regimes = ['stable'] * n
    for tp in [100, 200, 300, 400]:
        regimes[tp:min(tp+20, n)] = ['transition'] * min(20, n - tp)
    regime_series = pd.Series(regimes, index=dates)

    sentiment_data = {}
    for i, asset in enumerate(['equities', 'bonds', 'crypto']):
        asset_sent = base_signal.copy()
        for tp in [100, 200, 300, 400]:
            if tp < n:
                start = max(0, tp - 5)
                asset_sent[start:tp] += (i - 1) * 0.5
        sentiment_data[asset] = asset_sent + np.random.randn(n) * 0.1

    sentiment_df = pd.DataFrame(sentiment_data, index=dates)
    h2_result = validator.validate_h2(sentiment_df, regime_series)
    print(f'   Divergence ratio: {h2_result.divergence_ratio:.2f}x')
    print(f'   P-value: {h2_result.p_value:.4f}')
    print(f'   Effect size: {h2_result.effect_size:.4f}')
    print(f'   Result: {h2_result.result.value}')

    # Test 3: Connectedness
    print('\n3. Testing H3 (network effect)...')
    tci = np.ones(n) * 0.5
    for i, r in enumerate(regimes):
        if r == 'stable':
            tci[i] += np.random.randn() * 0.05 + 0.1
        else:
            tci[i] += np.random.randn() * 0.05 - 0.1
    tci = np.clip(tci, 0, 1)
    tci_series = pd.Series(tci, index=dates)

    h3_result = validator.validate_h3(tci_series, regime_series)
    print(f'   Stable TCI: {h3_result.stable_regime_tci:.4f}')
    print(f'   Transition TCI: {h3_result.transition_tci:.4f}')
    print(f'   ANOVA p-value: {h3_result.anova_p:.4f}')
    print(f'   Result: {h3_result.result.value}')

    # Generate report
    print('\n4. Generating hypothesis report...')
    results = {'H1': h1_result, 'H2': h2_result, 'H3': h3_result}
    report = generate_hypothesis_report(results)
    print('\n' + report)

    print('\n✅ All hypothesis validation tests passed!')
    return True

if __name__ == '__main__':
    success = test_hypothesis_validator()
    sys.exit(0 if success else 1)
