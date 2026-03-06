// Chatbot types matching the FastAPI backend schemas

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatSource {
  source: string
  snippet: string
}

export interface ChatQueryRequest {
  query: string
  conversation_history: ChatMessage[]
  max_history_turns?: number
}

export interface ChatQueryResponse {
  response: string
  sources_used: ChatSource[]
  regime_context_used: boolean
}

export interface ChatContextResponse {
  current_regime: string | null
  regime_confidence: number | null
  probabilities: Record<string, number>
  sentiment_scores: Record<string, number>
  stress_level: number | null
  vix_level: number | null
  volatility_regime: string | null
  volatility_score: number | null
  recent_transitions: Array<{
    from: string
    to: string
    date: string
    ciss: number | null
    vix: number | null
  }>
  summary: string
}
