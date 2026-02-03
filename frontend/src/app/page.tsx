'use client'

import { useEffect, useState } from 'react'
import { sentimentApi, regimeApi } from '@/services/api'
import type { SentimentResponse, RegimeResponse } from '@/types/api'
import SentimentCard from '@/components/SentimentCard'
import CrossAssetSummary from '@/components/CrossAssetSummary'
import SentimentComparisonChart from '@/components/SentimentComparisonChart'
import RegimePanel from '@/components/RegimePanel'
import CISSPanel from '@/components/CISSPanel'
import CISSHistoryChart from '@/components/CISSHistoryChart'
import SentimentHistoryChart from '@/components/SentimentHistoryChart'
import GARCHResultsPanel from '@/components/GARCHResultsPanel'
import RegimeTimeline from '@/components/RegimeTimeline'
import { RefreshCw } from 'lucide-react'

export default function Dashboard() {
  const [data, setData] = useState<SentimentResponse | null>(null)
  const [regime, setRegime] = useState<RegimeResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())

  const fetchData = async () => {
    try {
      setLoading(true)
      setError(null)
      const [sentimentResponse, regimeResponse] = await Promise.all([
        sentimentApi.getCurrentSentiment(),
        regimeApi.getCurrentRegime(),
      ])
      setData(sentimentResponse)
      setRegime(regimeResponse)
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
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        {/* Section 1: Regime & Market Stress */}
        <section>
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <span className="text-2xl">📊</span>
            Current Market Regime
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
            <RegimePanel />
            <CISSPanel
              cissLevel={regime?.features?.ciss_level as number | undefined}
              vixLevel={regime?.features?.vix_level as number | undefined}
            />
          </div>
          <CISSHistoryChart />
        </section>

        {/* Section 2: Cross-Asset Sentiment */}
        <section>
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <span className="text-2xl">💭</span>
            Cross-Asset Sentiment Analysis
          </h2>
          <CrossAssetSummary data={data} />
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
            {data.asset_classes
              .sort((a, b) => a.asset_class.localeCompare(b.asset_class))
              .map((sentiment) => (
                <SentimentCard key={sentiment.asset_class} sentiment={sentiment} />
              ))}
          </div>
          <div className="mt-6">
            <SentimentComparisonChart data={data.asset_classes} />
          </div>
          <div className="mt-6">
            <SentimentHistoryChart />
          </div>
        </section>

        {/* Section 3: Volatility & Transitions */}
        <section>
          <h2 className="text-xl font-semibold text-gray-800 mb-4 flex items-center gap-2">
            <span className="text-2xl">📈</span>
            Volatility Modeling & Regime History
          </h2>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <GARCHResultsPanel />
            <RegimeTimeline />
          </div>
        </section>

        {/* Footer Info */}
        <section className="mt-8">
          <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border border-blue-200 rounded-xl p-6">
            <div className="flex items-start gap-4">
              <div className="text-blue-600 text-2xl">ℹ️</div>
              <div className="flex-1">
                <h3 className="text-base font-semibold text-blue-900 mb-2">
                  About This Dashboard
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800">
                  <div>
                    <p className="font-medium mb-1">Sentiment Analysis</p>
                    <p className="text-xs">
                      DistilBERT NLP models analyze sentiment across equity, crypto, forex, and commodity markets.
                      Scores range from -1 (bearish) to +1 (bullish). Data from Reddit, news, and social media.
                    </p>
                  </div>
                  <div>
                    <p className="font-medium mb-1">Regime Detection</p>
                    <p className="text-xs">
                      ML-based classifier (99.45% accuracy) uses CISS, VIX, and sentiment features to identify
                      risk-on, risk-off, and transition regimes in real-time.
                    </p>
                  </div>
                  <div>
                    <p className="font-medium mb-1">Volatility Modeling</p>
                    <p className="text-xs">
                      GARCH(1,1) models forecast market volatility with high persistence (α+β=0.955),
                      combining ARCH effects and historical volatility memory.
                    </p>
                  </div>
                  <div>
                    <p className="font-medium mb-1">Data Sources</p>
                    <p className="text-xs">
                      ECB CISS (systemic stress), CBOE VIX (implied volatility), and 2.66M+ sentiment texts
                      from multiple sources provide comprehensive market coverage.
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>
      </main>
    </div>
  )
}
