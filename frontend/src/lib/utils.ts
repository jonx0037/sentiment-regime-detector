import type { AssetClass } from '@/types/api'

/**
 * Format a sentiment score to a readable percentage
 */
export function formatSentiment(score: number): string {
  return `${(score * 100).toFixed(1)}%`
}

/**
 * Get sentiment label based on compound score
 */
export function getSentimentLabel(score: number): 'Bullish' | 'Bearish' | 'Neutral' {
  if (score > 0.1) return 'Bullish'
  if (score < -0.1) return 'Bearish'
  return 'Neutral'
}

/**
 * Get color class based on sentiment score
 */
export function getSentimentColor(score: number): string {
  if (score > 0.1) return 'text-bullish'
  if (score < -0.1) return 'text-bearish'
  return 'text-neutral'
}

/**
 * Get background color class based on sentiment score
 */
export function getSentimentBgColor(score: number): string {
  if (score > 0.1) return 'bg-bullish/10 border-bullish'
  if (score < -0.1) return 'bg-bearish/10 border-bearish'
  return 'bg-neutral/10 border-neutral'
}

/**
 * Get emoji for sentiment
 */
export function getSentimentEmoji(score: number): string {
  if (score > 0.1) return '📈'
  if (score < -0.1) return '📉'
  return '↔️'
}

/**
 * Format asset class name for display
 */
export function formatAssetClass(assetClass: AssetClass): string {
  const names: Record<AssetClass, string> = {
    equity: 'Equities',
    crypto: 'Crypto',
    forex: 'Forex',
    commodity: 'Commodities',
  }
  return names[assetClass] || assetClass
}

/**
 * Format number as percentage
 */
export function formatPercent(value: number, decimals: number = 1): string {
  return `${(value * 100).toFixed(decimals)}%`
}

/**
 * Format large numbers with K/M suffix
 */
export function formatNumber(num: number): string {
  if (num >= 1000000) {
    return `${(num / 1000000).toFixed(1)}M`
  }
  if (num >= 1000) {
    return `${(num / 1000).toFixed(1)}K`
  }
  return num.toString()
}

/**
 * Calculate momentum indicator
 */
export function getMomentumIndicator(momentum: number): {
  symbol: string
  color: string
  label: string
} {
  if (momentum > 0.05) {
    return { symbol: '⬆️', color: 'text-bullish', label: 'Strong Up' }
  }
  if (momentum > 0.01) {
    return { symbol: '↗️', color: 'text-bullish-light', label: 'Up' }
  }
  if (momentum < -0.05) {
    return { symbol: '⬇️', color: 'text-bearish', label: 'Strong Down' }
  }
  if (momentum < -0.01) {
    return { symbol: '↘️', color: 'text-bearish-light', label: 'Down' }
  }
  return { symbol: '→', color: 'text-neutral', label: 'Stable' }
}
