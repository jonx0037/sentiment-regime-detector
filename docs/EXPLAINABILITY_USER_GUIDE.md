# SHAP Explainability System - User Guide

## Overview

The SHAP Explainability System makes regime predictions transparent by showing **why** the ML model makes specific predictions. Using SHAP (SHapley Additive exPlanations) values, users can understand which features drive each prediction and explore historical crisis events.

## Features

### 1. Real-Time Explanations

**Access**: Click the **"Explain"** button on the Regime Panel

**What You See**:

- **Regime Summary**: Current prediction with confidence score
- **Waterfall Plot**: Visual representation of how features contribute to the prediction
- **Top Features Table**: Ranked list of most influential features with SHAP values
- **Educational Banner**: "What is SHAP?" help section (expandable)

**How to Read**:

- **Green values** = Feature pushes *toward* the predicted regime
- **Red values** = Feature pushes *away* from the predicted regime
- **Larger absolute values** = Stronger influence on prediction

### 2. Crisis Events Browser

**Access**: Click the **"History"** button on the Regime Panel

**Available Events**:

1. **2008 Financial Crisis** (Nov 20, 2008)
   - CISS Peak: 0.980 | VIX Peak: 80.86
   - Global financial crisis triggered by subprime mortgage collapse

2. **COVID-19 Market Crash** (Mar 16, 2020)
   - CISS Peak: 0.660 | VIX Peak: 82.69
   - Pandemic-driven crash with unprecedented volatility

3. **GameStop/Meme Stock Episode** (Jan 28, 2021)
   - CISS Peak: 0.180 | VIX Peak: 37.21
   - Retail-driven short squeeze creating localized stress

4. **Luna/Terra Collapse** (May 9, 2022)
   - CISS Peak: 0.480 | VIX Peak: 34.66
   - Algorithmic stablecoin collapse causing crypto contagion

5. **Celsius/3AC Crypto Contagion** (Jun 15, 2022)
   - CISS Peak: 0.520 | VIX Peak: 33.89
   - Crypto lending platform failures and hedge fund liquidations

6. **Out-of-Sample Validation Period** (Oct 1, 2024)
   - Tests model generalization to unseen market conditions

**Features**:

- View SHAP explanations for each historical event
- Compare CISS/VIX peaks across crises
- Understand how the model behaves during different crisis types

### 3. Export Functionality

**Export Current Explanation**:

1. Open the Explainability Modal (click "Explain")
2. Click **"Export JSON"** button in footer
3. Downloads: `shap-explanation-{regime}-{date}.json`

**Export Crisis Event**:

1. Open Crisis Events Browser (click "History")
2. Select any event
3. Click **"Export"** button in footer
4. Downloads: `crisis-{event_id}-explanation.json`

**Export Format** (JSON):

```json
{
  "timestamp": "2026-02-06T12:30:00Z",
  "predicted_regime": "risk_on",
  "confidence": 0.9917,
  "model_version": "RF_v2023.12",
  "base_value": 0.3333,
  "prediction_value": 0.9917,
  "top_features": [
    {
      "feature_name": "ciss_ma5",
      "value": 0.1234,
      "shap_value": 0.0567,
      "rank": 1
    },
    // ... more features
  ],
  "all_features": [ /* complete list */ ]
}
```

## Feature Names Glossary

### CISS Features (Composite Indicator of Systemic Stress)

- **CISS**: Current systemic stress level
- **CISS (1-day lag)**: Previous day's stress
- **CISS (7-day lag)**: Stress from 7 days ago
- **CISS 5-Day Average**: 5-day moving average
- **CISS 20-Day Average**: 20-day moving average
- **CISS 20-Day Volatility**: Standard deviation over 20 days
- **CISS/VIX Ratio**: Ratio of systemic stress to market volatility
- **CISS Daily Change**: Day-over-day change

### VIX Features (Volatility Index)

- **VIX**: CBOE Volatility Index ("fear gauge")
- **VIX (1-day lag)**: Previous day's volatility expectation
- **VIX (7-day lag)**: Volatility from 7 days ago
- **VIX 5-Day Average**: 5-day moving average
- **VIX 20-Day Average**: 20-day moving average
- **VIX 20-Day Volatility**: Volatility of volatility
- **VIX Daily Change**: Day-over-day change

### Sentiment Features

- **Average Sentiment**: Mean across all asset classes
- **Equity Sentiment**: Stock market sentiment
- **Crypto Sentiment**: Cryptocurrency market sentiment
- **Forex Sentiment**: Foreign exchange sentiment
- **Commodity Sentiment**: Commodities sentiment
- **Sentiment Volatility**: Dispersion across asset classes
- **Minimum Sentiment**: Most bearish across classes
- **Maximum Sentiment**: Most bullish across classes

