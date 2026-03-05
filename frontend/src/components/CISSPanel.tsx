'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip as ChartTooltip, ResponsiveContainer, ReferenceLine, Area, ComposedChart } from 'recharts'
import { Activity, TrendingUp, TrendingDown, AlertTriangle } from 'lucide-react'
import Tooltip from './Tooltip'

interface CISSData {
  date: string
  ciss: number
  vix: number | null
}

interface CISSPanelProps {
  cissLevel?: number | null
  vixLevel?: number | null
  className?: string
  latestDataDate?: string | null
}

const getCISSStatus = (ciss: number): { label: string; color: string; bgColor: string; icon: React.ReactNode } => {
  if (ciss < 0.15) {
    return {
      label: 'Calm',
      color: 'text-green-700 dark:text-green-300',
      bgColor: 'bg-green-100 dark:bg-green-800',
      icon: <TrendingUp className="w-5 h-5 text-green-600" />,
    }
  } else if (ciss < 0.25) {
    return {
      label: 'Elevated',
      color: 'text-amber-700 dark:text-amber-300',
      bgColor: 'bg-amber-100 dark:bg-amber-800',
      icon: <Activity className="w-5 h-5 text-amber-600" />,
    }
  } else if (ciss < 0.5) {
    return {
      label: 'Stressed',
      color: 'text-orange-700 dark:text-orange-300',
      bgColor: 'bg-orange-100 dark:bg-orange-800',
      icon: <AlertTriangle className="w-5 h-5 text-orange-600" />,
    }
  } else {
    return {
      label: 'Crisis',
      color: 'text-red-700 dark:text-red-300',
      bgColor: 'bg-red-100 dark:bg-red-800',
      icon: <TrendingDown className="w-5 h-5 text-red-600" />,
    }
  }
}

const getVIXStatus = (vix: number): { label: string; color: string } => {
  if (vix < 15) {
    return { label: 'Low Vol', color: 'text-green-600' }
  } else if (vix < 20) {
    return { label: 'Normal', color: 'text-blue-600' }
  } else if (vix < 30) {
    return { label: 'Elevated', color: 'text-amber-600' }
  } else {
    return { label: 'High Vol', color: 'text-red-600' }
  }
}

export default function CISSPanel({ cissLevel, vixLevel, className = '', latestDataDate }: CISSPanelProps) {
  const ciss = cissLevel ?? 0
  const vix = vixLevel ?? 0

  const cissStatus = getCISSStatus(ciss)
  const vixStatus = getVIXStatus(vix)

  // Format CISS as percentage
  const cissPercent = (ciss * 100).toFixed(1)

  return (
    <div className={`bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 ${className}`}>
      <h2 className="text-lg font-semibold text-gray-900 dark:text-white mb-4 flex items-center gap-2">
        <Activity className="w-5 h-5 text-blue-600" />
        Systemic Stress Indicators
        <Tooltip content="Metrics measuring financial system stress and market volatility expectations" />
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4 sm:gap-6">
        {/* ECB CISS */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400 flex items-center gap-1">
              ECB CISS Index
              <Tooltip content="Composite Indicator of Systemic Stress - measures stress in European financial markets across money, bond, equity, and foreign exchange segments. Range: 0 (calm) to 1 (extreme stress)." />
            </span>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${cissStatus.bgColor} ${cissStatus.color}`}>
              {cissStatus.label}
            </span>
          </div>

          <div className="flex items-end gap-2">
            {cissStatus.icon}
            <span className="text-3xl font-bold text-gray-900 dark:text-white">{cissPercent}%</span>
          </div>

          {/* CISS Gauge */}
          <div className="relative h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className={`absolute left-0 top-0 h-full rounded-full transition-all duration-500 ${ciss < 0.15 ? 'bg-green-500' :
                  ciss < 0.25 ? 'bg-amber-500' :
                    ciss < 0.5 ? 'bg-orange-500' : 'bg-red-500'
                }`}
              style={{ width: `${Math.min(ciss * 100, 100)}%` }}
            />
            {/* Crisis threshold marker */}
            <div className="absolute top-0 h-full w-0.5 bg-red-600" style={{ left: '50%' }} />
          </div>

          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>Calm (0%)</span>
            <span>Crisis (50%+)</span>
          </div>

          <p className="text-xs text-gray-500 dark:text-gray-400">
            Composite Indicator of Systemic Stress from ECB. Values above 0.5 indicate crisis conditions.
          </p>
        </div>

        {/* VIX */}
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-600 dark:text-gray-400 flex items-center gap-1">
              CBOE VIX
              <Tooltip content="Chicago Board Options Exchange Volatility Index - the 'fear gauge' measuring expected 30-day volatility of the S&P 500 based on option prices. Higher values indicate greater expected market volatility." />
            </span>
            <span className={`px-2 py-0.5 rounded-full text-xs font-medium bg-gray-100 dark:bg-gray-800 ${vixStatus.color}`}>
              {vixStatus.label}
            </span>
          </div>

          <div className="flex items-end gap-2">
            <Activity className={`w-5 h-5 ${vixStatus.color}`} />
            <span className="text-3xl font-bold text-gray-900 dark:text-white">{vix.toFixed(1)}</span>
          </div>

          {/* VIX Gauge */}
          <div className="relative h-3 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
            <div
              className={`absolute left-0 top-0 h-full rounded-full transition-all duration-500 ${vix < 15 ? 'bg-green-500' :
                  vix < 20 ? 'bg-blue-500' :
                    vix < 30 ? 'bg-amber-500' : 'bg-red-500'
                }`}
              style={{ width: `${Math.min((vix / 80) * 100, 100)}%` }}
            />
            {/* Normal threshold marker */}
            <div className="absolute top-0 h-full w-0.5 bg-amber-600" style={{ left: `${(20 / 80) * 100}%` }} />
          </div>

          <div className="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>Low (0)</span>
            <span>Extreme (80+)</span>
          </div>

          <p className="text-xs text-gray-500 dark:text-gray-400">
            CBOE Volatility Index. "Fear gauge" measuring S&P 500 implied volatility.
          </p>
        </div>
      </div>

      {/* CISS-VIX Correlation Note */}
      <div className="mt-4 p-3 bg-blue-50 dark:bg-blue-950 border border-blue-100 dark:border-blue-800 rounded-lg">
        <p className="text-xs text-blue-800 dark:text-blue-300">
          <strong>CISS-VIX Correlation:</strong> During COVID-19 (Mar 2020), correlation was 0.92.
          CISS measures systemic stress while VIX measures implied volatility.
        </p>
      </div>

      {latestDataDate && (
        <div className="mt-3 text-xs text-gray-400 dark:text-gray-400 text-center font-medium">
          Data as of {new Date(latestDataDate + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
        </div>
      )}
    </div>
  )
}
