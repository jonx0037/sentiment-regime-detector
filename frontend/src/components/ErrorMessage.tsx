'use client'

import { AlertCircle, WifiOff, Server, Clock, RefreshCw } from 'lucide-react'

interface ErrorMessageProps {
  error: string | Error
  onRetry?: () => void
  className?: string
  variant?: 'inline' | 'card' | 'full'
}

interface ErrorContext {
  icon: React.ReactNode
  title: string
  message: string
  suggestions: string[]
  color: 'red' | 'amber' | 'blue'
}

function analyzeError(error: string | Error): ErrorContext {
  const errorMessage = error instanceof Error ? error.message : error

  // Network errors
  if (errorMessage.includes('Failed to fetch') || errorMessage.includes('NetworkError')) {
    return {
      icon: <WifiOff className="w-6 h-6" />,
      title: 'Connection Issue',
      message: 'Unable to reach the server. Please check your internet connection.',
      suggestions: [
        'Check your internet connection',
        'Verify the API server is running',
        'Try refreshing the page',
      ],
      color: 'amber',
    }
  }

  // Timeout errors
  if (errorMessage.includes('timeout') || errorMessage.includes('ETIMEDOUT')) {
    return {
      icon: <Clock className="w-6 h-6" />,
      title: 'Request Timeout',
      message: 'The server took too long to respond.',
      suggestions: [
        'The server might be busy - try again in a moment',
        'Check your internet connection speed',
        'Contact support if this persists',
      ],
      color: 'amber',
    }
  }

  // Server errors (5xx)
  if (errorMessage.includes('500') || errorMessage.includes('502') || errorMessage.includes('503')) {
    return {
      icon: <Server className="w-6 h-6" />,
      title: 'Server Error',
      message: 'The server encountered an error while processing your request.',
      suggestions: [
        'This is a temporary issue - try again in a moment',
        'If the problem persists, contact support',
        'Check the status page for known issues',
      ],
      color: 'red',
    }
  }

  // 404 errors
  if (errorMessage.includes('404') || errorMessage.includes('Not Found')) {
    return {
      icon: <AlertCircle className="w-6 h-6" />,
      title: 'Data Not Found',
      message: 'The requested data could not be found.',
      suggestions: [
        'The data may have been removed',
        'Check if you have the correct permissions',
        'Try refreshing the page',
      ],
      color: 'amber',
    }
  }

  // 401/403 errors
  if (errorMessage.includes('401') || errorMessage.includes('403') || errorMessage.includes('Unauthorized')) {
    return {
      icon: <AlertCircle className="w-6 h-6" />,
      title: 'Access Denied',
      message: 'You do not have permission to access this resource.',
      suggestions: [
        'Check if you are logged in',
        'Verify you have the correct permissions',
        'Contact an administrator if you should have access',
      ],
      color: 'red',
    }
  }

  // Generic error
  return {
    icon: <AlertCircle className="w-6 h-6" />,
    title: 'Error',
    message: errorMessage,
    suggestions: [
      'Try refreshing the page',
      'If this persists, contact support',
    ],
    color: 'red',
  }
}

export default function ErrorMessage({
  error,
  onRetry,
  className = '',
  variant = 'card'
}: ErrorMessageProps) {
  const context = analyzeError(error)

  const colorClasses = {
    red: {
      bg: 'bg-red-50',
      border: 'border-red-200',
      iconBg: 'bg-red-100',
      iconColor: 'text-red-600',
      titleColor: 'text-red-900',
      textColor: 'text-red-800',
    },
    amber: {
      bg: 'bg-amber-50',
      border: 'border-amber-200',
      iconBg: 'bg-amber-100',
      iconColor: 'text-amber-600',
      titleColor: 'text-amber-900',
      textColor: 'text-amber-800',
    },
    blue: {
      bg: 'bg-blue-50',
      border: 'border-blue-200',
      iconBg: 'bg-blue-100',
      iconColor: 'text-blue-600',
      titleColor: 'text-blue-900',
      textColor: 'text-blue-800',
    },
  }

  const colors = colorClasses[context.color]

  if (variant === 'inline') {
    return (
      <div className={`flex items-start gap-3 p-4 ${colors.bg} ${colors.border} border rounded-lg ${className}`}>
        <div className={`${colors.iconColor} flex-shrink-0`}>
          {context.icon}
        </div>
        <div className="flex-1 min-w-0">
          <p className={`font-medium ${colors.titleColor}`}>
            {context.title}
          </p>
          <p className={`text-sm ${colors.textColor} mt-1`}>
            {context.message}
          </p>
          {onRetry && (
            <button
              onClick={onRetry}
              className={`mt-2 text-sm font-medium ${colors.textColor} hover:underline flex items-center gap-1`}
            >
              <RefreshCw className="w-3 h-3" />
              Try again
            </button>
          )}
        </div>
      </div>
    )
  }

  if (variant === 'full') {
    return (
      <div className={`min-h-[400px] flex items-center justify-center p-6 ${className}`}>
        <div className={`max-w-md w-full ${colors.bg} rounded-xl shadow-lg border ${colors.border} p-8`}>
          <div className="flex flex-col items-center text-center">
            <div className={`w-16 h-16 ${colors.iconBg} rounded-full flex items-center justify-center mb-4`}>
              <div className={colors.iconColor}>
                {context.icon}
              </div>
            </div>

            <h2 className={`text-2xl font-bold ${colors.titleColor} mb-2`}>
              {context.title}
            </h2>

            <p className={`${colors.textColor} mb-6`}>
              {context.message}
            </p>

            <div className={`w-full text-left ${colors.bg} rounded-lg p-4 mb-6`}>
              <p className={`text-sm font-medium ${colors.titleColor} mb-2`}>
                What you can do:
              </p>
              <ul className={`text-sm ${colors.textColor} space-y-1`}>
                {context.suggestions.map((suggestion, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-xs mt-0.5">•</span>
                    <span>{suggestion}</span>
                  </li>
                ))}
              </ul>
            </div>

            {onRetry && (
              <button
                onClick={onRetry}
                className="flex items-center gap-2 px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
              >
                <RefreshCw className="w-4 h-4" />
                Try Again
              </button>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Card variant (default)
  return (
    <div className={`bg-white rounded-xl shadow-sm border ${colors.border} p-6 ${className}`}>
      <div className="flex items-start gap-4">
        <div className={`${colors.iconBg} p-3 rounded-lg flex-shrink-0`}>
          <div className={colors.iconColor}>
            {context.icon}
          </div>
        </div>

        <div className="flex-1 min-w-0">
          <h3 className={`font-semibold ${colors.titleColor} mb-1`}>
            {context.title}
          </h3>
          <p className={`text-sm ${colors.textColor} mb-3`}>
            {context.message}
          </p>

          <details className="mb-3">
            <summary className={`text-sm font-medium ${colors.titleColor} cursor-pointer hover:underline`}>
              What can I do?
            </summary>
            <ul className={`mt-2 text-sm ${colors.textColor} space-y-1 ml-4`}>
              {context.suggestions.map((suggestion, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-xs mt-0.5">•</span>
                  <span>{suggestion}</span>
                </li>
              ))}
            </ul>
          </details>

          {onRetry && (
            <button
              onClick={onRetry}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm font-medium"
            >
              <RefreshCw className="w-4 h-4" />
              Try Again
            </button>
          )}
        </div>
      </div>
    </div>
  )
}