### Technical Features

- **Sentiment (1-day lag)**: Previous day's sentiment
- **Sentiment (7-day lag)**: Sentiment from 7 days ago
- **Sentiment 5-Day Average**: 5-day MA
- **Sentiment 20-Day Average**: 20-day MA
- **Sentiment Daily Change**: Day-over-day change

### Composite Features

- **Cross-Asset Divergence**: Disagreement between asset classes
- **Stress-Sentiment Gap**: Difference between stress and sentiment
- **Risk-On Probability**: Model's estimate for Risk-On regime
- **Risk-Off Probability**: Model's estimate for Risk-Off regime
- **Transition Probability**: Model's estimate for Transition regime

## Understanding SHAP Values

### What is SHAP?

SHAP (SHapley Additive exPlanations) is a game-theoretic approach to explain ML model predictions. It assigns each feature a contribution value that shows how much it pushed the prediction from a baseline toward the final prediction.

### Key Concepts

**Base Value**: The average prediction across all training data (≈0.333 for 3 regimes)

**SHAP Value**: How much a feature's value changes the prediction from the base

- Positive SHAP = increases prediction
- Negative SHAP = decreases prediction

**Waterfall Plot**: Shows cumulative contributions

- Start at base value (bottom)
- Each bar adds/subtracts a feature's contribution
- End at final prediction (top)

### Interpretation Tips

1. **Focus on Magnitude**: Larger absolute SHAP values = more influential features
2. **Consider Direction**: Positive/negative indicates push direction
3. **Look for Patterns**: Similar features often move together (e.g., CISS indicators)
4. **Context Matters**: Feature values should be interpreted with domain knowledge

## Model Information

- **Model Type**: Random Forest Classifier
- **Model Version**: RF_v2023.12 (trained through Dec 2023)
- **Training Period**: 2006-01-01 to 2023-12-31
- **Test Accuracy**: 99.45%
- **Features**: 28 engineered features
- **Output Classes**: Risk-On, Risk-Off, Transition

## Performance

- **Cache Hit (Redis)**: <50ms response time
- **Cache Miss (SHAP computation)**: <500ms
- **Target Cache Hit Rate**: >80%
- **Waterfall Plot Generation**: ~200ms (cached after first generation)

## Troubleshooting

### Waterfall Plot Not Loading

- **Cause**: Backend is generating the plot for the first time
- **Solution**: Wait 2-3 seconds and refresh, or view Top Features table

### "Model Unknown" Display

- **Fixed in v1.0**: Now shows "RF_v2023.12"
- **If persists**: Restart backend server

### History Button Errors

- **Fixed in v1.0**: Null value handling improved
- **If persists**: Check browser console for details

### Export Not Working

- **Cause**: Pop-up blocker or browser security settings
- **Solution**: Allow downloads from the application domain

## Best Practices

### For Researchers

1. Export explanations for reproducibility
2. Compare SHAP values across different time periods
3. Use Crisis Events Browser to validate model behavior during known crises
4. Combine SHAP explanations with domain knowledge

### For Traders

1. Focus on top 3-5 features driving current prediction
2. Watch for divergence between stress and sentiment indicators
3. Use tooltips to understand what each feature measures
4. Compare current conditions to historical crises

### For Developers

1. Check cache hit rates in footer metadata
2. Monitor SHAP computation times
3. Review exported JSON for integration with other tools
4. Use educational banner to onboard new users

## API Reference

### Get Current Explanation

```bash
GET /api/v1/explainability/current
```

**Response**:

```json
{
  "timestamp": "2026-02-06T12:30:00Z",
  "predicted_regime": "risk_on",
  "confidence": 0.9917,
  "waterfall_plot": "data:image/png;base64,...",
  "top_features": [...],
  "all_features": [...],
  "model_version": "RF_v2023.12",
  "cache_hit": true
}
```

### List Crisis Events

```bash
GET /api/v1/explainability/events
```

**Response**:

```json
[
  {
    "event_id": "covid_crash_2020",
    "name": "COVID-19 Market Crash",
    "date": "2020-03-16",
    "description": "...",
    "ciss_peak": 0.66,
    "vix_peak": 82.69
  },
  // ... more events
]
```

### Get Event Explanation

```bash
GET /api/v1/explainability/events/{event_id}
```

**Response**:

```json
{
  "event": { /* event metadata */ },
  "explanation": { /* SHAP explanation */ }
}
```

## Support

For issues or questions:

- GitHub Issues: <https://github.com/jonx0037/sentiment-regime-detector/issues>
- Documentation: See `/docs/` directory
- Model Details: See `/docs/MODEL.md`

---

**Last Updated**: February 6, 2026
**Version**: 1.0.0
**Contributors**: Claude Sonnet 4.5, Jonathan Rocha
