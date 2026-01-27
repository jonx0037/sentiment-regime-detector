'use client'

import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import type { AssetClassSentiment } from '@/types/api'
import { formatAssetClass } from '@/lib/utils'

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
    <div className="bg-white rounded-lg border-2 border-gray-200 p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">
        Sentiment Comparison
      </h3>
      
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
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
            iconType="line"
          />
          <Line
            type="monotone"
            dataKey="score"
            stroke="#059669"
            strokeWidth={2}
            name="Compound Score"
            dot={{ r: 4 }}
            activeDot={{ r: 6 }}
          />
          <Line
            type="monotone"
            dataKey="positive"
            stroke="#10b981"
            strokeWidth={1.5}
            strokeDasharray="5 5"
            name="Positive %"
            dot={{ r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="negative"
            stroke="#dc2626"
            strokeWidth={1.5}
            strokeDasharray="5 5"
            name="Negative %"
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
