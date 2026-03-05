'use client'

import { RefreshCw } from 'lucide-react'

interface LoadingSkeletonProps {
  variant?: 'card' | 'chart' | 'panel' | 'page' | 'inline'
  className?: string
  showSpinner?: boolean
  message?: string
}

export default function LoadingSkeleton({
  variant = 'card',
  className = '',
  showSpinner = false,
  message,
}: LoadingSkeletonProps) {
  if (variant === 'page') {
    return (
      <div className={`min-h-screen bg-gray-50 dark:bg-gray-950 flex items-center justify-center ${className}`}>
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600 dark:text-gray-400 text-lg font-medium">
            {message || 'Loading dashboard...'}
          </p>
          <p className="text-gray-400 dark:text-gray-400 text-sm mt-2">
            Fetching latest market data
          </p>
        </div>
      </div>
    )
  }

  if (variant === 'inline') {
    return (
      <div className={`flex items-center gap-2 ${className}`}>
        <RefreshCw className="w-4 h-4 text-gray-400 dark:text-gray-400 animate-spin" />
        <span className="text-sm text-gray-500 dark:text-gray-400">
          {message || 'Loading...'}
        </span>
      </div>
    )
  }

  if (variant === 'chart') {
    return (
      <div className={`bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 ${className}`}>
        <div className="animate-pulse">
          {/* Header */}
          <div className="flex items-center justify-between mb-6">
            <div className="flex items-center gap-3">
              <div className="w-6 h-6 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-5 bg-gray-200 dark:bg-gray-700 rounded w-32"></div>
            </div>
            <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
          </div>

          {/* Chart area */}
          <div className="h-72 bg-gradient-to-b from-gray-100 to-gray-50 dark:from-gray-800 dark:to-gray-950 rounded-lg flex items-end justify-around px-4 pb-4">
            {[...Array(8)].map((_, i) => (
              <div
                key={i}
                className="bg-gray-200 dark:bg-gray-700 rounded-t"
                style={{
                  width: '8%',
                  height: `${30 + Math.random() * 60}%`,
                  animation: `pulse ${1.5 + Math.random()}s cubic-bezier(0.4, 0, 0.6, 1) infinite`,
                }}
              />
            ))}
          </div>

          {/* Legend */}
          <div className="flex items-center justify-center gap-6 mt-4">
            <div className="flex items-center gap-2">
              <div className="w-8 h-2 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-8 h-2 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
            </div>
          </div>
        </div>

        {showSpinner && (
          <div className="absolute inset-0 flex items-center justify-center bg-white/50 dark:bg-gray-900/50 backdrop-blur-sm rounded-xl">
            <RefreshCw className="w-8 h-8 text-blue-600 animate-spin" />
          </div>
        )}
      </div>
    )
  }

  if (variant === 'panel') {
    return (
      <div className={`bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 ${className}`}>
        <div className="animate-pulse">
          {/* Header */}
          <div className="flex items-center justify-between mb-4">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-32"></div>
            <div className="flex items-center gap-2">
              <div className="h-2 w-2 bg-gray-200 dark:bg-gray-700 rounded-full"></div>
              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-12"></div>
            </div>
          </div>

          {/* Content box */}
          <div className="p-4 bg-gray-50 dark:bg-gray-950 rounded-lg mb-4">
            <div className="flex items-center gap-3 mb-2">
              <div className="w-6 h-6 bg-gray-200 dark:bg-gray-700 rounded"></div>
              <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-40"></div>
            </div>
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-3 gap-4">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="text-center p-3 bg-gray-50 dark:bg-gray-950 rounded-lg">
                <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-16 mx-auto mb-2"></div>
                <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-12 mx-auto"></div>
              </div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // Default card variant
  return (
    <div className={`bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 ${className}`}>
      <div className="animate-pulse space-y-4">
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3"></div>
        <div className="space-y-3">
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded"></div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-4/6"></div>
        </div>
        <div className="pt-4">
          <div className="h-20 bg-gradient-to-b from-gray-100 to-gray-50 dark:from-gray-800 dark:to-gray-950 rounded"></div>
        </div>
      </div>
    </div>
  )
}

// Specialized skeletons for specific components
export function SentimentCardSkeleton({ className = '' }: { className?: string }) {
  return (
    <div className={`bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 ${className}`}>
      <div className="animate-pulse">
        <div className="flex items-center justify-between mb-4">
          <div className="h-5 bg-gray-200 dark:bg-gray-700 rounded w-24"></div>
          <div className="w-8 h-8 bg-gray-200 dark:bg-gray-700 rounded-full"></div>
        </div>
        <div className="h-12 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-4"></div>
        <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full mb-2"></div>
        <div className="flex justify-between text-xs mb-4">
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
          <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16"></div>
        </div>
        <div className="grid grid-cols-3 gap-2">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="p-2 bg-gray-50 dark:bg-gray-950 rounded text-center">
              <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-8 mx-auto mb-1"></div>
              <div className="h-2 bg-gray-200 dark:bg-gray-700 rounded w-12 mx-auto"></div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export function RegimePanelSkeleton({ className = '' }: { className?: string }) {
  return <LoadingSkeleton variant="panel" className={className} />
}

export function ChartSkeleton({ className = '' }: { className?: string }) {
  return <LoadingSkeleton variant="chart" className={className} />
}
