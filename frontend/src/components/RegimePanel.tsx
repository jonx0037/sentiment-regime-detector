'use client'

import { useState } from 'react'
import type { RegimeResponse } from '@/types/api'
import { Activity, TrendingUp, TrendingDown, AlertTriangle, Lightbulb, BookOpen } from 'lucide-react'
import { NoRegimeData } from './EmptyState'
import Tooltip from './Tooltip'
import ExplainabilityModal from './ExplainabilityModal'
import CrisisEventsBrowser from './CrisisEventsBrowser'

interface RegimePanelProps {
  regime: RegimeResponse | null
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
    color: 'text-green-700 dark:text-green-300',
    bgColor: 'bg-green-50 dark:bg-green-950',
    borderColor: 'border-green-200 dark:border-green-800',
    icon: <TrendingUp className="w-6 h-6 text-green-600" />,
    description: 'Stable market conditions with low VIX',
  },
  normal: {
    label: 'Normal',
    color: 'text-blue-700 dark:text-blue-300',
    bgColor: 'bg-blue-50 dark:bg-blue-950',
    borderColor: 'border-blue-200 dark:border-blue-800',
    icon: <Activity className="w-6 h-6 text-blue-600" />,
    description: 'Typical market volatility levels',
  },
  elevated: {
    label: 'Elevated',
    color: 'text-amber-700 dark:text-amber-300',
    bgColor: 'bg-amber-50 dark:bg-amber-950',
    borderColor: 'border-amber-200 dark:border-amber-800',
    icon: <AlertTriangle className="w-6 h-6 text-amber-600" />,
    description: 'Increased volatility - monitor closely',
  },
  high_volatility: {
    label: 'High Volatility',
    color: 'text-red-700 dark:text-red-300',
    bgColor: 'bg-red-50 dark:bg-red-950',
    borderColor: 'border-red-200 dark:border-red-800',
    icon: <TrendingDown className="w-6 h-6 text-red-600" />,
    description: 'Crisis-level volatility detected',
  },
  risk_on: {
    label: 'Risk On',
    color: 'text-green-700 dark:text-green-300',
    bgColor: 'bg-green-50 dark:bg-green-950',
    borderColor: 'border-green-200 dark:border-green-800',
    icon: <TrendingUp className="w-6 h-6 text-green-600" />,
    description: 'Positive sentiment - risk appetite increasing',
  },
  risk_off: {
    label: 'Risk Off',
    color: 'text-red-700 dark:text-red-300',
    bgColor: 'bg-red-50 dark:bg-red-950',
    borderColor: 'border-red-200 dark:border-red-800',
    icon: <TrendingDown className="w-6 h-6 text-red-600" />,
    description: 'Negative sentiment - flight to safety',
  },
  transition: {
    label: 'Transition',
    color: 'text-purple-700 dark:text-purple-300',
    bgColor: 'bg-purple-50 dark:bg-purple-950',
    borderColor: 'border-purple-200 dark:border-purple-800',
    icon: <Activity className="w-6 h-6 text-purple-600" />,
    description: 'Regime change in progress',
  },
}

