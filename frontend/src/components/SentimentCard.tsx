'use client'

import type { AssetClassSentiment } from '@/types/api'
import {
  formatAssetClass,
  formatPercent,
  getSentimentLabel,
  getSentimentColor,
  getSentimentBgColor,
  getSentimentEmoji,
  formatNumber,
} from '@/lib/utils'
import Tooltip from './Tooltip'

interface SentimentCardProps {
  sentiment: AssetClassSentiment
  latestDataDate?: string | null
}

/**
 * Momentum label based on 7-day change in compound score.
 * "Trending Up/Down" is clearer than "Strong Up/Down" which
 * sounds like it describes the level, not the direction of change.
 */
function getMomentumInfo(momentum: number): {
  symbol: string
  color: string
  label: string
} {
  if (momentum > 0.05) {
    return { symbol: '⬆️', color: 'text-bullish', label: 'Trending Up' }
  }
  if (momentum > 0.01) {
    return { symbol: '↗️', color: 'text-bullish-light', label: 'Drifting Up' }
  }
  if (momentum < -0.05) {
    return { symbol: '⬇️', color: 'text-bearish', label: 'Trending Down' }
  }
  if (momentum < -0.01) {
    return { symbol: '↘️', color: 'text-bearish-light', label: 'Drifting Down' }
  }
  return { symbol: '→', color: 'text-neutral', label: 'Stable' }
}

export default function SentimentCard({ sentiment, latestDataDate }: SentimentCardProps) {
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
  const momentumInfo = getMomentumInfo(momentum)

  return (
    <div className={`rounded-lg border-2 p-6 transition-all hover:shadow-lg ${bgClass}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-2xl">{emoji}</span>
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            {formatAssetClass(asset_class)}
          </h3>
        </div>
        <span className={`text-sm font-medium flex items-center gap-1 ${momentumInfo.color}`}>
          {momentumInfo.symbol} {momentumInfo.label}
          <Tooltip content={`7-day momentum: sentiment is ${momentum >= 0 ? 'rising' : 'falling'} compared to the prior 7-day period (Δ = ${momentum >= 0 ? '+' : ''}${(momentum * 100).toFixed(1)}). This measures the DIRECTION of change, not the current level.`} />
        </span>
      </div>

      {/* Main Score */}
      <div className="mb-4">
        <div className="flex items-baseline gap-1">
          <span className={`text-3xl font-bold ${colorClass}`}>
            {compound_score >= 0 ? '+' : ''}
            {(compound_score * 100).toFixed(1)}
          </span>
          <Tooltip content={`Compound sentiment score (×100). Raw score: ${compound_score.toFixed(4)}. Scale: -100 (most bearish) to +100 (most bullish). Averaged over the last 7 days of daily sentiment indices for ${formatAssetClass(asset_class)}.`} />
        </div>
        <div className={`text-sm font-medium ${colorClass}`}>{label}</div>
      </div>

      {/* Sentiment Breakdown */}
      <div className="space-y-2 mb-4">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600 dark:text-gray-400">Positive</span>
          <div className="flex items-center gap-2">
            <div className="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-bullish"
                style={{ width: `${positive_ratio * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-white w-12 text-right">
              {formatPercent(positive_ratio)}
            </span>
          </div>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600 dark:text-gray-400">Negative</span>
          <div className="flex items-center gap-2">
            <div className="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-bearish"
                style={{ width: `${negative_ratio * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-white w-12 text-right">
              {formatPercent(negative_ratio)}
            </span>
          </div>
        </div>

        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600 dark:text-gray-400">Neutral</span>
          <div className="flex items-center gap-2">
            <div className="w-20 h-2 bg-gray-200 dark:bg-gray-700 rounded-full overflow-hidden">
              <div
                className="h-full bg-neutral"
                style={{ width: `${neutral_ratio * 100}%` }}
              />
            </div>
            <span className="text-sm font-medium text-gray-900 dark:text-white w-12 text-right">
              {formatPercent(neutral_ratio)}
            </span>
          </div>
        </div>
      </div>

      {/* Volume & Data Freshness */}
      <div className="pt-4 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500 dark:text-gray-400 flex items-center gap-1">
            7-Day Volume
            <Tooltip content={`Total texts scored in the last 7 daily aggregation periods for ${formatAssetClass(asset_class)}. Sources include financial news (Finnhub, NewsAPI) and social data (Reddit).`} />
          </span>
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
            {formatNumber(sample_count)} texts
          </span>
        </div>
        {latestDataDate && (
          <div className="mt-2 text-xs text-gray-400 dark:text-gray-400 text-right">
            Data as of {new Date(latestDataDate + 'T00:00:00').toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>
        )}
      </div>
    </div>
  )
}
