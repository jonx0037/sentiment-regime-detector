'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { AssetClassSentiment } from '@/types/api'
import { formatAssetClass } from '@/lib/utils'
import ExportButton from '@/components/ExportButton'
import { exportChartAsPNG, exportChartAsSVG } from '@/utils/exportChart'
import { useTheme } from '@/components/ThemeProvider'

interface SentimentComparisonChartProps {
  data: AssetClassSentiment[]
  latestDataDate?: string | null
}

export default function SentimentComparisonChart({ data, latestDataDate }: SentimentComparisonChartProps) {
  const { theme } = useTheme()
  const isDark = theme === 'dark'

  // Transform data for the chart
  const chartData = data.map((item) => ({
    name: formatAssetClass(item.asset_class),
    score: parseFloat((item.compound_score * 100).toFixed(2)),
    positive: parseFloat((item.positive_ratio * 100).toFixed(2)),
    negative: parseFloat((item.negative_ratio * 100).toFixed(2)),
  }))

  return (
    <div id="sentiment-comparison-chart" className="bg-white dark:bg-gray-900 rounded-lg border-2 border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
          Sentiment Comparison
        </h3>
        <div className="flex items-center gap-3">
          {latestDataDate && (
            <span className="text-xs text-gray-400">
              Data as of {new Date(latestDataDate + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
            </span>
          )}
          <ExportButton
            onExportPNG={() => exportChartAsPNG('sentiment-comparison-chart', 'sentiment-comparison')}
            onExportSVG={() => exportChartAsSVG('sentiment-comparison-chart', 'sentiment-comparison')}
          />
        </div>
      </div>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke={isDark ? '#374151' : '#e5e7eb'} />
          <XAxis
            dataKey="name"
            tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
            stroke={isDark ? '#4b5563' : '#9ca3af'}
          />
          <YAxis
            tick={{ fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
            stroke={isDark ? '#4b5563' : '#9ca3af'}
            label={{ value: 'Sentiment Score', angle: -90, position: 'insideLeft', fill: isDark ? '#9ca3af' : '#6b7280', fontSize: 12 }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: isDark ? '#1f2937' : '#ffffff',
              border: `1px solid ${isDark ? '#374151' : '#e5e7eb'}`,
              borderRadius: '8px',
              padding: '12px',
              color: isDark ? '#e5e7eb' : '#374151',
            }}
            formatter={(value: number) => `${value.toFixed(1)}%`}
          />
          <Legend
            wrapperStyle={{ paddingTop: '20px' }}
          />
          <Bar
            dataKey="score"
            fill="#059669"
            name="Compound Score"
            radius={[4, 4, 0, 0]}
          />
          <Bar
            dataKey="positive"
            fill="#10b981"
            name="Positive %"
            radius={[4, 4, 0, 0]}
          />
          <Bar
            dataKey="negative"
            fill="#dc2626"
            name="Negative %"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
