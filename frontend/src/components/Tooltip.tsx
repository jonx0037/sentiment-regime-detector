'use client'

import { ReactNode, useState } from 'react'
import { HelpCircle } from 'lucide-react'

interface TooltipProps {
  content: string | ReactNode
  children?: ReactNode
  side?: 'top' | 'bottom' | 'left' | 'right'
  showIcon?: boolean
  className?: string
}

export default function Tooltip({
  content,
  children,
  side = 'top',
  showIcon = true,
  className = ''
}: TooltipProps) {
  const [isVisible, setIsVisible] = useState(false)

  const sideClasses = {
    top: 'bottom-full left-1/2 -translate-x-1/2 mb-2',
    bottom: 'top-full left-1/2 -translate-x-1/2 mt-2',
    left: 'right-full top-1/2 -translate-y-1/2 mr-2',
    right: 'left-full top-1/2 -translate-y-1/2 ml-2',
  }

  const arrowClasses = {
    top: 'top-full left-1/2 -translate-x-1/2 border-l-transparent border-r-transparent border-b-transparent border-t-gray-900',
    bottom: 'bottom-full left-1/2 -translate-x-1/2 border-l-transparent border-r-transparent border-t-transparent border-b-gray-900',
    left: 'left-full top-1/2 -translate-y-1/2 border-t-transparent border-b-transparent border-r-transparent border-l-gray-900',
    right: 'right-full top-1/2 -translate-y-1/2 border-t-transparent border-b-transparent border-l-transparent border-r-gray-900',
  }

  return (
    <span className={`relative inline-flex items-center ${className}`}>
      <span
        className="inline-flex items-center cursor-help touch-manipulation"
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onTouchStart={() => setIsVisible(true)}
        onTouchEnd={() => setTimeout(() => setIsVisible(false), 2000)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}
        tabIndex={0}
        role="button"
        aria-label="More information"
      >
        {children || (
          showIcon && <HelpCircle className="w-3.5 h-3.5 text-gray-400 hover:text-gray-600 transition-colors" />
        )}
      </span>

      {/* Tooltip */}
      {isVisible && (
        <span
          role="tooltip"
          className={`
            absolute z-50 px-3 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg shadow-lg
            whitespace-normal max-w-xs
            animate-in fade-in-0 zoom-in-95 duration-200
            ${sideClasses[side]}
          `}
        >
          {content}
          {/* Arrow */}
          <span
            className={`
              absolute w-0 h-0 border-4
              ${arrowClasses[side]}
            `}
          />
        </span>
      )}
    </span>
  )
}

/**
 * Inline tooltip for wrapping text with underline decoration
 */
interface InlineTooltipProps {
  term: string
  definition: string | ReactNode
  className?: string
}

export function InlineTooltip({ term, definition, className = '' }: InlineTooltipProps) {
  const [isVisible, setIsVisible] = useState(false)

  return (
    <span className={`relative inline-block ${className}`}>
      <span
        className="border-b border-dotted border-gray-400 cursor-help hover:border-gray-600 transition-colors touch-manipulation"
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
        onTouchStart={() => setIsVisible(true)}
        onTouchEnd={() => setTimeout(() => setIsVisible(false), 2000)}
        onFocus={() => setIsVisible(true)}
        onBlur={() => setIsVisible(false)}
        tabIndex={0}
        role="button"
        aria-label={`Definition of ${term}`}
      >
        {term}
      </span>

      {isVisible && (
        <span
          role="tooltip"
          className="
            absolute z-50 px-3 py-2 text-xs font-medium text-white bg-gray-900 rounded-lg shadow-lg
            whitespace-normal max-w-xs
            bottom-full left-1/2 -translate-x-1/2 mb-2
            animate-in fade-in-0 zoom-in-95 duration-200
          "
        >
          {definition}
          <span className="absolute top-full left-1/2 -translate-x-1/2 w-0 h-0 border-4 border-l-transparent border-r-transparent border-b-transparent border-t-gray-900" />
        </span>
      )}
    </span>
  )
}
