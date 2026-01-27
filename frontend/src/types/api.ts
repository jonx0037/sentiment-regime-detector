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

export interface RegimeState {
  regime_type: string
  confidence: number
  features: Record<string, number>
  timestamp: string
}

export interface RegimeResponse {
  current_regime: RegimeState
  previous_regime?: RegimeState
  duration_hours: number
  volatility_level: string
}
