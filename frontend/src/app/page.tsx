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
import ErrorBoundary from '@/components/ErrorBoundary'
import ErrorMessage from '@/components/ErrorMessage'
import LoadingSkeleton from '@/components/LoadingSkeleton'
import { NoSentimentData } from '@/components/EmptyState'
import FadeIn from '@/components/FadeIn'
import { InlineTooltip } from '@/components/Tooltip'
import HelpModal from '@/components/HelpModal'
import ExportMenu from '@/components/ExportMenu'
import { ToastContainer, useToast } from '@/components/Toast'
import { RefreshCw, HelpCircle } from 'lucide-react'

export default function Dashboard() {
  const [data, setData] = useState<SentimentResponse | null>(null)
  const [regime, setRegime] = useState<RegimeResponse | null>(null)
  const [garch, setGarch] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [helpModalOpen, setHelpModalOpen] = useState(false)
  const { toasts, showToast, removeToast } = useToast()

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
    return <LoadingSkeleton variant="page" message="Loading dashboard..." />
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50">
        <ErrorMessage
          error={error}
          onRetry={fetchData}
          variant="full"
        />
      </div>
    )
  }

  if (!data || !data.asset_classes || data.asset_classes.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <h1 className="text-3xl font-bold text-gray-900">
              Sentiment Regime Detector
            </h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <NoSentimentData onRefresh={fetchData} />
        </main>
      </div>
    )
  }

  return (
    <ErrorBoundary onReset={fetchData}>
      <HelpModal isOpen={helpModalOpen} onClose={() => setHelpModalOpen(false)} />
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
              <div className="flex items-center gap-3">
                <ExportMenu
                  sentiment={data}
                  regime={regime}
                  garch={garch}
                  onToast={showToast}
                />
                <button
                  type="button"
                  onClick={() => setHelpModalOpen(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                  aria-label="Open help guide"
                >
                  <HelpCircle className="w-4 h-4" />
                  <span className="hidden sm:inline">Help</span>
                </button>
                <button
                  type="button"
                  onClick={fetchData}
                  disabled={loading}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
                  Refresh
                </button>
              </div>
            </div>
            <div className="mt-2 text-xs text-gray-500">
              Last updated: {lastUpdate.toLocaleTimeString()}
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          {/* Section 1: Regime & Market Stress */}
          <FadeIn delay={0}>
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
          </FadeIn>

          {/* Section 2: Cross-Asset Sentiment */}
          <FadeIn delay={100}>
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
          </FadeIn>

          {/* Section 3: Volatility & Transitions */}
          <FadeIn delay={200}>
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
          </FadeIn>

          {/* Footer Info */}
          <FadeIn delay={300}>
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
                          A{' '}
                          <InlineTooltip
                            term="6-model ensemble"
                            definition="FinBERT, RoBERTa, VADER, TextBlob, DistilBERT, and Llama 3 (8B). Weighted predictions are combined for robust, multi-perspective sentiment classification across source types."
                          />
                          {' '}scored ~33M texts from Reddit, Twitter, and financial news across four
                          asset classes: Equities, Crypto, Forex, and Commodities.
                          Compound scores range from -1 (most bearish) to +1 (most bullish).
                        </p>
                      </div>
                      <div>
                        <p className="font-medium mb-1">Regime Detection</p>
                        <p className="text-xs">
                          Two-Layer model: <InlineTooltip
                            term="GARCH-MIDAS"
                            definition="Generalized Autoregressive Conditional Heteroskedasticity — Mixed Data Sampling. Isolates long-term volatility driven by sentiment from short-term noise."
                          />
                          {' '}isolates sentiment-driven volatility; a{' '}
                          <InlineTooltip
                            term="Statistical Jump Model"
                            definition="Classifies discrete regime states while penalizing frequent switching, producing more stable and persistent regime identifications than Hidden Markov Models (Shu et al., 2024)."
                          />
                          {' '}classifies Risk-On / Risk-Off / Transition states using{' '}
                          <InlineTooltip
                            term="CISS"
                            definition="Composite Indicator of Systemic Stress from the European Central Bank"
                          />, <InlineTooltip
                            term="VIX"
                            definition="CBOE Volatility Index — the market's expectation of 30-day forward volatility"
                          />, and cross-asset sentiment features.
                        </p>
                      </div>
                      <div>
                        <p className="font-medium mb-1">Volatility Modeling</p>
                        <p className="text-xs">
                          <InlineTooltip
                            term="GARCH(1,1)"
                            definition="Generalized Autoregressive Conditional Heteroskedasticity — decomposes volatility into short-term shocks (α / ARCH) and long-term memory (β / GARCH)"
                          />
                          {' '}decomposes volatility into short-term shocks (α) and long-term memory (β). High <InlineTooltip
                            term="persistence"
                            definition="α+β near 1.0 means volatility shocks decay very slowly — current volatility strongly predicts future volatility"
                          /> (α+β ≈ 1.0) means
                          current volatility strongly predicts future volatility.
                        </p>
                      </div>
                      <div>
                        <p className="font-medium mb-1">Data Sources</p>
                        <p className="text-xs">
                          ~33M texts from 21 Kaggle datasets + live APIs (Finnhub, NewsAPI, Reddit), processed on SMU MANEFRAME HPC.
                          Systemic stress from ECB (CISS) and CBOE (VIX). Data spans 2005–present.
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>
          </FadeIn>
        </main>
      </div>
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ErrorBoundary>
  )
}
