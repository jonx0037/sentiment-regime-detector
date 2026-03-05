'use client'

import { useCallback, useRef, useState } from 'react'
import { chatbotApi } from '@/services/api'
import type { ChatMessage, ChatSource } from '@/types/chatbot'

const MAX_HISTORY_TURNS = 6

export function useChatbot() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [sources, setSources] = useState<ChatSource[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const abortRef = useRef<AbortController | null>(null)

  const sendMessage = useCallback(async (query: string) => {
    const userMsg: ChatMessage = { role: 'user', content: query }
    setMessages((prev) => [...prev, userMsg])
    setLoading(true)
    setError(null)
    setSources([])

    try {
      abortRef.current = new AbortController()
      const history = [...messages, userMsg].slice(-(MAX_HISTORY_TURNS * 2))

      const result = await chatbotApi.query({
        query,
        conversation_history: history,
        max_history_turns: MAX_HISTORY_TURNS,
      })

      const assistantMsg: ChatMessage = { role: 'assistant', content: result.response }
      setMessages((prev) => [...prev, assistantMsg])
      setSources(result.sources_used)
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Something went wrong'
      setError(msg)
    } finally {
      setLoading(false)
      abortRef.current = null
    }
  }, [messages])

  const clearChat = useCallback(() => {
    setMessages([])
    setSources([])
    setError(null)
  }, [])

  return { messages, sources, loading, error, sendMessage, clearChat }
}
