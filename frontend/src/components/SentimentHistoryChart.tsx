'use client'

import { useEffect, useState } from 'react'
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine, Legend, CartesianGrid } from 'recharts'
import { TrendingUp, Calendar } from 'lucide-react'
import ExportButton from '@/components/ExportButton'
import { exportChartAsPNG, exportChartAsSVG } from '@/utils/exportChart'
import { useTheme } from '@/components/ThemeProvider'

interface SentimentDataPoint {
  date: string
  equity?: number | null
  crypto?: number | null
  forex?: number | null
  commodity?: number | null
}

interface SentimentHistoryResponse {
  start_date: string
  end_date: string
  count: number
  data: SentimentDataPoint[]
}

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1'

export default function SentimentHistoryChart() {
  const [data, setData] = useState<SentimentDataPoint[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [days, setDays] = useState(90)
  const [dateRange, setDateRange] = useState<{ start: string | null; end: string | null }>({ start: null, end: null })
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true)
        const response = await fetch(`${API_BASE}/sentiment/cross-asset/history?days=${days}`)
        if (!response.ok) throw new Error('Failed to fetch sentiment history')
        const result: SentimentHistoryResponse = await response.json()
        setData(result.data)
        setDateRange({ start: result.start_date, end: result.end_date })
        setError(null)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Unknown error')
      } finally {
        setLoading(false)
      }
    }

    fetchHistory()
  }, [days])

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/3 mb-4"></div>
          <div className="h-64 bg-gray-100 dark:bg-gray-800 rounded"></div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-red-200 dark:border-red-800 p-6">
        <p className="text-red-600 dark:text-red-400">Error loading sentiment history: {error}</p>
      </div>
    )
  }

  // Format data for chart
  const chartData = data.map(d => ({
    date: new Date(d.date).toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
    equity: d.equity,
    crypto: d.crypto,
    forex: d.forex,
    commodity: d.commodity,
  }))

  return (
    <div id="sentiment-history-chart" className="bg-white dark:bg-gray-900 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gray-900 dark:text-white flex items-center gap-2">
          <TrendingUp className="w-5 h-5 text-indigo-600" />
          Cross-Asset Sentiment History
        </h2>

        <div className="flex items-center gap-2">
          <ExportButton
            onExportPNG={() => exportChartAsPNG('sentiment-history-chart', 'sentiment-history')}
            onExportSVG={() => exportChartAsSVG('sentiment-history-chart', 'sentiment-history')}
          />
          <Calendar className="w-4 h-4 text-gray-400" />
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            title="Select time period"
            aria-label="Select time period for sentiment history"
            className="text-sm border border-gray-300 dark:border-gray-600 dark:bg-gray-800 dark:text-gray-200 rounded-md px-2 py-1 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value={7}>7 days</option>
            <option value={30}>30 days</option>
            <option value={90}>90 days</option>
            <option value={180}>180 days</option>
          </select>
        </div>
      </div>

      {/* Date range label */}
      {dateRange.end && (
        <p className="text-xs text-gray-400 mb-2">
          Showing data from {new Date(dateRange.start + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} to {new Date(dateRange.end + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })} · {data.length} data points
        </p>
      )}

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
              tick={{ fontSize: 11, fill: isDark ? '#9ca3af' : '#374151' }}
              domain={[-1, 1]}
              tickFormatter={(v) => v.toFixed(1)}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: isDark ? '#1f2937' : 'white',
                border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
                borderRadius: '8px',
                fontSize: '12px',
                color: isDark ? '#e5e7eb' : '#374151'
              }}
              formatter={(value) => {
                if (value === null || value === undefined) return ['N/A', '']
                if (typeof value === 'number') return [value.toFixed(3), '']
                return [String(value), '']
              }}
            />
            <Legend
              wrapperStyle={{ fontSize: '12px' }}
            />

            {/* Neutral sentiment line */}
            <ReferenceLine
              y={0}
              stroke="#9ca3af"
              strokeDasharray="3 3"
              label={{ value: 'Neutral', position: 'right', fill: '#9ca3af', fontSize: 10 }}
            />

            <Line
              type="monotone"
              dataKey="equity"
              stroke="#3b82f6"
              strokeWidth={2}
              dot={false}
              name="Equity"
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="crypto"
              stroke="#f59e0b"
              strokeWidth={2}
              dot={false}
              name="Crypto"
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="forex"
              stroke="#10b981"
              strokeWidth={2}
              dot={false}
              name="Forex"
              connectNulls
            />
            <Line
              type="monotone"
              dataKey="commodity"
              stroke="#8b5cf6"
              strokeWidth={2}
              dot={false}
              name="Commodity"
              connectNulls
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      {/* Stats */}
      <div className="mt-4 grid grid-cols-4 gap-4 text-center text-sm">
        <div className="p-2 bg-blue-50 dark:bg-blue-950 rounded">
          <p className="text-gray-500 dark:text-gray-400">Equity</p>
          <p className="font-semibold text-blue-600">
            {data.filter(d => d.equity !== null && d.equity !== undefined).length > 0
              ? (data.filter(d => d.equity !== null && d.equity !== undefined).reduce((a, b) => a + (b.equity || 0), 0) /
                data.filter(d => d.equity !== null && d.equity !== undefined).length).toFixed(3)
              : 'N/A'}
          </p>
        </div>
        <div className="p-2 bg-amber-50 dark:bg-amber-950 rounded">
          <p className="text-gray-500 dark:text-gray-400">Crypto</p>
          <p className="font-semibold text-amber-600">
            {data.filter(d => d.crypto !== null && d.crypto !== undefined).length > 0
              ? (data.filter(d => d.crypto !== null && d.crypto !== undefined).reduce((a, b) => a + (b.crypto || 0), 0) /
                data.filter(d => d.crypto !== null && d.crypto !== undefined).length).toFixed(3)
              : 'N/A'}
          </p>
        </div>
        <div className="p-2 bg-green-50 dark:bg-green-950 rounded">
          <p className="text-gray-500 dark:text-gray-400">Forex</p>
          <p className="font-semibold text-green-600">
            {data.filter(d => d.forex !== null && d.forex !== undefined).length > 0
              ? (data.filter(d => d.forex !== null && d.forex !== undefined).reduce((a, b) => a + (b.forex || 0), 0) /
                data.filter(d => d.forex !== null && d.forex !== undefined).length).toFixed(3)
              : 'N/A'}
          </p>
        </div>
        <div className="p-2 bg-purple-50 dark:bg-purple-950 rounded">
          <p className="text-gray-500 dark:text-gray-400">Commodity</p>
          <p className="font-semibold text-purple-600">
            {data.filter(d => d.commodity !== null && d.commodity !== undefined).length > 0
              ? (data.filter(d => d.commodity !== null && d.commodity !== undefined).reduce((a, b) => a + (b.commodity || 0), 0) /
                data.filter(d => d.commodity !== null && d.commodity !== undefined).length).toFixed(3)
              : 'N/A'}
          </p>
        </div>
      </div>
    </div>
  )
}
