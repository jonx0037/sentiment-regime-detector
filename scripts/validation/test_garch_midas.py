#!/usr/bin/env python3
"""Test GARCH-MIDAS implementation."""

import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from sentiment_detector.models.garch_midas import GARCHMIDASModel, MIDASWeights

# Create test data
np.random.seed(42)
dates = pd.date_range('2020-01-01', periods=252, freq='B')
returns = pd.Series(np.random.randn(252) * 0.02, index=dates)
sentiment = pd.Series(np.random.randn(252) * 0.3, index=dates)

# Test MIDAS weights
weights = MIDASWeights(omega1=1.0, omega2=2.0, K=22)
print('MIDAS Weights (first 5):', weights.weights[:5].round(3))
print('Sum of weights:', weights.weights.sum().round(3))

# Test model
model = GARCHMIDASModel(midas_lags=22)
result = model.fit(returns, sentiment)

print('\n--- GARCH-MIDAS Results ---')
print('Params:', {k: round(v, 4) for k, v in result.params.items()})
print('Sentiment Coefficient:', round(result.sentiment_coefficient or 0, 4))
print('AIC:', round(result.aic, 2) if not np.isnan(result.aic) else 'N/A')
print('Convergence:', result.convergence)
print('Volatility Mean:', round(result.conditional_volatility.mean(), 4))
print('Volatility Std:', round(result.conditional_volatility.std(), 4))

# Test regime classification
regimes = model.get_volatility_regimes()
print('\nRegime Distribution:')
print(regimes.value_counts())

# Test forecast
fcast = model.forecast(steps=5)
print('\n5-day Volatility Forecast:')
print(fcast.round(4))

print('\n✅ GARCH-MIDAS test passed!')
