'use client'

import { useEffect, useState } from 'react'
import { Activity, TrendingUp } from 'lucide-react'
import Tooltip from './Tooltip'

interface GARCHParameters {
  mu: number
  omega: number
  'alpha[1]': number
  'beta[1]': number
}

interface GARCHInterpretation {
  persistence: string
  shock_impact: string
  memory: string
}

interface GARCHResponse {
  parameters: GARCHParameters
  persistence: number
  aic: number
  bic: number
  loglikelihood: number
  interpretation: GARCHInterpretation
}

interface VolatilityForecast {
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

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function GARCHResultsPanel() {
  const [params, setParams] = useState<GARCHResponse | null>(null)
  const [forecast, setForecast] = useState<VolatilityForecast | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true)

        // Fetch both parameters and forecast
        const [paramsRes, forecastRes] = await Promise.all([
          fetch(`${API_BASE}/garch/parameters`),
          fetch(`${API_BASE}/garch/volatility/forecast?horizon=30`)
        ])

        if (!paramsRes.ok || !forecastRes.ok) {
          throw new Error('Failed to fetch GARCH data')
        }

        const paramsData = await paramsRes.json()
        const forecastData = await forecastRes.json()

        setParams(paramsData)
        setForecast(forecastData)
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

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
      <div className="bg-white rounded-xl shadow-sm border border-red-200 p-6">
        <p className="text-red-600">Error loading GARCH results: {error}</p>
      </div>
    )
  }

  if (!params || !forecast) {
    return null
  }

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
      <div className="flex items-center gap-2 mb-4">
        <Activity className="w-5 h-5 text-purple-600" />
        <h2 className="text-lg font-semibold text-gray-900">GARCH(1,1) Volatility Model</h2>
        <Tooltip content="Generalized Autoregressive Conditional Heteroskedasticity - a time series model that predicts volatility based on past shocks (ARCH effects) and historical volatility. The (1,1) means 1 lag for both terms." />
      </div>

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
          AIC: {params.aic.toFixed(2)}
          <Tooltip content="Akaike Information Criterion - measures model quality. Lower values indicate better fit while penalizing complexity." side="top" />
        </span>
        <span className="flex items-center gap-1">
          BIC: {params.bic.toFixed(2)}
          <Tooltip content="Bayesian Information Criterion - similar to AIC but penalizes model complexity more heavily. Lower is better." side="top" />
        </span>
        <span className="flex items-center gap-1">
          Log-Likelihood: {params.loglikelihood.toFixed(2)}
          <Tooltip content="Measures how well the model fits the data. Higher (less negative) values indicate better fit." side="top" />
        </span>
      </div>
    </div>
  )
}
