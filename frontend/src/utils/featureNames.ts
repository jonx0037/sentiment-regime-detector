/**
 * Feature name mappings for SHAP explainability
 * Maps technical feature names to user-friendly display names and descriptions
 */

export interface FeatureMetadata {
  displayName: string
  description: string
  category: 'CISS' | 'VIX' | 'Sentiment' | 'Technical' | 'Composite'
}

export const FEATURE_METADATA: Record<string, FeatureMetadata> = {
  // CISS (Composite Indicator of Systemic Stress) Features
  ciss: {
    displayName: 'CISS',
    description: 'Composite Indicator of Systemic Stress - measures stress across financial markets',
    category: 'CISS',
  },
  ciss_lag1: {
    displayName: 'CISS (1-day lag)',
    description: 'Previous day\'s systemic stress level',
    category: 'CISS',
  },
  ciss_lag7: {
    displayName: 'CISS (7-day lag)',
    description: 'Systemic stress level from 7 days ago',
    category: 'CISS',
  },
  ciss_ma5: {
    displayName: 'CISS 5-Day Average',
    description: '5-day moving average of systemic stress',
    category: 'CISS',
  },
  ciss_ma20: {
    displayName: 'CISS 20-Day Average',
    description: '20-day moving average of systemic stress',
    category: 'CISS',
  },
  ciss_std_20d: {
    displayName: 'CISS 20-Day Volatility',
    description: 'Standard deviation of CISS over 20 days - measures stress volatility',
    category: 'CISS',
  },
  ciss_vix_ratio: {
    displayName: 'CISS/VIX Ratio',
    description: 'Ratio of systemic stress to market volatility',
    category: 'CISS',
  },
  ciss_diff: {
    displayName: 'CISS Daily Change',
    description: 'Day-over-day change in systemic stress',
    category: 'CISS',
  },

  // VIX (Volatility Index) Features
  vix: {
    displayName: 'VIX',
    description: 'CBOE Volatility Index - the "fear gauge" measuring expected market volatility',
    category: 'VIX',
  },
  vix_lag1: {
    displayName: 'VIX (1-day lag)',
    description: 'Previous day\'s market volatility expectation',
    category: 'VIX',
  },
  vix_lag7: {
    displayName: 'VIX (7-day lag)',
    description: 'Market volatility expectation from 7 days ago',
    category: 'VIX',
  },
  vix_ma5: {
    displayName: 'VIX 5-Day Average',
    description: '5-day moving average of expected volatility',
    category: 'VIX',
  },
  vix_ma20: {
    displayName: 'VIX 20-Day Average',
    description: '20-day moving average of expected volatility',
    category: 'VIX',
  },
  vix_std_20d: {
    displayName: 'VIX 20-Day Volatility',
    description: 'Standard deviation of VIX over 20 days - volatility of volatility',
    category: 'VIX',
  },
  vix_diff: {
    displayName: 'VIX Daily Change',
    description: 'Day-over-day change in expected volatility',
    category: 'VIX',
  },

  // Sentiment Features
  sentiment_mean: {
    displayName: 'Average Sentiment',
    description: 'Mean sentiment score across all asset classes',
    category: 'Sentiment',
  },
  sentiment_equity: {
    displayName: 'Equity Sentiment',
    description: 'Sentiment score for equity markets',
    category: 'Sentiment',
  },
  sentiment_crypto: {
    displayName: 'Crypto Sentiment',
    description: 'Sentiment score for cryptocurrency markets',
    category: 'Sentiment',
  },
  sentiment_forex: {
    displayName: 'Forex Sentiment',
    description: 'Sentiment score for foreign exchange markets',
    category: 'Sentiment',
  },
  sentiment_commodity: {
    displayName: 'Commodity Sentiment',
    description: 'Sentiment score for commodity markets',
    category: 'Sentiment',
  },
  sentiment_std: {
    displayName: 'Sentiment Volatility',
    description: 'Standard deviation of sentiment across asset classes',
    category: 'Sentiment',
  },
  sentiment_min: {
    displayName: 'Minimum Sentiment',
    description: 'Most bearish sentiment across asset classes',
    category: 'Sentiment',
  },
  sentiment_max: {
    displayName: 'Maximum Sentiment',
    description: 'Most bullish sentiment across asset classes',
    category: 'Sentiment',
  },

  // Technical Features
  sentiment_lag1: {
    displayName: 'Sentiment (1-day lag)',
    description: 'Previous day\'s sentiment score',
    category: 'Technical',
  },
  sentiment_lag7: {
    displayName: 'Sentiment (7-day lag)',
    description: 'Sentiment score from 7 days ago',
    category: 'Technical',
  },
  sentiment_ma5: {
    displayName: 'Sentiment 5-Day Average',
    description: '5-day moving average of sentiment',
    category: 'Technical',
  },
  sentiment_ma20: {
    displayName: 'Sentiment 20-Day Average',
    description: '20-day moving average of sentiment',
    category: 'Technical',
  },
  sentiment_diff: {
    displayName: 'Sentiment Daily Change',
    description: 'Day-over-day change in sentiment',
    category: 'Technical',
  },

  // Composite Features
  cross_asset_divergence: {
    displayName: 'Cross-Asset Divergence',
    description: 'Measure of disagreement between different asset class sentiments',
    category: 'Composite',
  },
  stress_sentiment_diff: {
    displayName: 'Stress-Sentiment Gap',
    description: 'Difference between market stress and sentiment indicators',
    category: 'Composite',
  },
  regime_probability_risk_on: {
    displayName: 'Risk-On Probability',
    description: 'Model\'s probability estimate for Risk-On regime',
    category: 'Composite',
  },
  regime_probability_risk_off: {
    displayName: 'Risk-Off Probability',
    description: 'Model\'s probability estimate for Risk-Off regime',
    category: 'Composite',
  },
  regime_probability_transition: {
    displayName: 'Transition Probability',
    description: 'Model\'s probability estimate for Transition regime',
    category: 'Composite',
  },
}

/**
 * Get display name for a feature
 * Returns the user-friendly name or falls back to the technical name
 */
export function getFeatureDisplayName(technicalName: string): string {
  return FEATURE_METADATA[technicalName]?.displayName || formatTechnicalName(technicalName)
}

/**
 * Get description for a feature
 * Returns the description or a generic message
 */
export function getFeatureDescription(technicalName: string): string {
  return FEATURE_METADATA[technicalName]?.description || `Technical feature: ${technicalName}`
}

/**
 * Get category for a feature
 */
export function getFeatureCategory(technicalName: string): string {
  return FEATURE_METADATA[technicalName]?.category || 'Technical'
}

/**
 * Format technical name to a more readable form (fallback)
 * Example: "ciss_ma20" -> "Ciss Ma20"
 */
function formatTechnicalName(name: string): string {
  return name
    .split('_')
    .map(word => word.charAt(0).toUpperCase() + word.slice(1))
    .join(' ')
}

/**
 * Get full feature metadata
 */
export function getFeatureMetadata(technicalName: string): FeatureMetadata {
  return FEATURE_METADATA[technicalName] || {
    displayName: formatTechnicalName(technicalName),
    description: `Technical feature: ${technicalName}`,
    category: 'Technical',
  }
}
