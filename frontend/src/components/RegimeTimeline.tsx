'use client'

import { useEffect, useState } from 'react'
import { Clock, ArrowRight, TrendingUp, TrendingDown, Minus } from 'lucide-react'

interface RegimeTransition {
  date: string
  from_regime: string
  to_regime: string
  ciss: number | null
  vix: number | null
}

interface TransitionsResponse {
  count: number
  transitions: RegimeTransition[]
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function RegimeTimeline() {
  const [transitions, setTransitions] = useState<RegimeTransition[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchTransitions = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${API_BASE}/regime/transitions?limit=20`)
        if (!response.ok) throw new Error('Failed to fetch regime transitions')
        const result: TransitionsResponse = await response.json()
        setTransitions(result.transitions)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchTransitions()
  }, [])

  const getRegimeIcon = (regime: string) => {
    switch (regime) {
      case 'risk_on':
        return <TrendingUp className="w-4 h-4 text-green-600" />
      case 'risk_off':
        return <TrendingDown className="w-4 h-4 text-red-600" />
      case 'transition':
        return <Minus className="w-4 h-4 text-yellow-600" />
      default:
        return <Minus className="w-4 h-4 text-gray-600" />
    }
  }

  const getRegimeColor = (regime: string) => {
    switch (regime) {
      case 'risk_on':
        return 'bg-green-100 text-green-700 border-green-300'
      case 'risk_off':
        return 'bg-red-100 text-red-700 border-red-300'
      case 'transition':
        return 'bg-yellow-100 text-yellow-700 border-yellow-300'
      default:
        return 'bg-gray-100 text-gray-700 border-gray-300'
    }
  }

  const getRegimeLabel = (regime: string) => {
    return regime.replace('_', ' ').split(' ').map(word =>
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ')
  }

  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="space-y-3">
            {[1, 2, 3].map(i => (
              <div key={i} className="h-16 bg-gray-100 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
        <p className="text-red-600">Error loading transitions: {error}</p>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-4">
        <Clock className="w-5 h-5 text-blue-600" />
        <h2 className="text-lg font-semibold text-gray-900">Regime Transition History</h2>
        <span className="ml-auto text-sm text-gray-500">{transitions.length} recent changes</span>
      </div>

      {/* Timeline */}
      <div className="space-y-3 max-h-96 overflow-y-auto">
        {transitions.map((transition, idx) => (
          <div
            key={idx}
            className="flex items-center gap-3 p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors"
          >
            {/* Date */}
            <div className="flex-shrink-0 w-24 text-right">
              <p className="text-xs font-medium text-gray-900">
                {new Date(transition.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
              </p>
              <p className="text-xs text-gray-500">
                {new Date(transition.date).getFullYear()}
              </p>
            </div>

            {/* Timeline Dot */}
            <div className="flex-shrink-0 w-2 h-2 rounded-full bg-blue-500" />

            {/* From Regime */}
            <div className={`flex items-center gap-1.5 px-2 py-1 rounded-md border text-xs font-medium ${getRegimeColor(transition.from_regime)}`}>
              {getRegimeIcon(transition.from_regime)}
              <span>{getRegimeLabel(transition.from_regime)}</span>
            </div>

            {/* Arrow */}
            <ArrowRight className="w-4 h-4 text-gray-400" />

            {/* To Regime */}
            <div className={`flex items-center gap-1.5 px-2 py-1 rounded-md border text-xs font-medium ${getRegimeColor(transition.to_regime)}`}>
              {getRegimeIcon(transition.to_regime)}
              <span>{getRegimeLabel(transition.to_regime)}</span>
            </div>

            {/* Metrics */}
            <div className="ml-auto flex gap-3 text-xs">
              {transition.ciss !== null && (
                <div className="text-right">
                  <p className="text-gray-500">CISS</p>
                  <p className="font-semibold text-gray-900">{(transition.ciss * 100).toFixed(1)}%</p>
                </div>
              )}
              {transition.vix !== null && (
                <div className="text-right">
                  <p className="text-gray-500">VIX</p>
                  <p className="font-semibold text-gray-900">{transition.vix.toFixed(1)}</p>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Summary Stats */}
      <div className="mt-4 pt-4 border-t border-gray-200 grid grid-cols-3 gap-4 text-center text-sm">
        <div className="p-2 bg-green-50 rounded">
          <p className="text-gray-500 text-xs">To Risk On</p>
          <p className="font-semibold text-green-700">
            {transitions.filter(t => t.to_regime === 'risk_on').length}
          </p>
        </div>
        <div className="p-2 bg-yellow-50 rounded">
          <p className="text-gray-500 text-xs">To Transition</p>
          <p className="font-semibold text-yellow-700">
            {transitions.filter(t => t.to_regime === 'transition').length}
          </p>
        </div>
        <div className="p-2 bg-red-50 rounded">
          <p className="text-gray-500 text-xs">To Risk Off</p>
          <p className="font-semibold text-red-700">
            {transitions.filter(t => t.to_regime === 'risk_off').length}
          </p>
        </div>
      </div>
    </div>
  )
}
