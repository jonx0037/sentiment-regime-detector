'use client'

import { Activity } from 'lucide-react'
import Tooltip from './Tooltip'

export interface GARCHParameters {
  mu: number
  omega: number
  'alpha[1]': number
  'beta[1]': number
}

export interface GARCHInterpretation {
  persistence: string
  shock_impact: string
  memory: string
}

export interface GARCHResponse {
  parameters: GARCHParameters
  persistence: number
  aic: number
  bic: number
  loglikelihood: number
  interpretation: GARCHInterpretation
  run_timestamp?: string
  data_range?: { start: string; end: string; num_observations?: number }
}

export interface VolatilityForecast {
  horizon: number
  forecast: number[]
  statistics: {
    mean: number
    max: number
    min: number
  }
  model: {
    params: GARCHParameters
    aic: number
    bic: number
  }
}

interface GARCHResultsPanelProps {
  parameters: GARCHResponse | null
  forecast: VolatilityForecast | null
  loading: boolean
  error: string | null
  onRetry: () => Promise<void> | void
}

const getColorByLevel = (level: string) => {
  switch (level) {
    case 'high':
      return 'text-red-600 bg-red-50'
    case 'moderate':
      return 'text-yellow-600 bg-yellow-50'
    case 'low':
      return 'text-green-600 bg-green-50'
    default:
      return 'text-gray-600 bg-gray-50'
  }
}

