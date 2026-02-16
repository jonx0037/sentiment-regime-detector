'use client'

import { Activity, RefreshCw, TrendingUp } from 'lucide-react'
import Tooltip from './Tooltip'
import type { GARCHBundle } from '@/types/api'

interface GARCHResultsPanelProps {
  data: GARCHBundle | null
  loading?: boolean
  error?: string | null
  onRetry?: () => void
}

export default function GARCHResultsPanel({
  data,
  loading = false,
  error = null,
  onRetry,
}: GARCHResultsPanelProps) {
  const formatNumber = (value: number | null | undefined, digits: number): string =>
    typeof value === 'number' ? value.toFixed(digits) : 'N/A'

  if (loading && !data) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-32 bg-gray-100 rounded"></div>
        </div>
      </div>
    )
  }

  if (!data && error) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
        <p className="text-red-600">Error loading GARCH results: {error}</p>
        {onRetry && (
          <button
            type="button"
            onClick={onRetry}
            className="mt-3 inline-flex items-center gap-2 px-3 py-2 text-sm bg-red-50 text-red-700 rounded-lg hover:bg-red-100 transition-colors"
          >
            <RefreshCw className="w-4 h-4" />
            Retry
          </button>
        )}
      </div>
    )
  }

  if (!data) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <p className="text-gray-500">GARCH results are not available yet.</p>
      </div>
    )
  }

  const params = data.parameters
  const forecast = data.forecast

  const getColorByLevel = (level: string) => {
    switch (level) {
      case 'high': return 'text-red-600 bg-red-50'
      case 'moderate': return 'text-yellow-600 bg-yellow-50'
      case 'low': return 'text-green-600 bg-green-50'
      default: return 'text-gray-600 bg-gray-50'
    }
  }

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      {/* Header */}
      <div className="flex items-center gap-2 mb-1">
        <Activity className="w-5 h-5 text-purple-600" />
        <h2 className="text-lg font-semibold text-gray-900">GARCH(1,1) Volatility Model</h2>
        <Tooltip content="Layer 1 of the Two-Layer Regime Detector. GARCH-MIDAS isolates the long-term volatility component driven by sentiment. The (1,1) means 1 lag for both ARCH and GARCH terms." />
      </div>
      {error && (
        <div className="mt-3 mb-2 p-2 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-800">
          Live refresh failed; showing last successful GARCH snapshot.
        </div>
      )}
      {(() => {
        const dataEnd = params.data_range?.end ? new Date(params.data_range.end) : null
        const dataStart = params.data_range?.start ? new Date(params.data_range.start) : null
        // Guard against epoch dates (1969/1970)
        const validStart = dataStart && dataStart.getFullYear() > 2000 ? dataStart : null
        const daysSinceData = dataEnd ? Math.floor((Date.now() - dataEnd.getTime()) / (1000 * 60 * 60 * 24)) : null
        const isStale = daysSinceData !== null && daysSinceData > 30

        return (
          <>
            <p className="text-xs text-gray-400 mb-2 ml-7">
              {params.run_timestamp && (
                <>Model fitted: {new Date(params.run_timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</>
              )}
              {params.data_range && (
                <> · Data: {validStart ? validStart.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '—'} to {dataEnd ? dataEnd.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '—'}
                  {(params.data_range.num_observations || params.data_range.n_observations) && ` (${(params.data_range.num_observations || params.data_range.n_observations)?.toLocaleString()} obs)`}
                </>
              )}
            </p>
            {isStale && (
              <div className="mb-3 ml-7 p-2 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-800">
                ⚠️ Data ends {dataEnd!.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} ({daysSinceData} days ago) — model may not reflect current market conditions.
              </div>
            )}
          </>
        )
      })()}

      {/* Model Parameters */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-4">
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Mean (μ)
            <Tooltip content="Expected return of the series" side="top" />
          </p>
          <p className="text-lg font-semibold text-gray-900">{params.parameters.mu.toFixed(4)}</p>
        </div>
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Omega (ω)
            <Tooltip content="Constant term in variance equation - baseline volatility level" side="top" />
          </p>
          <p className="text-lg font-semibold text-gray-900">{params.parameters.omega.toFixed(4)}</p>
        </div>
        <div className="p-3 bg-blue-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Alpha (α)
            <Tooltip content="ARCH effect - how much recent shocks impact current volatility. Higher α = more reactive to news." side="top" />
          </p>
          <p className="text-lg font-semibold text-blue-600">{params.parameters['alpha[1]'].toFixed(4)}</p>
        </div>
        <div className="p-3 bg-indigo-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Beta (β)
            <Tooltip content="GARCH effect - persistence of past volatility. Higher β = longer volatility memory." side="top" />
          </p>
          <p className="text-lg font-semibold text-indigo-600">{params.parameters['beta[1]'].toFixed(4)}</p>
        </div>
      </div>

      {/* Persistence Indicator */}
      <div className="mb-4 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg border border-purple-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 flex items-center gap-1">
              Volatility Persistence (α + β)
              <Tooltip content="Sum of α + β measures how long volatility shocks persist. Values near 1.0 mean shocks decay very slowly (high persistence). Values >0.95 suggest nearly permanent impact." side="right" />
            </p>
            <p className="text-2xl font-bold text-purple-700">{params.persistence.toFixed(4)}</p>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getColorByLevel(params.interpretation.persistence)}`}>
            {params.interpretation.persistence.toUpperCase()}
          </div>
        </div>
        <p className="text-xs text-gray-500 mt-2">
          High persistence (&gt;0.9) indicates shocks have long-lasting impact on volatility
        </p>
      </div>

      {/* Interpretation Cards */}
      <div className="grid grid-cols-2 gap-4 mb-4">
        <div className="p-3 bg-white border border-gray-200 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">Shock Impact</p>
          <div className="flex items-center gap-2">
            <span className={`px-2 py-0.5 rounded text-xs font-semibold ${getColorByLevel(params.interpretation.shock_impact)}`}>
              {params.interpretation.shock_impact}
            </span>
            <p className="text-sm text-gray-600">α = {params.parameters['alpha[1]'].toFixed(3)}</p>
          </div>
        </div>
        <div className="p-3 bg-white border border-gray-200 rounded-lg">
          <p className="text-xs text-gray-500 mb-1">Memory Effect</p>
          <div className="flex items-center gap-2">
            <span className={`px-2 py-0.5 rounded text-xs font-semibold ${getColorByLevel(params.interpretation.memory)}`}>
              {params.interpretation.memory}
            </span>
            <p className="text-sm text-gray-600">β = {params.parameters['beta[1]'].toFixed(3)}</p>
          </div>
        </div>
      </div>

      {/* Volatility Forecast Stats */}
      <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
        <div className="flex items-center gap-2 mb-3">
          <TrendingUp className="w-4 h-4 text-purple-600" />
          <p className="text-sm font-semibold text-gray-700">30-Day Volatility Forecast</p>
        </div>
        <div className="grid grid-cols-3 gap-4">
          <div>
            <p className="text-xs text-gray-500">Mean</p>
            <p className="text-lg font-semibold text-gray-900">{forecast.statistics.mean.toFixed(3)}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Max</p>
            <p className="text-lg font-semibold text-red-600">{forecast.statistics.max.toFixed(3)}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Min</p>
            <p className="text-lg font-semibold text-green-600">{forecast.statistics.min.toFixed(3)}</p>
          </div>
        </div>
      </div>

      {/* Model Fit */}
      <div className="mt-4 pt-4 border-t border-gray-200 flex justify-between text-xs text-gray-500">
        <span className="flex items-center gap-1">
          AIC: {formatNumber(params.aic, 2)}
          <Tooltip content="Akaike Information Criterion - measures model quality. Lower values indicate better fit while penalizing complexity." side="top" />
        </span>
        <span className="flex items-center gap-1">
          BIC: {formatNumber(params.bic, 2)}
          <Tooltip content="Bayesian Information Criterion - similar to AIC but penalizes model complexity more heavily. Lower is better." side="top" />
        </span>
        <span className="flex items-center gap-1">
          Log-Likelihood: {formatNumber(params.loglikelihood, 2)}
          <Tooltip content="Measures how well the model fits the data. Higher (less negative) values indicate better fit." side="top" />
        </span>
      </div>
    </div>
  )
}
