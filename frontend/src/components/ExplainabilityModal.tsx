'use client'

import { useEffect, useState } from 'react'
import { X, Lightbulb, RefreshCw, Download, Info, ChevronDown, ChevronUp } from 'lucide-react'
import { explainabilityApi } from '@/services/api'
import type { ExplanationResponse } from '@/types/explainability'
import ErrorMessage from './ErrorMessage'
import { getFeatureDisplayName, getFeatureDescription } from '@/utils/featureNames'
import Tooltip from './Tooltip'

interface ExplainabilityModalProps {
  isOpen: boolean
  onClose: () => void
  regime: 'risk_on' | 'risk_off' | 'transition'
  confidence: number
}

const regimeConfig = {
  risk_on: {
    label: 'Risk On',
    color: 'text-green-700 dark:text-green-300',
    bgColor: 'bg-green-50 dark:bg-green-950',
    description: 'Positive sentiment - risk appetite increasing',
  },
  risk_off: {
    label: 'Risk Off',
    color: 'text-red-700 dark:text-red-300',
    bgColor: 'bg-red-50 dark:bg-red-950',
    description: 'Negative sentiment - flight to safety',
  },
  transition: {
    label: 'Transition',
    color: 'text-purple-700 dark:text-purple-300',
    bgColor: 'bg-purple-50 dark:bg-purple-950',
    description: 'Regime change in progress',
  },
}