export default function GARCHResultsPanel({
  parameters,
  forecast,
  loading,
  error,
  onRetry,
}: GARCHResultsPanelProps) {
  if (loading) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-32 bg-gray-100 rounded"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6 flex flex-col gap-3">
        <p className="text-red-600">Error loading GARCH results: {error}</p>
        <button
          type="button"
          onClick={() => onRetry()}
          className="self-start px-3 py-2 text-sm font-medium bg-red-600 text-white rounded-lg hover:bg-red-700"
        >
          Retry
        </button>
      </div>
    )
  }

  if (!parameters || !forecast) {
    return null
  }

  const dataEnd = parameters.data_range?.end ? new Date(parameters.data_range.end) : null
  const dataStart = parameters.data_range?.start ? new Date(parameters.data_range.start) : null
  const validStart = dataStart && dataStart.getFullYear() > 2000 ? dataStart : null
  const daysSinceData = dataEnd ? Math.floor((Date.now() - dataEnd.getTime()) / (1000 * 60 * 60 * 24)) : null
  const isStale = daysSinceData !== null && daysSinceData > 30

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <div className="flex items-center gap-2 mb-1">
        <Activity className="w-5 h-5 text-purple-600" />
        <h2 className="text-lg font-semibold text-gray-900">GARCH(1,1) Volatility Model</h2>
        <Tooltip content="Layer 1 of the Two-Layer Regime Detector. GARCH-MIDAS isolates the long-term volatility component driven by sentiment. The (1,1) means 1 lag for both ARCH and GARCH terms." />
      </div>
      <p className="text-xs text-gray-400 mb-2 ml-7">
        {parameters.run_timestamp && (
          <>Model fitted: {new Date(parameters.run_timestamp).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}</>
        )}
        {parameters.data_range && (
          <> · Data: {validStart ? validStart.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '—'} to {dataEnd ? dataEnd.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' }) : '—'}
            {parameters.data_range.num_observations && ` (${parameters.data_range.num_observations.toLocaleString()} obs)`}
          </>
        )}
      </p>
      {isStale && dataEnd && (
        <div className="mb-3 ml-7 p-2 bg-amber-50 border border-amber-200 rounded-lg text-xs text-amber-800">
          ⚠️ Data ends {dataEnd.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} ({daysSinceData} days ago) — model may not reflect current market conditions.
        </div>
      )}

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4 mb-4">
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Mean (μ)
            <Tooltip content="Expected return of the series" side="top" />
          </p>
          <p className="text-lg font-semibold text-gray-900">{parameters.parameters.mu.toFixed(4)}</p>
        </div>
        <div className="p-3 bg-gray-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Omega (ω)
            <Tooltip content="Constant term in variance equation - baseline volatility level" side="top" />
          </p>
          <p className="text-lg font-semibold text-gray-900">{parameters.parameters.omega.toFixed(4)}</p>
        </div>
        <div className="p-3 bg-blue-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Alpha (α)
            <Tooltip content="ARCH effect - how much recent shocks impact current volatility. Higher α = more reactive to news." side="top" />
          </p>
          <p className="text-lg font-semibold text-blue-600">{parameters.parameters['alpha[1]'].toFixed(4)}</p>
        </div>
        <div className="p-3 bg-indigo-50 rounded-lg">
          <p className="text-xs text-gray-500 mb-1 flex items-center gap-1">
            Beta (β)
            <Tooltip content="GARCH effect - persistence of past volatility. Higher β = longer volatility memory." side="top" />
          </p>
          <p className="text-lg font-semibold text-indigo-600">{parameters.parameters['beta[1]'].toFixed(4)}</p>
        </div>
      </div>

      <div className="mb-4 p-4 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg border border-purple-200">
        <div className="flex items-center justify-between">
          <div>
            <p className="text-sm text-gray-600 flex items-center gap-1">
              Volatility Persistence (α + β)
              <Tooltip content="Sum of α + β measures how long volatility shocks persist. Values near 1.0 mean shocks decay very slowly (high persistence). Values >0.95 suggest nearly permanent impact." side="right" />
            </p>
            <p className="text-2xl font-bold text-purple-700">{parameters.persistence.toFixed(4)}</p>
          </div>
          <div className={`px-3 py-1 rounded-full text-sm font-semibold ${getColorByLevel(parameters.interpretation.persistence)}`}>
            {parameters.interpretation.persistence.toUpperCase()}
          </div>
        </div>
        <p className="text-sm text-gray-600">
          {parameters.interpretation.persistence === 'high'
            ? 'Volatility shocks are highly persistent. Expect elevated volatility to linger.'
            : parameters.interpretation.persistence === 'moderate'
              ? 'Volatility is moderately persistent. Shocks decay over weeks.'
              : 'Volatility shocks decay quickly. Markets should normalize faster.'}
        </p>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-4">
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide">Shock Impact</p>
          <p className={`text-sm font-semibold ${getColorByLevel(parameters.interpretation.shock_impact)}`}>
            {parameters.interpretation.shock_impact.toUpperCase()}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 uppercase tracking-wide">Volatility Memory</p>
          <p className={`text-sm font-semibold ${getColorByLevel(parameters.interpretation.memory)}`}>
            {parameters.interpretation.memory.toUpperCase()}
          </p>
        </div>
      </div>

      <div className="bg-gray-50 rounded-lg p-4 mb-4">
        <p className="text-xs font-semibold text-gray-500 mb-2 uppercase">Model Diagnostics</p>
        <div className="grid grid-cols-3 gap-4 text-center">
          <div>
            <p className="text-gray-500">AIC</p>
            <p className="text-lg font-semibold text-gray-900">{parameters.aic.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500">BIC</p>
            <p className="text-lg font-semibold text-gray-900">{parameters.bic.toFixed(2)}</p>
          </div>
          <div>
            <p className="text-gray-500">Log Likelihood</p>
            <p className="text-lg font-semibold text-gray-900">{parameters.loglikelihood.toFixed(2)}</p>
          </div>
        </div>
      </div>

      <div>
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-sm font-semibold text-gray-700 flex items-center gap-2">
            Volatility Forecast ({forecast.horizon} days)
            <Tooltip content="Expected conditional volatility over the next 30 days based on current GARCH parameters." side="top" />
          </h3>
          <div className="flex gap-3 text-xs text-gray-500">
            <span>Mean: {forecast.statistics.mean.toFixed(4)}</span>
            <span>Max: {forecast.statistics.max.toFixed(4)}</span>
            <span>Min: {forecast.statistics.min.toFixed(4)}</span>
          </div>
        </div>
        <div className="h-32 overflow-hidden rounded-lg border border-gray-100">
          <div className="grid grid-cols-10 h-full">
            {forecast.forecast.map((value, index) => (
              <div key={index} className="flex flex-col items-center justify-end text-[10px] text-gray-500">
                <div
                  className="w-full bg-indigo-200"
                  style={{ height: `${Math.min(Math.abs(value) * 200, 100)}%` }}
                />
                <span className="mt-1">D{index + 1}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
