// Type definitions matching the FastAPI backend schemas

export type AssetClass = 'equity' | 'crypto' | 'forex' | 'commodity'

export interface AssetClassSentiment {
  asset_class: AssetClass
  compound_score: number
  positive_ratio: number
  negative_ratio: number
  neutral_ratio: number
  sample_count: number
  momentum: number
}

export interface SentimentResponse {
  timestamp: string
  asset_classes: AssetClassSentiment[]
  cross_asset_mean: number
  cross_asset_std: number
  latest_data_date: string | null
}

export interface SentimentDataPoint {
  timestamp: string
  compound_score: number
  sample_count: number
  momentum?: number | null
}

export interface SentimentHistoryResponse {
  asset_class: AssetClass
  start_date: string
  end_date: string
  granularity: 'hourly' | 'daily'
  data_points: SentimentDataPoint[]
  total_count: number
}

export type RegimeState = 'risk_on' | 'risk_off' | 'transition'

export interface RegimeFeatures {
  equity_sentiment?: number
  crypto_sentiment?: number
  forex_sentiment?: number
  commodity_sentiment?: number
  cross_asset_mean?: number
  sentiment_momentum_7d?: number
  max_divergence?: number
  ciss_level?: number | null
  vix_level?: number | null
}

export interface RegimeResponse {
  timestamp: string
  regime: RegimeState
  confidence: number
  probabilities: Record<RegimeState, number>
  features: RegimeFeatures
  model_version: string
}