export default function ExplainabilityModal({
  isOpen,
  onClose,
  regime,
  confidence,
}: ExplainabilityModalProps) {
  const [explanation, setExplanation] = useState<ExplanationResponse | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [showInfo, setShowInfo] = useState(false)

  const handleExport = () => {
    if (!explanation) return

    // Create exportable data (exclude base64 image to keep size reasonable)
    const exportData = {
      timestamp: explanation.timestamp,
      predicted_regime: explanation.predicted_regime,
      confidence: explanation.confidence,
      model_version: explanation.model_version,
      base_value: explanation.base_value,
      prediction_value: explanation.prediction_value,
      top_features: explanation.top_features,
      all_features: explanation.all_features,
    }

    // Convert to JSON
    const jsonString = JSON.stringify(exportData, null, 2)
    const blob = new Blob([jsonString], { type: 'application/json' })
    const url = URL.createObjectURL(blob)

    // Download
    const link = document.createElement('a')
    link.href = url
    link.download = `shap-explanation-${regime}-${new Date().toISOString().split('T')[0]}.json`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    URL.revokeObjectURL(url)
  }

  useEffect(() => {
    if (!isOpen) return

    const fetchExplanation = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await explainabilityApi.getCurrentExplanation()
        setExplanation(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch explanation')
        console.error('Error fetching explanation:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchExplanation()
  }, [isOpen])

  if (!isOpen) return null

  const config = regimeConfig[regime]

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black bg-opacity-50 transition-opacity"
        onClick={onClose}
      />

      {/* Modal */}
      <div className="relative min-h-screen flex items-center justify-center p-2 sm:p-4">
        <div className="relative bg-white dark:bg-gray-900 rounded-xl sm:rounded-2xl shadow-2xl dark:shadow-gray-900/50 max-w-6xl w-full max-h-[95vh] sm:max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 to-indigo-600 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Lightbulb className="w-6 h-6 text-white" />
              <div>
                <h2 className="text-2xl font-bold text-white">Model Explainability</h2>
                <p className="text-blue-100 text-sm">
                  Understanding the {config.label} prediction
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label="Close explainability modal"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="p-4 sm:p-6 overflow-y-auto max-h-[calc(95vh-200px)] sm:max-h-[calc(90vh-180px)]">
            {loading ? (
              <div className="space-y-6 animate-pulse">
                {/* Regime Summary Skeleton */}
                <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-2"></div>
                      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-48"></div>
                    </div>
                    <div className="text-right">
                      <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded w-20 mb-1"></div>
                      <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-16 ml-auto"></div>
                    </div>
                  </div>
                </div>

                {/* Content Grid Skeleton */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Waterfall Plot Skeleton - 2/3 width */}
                  <div className="lg:col-span-2">
                    <div className="bg-gray-50 dark:bg-gray-950 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                      <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-48 mb-4"></div>
                      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full mb-4"></div>
                      <div className="h-96 bg-gradient-to-b from-gray-100 dark:from-gray-800 to-gray-50 dark:to-gray-950 rounded flex items-end justify-around px-4 pb-4">
                        {[...Array(10)].map((_, i) => (
                          <div
                            key={i}
                            className="bg-gray-200 dark:bg-gray-700 rounded-t"
                            style={{
                              width: '6%',
                              height: `${40 + Math.random() * 50}%`,
                            }}
                          />
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Features Table Skeleton - 1/3 width */}
                  <div className="lg:col-span-1">
                    <div className="bg-gray-50 dark:bg-gray-950 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                      <div className="h-6 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-4"></div>
                      <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-full mb-4"></div>
                      <div className="space-y-3">
                        {[...Array(10)].map((_, i) => (
                          <div key={i} className="bg-white dark:bg-gray-900 rounded-lg p-3 border border-gray-200 dark:border-gray-700">
                            <div className="flex items-center gap-2 mb-2">
                              <div className="w-5 h-5 bg-gray-200 dark:bg-gray-700 rounded-full"></div>
                              <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded flex-1"></div>
                            </div>
                            <div className="ml-7">
                              <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-20 mb-2"></div>
                              <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full"></div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Loading Indicator */}
                <div className="flex items-center justify-center gap-3 py-4">
                  <RefreshCw className="w-5 h-5 text-blue-600 animate-spin" />
                  <p className="text-gray-600 dark:text-gray-400 text-sm font-medium">
                    Computing SHAP explanations...
                  </p>
                </div>
              </div>
            ) : error ? (
              <ErrorMessage
                error={error}
                onRetry={() => window.location.reload()}
                variant="inline"
              />
            ) : explanation ? (
              <div className="space-y-6">
                {/* Regime Summary */}
                <div className={`p-4 rounded-lg ${config.bgColor}`}>
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className={`text-xl font-bold ${config.color}`}>
                        {config.label} Regime
                      </h3>
                      <p className={`text-sm ${config.color} opacity-80`}>
                        {config.description}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className={`text-3xl font-bold ${config.color}`}>
                        {(confidence * 100).toFixed(1)}%
                      </p>
                      <p className="text-xs text-gray-500 dark:text-gray-400">Confidence</p>
                    </div>
                  </div>
                </div>

                {/* What is SHAP? Info Banner */}
                <div className="bg-blue-50 dark:bg-blue-950 border border-blue-200 dark:border-blue-800 rounded-lg overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setShowInfo(!showInfo)}
                    className="w-full px-4 py-3 flex items-center justify-between hover:bg-blue-100 dark:hover:bg-blue-900 transition-colors"
                  >
                    <div className="flex items-center gap-2">
                      <Info className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                      <span className="font-medium text-blue-900 dark:text-blue-300 text-sm">
                        What is SHAP? How to read this explanation
                      </span>
                    </div>
                    {showInfo ? (
                      <ChevronUp className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    ) : (
                      <ChevronDown className="w-5 h-5 text-blue-600 dark:text-blue-400" />
                    )}
                  </button>

                  {showInfo && (
                    <div className="px-4 pb-4 text-sm text-gray-700 dark:text-gray-300 space-y-3 border-t border-blue-200 dark:border-blue-800 pt-3">
                      <p>
                        <strong className="text-blue-900 dark:text-blue-300">SHAP</strong> (SHapley Additive exPlanations) values explain how much each feature contributed to this prediction.
                      </p>
                      <ul className="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400 ml-2">
                        <li>
                          <strong className="text-green-700 dark:text-green-300">Positive SHAP values (green)</strong> push the prediction toward the displayed regime
                        </li>
                        <li>
                          <strong className="text-red-700 dark:text-red-300">Negative SHAP values (red)</strong> push the prediction away from the displayed regime
                        </li>
                        <li>
                          <strong>Larger absolute values</strong> = stronger influence on the prediction
                        </li>
                        <li>
                          The <strong>waterfall plot</strong> shows how the model starts from a base value and adds/subtracts each feature's contribution
                        </li>
                      </ul>
                      <p className="text-xs text-gray-500 dark:text-gray-400 italic border-t border-blue-100 dark:border-blue-800 pt-2 mt-3">
                        Tip: Hover over feature names to see detailed descriptions of what each indicator measures.
                      </p>
                    </div>
                  )}
                </div>

                {/* Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Waterfall Plot - 2/3 width on large screens */}
                  <div className="lg:col-span-2">
                    <div className="bg-gray-50 dark:bg-gray-950 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                      <div className="flex items-center gap-2 mb-4">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                          Feature Contribution Waterfall
                        </h4>
                        <Tooltip
                          content="SHAP waterfall plot showing how each feature pushes the model prediction from the base value toward the final prediction. Positive contributions (green) increase the prediction, negative contributions (red) decrease it."
                          side="right"
                        />
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        Shows how each feature pushes the model prediction from the base value toward the final prediction.
                      </p>

                      {explanation.waterfall_plot ? (
                        <div className="bg-white dark:bg-gray-900 rounded border border-gray-200 dark:border-gray-700 p-4">
                          <img
                            src={explanation.waterfall_plot}
                            alt="SHAP waterfall plot showing feature contributions to regime prediction"
                            className="w-full h-auto"
                          />
                        </div>
                      ) : (
                        <div className="h-96 flex flex-col items-center justify-center bg-white dark:bg-gray-900 rounded border border-gray-200 dark:border-gray-700 border-dashed p-8">
                          <svg
                            className="w-16 h-16 text-gray-300 dark:text-gray-600 mb-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={1.5}
                              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                            />
                          </svg>
                          <p className="text-gray-500 dark:text-gray-400 font-medium mb-2">
                            Waterfall plot not available
                          </p>
                          <p className="text-gray-400 dark:text-gray-500 text-sm text-center max-w-sm">
                            The visualization is being generated. See the features table for
                            detailed SHAP values.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Top Features Table - 1/3 width on large screens */}
                  <div className="lg:col-span-1">
                    <div className="bg-gray-50 dark:bg-gray-950 border border-gray-200 dark:border-gray-700 rounded-lg p-6">
                      <div className="flex items-center gap-2 mb-4">
                        <h4 className="text-lg font-semibold text-gray-900 dark:text-white">
                          Top Features
                        </h4>
                        <Tooltip
                          content="Features ranked by absolute SHAP value impact. Green bars indicate features pushing toward the predicted regime, red bars indicate features pushing away from it."
                          side="right"
                        />
                      </div>
                      <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                        Features ranked by impact on the model's prediction
                      </p>

                      <div className="space-y-3">
                        {explanation.top_features.map((feature) => {
                          const isPositive = feature.shap_value >= 0
                          const maxAbsShap = Math.max(
                            ...explanation.top_features.map((f) => Math.abs(f.shap_value))
                          )
                          const barWidth = (Math.abs(feature.shap_value) / maxAbsShap) * 100

                          return (
                            <div
                              key={feature.feature_name}
                              className="bg-white dark:bg-gray-900 rounded-lg p-3 border border-gray-200 dark:border-gray-700"
                            >
                              {/* Feature Header */}
                              <div className="flex items-start justify-between mb-2">
                                <div className="flex-1 min-w-0">
                                  <div className="flex items-center gap-2">
                                    <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-400 text-xs font-medium flex-shrink-0">
                                      {feature.rank}
                                    </span>
                                    <div className="flex-1 min-w-0">
                                      <div className="flex items-center gap-1.5">
                                        <p className="text-sm font-medium text-gray-900 dark:text-white truncate">
                                          {getFeatureDisplayName(feature.feature_name)}
                                        </p>
                                        <Tooltip
                                          content={getFeatureDescription(feature.feature_name)}
                                          side="right"
                                        />
                                      </div>
                                      <p className="text-xs text-gray-400 dark:text-gray-500 truncate">
                                        {feature.feature_name}
                                      </p>
                                    </div>
                                  </div>
                                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1 ml-7">
                                    Value: {feature.value.toFixed(4)}
                                  </p>
                                </div>
                              </div>

                              {/* SHAP Value Bar */}
                              <div className="ml-7">
                                <div className="flex items-center gap-2 mb-1">
                                  <span
                                    className={`text-xs font-semibold ${
                                      isPositive ? 'text-green-700 dark:text-green-300' : 'text-red-700 dark:text-red-300'
                                    }`}
                                  >
                                    {isPositive ? '+' : ''}
                                    {feature.shap_value.toFixed(4)}
                                  </span>
                                  <span className="text-xs text-gray-400 dark:text-gray-500">SHAP</span>
                                  <Tooltip
                                    content={`SHAP value represents how much this feature contributes to the prediction. ${isPositive ? 'Positive values push toward the predicted regime.' : 'Negative values push away from the predicted regime.'}`}
                                    side="right"
                                  />
                                </div>
                                <div className="h-2 bg-gray-100 dark:bg-gray-800 rounded-full overflow-hidden">
                                  <div
                                    className={`h-full ${
                                      isPositive ? 'bg-green-500' : 'bg-red-500'
                                    }`}
                                    style={{ width: `${barWidth}%` }}
                                  />
                                </div>
                              </div>
                            </div>
                          )
                        })}
                      </div>

                      {explanation.all_features.length > explanation.top_features.length && (
                        <div className="mt-4 text-center">
                          <p className="text-xs text-gray-500 dark:text-gray-400">
                            Showing top {explanation.top_features.length} of{' '}
                            {explanation.all_features.length} features
                          </p>
                        </div>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            ) : null}
          </div>

          {/* Footer */}
          <div className="border-t border-gray-200 dark:border-gray-700 px-4 sm:px-6 py-3 sm:py-4 bg-gray-50 dark:bg-gray-950 flex flex-col sm:flex-row justify-between items-center gap-3">
            <div className="text-xs sm:text-sm text-gray-600 dark:text-gray-400 text-center sm:text-left">
              {explanation && (
                <>
                  Model: {explanation.model_version} •
                  {explanation.cache_hit ? ' Cached' : ' Fresh'} •
                  {new Date(explanation.timestamp).toLocaleString()}
                </>
              )}
            </div>
            <div className="flex items-center gap-3">
              {explanation && (
                <button
                  type="button"
                  onClick={handleExport}
                  className="flex items-center gap-2 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700 transition-colors font-medium text-sm"
                >
                  <Download className="w-4 h-4" />
                  Export JSON
                </button>
              )}
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium text-sm"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