export default function RegimePanel({ regime, className = '' }: RegimePanelProps) {
  const [isExplainModalOpen, setIsExplainModalOpen] = useState(false)
  const [isCrisisEventsOpen, setIsCrisisEventsOpen] = useState(false)

  if (!regime) {
    return <NoRegimeData className={className} />
  }

  const currentRegime = regime.regime
  const confidence = regime.confidence
  const config = regimeConfig[currentRegime] || regimeConfig.normal
  const volatilityState = regime.volatility_regime
  const volatilityConfig = regimeConfig[volatilityState] || regimeConfig.normal
  const volatilityScore = regime.volatility_score

  return (
    <div className={`p-6 bg-white dark:bg-gray-900 rounded-xl shadow-sm border ${config.borderColor} ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-sm font-semibold text-gray-600 dark:text-gray-400 uppercase tracking-wider flex items-center gap-1">
          Current Regime
          <Tooltip content="Layer 2 of the Two-Layer Regime Detector. A Statistical Jump Model classifies Risk-On / Risk-Off / Transition states from CISS, VIX, and cross-asset sentiment features. Regime data covers 2005–present (HPC-processed)." />
        </h2>
        <div className="flex items-center gap-2">
          <span className="inline-flex h-2 w-2 rounded-full bg-blue-500"></span>
          <span className="text-xs text-gray-500 dark:text-gray-400">Jump Model</span>
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
      <div className="grid grid-cols-3 gap-4">
        <div className="text-center p-3 bg-gray-50 dark:bg-gray-950 rounded-lg">
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {(confidence * 100).toFixed(0)}%
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center justify-center gap-1">
            Confidence
            <Tooltip content="Model confidence in the predicted regime. Based on sentiment dispersion, CISS/VIX alignment, and feature consistency. Not a probability of being correct." />
          </p>
        </div>
        <div className="text-center p-3 bg-gray-50 dark:bg-gray-950 rounded-lg">
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {((regime.probabilities?.risk_on || 0) * 100).toFixed(0)}%
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center justify-center gap-1">
            Risk On
            <Tooltip content="Probability of bullish regime - investors seeking higher returns, positive sentiment, lower stress" />
          </p>
        </div>
        <div className="text-center p-3 bg-gray-50 dark:bg-gray-950 rounded-lg">
          <p className="text-2xl font-bold text-gray-900 dark:text-white">
            {((regime.probabilities?.risk_off || 0) * 100).toFixed(0)}%
          </p>
          <p className="text-xs text-gray-500 dark:text-gray-400 flex items-center justify-center gap-1">
            Risk Off
            <Tooltip content="Probability of bearish regime - flight to safety, negative sentiment, elevated stress" />
          </p>
        </div>
      </div>

      {/* Volatility Regime */}
      <div className="mt-4 p-4 border border-gray-100 dark:border-gray-700 rounded-lg bg-gray-50 dark:bg-gray-950">
        <p className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wide mb-2 flex items-center gap-1">
          Volatility Regime (Jump Model)
          <Tooltip content="Layer 1 output. Combines VIX, ECB CISS, and sentiment dispersion to approximate the four jump-model regimes described in Draft 1." />
        </p>
        <div className={`flex items-center gap-3 p-3 rounded-lg ${volatilityConfig.bgColor}`}>
          {volatilityConfig.icon}
          <div>
            <p className={`text-lg font-semibold ${volatilityConfig.color}`}>{volatilityConfig.label}</p>
            <p className={`text-xs ${volatilityConfig.color} opacity-80`}>{volatilityConfig.description}</p>
          </div>
          <div className="ml-auto text-right">
            <p className="text-xs text-gray-500 dark:text-gray-400">Volatility Score</p>
            <p className="text-lg font-bold text-gray-900 dark:text-white">{(volatilityScore * 100).toFixed(0)}%</p>
          </div>
        </div>
        <div className="mt-2 h-2 bg-white dark:bg-gray-900 rounded-full overflow-hidden">
          <div
            className={`${volatilityConfig.color?.replace('text', 'bg') || 'bg-purple-500'} h-full transition-all`}
            style={{ width: `${Math.min(volatilityScore * 100, 100)}%` }}
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="mt-4 grid grid-cols-2 gap-3">
        <button
          type="button"
          onClick={() => setIsExplainModalOpen(true)}
          className="flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-lg hover:from-blue-700 hover:to-indigo-700 transition-all shadow-sm hover:shadow-md font-medium text-sm"
        >
          <Lightbulb className="w-4 h-4" />
          Explain
        </button>
        <button
          type="button"
          onClick={() => setIsCrisisEventsOpen(true)}
          className="flex items-center justify-center gap-2 px-4 py-2.5 bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-lg hover:from-indigo-700 hover:to-purple-700 transition-all shadow-sm hover:shadow-md font-medium text-sm"
        >
          <BookOpen className="w-4 h-4" />
          History
        </button>
      </div>

      {/* Data Provenance */}
      <div className="mt-4 text-xs text-gray-400 dark:text-gray-400 text-center space-y-1">
        <div>Classification from ECB CISS, CBOE VIX &amp; cross-asset sentiment</div>
        <div>Total corpus: ~33M texts (21 Kaggle datasets + live APIs · 2005–present)</div>
        <div>Research signal for market context; use with other analysis and risk controls.</div>
        <div className="font-medium text-gray-500 dark:text-gray-400">
          Data as of {new Date(regime.timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
        </div>
      </div>

      {/* Explainability Modal */}
      <>
        <ExplainabilityModal
          isOpen={isExplainModalOpen}
          onClose={() => setIsExplainModalOpen(false)}
          regime={currentRegime as 'risk_on' | 'risk_off' | 'transition'}
          confidence={confidence}
        />
        <CrisisEventsBrowser
          isOpen={isCrisisEventsOpen}
          onClose={() => setIsCrisisEventsOpen(false)}
        />
      </>
    </div>
  )
}
