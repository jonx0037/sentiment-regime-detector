'use client'

import Image from 'next/image'
import type { ChatMessage as ChatMessageType } from '@/types/chatbot'

interface Props {
  message: ChatMessageType
}

/**
 * Light inline-markdown renderer — handles **bold**, bullet lists (- / *),
 * and numbered lists while keeping the output simple React nodes.
 */
function renderMarkdown(text: string) {
  return text.split('\n').map((line, i) => {
    // Bold: **text**
    const parts = line.split(/(\*\*[^*]+\*\*)/g).map((seg, j) => {
      if (seg.startsWith('**') && seg.endsWith('**')) {
        return (
          <strong key={j} className="font-semibold">
            {seg.slice(2, -2)}
          </strong>
        )
      }
      return seg
    })

    // Bullet / numbered list detection
    const isBullet = /^[-•]\s/.test(line)
    const isNumbered = /^\d+[.)]\s/.test(line)

    if (isBullet || isNumbered) {
      return (
        <p key={i} className={`${i > 0 ? 'mt-1' : ''} pl-3`}>
          {parts}
        </p>
      )
    }

    return (
      <p key={i} className={i > 0 ? 'mt-1.5' : ''}>
        {parts}
      </p>
    )
  })
}

export default function ChatMessage({ message }: Props) {
  const isUser = message.role === 'user'

  return (
    <div className={`flex gap-3 ${isUser ? 'flex-row-reverse' : 'flex-row'}`}>
      {/* Avatar */}
      {isUser ? (
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center flex-shrink-0">
          <span className="text-white text-xs font-medium">You</span>
        </div>
      ) : (
        <div className="w-8 h-8 rounded-full overflow-hidden flex-shrink-0 bg-gray-200 dark:bg-gray-700">
          <Image
            src="/jon-avatar.png"
            alt="Jon"
            width={64}
            height={64}
            className="object-cover"
          />
        </div>
      )}

      {/* Bubble */}
      <div
        className={`max-w-[80%] rounded-2xl px-4 py-2.5 text-sm leading-relaxed ${
          isUser
            ? 'bg-blue-600 text-white rounded-br-md'
            : 'bg-gray-100 dark:bg-gray-700 text-gray-800 dark:text-gray-100 rounded-bl-md'
        }`}
      >
        {isUser
          ? message.content.split('\n').map((line, i) => (
              <p key={i} className={i > 0 ? 'mt-1.5' : ''}>{line}</p>
            ))
          : renderMarkdown(message.content)
        }
      </div>
    </div>
  )
}
