import type {
  SentimentResponse,
  SentimentHistoryResponse,
  RegimeResponse,
  AssetClass,
  GARCHParametersResponse,
  GARCHForecastResponse,
} from '@/types/api'
import type {
  ExplanationResponse,
  CrisisEvent,
  EventDetailResponse,
} from '@/types/explainability'

// In production (no env var set), use relative URLs to leverage Vercel proxy
// In development, use localhost or custom NEXT_PUBLIC_API_URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ||
  (typeof window !== 'undefined' && window.location.hostname !== 'localhost'
    ? '/api/v1'
    : 'http://localhost:8000/api/v1')

class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public data?: any
  ) {
    super(message)
    this.name = 'ApiError'
  }
}

async function fetchApi<T>(endpoint: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options?.headers,
      },
    })

    if (!response.ok) {
      const errorData = await response.json().catch(() => null)
      throw new ApiError(
        errorData?.detail || `API request failed: ${response.statusText}`,
        response.status,
        errorData
      )
    }

    return response.json()
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError('Network error or server unreachable')
  }
}

export const sentimentApi = {
  /**
   * Get current sentiment for all asset classes
   */
  async getCurrentSentiment(): Promise<SentimentResponse> {
    return fetchApi<SentimentResponse>('/sentiment/current')
  },

  /**
   * Get historical sentiment data for a specific asset class
   */
  async getSentimentHistory(
    assetClass: AssetClass,
    startDate: string,
    endDate?: string,
    granularity: 'hourly' | 'daily' = 'daily'
  ): Promise<SentimentHistoryResponse> {
    const params = new URLSearchParams({
      asset_class: assetClass,
      start_date: startDate,
      granularity,
    })
    
    if (endDate) {
      params.append('end_date', endDate)
    }

    return fetchApi<SentimentHistoryResponse>(`/sentiment/history?${params}`)
  },

  /**
   * Get sentiment breakdown by source
   */
  async getSentimentBySource(assetClass: AssetClass): Promise<any> {
    return fetchApi(`/sentiment/by-source?asset_class=${assetClass}`)
  },
}

export const regimeApi = {
  /**
   * Get current market regime
   */
  async getCurrentRegime(): Promise<RegimeResponse> {
    return fetchApi<RegimeResponse>('/regime/current')
  },

  /**
   * Get regime transitions history
   */
  async getRegimeTransitions(
    startDate: string,
    endDate?: string
  ): Promise<any> {
    const params = new URLSearchParams({ start_date: startDate })
    if (endDate) {
      params.append('end_date', endDate)
    }
    return fetchApi(`/regime/transitions?${params}`)
  },
}

export const garchApi = {
  /**
   * Get GARCH model parameters and diagnostics
   */
  async getParameters(): Promise<GARCHParametersResponse> {
    return fetchApi<GARCHParametersResponse>('/garch/parameters')
  },

  /**
   * Get volatility forecast for the next N days
   */
  async getVolatilityForecast(horizon: number = 30): Promise<GARCHForecastResponse> {
    return fetchApi<GARCHForecastResponse>(`/garch/volatility/forecast?horizon=${horizon}`)
  },
}

export const healthApi = {
  /**
   * Check API health status
   */
  async checkHealth(): Promise<any> {
    return fetchApi('/health')
  },
}

export const explainabilityApi = {
  /**
   * Get SHAP explanation for current regime prediction
   */
  async getCurrentExplanation(): Promise<ExplanationResponse> {
    return fetchApi<ExplanationResponse>('/explainability/current')
  },

  /**
   * Get list of historical crisis events
   */
  async getEventsList(): Promise<CrisisEvent[]> {
    return fetchApi<CrisisEvent[]>('/explainability/events')
  },

  /**
   * Get SHAP explanation for specific historical event
   */
  async getEventExplanation(eventId: string): Promise<EventDetailResponse> {
    return fetchApi<EventDetailResponse>(`/explainability/events/${eventId}`)
  },
}
