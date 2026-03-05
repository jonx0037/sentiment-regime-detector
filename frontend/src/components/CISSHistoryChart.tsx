'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Legend, CartesianGrid } from 'recharts'
import { TrendingUp, Calendar } from 'lucide-react'
import ErrorMessage from './ErrorMessage'
import { ChartSkeleton } from './LoadingSkeleton'
import { NoHistoricalData } from './EmptyState'
import ExportButton from '@/components/ExportButton'
import { exportChartAsPNG, exportChartAsSVG } from '@/utils/exportChart'
import { useTheme } from '@/components/ThemeProvider'

interface CISSDataPoint {
  date: string
  ciss: number | null
  vix: number | null
}

interface CISSHistoryResponse {
  start_date: string
  end_date: string
  count: number
  data: CISSDataPoint[]
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function CISSHistoryChart() {
  const [data, setData] = useState<CISSDataPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [days, setDays] = useState(90)
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  const fetchHistory = async () => {
    try {
      setLoading(true)
      const response = await fetch(`${API_BASE}/regime/ciss/history?days=${days}`)
      if (!response.ok) throw new Error('Failed to fetch CISS history')
      const result: CISSHistoryResponse = await response.json()
      setData(result.data)
      setError(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchHistory()
  }, [days])

  if (loading) {
    return <ChartSkeleton />
  }

  if (error) {
    return (
      <ErrorMessage
        error={error}
        onRetry={fetchHistory}
        variant="card"
      />
    )
  }

  if (data.length === 0) {
    return (
      <NoHistoricalData
        period={`the last ${days} days`}
        onRefresh={fetchHistory}
      />
    )
  }

  const toLocalDate = (dateStr: string): Date => {
    const [year, month, day] = dateStr.split('-').map(Number)
    return new Date(year, month - 1, day)
  }

  const formatDate = (dateStr: string, options: Intl.DateTimeFormatOptions): string => {
    return toLocalDate(dateStr).toLocaleDateString('en-US', options)
  }

  // Format data for chart - multiply CISS by 100 for percentage
  const chartData = data.map(d => ({
    date: formatDate(d.date, { month: 'short', day: 'numeric' }),
    ciss: d.ciss !== null ? d.ciss * 100 : null,
    vix: d.vix,
  }))

  const cissValues = data.filter(d => d.ciss !== null).map(d => d.ciss as number)
  const vixValues = data.filter(d => d.vix !== null).map(d => d.vix as number)
  const latestCissPoint = [...data].reverse().find(d => d.ciss !== null)
  const latestVixPoint = [...data].reverse().find(d => d.vix !== null)

  return (
    <div id="ciss-history-chart" className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div>
          <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-blue-600" />
            CISS & VIX History
          </h2>
          <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
            Coverage: CISS through {latestCissPoint ? formatDate(latestCissPoint.date, { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A'} •
            {' '}VIX through {latestVixPoint ? formatDate(latestVixPoint.date, { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A'}.
            {' '}Chart timeline extends through today.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <ExportButton
            onExportPNG={() => exportChartAsPNG('ciss-history-chart', 'ciss-history')}
            onExportSVG={() => exportChartAsSVG('ciss-history-chart', 'ciss-history')}
          />
          <Calendar className="w-4 h-4 text-gray-400" />
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            title="Select time period"
            aria-label="Select time period for CISS history"
            className="text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200 rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
            <option value={180}>180 days</option>
            <option value={365}>1 year</option>
          </select>
        </div>
      </div>

      {/* Chart */}
      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={chartData} margin={{ top: 5, right: 30, left: 0, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#f0f0f0'} />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 11, fill: isDark ? '#9ca3af' : '#374151' }}
              tickLine={false}
              interval="preserveStartEnd"
            />
            <YAxis
              yAxisId="ciss"
              tick={{ fontSize: 11, fill: isDark ? '#9ca3af' : '#374151' }}
              tickFormatter={(v) => `${v}%`}
              domain={[0, 'auto']}
              orientation="left"
            />
            <YAxis
              yAxisId="vix"
              tick={{ fontSize: 11, fill: isDark ? '#9ca3af' : '#374151' }}
              domain={[0, 'auto']}
              orientation="right"
            />
            <Tooltip
              contentStyle={{
                backgroundColor: isDark ? '#1f2937' : 'white',
                border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                borderRadius: '8px',
                fontSize: '12px',
                color: isDark ? '#e5e7eb' : '#374151'
              }}
              formatter={(value: number, name: string) => {
                if (name === 'ciss') return [`${value.toFixed(1)}%`, 'CISS']
                return [value?.toFixed(1), 'VIX']
              }}
            />
            <Legend 
              formatter={(value) => value === 'ciss' ? 'ECB CISS (%)' : 'CBOE VIX'}
            />
            
            {/* Crisis threshold line */}
            <ReferenceLine 
              yAxisId="ciss"
              y={50} 
              stroke="#ef4444" 
              strokeDasharray="5 5" 
              label={{ value: 'Crisis', position: 'right', fill: '#ef4444', fontSize: 10 }}
            />
            
            <Line 
              yAxisId="ciss"
              type="monotone" 
              dataKey="ciss" 
              stroke="#3b82f6" 
              strokeWidth={2}
              dot={false}
              name="ciss"
            />
            <Line 
              yAxisId="vix"
              type="monotone" 
              dataKey="vix" 
              stroke="#f59e0b" 
              strokeWidth={1.5}
              dot={false}
              name="vix"
              strokeDasharray="3 3"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Stats */}
      <div className="mt-4 grid grid-cols-4 gap-4 text-center text-sm">
        <div className="p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <p className="text-gray-500 dark:text-gray-400">Data Points</p>
          <p className="font-semibold text-gray-900 dark:text-white">{data.length}</p>
        </div>
        <div className="p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <p className="text-gray-500 dark:text-gray-400">CISS Mean</p>
          <p className="font-semibold text-gray-900 dark:text-white">
            {cissValues.length ? `${(cissValues.reduce((a, b) => a + b, 0) / cissValues.length * 100).toFixed(1)}%` : 'N/A'}
          </p>
        </div>
        <div className="p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <p className="text-gray-500 dark:text-gray-400">CISS Max</p>
          <p className="font-semibold text-gray-900 dark:text-white">
            {cissValues.length ? `${(Math.max(...cissValues) * 100).toFixed(1)}%` : 'N/A'}
          </p>
        </div>
        <div className="p-2 bg-gray-50 dark:bg-gray-800 rounded">
          <p className="text-gray-500 dark:text-gray-400">VIX Mean</p>
          <p className="font-semibold text-gray-900 dark:text-white">
            {vixValues.length ? (vixValues.reduce((a, b) => a + b, 0) / vixValues.length).toFixed(1) : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )
}
