'use client'

import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { AssetClassSentiment } from '@/types/api'
import { formatAssetClass } from '@/lib/utils'
import ExportButton from '@/components/ExportButton'
import { exportChartAsPNG, exportChartAsSVG } from '@/utils/exportChart'

interface SentimentComparisonChartProps {
  data: AssetClassSentiment[]
}

export default function SentimentComparisonChart({ data }: SentimentComparisonChartProps) {
  // Transform data for the chart
  const chartData = data.map((item) => ({
    name: formatAssetClass(item.asset_class),
    score: parseFloat((item.compound_score * 100).toFixed(2)),
    positive: parseFloat((item.positive_ratio * 100).toFixed(2)),
    negative: parseFloat((item.negative_ratio * 100).toFixed(2)),
  }))

  return (
    <div id="sentiment-comparison-chart" className="bg-white rounded-lg border-2 border-gray-200 p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">
          Sentiment Comparison
        </h3>
        <ExportButton
          onExportPNG={() => exportChartAsPNG('sentiment-comparison-chart', 'sentiment-comparison')}
          onExportSVG={() => exportChartAsSVG('sentiment-comparison-chart', 'sentiment-comparison')}
        />
      </div>
      
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis
            dataKey="name"
            tick={{ fill: '#6b7280', fontSize: 12 }}
            stroke="#9ca3af"
          />
          <YAxis
            tick={{ fill: '#6b7280', fontSize: 12 }}
            stroke="#9ca3af"
            label={{ value: 'Sentiment Score (%)', angle: -90, position: 'insideLeft', fill: '#6b7280' }}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#ffffff',
              border: '1px solid #e5e7eb',
              borderRadius: '8px',
              padding: '12px',
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
