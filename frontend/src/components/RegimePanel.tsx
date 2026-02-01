'use client'

import { useEffect, useState } from 'react'
import { regimeApi } from '@/services/api'
import type { RegimeResponse } from '@/types/api'
import { Activity, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'

interface RegimePanelProps {
  className?: string
}

const regimeConfig: Record<string, {
  label: string
  color: string
  bgColor: string
  borderColor: string
  icon: React.ReactNode
  description: string
}> = {
  low_volatility: {
    label: 'Low Volatility',
    color: 'text-green-700',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    icon: <TrendingUp className="w-6 h-6 text-green-600" />,
    description: 'Stable market conditions with low VIX',
  },
  normal: {
    label: 'Normal',
    color: 'text-blue-700',
    bgColor: 'bg-blue-50',
    borderColor: 'border-blue-200',
    icon: <Activity className="w-6 h-6 text-blue-600" />,
    description: 'Typical market volatility levels',
  },
  elevated: {
    label: 'Elevated',
    color: 'text-amber-700',
    bgColor: 'bg-amber-50',
    borderColor: 'border-amber-200',
    icon: <AlertTriangle className="w-6 h-6 text-amber-600" />,
    description: 'Increased volatility - monitor closely',
  },
  high_volatility: {
    label: 'High Volatility',
    color: 'text-red-700',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    icon: <TrendingDown className="w-6 h-6 text-red-600" />,
    description: 'Crisis-level volatility detected',
  },
  risk_on: {
    label: 'Risk On',
    color: 'text-green-700',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
    icon: <TrendingUp className="w-6 h-6 text-green-600" />,
    description: 'Positive sentiment - risk appetite increasing',
  },
  risk_off: {
    label: 'Risk Off',
    color: 'text-red-700',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
    icon: <TrendingDown className="w-6 h-6 text-red-600" />,
    description: 'Negative sentiment - flight to safety',
  },
  transition: {
    label: 'Transition',
    color: 'text-purple-700',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-200',
    icon: <Activity className="w-6 h-6 text-purple-600" />,
    description: 'Regime change in progress',
  },
}

export default function RegimePanel({ className = '' }: RegimePanelProps) {
  const [regime, setRegime] = useState<RegimeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchRegime = async () => {
      try {
        setLoading(true)
        const response = await regimeApi.getCurrentRegime()
        setRegime(response)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch regime')
        console.error('Error fetching regime:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchRegime()

    // Auto-refresh every 30 seconds
    const interval = setInterval(fetchRegime, 30000)
    return () => clearInterval(interval)
  }, [])

  if (loading && !regime) {
    return (
      <div className={`p-6 bg-white rounded-xl shadow-sm border border-gray-200 ${className}`}>
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-2/3 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className={`p-6 bg-white rounded-xl shadow-sm border border-red-200 ${className}`}>
        <div className="text-red-600">
          <p className="font-medium">Failed to load regime</p>
          <p className="text-sm">{error}</p>
        </div>
      </div>
    )
  }

  // Use the flat structure from the API
  const currentRegime = regime?.regime || 'normal'
  const confidence = regime?.confidence || 0
  const config = regimeConfig[currentRegime] || regimeConfig.normal

  return (
    <div className={`p-6 bg-white rounded-xl shadow-sm border ${config.borderColor} ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-600 uppercase tracking-wider">
          Current Regime
        </h2>
        <div className="flex items-center gap-2">
          <span className="inline-flex h-2 w-2 rounded-full bg-green-500 animate-pulse"></span>
          <span className="text-xs text-gray-500">Live</span>
        </div>
      </div>

      {/* Regime Display */}
      <div className={`p-4 rounded-lg ${config.bgColor} mb-4`}>
        <div className="flex items-center gap-3">
          {config.icon}
          <div>
            <h3 className={`text-2xl font-bold ${config.color}`}>
              {config.label}
            </h3>
            <p className={`text-sm ${config.color} opacity-80`}>
              {config.description}
            </p>
          </div>
        </div>
      </div>

      {/* Metrics */}
      {regime && (
        <div className="grid grid-cols-3 gap-4">
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-2xl font-bold text-gray-900">
              {(confidence * 100).toFixed(0)}%
            </p>
            <p className="text-xs text-gray-500">Confidence</p>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-2xl font-bold text-gray-900">
              {((regime.probabilities?.risk_on || 0) * 100).toFixed(0)}%
            </p>
            <p className="text-xs text-gray-500">Risk On</p>
          </div>
          <div className="text-center p-3 bg-gray-50 rounded-lg">
            <p className="text-2xl font-bold text-gray-900">
              {((regime.probabilities?.risk_off || 0) * 100).toFixed(0)}%
            </p>
            <p className="text-xs text-gray-500">Risk Off</p>
          </div>
        </div>
      )}

      {/* Timestamp */}
      <div className="mt-4 text-xs text-gray-500 text-center">
        Last updated: {new Date().toLocaleTimeString()}
      </div>
    </div>
  )
}
