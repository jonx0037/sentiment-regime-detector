'use client'

import { useEffect, useRef, useState } from 'react'
import Image from 'next/image'
import { MessageCircle, X, Trash2 } from 'lucide-react'
import { useChatbot } from './useChatbot'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'

export default function ChatbotWidget() {
  const [isOpen, setIsOpen] = useState(false)
  const { messages, sources, loading, error, sendMessage, clearChat } = useChatbot()
  const scrollRef = useRef<HTMLDivElement>(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight
    }
  }, [messages, loading])

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          type="button"
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-blue-600 text-white shadow-lg hover:bg-blue-700 hover:scale-105 transition-all flex items-center justify-center"
          aria-label="Open chatbot"
        >
          <MessageCircle className="w-6 h-6" />
        </button>
      )}

      {/* Chat Panel */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-[380px] h-[520px] bg-gray-900 rounded-2xl shadow-2xl flex flex-col overflow-hidden border border-gray-700">
          {/* Header */}
          <div className="flex items-center justify-between px-4 py-3 bg-gray-800 border-b border-gray-700">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-full overflow-hidden bg-gray-700">
                <Image
                  src="/jon-avatar.png"
                  alt="Jon"
                  width={36}
                  height={36}
                  className="object-cover"
                />
              </div>
              <div>
                <p className="text-sm font-semibold text-gray-100">Jon</p>
                <p className="text-xs text-gray-400">Research Assistant</p>
              </div>
            </div>
            <div className="flex items-center gap-1">
              <button
                type="button"
                onClick={clearChat}
                className="p-1.5 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-gray-700 transition-colors"
                aria-label="Clear chat"
                title="Clear chat"
              >
                <Trash2 className="w-4 h-4" />
              </button>
              <button
                type="button"
                onClick={() => setIsOpen(false)}
                className="p-1.5 rounded-lg text-gray-400 hover:text-gray-200 hover:bg-gray-700 transition-colors"
                aria-label="Close chatbot"
              >
                <X className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Messages Area */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto px-4 py-4 space-y-4">
            {messages.length === 0 && !loading && (
              <div className="text-center text-gray-400 text-sm mt-8">
                <p className="mb-2">Hi! I&apos;m Jon, your research assistant.</p>
                <p className="text-xs text-gray-500">
                  Ask me about the dashboard, methodology, or current market conditions.
                </p>
              </div>
            )}

            {messages.map((msg, i) => (
              <ChatMessage key={i} message={msg} />
            ))}

            {/* Loading indicator */}
            {loading && (
              <div className="flex gap-3">
                <div className="w-8 h-8 rounded-full overflow-hidden flex-shrink-0 bg-gray-700">
                  <Image
                    src="/jon-avatar.png"
                    alt="Jon"
                    width={32}
                    height={32}
                    className="object-cover"
                  />
                </div>
                <div className="bg-gray-700 rounded-2xl rounded-bl-md px-4 py-3">
                  <div className="flex gap-1.5">
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:0ms]" />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:150ms]" />
                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce [animation-delay:300ms]" />
                  </div>
                </div>
              </div>
            )}

            {/* Error */}
            {error && (
              <div className="text-center text-red-400 text-xs bg-red-900/20 rounded-lg py-2 px-3">
                {error}
              </div>
            )}

            {/* Sources */}
            {sources.length > 0 && !loading && (
              <div className="border-t border-gray-700 pt-3 mt-2">
                <p className="text-xs text-gray-500 mb-1.5">Sources:</p>
                {sources.map((s, i) => (
                  <p key={i} className="text-xs text-gray-400 truncate" title={s.snippet}>
                    {i + 1}. {s.source}
                  </p>
                ))}
              </div>
            )}
          </div>

          {/* Input */}
          <ChatInput onSend={sendMessage} disabled={loading} />
        </div>
      )}
    </>
  )
}
