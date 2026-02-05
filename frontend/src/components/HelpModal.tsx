'use client'

import { useState } from 'react'
import { X, HelpCircle, BookOpen, BarChart3, Activity, TrendingUp } from 'lucide-react'

interface HelpModalProps {
  isOpen: boolean
  onClose: () => void
}

export default function HelpModal({ isOpen, onClose }: HelpModalProps) {
  const [activeTab, setActiveTab] = useState<'overview' | 'terms' | 'interpret' | 'faq'>('overview')

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative min-h-screen flex items-center justify-center p-2 sm:p-4">
        <div className="relative bg-white rounded-xl sm:rounded-2xl shadow-2xl max-w-4xl w-full max-h-[95vh] sm:max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <HelpCircle className="w-6 h-6 text-white" />
              <h2 className="text-2xl font-bold text-white">Dashboard Guide</h2>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label="Close help modal"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Tabs */}
          <div className="border-b border-gray-200 bg-gray-50 px-3 sm:px-6 overflow-x-auto">
            <nav className="flex gap-3 sm:gap-6 min-w-max" aria-label="Help sections">
              <button
                type="button"
                onClick={() => setActiveTab('overview')}
                className={`py-3 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'overview'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <BookOpen className="w-4 h-4 inline mr-2" />
                Overview
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('terms')}
                className={`py-3 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'terms'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <Activity className="w-4 h-4 inline mr-2" />
                Key Terms
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('interpret')}
                className={`py-3 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'interpret'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <BarChart3 className="w-4 h-4 inline mr-2" />
                How to Read
              </button>
              <button
                type="button"
                onClick={() => setActiveTab('faq')}
                className={`py-3 px-2 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === 'faq'
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <TrendingUp className="w-4 h-4 inline mr-2" />
                FAQ
              </button>
            </nav>
          </div>

          {/* Content */}
          <div className="p-4 sm:p-6 overflow-y-auto max-h-[calc(95vh-200px)] sm:max-h-[calc(90vh-180px)]">
            {activeTab === 'overview' && (
              <div className="space-y-6">
                <div>
                  <h3 className="text-xl font-semibold text-gray-900 mb-3">What This Dashboard Does</h3>
                  <p className="text-gray-700 leading-relaxed">
                    The Sentiment Regime Detector analyzes cross-asset market sentiment in real-time to identify
                    market regimes (Risk-On, Risk-Off, or Transition). It combines sentiment analysis from 2.66M+ texts,
                    systemic stress indicators, and volatility modeling to provide comprehensive market insights.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
                    <h4 className="font-semibold text-blue-900 mb-2">🎯 Sentiment Analysis</h4>
                    <p className="text-sm text-blue-800">
                      Uses DistilBERT NLP models to analyze sentiment across equity, crypto, forex, and commodity markets.
                      Scores from -1 (bearish) to +1 (bullish).
                    </p>
                  </div>
                  <div className="p-4 bg-purple-50 rounded-lg border border-purple-200">
                    <h4 className="font-semibold text-purple-900 mb-2">🔮 Regime Detection</h4>
                    <p className="text-sm text-purple-800">
                      ML classifier (99.45% accuracy) identifies Risk-On, Risk-Off, and Transition regimes using
                      sentiment, CISS, and VIX features.
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg border border-green-200">
                    <h4 className="font-semibold text-green-900 mb-2">📊 Volatility Modeling</h4>
                    <p className="text-sm text-green-800">
                      GARCH(1,1) models forecast market volatility with high persistence (α+β=0.955),
                      combining recent shocks with historical patterns.
                    </p>
                  </div>
                  <div className="p-4 bg-amber-50 rounded-lg border border-amber-200">
                    <h4 className="font-semibold text-amber-900 mb-2">🌐 Systemic Stress</h4>
                    <p className="text-sm text-amber-800">
                      Tracks ECB CISS and CBOE VIX to measure financial system stress and market fear levels
                      in real-time.
                    </p>
                  </div>
                </div>

                <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <h4 className="font-semibold text-gray-900 mb-2">🔄 Auto-Refresh</h4>
                  <p className="text-sm text-gray-700">
                    Data refreshes automatically every 60 seconds. The regime panel updates every 30 seconds.
                    You can also manually refresh using the button in the header.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'terms' && (
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Glossary of Technical Terms</h3>

                <div className="space-y-3">
                  <TermDefinition
                    term="CISS (Composite Indicator of Systemic Stress)"
                    definition="A measure from the European Central Bank that aggregates stress across money, bond, equity, and FX markets. Values range from 0 (calm) to 1 (extreme stress). Above 0.5 indicates crisis conditions."
                  />
                  <TermDefinition
                    term="VIX (Volatility Index)"
                    definition="The 'fear gauge' measuring expected 30-day volatility of the S&P 500 based on option prices. <15 is calm, 15-20 is normal, 20-30 is elevated, >30 is high volatility."
                  />
                  <TermDefinition
                    term="GARCH(1,1)"
                    definition="Generalized Autoregressive Conditional Heteroskedasticity - a model that predicts volatility using recent shocks (ARCH) and historical volatility. The (1,1) means one lag for each component."
                  />
                  <TermDefinition
                    term="α (Alpha) - ARCH Parameter"
                    definition="Measures the impact of recent market shocks on current volatility. Higher α means markets react more strongly to new information."
                  />
                  <TermDefinition
                    term="β (Beta) - GARCH Parameter"
                    definition="Measures volatility memory - how much past volatility predicts future volatility. Higher β means volatility patterns persist longer."
                  />
                  <TermDefinition
                    term="Persistence (α + β)"
                    definition="Sum of α and β. Values near 1.0 mean volatility shocks decay very slowly. Values >0.95 suggest nearly permanent impact."
                  />
                  <TermDefinition
                    term="DistilBERT"
                    definition="A distilled transformer model for NLP. 40% smaller and 60% faster than BERT while retaining 97% of language understanding capability."
                  />
                  <TermDefinition
                    term="Risk-On Regime"
                    definition="Bullish market environment where investors seek higher returns, sentiment is positive, and stress indicators are low."
                  />
                  <TermDefinition
                    term="Risk-Off Regime"
                    definition="Bearish market environment characterized by flight to safety, negative sentiment, and elevated stress indicators."
                  />
                  <TermDefinition
                    term="Transition Regime"
                    definition="Uncertain period where markets are shifting between Risk-On and Risk-Off states. Mixed signals across indicators."
                  />
                  <TermDefinition
                    term="AIC / BIC"
                    definition="Akaike/Bayesian Information Criterion - measures model quality. Lower values indicate better fit while penalizing complexity."
                  />
                </div>
              </div>
            )}

            {activeTab === 'interpret' && (
              <div className="space-y-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">How to Interpret the Dashboard</h3>

                <div className="space-y-4">
                  <InterpretSection
                    title="📊 Current Market Regime"
                    items={[
                      'Check the regime classification (Risk-On, Risk-Off, or Transition)',
                      'High confidence (>80%) suggests clear market conditions',
                      'Look at probabilities - mixed values indicate transitional periods',
                      'Green = bullish conditions, Red = bearish conditions, Purple = uncertainty'
                    ]}
                  />

                  <InterpretSection
                    title="⚠️ Systemic Stress Indicators"
                    items={[
                      'CISS >0.5 indicates crisis-level systemic stress',
                      'VIX >30 suggests high market fear and expected volatility',
                      'Both indicators together provide confirmation of stress levels',
                      'Historical correlation: CISS and VIX were 0.92 correlated during COVID-19'
                    ]}
                  />

                  <InterpretSection
                    title="💭 Cross-Asset Sentiment"
                    items={[
                      'Scores range from -1 (very bearish) to +1 (very bullish)',
                      'Compare sentiment across asset classes for divergence/convergence',
                      'Text count shows data recency and volume',
                      'Look for sentiment-stress mismatches (positive sentiment + high stress = caution)'
                    ]}
                  />

                  <InterpretSection
                    title="📈 GARCH Volatility"
                    items={[
                      'High persistence (>0.95) means current volatility predicts future volatility',
                      'High α suggests markets are reactive to new information',
                      'High β suggests volatility patterns persist over time',
                      'Use 30-day forecast statistics for risk management'
                    ]}
                  />
                </div>

                <div className="p-4 bg-yellow-50 border border-yellow-200 rounded-lg">
                  <h4 className="font-semibold text-yellow-900 mb-2">⚡ Key Insight</h4>
                  <p className="text-sm text-yellow-800">
                    The most reliable signals occur when <strong>all indicators align</strong>: sentiment, regime
                    classification, CISS/VIX levels, and volatility forecasts all pointing in the same direction.
                    Divergences signal uncertainty or transition periods.
                  </p>
                </div>
              </div>
            )}

            {activeTab === 'faq' && (
              <div className="space-y-4">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">Frequently Asked Questions</h3>

                <FAQItem
                  question="How often is the data updated?"
                  answer="Sentiment data and regime classifications refresh every 60 seconds. CISS and VIX data update based on market hours (real-time during trading sessions)."
                />
                <FAQItem
                  question="What data sources are used?"
                  answer="The system analyzes 2.66M+ texts from 21 Kaggle datasets, including Reddit posts, financial news, social media, and market commentary across multiple asset classes."
                />
                <FAQItem
                  question="How accurate is the regime classifier?"
                  answer="The ML classifier achieved 99.45% accuracy on test data, validated across multiple market crises including the 2008 Financial Crisis, COVID-19 crash, and recent market events."
                />
                <FAQItem
                  question="Can I use this for trading decisions?"
                  answer="This dashboard is for educational and research purposes. While it provides valuable market insights, it should not be the sole basis for investment decisions. Always consult with financial advisors."
                />
                <FAQItem
                  question="What do the sentiment scores mean?"
                  answer="Sentiment scores from -1 to +1 represent the overall market mood: -1 is extremely bearish, 0 is neutral, +1 is extremely bullish. Scores are aggregated across thousands of texts using NLP."
                />
                <FAQItem
                  question="Why might indicators disagree?"
                  answer="Disagreements (e.g., positive sentiment but high VIX) often signal transition periods or market uncertainty. These mixed signals can precede regime changes and warrant caution."
                />
                <FAQItem
                  question="What makes GARCH persistence important?"
                  answer="High persistence (α+β near 1.0) means volatility shocks last longer. This helps predict whether market turbulence will be short-lived or prolonged."
                />
                <FAQItem
                  question="How was this system validated?"
                  answer="Extensive backtesting across major market events: 2008 Financial Crisis, 2020 COVID-19 crash, 2022 crypto winter, and recent market volatility. See the research paper for detailed results."
                />
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="border-t border-gray-200 px-4 sm:px-6 py-3 sm:py-4 bg-gray-50 flex flex-col sm:flex-row justify-between items-center gap-3">
            <p className="text-xs sm:text-sm text-gray-600 text-center sm:text-left">
              SMU DS-6210 Capstone Project • Built with Next.js, FastAPI, and DistilBERT
            </p>
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Got it!
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

// Helper components
function TermDefinition({ term, definition }: { term: string; definition: string }) {
  return (
    <div className="p-3 bg-white border border-gray-200 rounded-lg">
      <h4 className="font-semibold text-gray-900 text-sm mb-1">{term}</h4>
      <p className="text-sm text-gray-600">{definition}</p>
    </div>
  )
}

function InterpretSection({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="p-4 bg-white border border-gray-200 rounded-lg">
      <h4 className="font-semibold text-gray-900 mb-2">{title}</h4>
      <ul className="space-y-2">
        {items.map((item, idx) => (
          <li key={idx} className="text-sm text-gray-700 flex items-start">
            <span className="text-blue-600 mr-2">•</span>
            <span>{item}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}

function FAQItem({ question, answer }: { question: string; answer: string }) {
  return (
    <div className="p-4 bg-white border border-gray-200 rounded-lg">
      <h4 className="font-semibold text-gray-900 mb-2">{question}</h4>
      <p className="text-sm text-gray-700">{answer}</p>
    </div>
  )
}
