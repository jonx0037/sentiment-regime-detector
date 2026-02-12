import type { SentimentResponse } from '@/types/api'
import { formatPercent, getSentimentLabel, getSentimentColor } from '@/lib/utils'

interface CrossAssetSummaryProps {
  data: SentimentResponse
}

export default function CrossAssetSummary({ data }: CrossAssetSummaryProps) {
  const { cross_asset_mean, cross_asset_std, asset_classes } = data

  const label = getSentimentLabel(cross_asset_mean)
  const colorClass = getSentimentColor(cross_asset_mean)

  // Calculate correlations and divergence
  const scores = asset_classes.map((ac) => ac.compound_score)
  const maxScore = Math.max(...scores)
  const minScore = Math.min(...scores)
  const spread = maxScore - minScore

  return (
    <div className="bg-white rounded-lg border-2 border-gray-200 p-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-bold text-gray-900">
          Cross-Asset Summary
        </h2>
        <span className="text-xs text-gray-400 bg-gray-50 px-2 py-1 rounded">Last 7 days</span>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-6">
        {/* Mean Sentiment */}
        <div>
          <div className="text-sm text-gray-600 mb-1">Mean Sentiment</div>
          <div className={`text-2xl font-bold ${colorClass}`}>
            {cross_asset_mean >= 0 ? '+' : ''}
            {(cross_asset_mean * 100).toFixed(1)}
          </div>
          <div className={`text-xs font-medium ${colorClass}`}>{label}</div>
        </div>

        {/* Standard Deviation */}
        <div>
          <div className="text-sm text-gray-600 mb-1">Dispersion</div>
          <div className="text-2xl font-bold text-gray-900">
            {formatPercent(cross_asset_std)}
          </div>
          <div className="text-xs text-gray-500">
            {cross_asset_std > 0.2 ? 'High Divergence' : cross_asset_std > 0.1 ? 'Moderate' : 'Low Divergence'}
          </div>
        </div>

        {/* Spread */}
        <div>
          <div className="text-sm text-gray-600 mb-1">Score Spread</div>
          <div className="text-2xl font-bold text-gray-900">
            {formatPercent(spread)}
          </div>
          <div className="text-xs text-gray-500">
            Max - Min
          </div>
        </div>

        {/* Total Corpus */}
        <div>
          <div className="text-sm text-gray-600 mb-1">Total Corpus</div>
          <div className="text-2xl font-bold text-gray-900">
            ~8.5M
          </div>
          <div className="text-xs text-gray-500">
            Texts Scored (HPC)
          </div>
        </div>
      </div>

      {/* Market Condition Indicator */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <div className="flex items-center justify-between">
          <span className="text-sm font-medium text-gray-700">
            Market Condition
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
