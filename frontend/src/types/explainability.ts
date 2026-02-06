export interface ExplanationResponse {
  predicted_regime: 'risk_on' | 'risk_off' | 'transition'
  confidence: number
  timestamp: string
  model_version: string
  waterfall_plot?: string  // base64 PNG data URI (optional until implemented)
  top_features: TopFeature[]
  all_features: TopFeature[]
  base_value: number
  prediction_value: number
  cache_hit: boolean
}

export interface TopFeature {
  feature_name: string      // Technical name (e.g., "ciss_lag1")
  value: number             // Current feature value
  shap_value: number        // SHAP contribution
  rank: number              // Feature importance rank
}

export interface CrisisEvent {
  event_id: string
  name: string
  date: string
  description: string
  ciss_peak: number
  vix_peak: number
}

export interface EventsListResponse {
  events: CrisisEvent[]
}

export interface EventDetailResponse {
  event: CrisisEvent
  explanation: ExplanationResponse
}
