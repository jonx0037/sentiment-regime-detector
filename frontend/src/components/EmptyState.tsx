'use client'

import {
  Inbox,
  TrendingUp,
  AlertCircle,
  Database,
  LineChart,
  RefreshCw,
  Clock,
  Search
} from 'lucide-react'

interface EmptyStateProps {
  variant?: 'no-data' | 'no-results' | 'no-sentiment' | 'no-history' | 'no-regime' | 'coming-soon'
  title?: string
  message?: string
  action?: {
    label: string
    onClick: () => void
  }
  className?: string
}

const variants = {
  'no-data': {
    icon: <Database className="w-12 h-12" />,
    defaultTitle: 'No Data Available',
    defaultMessage: 'There is no data to display at the moment. This could be temporary.',
    color: 'text-gray-400',
    bgColor: 'bg-gray-50',
  },
  'no-results': {
    icon: <Search className="w-12 h-12" />,
    defaultTitle: 'No Results Found',
    defaultMessage: 'We couldn\'t find any data matching your criteria. Try adjusting your filters.',
    color: 'text-gray-400',
    bgColor: 'bg-gray-50',
  },
  'no-sentiment': {
    icon: <TrendingUp className="w-12 h-12" />,
    defaultTitle: 'No Sentiment Data',
    defaultMessage: 'Sentiment data is currently unavailable. Check back soon or refresh to try again.',
    color: 'text-blue-400',
    bgColor: 'bg-blue-50',
  },
  'no-history': {
    icon: <LineChart className="w-12 h-12" />,
    defaultTitle: 'No Historical Data',
    defaultMessage: 'Historical data is not yet available for this time period.',
    color: 'text-amber-400',
    bgColor: 'bg-amber-50',
  },
  'no-regime': {
    icon: <AlertCircle className="w-12 h-12" />,
    defaultTitle: 'No Regime Data',
    defaultMessage: 'Market regime information is currently being calculated.',
    color: 'text-purple-400',
    bgColor: 'bg-purple-50',
  },
  'coming-soon': {
    icon: <Clock className="w-12 h-12" />,
    defaultTitle: 'Coming Soon',
    defaultMessage: 'This feature is currently under development and will be available soon.',
    color: 'text-indigo-400',
    bgColor: 'bg-indigo-50',
  },
}

export default function EmptyState({
  variant = 'no-data',
  title,
  message,
  action,
  className = '',
}: EmptyStateProps) {
  const config = variants[variant]

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 p-8 ${className}`}>
      <div className="flex flex-col items-center justify-center text-center max-w-md mx-auto py-8">
        {/* Icon */}
        <div className={`${config.bgColor} ${config.color} p-4 rounded-full mb-4`}>
          {config.icon}
        </div>

        {/* Title */}
        <h3 className="text-lg font-semibold text-gray-900 mb-2">
          {title || config.defaultTitle}
        </h3>

        {/* Message */}
        <p className="text-sm text-gray-600 mb-6">
          {message || config.defaultMessage}
        </p>

        {/* Action Button */}
        {action && (
          <button
            onClick={action.onClick}
            className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
          >
            <RefreshCw className="w-4 h-4" />
            {action.label}
          </button>
        )}

        {/* Suggestions (optional) */}
        {!action && (
          <div className="mt-4 text-xs text-gray-500">
            <p>Try refreshing the page or check back later</p>
          </div>
        )}
      </div>
    </div>
  )
}

// Specialized empty states for specific use cases
export function NoSentimentData({ onRefresh, className = '' }: { onRefresh?: () => void; className?: string }) {
  return (
    <EmptyState
      variant="no-sentiment"
      title="No Sentiment Data Available"
      message="We're currently unable to retrieve sentiment data. This could be due to a temporary issue with data collection or processing."
      action={onRefresh ? {
        label: 'Refresh Data',
        onClick: onRefresh,
      } : undefined}
      className={className}
    />
  )
}

export function NoHistoricalData({ period, onRefresh, className = '' }: { period?: string; onRefresh?: () => void; className?: string }) {
  return (
    <EmptyState
      variant="no-history"
      title="No Historical Data"
      message={period
        ? `No historical data is available for ${period}. Try selecting a different time period.`
        : 'Historical data is not yet available for this selection.'
      }
      action={onRefresh ? {
        label: 'Try Again',
        onClick: onRefresh,
      } : undefined}
      className={className}
    />
  )
}

export function NoRegimeData({ onRefresh, className = '' }: { onRefresh?: () => void; className?: string }) {
  return (
    <EmptyState
      variant="no-regime"
      title="Regime Calculation In Progress"
      message="Market regime classification is currently being calculated. This typically takes a few moments."
      action={onRefresh ? {
        label: 'Check Again',
        onClick: onRefresh,
      } : undefined}
      className={className}
    />
  )
}

export function NoSearchResults({ query, onClear, className = '' }: { query?: string; onClear?: () => void; className?: string }) {
  return (
    <EmptyState
      variant="no-results"
      title="No Results Found"
      message={query
        ? `No results found for "${query}". Try a different search term or clear your filters.`
        : 'No results match your current filters.'
      }
      action={onClear ? {
        label: 'Clear Filters',
        onClick: onClear,
      } : undefined}
      className={className}
    />
  )
}
