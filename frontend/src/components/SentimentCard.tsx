import type { AssetClassSentiment } from '@/types/api'
import {
  formatAssetClass,
  formatPercent,
  getSentimentLabel,
  getSentimentColor,
  getSentimentBgColor,
  getSentimentEmoji,
  formatNumber,
  getMomentumIndicator,
} from '@/lib/utils'

interface SentimentCardProps {
  sentiment: AssetClassSentiment
}

export default function SentimentCard({ sentiment }: SentimentCardProps) {
  const {
    asset_class,
    compound_score,
    positive_ratio,
    negative_ratio,
    neutral_ratio,
    sample_count,
    momentum,
  } = sentiment

  const label = getSentimentLabel(compound_score)
  const colorClass = getSentimentColor(compound_score)
  const bgClass = getSentimentBgColor(compound_score)
  const emoji = getSentimentEmoji(compound_score)
  const momentumInfo = getMomentumIndicator(momentum)

  return (
    <div className={`rounded-lg border-2 p-6 transition-all hover:shadow-lg ${bgClass}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{emoji}</span>
          <h3 className="text-lg font-semibold text-gray-900">
            {formatAssetClass(asset_class)}
          </h3>
        </div>
        <span className={`text-sm font-medium ${momentumInfo.color}`}>
          {momentumInfo.symbol} {momentumInfo.label}
        </span>
      </div>

      {/* Main Score */}
      <div className="mb-4">
        <div className={`text-3xl font-bold ${colorClass}`}>
          {compound_score >= 0 ? '+' : ''}
          {(compound_score * 100).toFixed(1)}
        </div>
        <div className={`text-sm font-medium ${colorClass}`}>{label}</div>
      </div>

      {/* Sentiment Breakdown */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Positive</span>
          <div className="flex items-center gap-2">
            <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-bullish"
                style={{ width: `${positive_ratio * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 w-12 text-right">
              {formatPercent(positive_ratio)}
            </span>
          </div>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Negative</span>
          <div className="flex items-center gap-2">
            <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-bearish"
                style={{ width: `${negative_ratio * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 w-12 text-right">
              {formatPercent(negative_ratio)}
            </span>
          </div>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Neutral</span>
          <div className="flex items-center gap-2">
            <div className="w-20 h-2 bg-gray-200 rounded-full overflow-hidden">
              <div
                className="h-full bg-neutral"
                style={{ width: `${neutral_ratio * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 w-12 text-right">
              {formatPercent(neutral_ratio)}
            </span>
          </div>
        </div>
      </div>

      {/* Sample Count */}
      <div className="pt-4 border-t border-gray-200">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">7-Day Volume</span>
          <span className="text-sm font-medium text-gray-700">
            {formatNumber(sample_count)} texts
          </span>
        </div>
      </div>
    </div>
  )
}
