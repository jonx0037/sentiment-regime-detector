'use client'

import { useEffect, useState } from 'react'
import { sentimentApi } from '@/services/api'
import type { SentimentResponse } from '@/types/api'
import SentimentCard from '@/components/SentimentCard'
import CrossAssetSummary from '@/components/CrossAssetSummary'
import SentimentComparisonChart from '@/components/SentimentComparisonChart'
import RegimePanel from '@/components/RegimePanel'
import { RefreshCw } from 'lucide-react'

export default function Dashboard() {
  const [data, setData] = useState<SentimentResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await sentimentApi.getCurrentSentiment()
      setData(response)
      setLastUpdate(new Date())
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch data')
      console.error('Error fetching sentiment data:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchData()
    
    // Auto-refresh every 60 seconds
    const interval = setInterval(fetchData, 60000)
    return () => clearInterval(interval)
  }, [])

  if (loading && !data) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading sentiment data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center max-w-md">
          <div className="text-red-600 text-5xl mb-4">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-900 mb-2">
            Unable to Load Data
          </h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={fetchData}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (!data) {
    return null
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                Sentiment Regime Detector
              </h1>
              <p className="text-sm text-gray-600 mt-1">
                Cross-Asset Sentiment Analysis Dashboard
              </p>
            </div>
            <button
              onClick={fetchData}
              disabled={loading}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              Refresh
            </button>
          </div>
          <div className="mt-2 text-xs text-gray-500">
            Last updated: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Regime Detection Panel */}
        <div className="mb-8">
          <RegimePanel />
        </div>

        {/* Cross-Asset Summary */}
        <div className="mb-8">
          <CrossAssetSummary data={data} />
        </div>

        {/* Sentiment Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {data.asset_classes
            .sort((a, b) => a.asset_class.localeCompare(b.asset_class))
            .map((sentiment) => (
              <SentimentCard key={sentiment.asset_class} sentiment={sentiment} />
            ))}
        </div>

        {/* Comparison Chart */}
        <div className="mb-8">
          <SentimentComparisonChart data={data.asset_classes} />
        </div>

        {/* Footer Info */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-start gap-3">
            <div className="text-blue-600 text-xl">ℹ️</div>
            <div className="flex-1">
              <h3 className="text-sm font-semibold text-blue-900 mb-1">
                About This Dashboard
              </h3>
              <p className="text-xs text-blue-800">
                This dashboard displays real-time sentiment analysis across major asset classes using 
                DistilBERT NLP models. Sentiment scores range from -100 (extremely bearish) to +100 
                (extremely bullish). Data is aggregated from Reddit, news sources, and social media.
              </p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
