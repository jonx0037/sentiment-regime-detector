'use client'

import { useEffect, useRef, useState } from 'react'
import { garchApi, sentimentApi, regimeApi } from '@/services/api'
import type { SentimentResponse, RegimeResponse, GARCHBundle } from '@/types/api'
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
import { ChatbotWidget } from '@/components/chatbot'
import { useTheme } from '@/components/ThemeProvider'
import { RefreshCw, HelpCircle, Sun, Moon } from 'lucide-react'

export default function Dashboard() {
  const [data, setData] = useState<SentimentResponse | null>(null)
  const [regime, setRegime] = useState<RegimeResponse | null>(null)
  const [garch, setGarch] = useState<GARCHBundle | null>(null)
  const [loading, setLoading] = useState(true)
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [garchError, setGarchError] = useState<string | null>(null)
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date())
  const [lastApiSuccess, setLastApiSuccess] = useState<Date | null>(null)
  const [lastSentimentSuccess, setLastSentimentSuccess] = useState<Date | null>(null)
  const [lastRegimeSuccess, setLastRegimeSuccess] = useState<Date | null>(null)
  const [lastGarchSuccess, setLastGarchSuccess] = useState<Date | null>(null)
  const [healthStatus, setHealthStatus] = useState<'connecting' | 'live' | 'degraded' | 'offline'>('connecting')
  const [clockNow, setClockNow] = useState<number>(Date.now())
  const [helpModalOpen, setHelpModalOpen] = useState(false)
  const hasSentimentDataRef = useRef(false)
  const hasGarchErrorRef = useRef(false)
  const { toasts, showToast, removeToast } = useToast()
  const { theme, toggleTheme } = useTheme()

  useEffect(() => {
    hasSentimentDataRef.current = Boolean(data?.asset_classes?.length)
  }, [data])

  useEffect(() => {
    hasGarchErrorRef.current = Boolean(garchError)
  }, [garchError])

  const fetchGarchData = async (): Promise<GARCHBundle> => {
    const [parameters, forecast] = await Promise.all([
      garchApi.getParameters(),
      garchApi.getVolatilityForecast(30),
    ])
    return { parameters, forecast }
  }

  const fetchAllData = async ({ initial = false, manual = false }: { initial?: boolean; manual?: boolean } = {}) => {
    if (initial) {
      setLoading(true)
    }
    if (manual) {
      setIsRefreshing(true)
    }

    try {
      const [sentimentResult, regimeResult, garchResult] = await Promise.allSettled([
        sentimentApi.getCurrentSentiment(),
        regimeApi.getCurrentRegime(),
        fetchGarchData(),
      ])

      const now = new Date()
      let hadAnySuccess = false
      let hadAnyFailure = false

      if (sentimentResult.status === 'fulfilled') {
        setData(sentimentResult.value)
        setLastSentimentSuccess(now)
        hadAnySuccess = true
      } else {
        hadAnyFailure = true
        console.error('Error fetching sentiment data:', sentimentResult.reason)
      }

      if (regimeResult.status === 'fulfilled') {
        setRegime(regimeResult.value)
        setLastRegimeSuccess(now)
        hadAnySuccess = true
      } else {
        hadAnyFailure = true
        console.error('Error fetching regime data:', regimeResult.reason)
      }

      if (garchResult.status === 'fulfilled') {
        setGarch(garchResult.value)
        setGarchError(null)
        setLastGarchSuccess(now)
        hadAnySuccess = true
      } else {
        hadAnyFailure = true
        const garchMessage = garchResult.reason instanceof Error
          ? garchResult.reason.message
          : 'Failed to fetch GARCH data'
        setGarchError(garchMessage)
        console.error('Error fetching GARCH data:', garchResult.reason)
      }

      if (hadAnySuccess) {
        setError(null)
        setHealthStatus(hadAnyFailure ? 'degraded' : 'live')
        setLastUpdate(now)
        setLastApiSuccess(now)
      } else {
        setHealthStatus(hasSentimentDataRef.current ? 'degraded' : 'offline')
        if (!hasSentimentDataRef.current) {
          setError('Failed to fetch dashboard data')
        }
        if (manual) {
          showToast('Refresh failed. Please try again.', 'error')
        }
      }
    } catch (err) {
      console.error('Unexpected dashboard fetch error:', err)
      setHealthStatus(hasSentimentDataRef.current ? 'degraded' : 'offline')
      if (!hasSentimentDataRef.current) {
        setError(err instanceof Error ? err.message : 'Failed to fetch dashboard data')
      }
      if (manual) {
        showToast('Refresh failed. Please try again.', 'error')
      }
    } finally {
      if (initial) {
        setLoading(false)
      }
      if (manual) {
        setIsRefreshing(false)
      }
    }
  }

  const refreshRegimeOnly = async () => {
    try {
      const regimeResponse = await regimeApi.getCurrentRegime()
      const now = new Date()
      setRegime(regimeResponse)
      setLastRegimeSuccess(now)
      setHealthStatus(hasGarchErrorRef.current ? 'degraded' : 'live')
      setLastUpdate(now)
      setLastApiSuccess(now)
    } catch (err) {
      console.error('Error refreshing regime data:', err)
      setHealthStatus(hasSentimentDataRef.current ? 'degraded' : 'offline')
    }
  }

  useEffect(() => {
    fetchAllData({ initial: true })

    // Full refresh every 60 seconds (sentiment + regime + garch)
    const fullRefreshInterval = setInterval(() => {
      fetchAllData()
    }, 60000)

    // Regime-only refresh every 30 seconds
    const regimeRefreshInterval = setInterval(() => {
      refreshRegimeOnly()
    }, 30000)

    // Update staleness indicators even without new network events
    const heartbeatInterval = setInterval(() => {
      setClockNow(Date.now())
    }, 15000)

    return () => {
      clearInterval(fullRefreshInterval)
      clearInterval(regimeRefreshInterval)
      clearInterval(heartbeatInterval)
    }
  }, [])

  const secondsSinceLastSuccess = lastApiSuccess
    ? Math.floor((clockNow - lastApiSuccess.getTime()) / 1000)
    : null

  const isStale = secondsSinceLastSuccess !== null && secondsSinceLastSuccess > 90
  const effectiveHealthStatus = healthStatus === 'live' && isStale ? 'degraded' : healthStatus

  const healthMap = {
    connecting: {
      label: 'Connecting',
      dot: 'bg-gray-400',
      badge: 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 border-gray-200 dark:border-gray-700',
    },
    live: {
      label: 'Live',
      dot: 'bg-emerald-500',
      badge: 'bg-emerald-50 dark:bg-emerald-950 text-emerald-700 dark:text-emerald-400 border-emerald-200 dark:border-emerald-800',
    },
    degraded: {
      label: isStale ? 'Stale' : 'Degraded',
      dot: 'bg-amber-500',
      badge: 'bg-amber-50 dark:bg-amber-950 text-amber-700 dark:text-amber-400 border-amber-200 dark:border-amber-800',
    },
    offline: {
      label: 'Offline',
      dot: 'bg-red-500',
      badge: 'bg-red-50 dark:bg-red-950 text-red-700 dark:text-red-400 border-red-200 dark:border-red-800',
    },
  } as const

  const health = healthMap[effectiveHealthStatus]

  if (loading && !data) {
    return (
      <>
        <LoadingSkeleton variant="page" message="Loading dashboard..." />
        <ChatbotWidget />
      </>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
        <ErrorMessage
          error={error}
          onRetry={() => fetchAllData({ manual: true })}
          variant="full"
        />
        <ChatbotWidget />
      </div>
    )
  }

  if (!data || !data.asset_classes || data.asset_classes.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
        <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
              Sentiment Regime Detector
            </h1>
          </div>
        </header>
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <NoSentimentData onRefresh={() => fetchAllData({ manual: true })} />
        </main>
        <ChatbotWidget />
      </div>
    )
  }

  return (
    <ErrorBoundary onReset={() => fetchAllData({ manual: true })}>
      <HelpModal isOpen={helpModalOpen} onClose={() => setHelpModalOpen(false)} />
      <div className="min-h-screen bg-gray-50 dark:bg-gray-950">
        {/* Header */}
        <header className="bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold text-gray-900 dark:text-white">
                  Sentiment Regime Detector
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
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
                  onClick={toggleTheme}
                  className="flex items-center gap-2 px-3 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                  aria-label={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
                >
                  {theme === 'dark' ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                </button>
                <button
                  type="button"
                  onClick={() => setHelpModalOpen(true)}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                  aria-label="Open help guide"
                >
                  <HelpCircle className="w-4 h-4" />
                  <span className="hidden sm:inline">Help</span>
                </button>
                <button
                  type="button"
                  onClick={() => fetchAllData({ manual: true })}
                  disabled={isRefreshing || loading}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                >
                  <RefreshCw className={`w-4 h-4 ${(isRefreshing || loading) ? 'animate-spin' : ''}`} />
                  Refresh
                </button>
              </div>
            </div>
            <div className="mt-3 flex flex-wrap items-center gap-3 text-xs text-gray-500 dark:text-gray-400">
              <span className={`inline-flex items-center gap-2 px-2.5 py-1 rounded-full border ${health.badge}`}>
                <span className={`h-2 w-2 rounded-full ${health.dot}`}></span>
                API {health.label}
              </span>
              <span>Last API success: {lastApiSuccess ? lastApiSuccess.toLocaleTimeString() : '—'}</span>
              <span>Sentiment: {lastSentimentSuccess ? lastSentimentSuccess.toLocaleTimeString() : '—'}</span>
              <span>Regime: {lastRegimeSuccess ? lastRegimeSuccess.toLocaleTimeString() : '—'}</span>
              <span>GARCH: {lastGarchSuccess ? lastGarchSuccess.toLocaleTimeString() : '—'}</span>
              <span>Last dashboard update: {lastUpdate.toLocaleTimeString()}</span>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
          <FadeIn delay={0}>
            <section>
              <div className="bg-amber-50 dark:bg-amber-950 border border-amber-200 dark:border-amber-800 rounded-lg px-4 py-3 text-xs text-amber-800 dark:text-amber-300">
                This dashboard is for educational and research insight only. It is not personal financial advice;
                consult a licensed financial professional before making investment decisions.
              </div>
            </section>
          </FadeIn>

          {/* Section 1: Regime & Market Stress */}
          <FadeIn delay={80}>
            <section>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-4 flex items-center gap-2">
                <span className="text-2xl">📊</span>
                Current Market Regime
              </h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                <RegimePanel regime={regime} />
                <CISSPanel
                  cissLevel={regime?.features?.ciss_level as number | undefined}
                  vixLevel={regime?.features?.vix_level as number | undefined}
                  latestDataDate={data?.latest_data_date}
                />
              </div>
              <CISSHistoryChart />
            </section>
          </FadeIn>

          {/* Section 2: Cross-Asset Sentiment */}
          <FadeIn delay={160}>
            <section>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-4 flex items-center gap-2">
                <span className="text-2xl">💭</span>
                Cross-Asset Sentiment Analysis
              </h2>
              <CrossAssetSummary data={data} />
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mt-6">
                {data.asset_classes
                  .sort((a, b) => a.asset_class.localeCompare(b.asset_class))
                  .map((sentiment) => (
                    <SentimentCard key={sentiment.asset_class} sentiment={sentiment} latestDataDate={data.latest_data_date} />
                  ))}
              </div>
              <div className="mt-6">
                <SentimentComparisonChart data={data.asset_classes} latestDataDate={data.latest_data_date} />
              </div>
              <div className="mt-6">
                <SentimentHistoryChart />
              </div>
            </section>
          </FadeIn>

          {/* Section 3: Volatility & Transitions */}
          <FadeIn delay={240}>
            <section>
              <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100 mb-4 flex items-center gap-2">
                <span className="text-2xl">📈</span>
                Volatility Modeling & Regime History
              </h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <GARCHResultsPanel
                  data={garch}
                  loading={loading && !garch}
                  error={garchError}
                  onRetry={() => fetchAllData({ manual: true })}
                />
                <RegimeTimeline />
              </div>
            </section>
          </FadeIn>

          {/* Footer Info */}
          <FadeIn delay={320}>
            <section className="mt-8">
              <div className="bg-gradient-to-r from-blue-50 to-indigo-50 dark:from-blue-950 dark:to-indigo-950 border border-blue-200 dark:border-blue-800 rounded-xl p-6">
                <div className="flex items-start gap-4">
                  <div className="text-blue-600 dark:text-blue-400 text-2xl">ℹ️</div>
                  <div className="flex-1">
                    <h3 className="text-base font-semibold text-blue-900 dark:text-blue-200 mb-2">
                      About This Dashboard
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm text-blue-800 dark:text-blue-300">
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
                          {' '}currently implemented as a GARCH(1,1)-based volatility layer; a{' '}
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
                      <div>
                        <p className="font-medium mb-1">How To Use This Signal</p>
                        <p className="text-xs">
                          Treat this as a research-grade market monitoring tool, not a stand-alone trade signal.
                          It is most useful for tracking broad shifts in market tone and stress across assets over time.
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
      <ChatbotWidget />
    </ErrorBoundary>
  )
}
