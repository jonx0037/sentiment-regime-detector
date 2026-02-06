'use client'

import { useEffect, useState } from 'react'
import { X, Lightbulb, RefreshCw } from 'lucide-react'
import { explainabilityApi } from '@/services/api'
import type { ExplanationResponse } from '@/types/explainability'
import ErrorMessage from './ErrorMessage'

interface ExplainabilityModalProps {
  isOpen: boolean
  onClose: () => void
  regime: 'risk_on' | 'risk_off' | 'transition'
  confidence: number
}

const regimeConfig = {
  risk_on: {
    label: 'Risk On',
    color: 'text-green-700',
    bgColor: 'bg-green-50',
    description: 'Positive sentiment - risk appetite increasing',
  },
  risk_off: {
    label: 'Risk Off',
    color: 'text-red-700',
    bgColor: 'bg-red-50',
    description: 'Negative sentiment - flight to safety',
  },
  transition: {
    label: 'Transition',
    color: 'text-purple-700',
    bgColor: 'bg-purple-50',
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
        <div className="relative bg-white rounded-xl sm:rounded-2xl shadow-2xl max-w-6xl w-full max-h-[95vh] sm:max-h-[90vh] overflow-hidden">
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
              <div className="flex flex-col items-center justify-center py-12">
                <RefreshCw className="w-12 h-12 text-blue-600 animate-spin mb-4" />
                <p className="text-gray-600 text-lg font-medium">
                  Computing SHAP explanations...
                </p>
                <p className="text-gray-400 text-sm mt-2">
                  Analyzing feature contributions
                </p>
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
                      <p className="text-xs text-gray-500">Confidence</p>
                    </div>
                  </div>
                </div>

                {/* Content Grid */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Waterfall Plot - 2/3 width on large screens */}
                  <div className="lg:col-span-2">
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                      <h4 className="text-lg font-semibold text-gray-900 mb-4">
                        Feature Contribution Waterfall
                      </h4>
                      <p className="text-sm text-gray-600 mb-4">
                        SHAP waterfall plot showing how each feature pushes the model prediction
                        from the base value toward the final prediction.
                      </p>

                      {explanation.waterfall_plot ? (
                        <div className="bg-white rounded border border-gray-200 p-4">
                          <img
                            src={explanation.waterfall_plot}
                            alt="SHAP waterfall plot showing feature contributions to regime prediction"
                            className="w-full h-auto"
                          />
                        </div>
                      ) : (
                        <div className="h-96 flex flex-col items-center justify-center bg-white rounded border border-gray-200 border-dashed p-8">
                          <svg
                            className="w-16 h-16 text-gray-300 mb-4"
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
                          <p className="text-gray-500 font-medium mb-2">
                            Waterfall plot not available
                          </p>
                          <p className="text-gray-400 text-sm text-center max-w-sm">
                            The visualization is being generated. See the features table for
                            detailed SHAP values.
                          </p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Top Features Table - 1/3 width on large screens */}
                  <div className="lg:col-span-1">
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                      <h4 className="text-lg font-semibold text-gray-900 mb-4">
                        Top Features
                      </h4>
                      {/* Placeholder for features table */}
                      <div className="space-y-2">
                        <p className="text-gray-400 text-sm">Features table will be displayed here</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : null}
          </div>

          {/* Footer */}
          <div className="border-t border-gray-200 px-4 sm:px-6 py-3 sm:py-4 bg-gray-50 flex flex-col sm:flex-row justify-between items-center gap-3">
            <div className="text-xs sm:text-sm text-gray-600 text-center sm:text-left">
              {explanation && (
                <>
                  Model: {explanation.model_version} •
                  {explanation.cache_hit ? ' Cached' : ' Fresh'} •
                  {new Date(explanation.timestamp).toLocaleString()}
                </>
              )}
            </div>
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors font-medium"
            >
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
