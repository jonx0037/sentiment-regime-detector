'use client'

import type { SentimentResponse } from '@/types/api'
import { formatPercent, getSentimentLabel, getSentimentColor } from '@/lib/utils'
import Tooltip from './Tooltip'

interface CrossAssetSummaryProps {
  data: SentimentResponse
}

export default function CrossAssetSummary({ data }: CrossAssetSummaryProps) {
  const { cross_asset_mean, cross_asset_std, asset_classes, latest_data_date } = data

  const label = getSentimentLabel(cross_asset_mean)
  const colorClass = getSentimentColor(cross_asset_mean)

  // Calculate correlations and divergence
  const scores = asset_classes.map((ac) => ac.compound_score)
  const maxScore = Math.max(...scores)
  const minScore = Math.min(...scores)
  const spread = maxScore - minScore
  const recentVolume = asset_classes.reduce((sum, ac) => sum + ac.sample_count, 0)

  // Format the data date for display
  const dataDateDisplay = latest_data_date
    ? new Date(latest_data_date + 'T00:00:00').toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
    })
    : 'Unknown'

  return (
    <div className="bg-white dark:bg-gray-900 rounded-lg border-2 border-gray-200 dark:border-gray-700 p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900 dark:text-white">
          Cross-Asset Summary
        </h2>
        <div className="flex items-center gap-3">
          <span className="text-xs font-medium text-green-700 dark:text-green-300 bg-green-50 dark:bg-green-950 border border-green-200 dark:border-green-800 px-3 py-1 rounded-full">
            📡 Data as of {dataDateDisplay}
          </span>
          <span className="text-xs text-gray-400 dark:text-gray-400 bg-gray-50 dark:bg-gray-950 px-2 py-1 rounded">Last 7 days</span>
        </div>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-5 gap-6">
        {/* Mean Sentiment */}
        <div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1 flex items-center gap-1">
            Mean Sentiment
            <Tooltip content="Average compound sentiment across all 4 asset classes over the last 7 daily indices. Scale: -100 (most bearish) to +100 (most bullish). Derived from VADER + TextBlob ensemble scores on recent financial texts." />
          </div>
          <div className={`text-2xl font-bold ${colorClass}`}>
            {cross_asset_mean >= 0 ? '+' : ''}
            {(cross_asset_mean * 100).toFixed(1)}
          </div>
          <div className={`text-xs font-medium ${colorClass}`}>{label}</div>
        </div>

        {/* Standard Deviation */}
        <div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1 flex items-center gap-1">
            Dispersion
            <Tooltip content="Standard deviation of sentiment scores across the 4 asset classes. High dispersion (>20%) means asset classes are moving in different directions — a potential divergence signal." />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {formatPercent(cross_asset_std)}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            {cross_asset_std > 0.2 ? 'High Divergence' : cross_asset_std > 0.1 ? 'Moderate' : 'Low Divergence'}
          </div>
        </div>

        {/* Spread */}
        <div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1 flex items-center gap-1">
            Score Spread
            <Tooltip content="Difference between the most bullish and most bearish asset class. A wide spread (>40%) often precedes regime transitions as sentiment fractures across markets." />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {formatPercent(spread)}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Max − Min
          </div>
        </div>

        {/* 7-Day Volume */}
        <div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1 flex items-center gap-1">
            7-Day Volume
            <Tooltip content="Total scored texts in the last 7 daily aggregation periods across all 4 asset classes. Sources: Finnhub, NewsAPI, Reddit, and HPC-processed financial texts." />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            {recentVolume.toLocaleString()}
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Recent Texts
          </div>
        </div>

        {/* Total Corpus */}
        <div>
          <div className="text-sm text-gray-600 dark:text-gray-400 mb-1 flex items-center gap-1">
            Total Corpus
            <Tooltip content="~33M texts scored by a 6-model ensemble (FinBERT, RoBERTa, VADER, TextBlob, DistilBERT, Llama 3) on SMU MANEFRAME HPC. Sources include 21 Kaggle datasets + live APIs (Finnhub, NewsAPI, Reddit) spanning 2005–present." />
          </div>
          <div className="text-2xl font-bold text-gray-900 dark:text-white">
            ~33M
          </div>
          <div className="text-xs text-gray-500 dark:text-gray-400">
            Texts Scored (HPC)
          </div>
        </div>
      </div>

      {/* Market Condition Indicator */}
      <div className="mt-6 pt-6 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700 dark:text-gray-300 flex items-center gap-1">
            Market Condition
            <Tooltip content="A heuristic classification based on the mean sentiment, dispersion, and spread. Not a trading signal — it summarizes the current cross-asset mood." />
          </span>
          <span className={`text-sm font-bold ${colorClass}`}>
            {getMarketCondition(cross_asset_mean, cross_asset_std, spread)}
          </span>
        </div>
      </div>
    </div>
  )
}

function getMarketCondition(mean: number, std: number, spread: number): string {
  // High divergence
  if (std > 0.2 || spread > 0.4) {
    return 'Divergent - Asset-Specific Moves'
  }

  // Strong directional
  if (Math.abs(mean) > 0.2) {
    return mean > 0 ? 'Risk-On - Broad Bullish' : 'Risk-Off - Broad Bearish'
  }

  // Moderate directional
  if (Math.abs(mean) > 0.1) {
    return mean > 0 ? 'Cautiously Bullish' : 'Cautiously Bearish'
  }

  // Low conviction
  return 'Mixed - Low Conviction'
}
