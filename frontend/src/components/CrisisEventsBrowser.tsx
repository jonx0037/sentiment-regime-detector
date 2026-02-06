'use client'

import { useEffect, useState } from 'react'
import { X, Calendar, TrendingUp, Activity, ChevronRight, BookOpen } from 'lucide-react'
import { explainabilityApi } from '@/services/api'
import type { CrisisEvent, EventDetailResponse } from '@/types/explainability'
import ErrorMessage from './ErrorMessage'
import LoadingSkeleton from './LoadingSkeleton'
import { getFeatureDisplayName } from '@/utils/featureNames'
import Tooltip from './Tooltip'

interface CrisisEventsBrowserProps {
  isOpen: boolean
  onClose: () => void
}

const regimeConfig = {
  risk_on: {
    label: 'Risk On',
    color: 'text-green-700',
    bgColor: 'bg-green-50',
    borderColor: 'border-green-200',
  },
  risk_off: {
    label: 'Risk Off',
    color: 'text-red-700',
    bgColor: 'bg-red-50',
    borderColor: 'border-red-200',
  },
  transition: {
    label: 'Transition',
    color: 'text-purple-700',
    bgColor: 'bg-purple-50',
    borderColor: 'border-purple-200',
  },
}

export default function CrisisEventsBrowser({ isOpen, onClose }: CrisisEventsBrowserProps) {
  const [events, setEvents] = useState<CrisisEvent[]>([])
  const [selectedEvent, setSelectedEvent] = useState<EventDetailResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [loadingEventId, setLoadingEventId] = useState<string | null>(null)

  useEffect(() => {
    if (!isOpen) return

    const fetchEvents = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await explainabilityApi.getEventsList()
        setEvents(data)
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to fetch crisis events')
        console.error('Error fetching crisis events:', err)
      } finally {
        setLoading(false)
      }
    }

    fetchEvents()
  }, [isOpen])

  const handleEventClick = async (eventId: string) => {
    try {
      setLoadingEventId(eventId)
      setError(null)
      const data = await explainabilityApi.getEventExplanation(eventId)
      setSelectedEvent(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to fetch event details')
      console.error('Error fetching event details:', err)
    } finally {
      setLoadingEventId(null)
    }
  }

  const handleBackToList = () => {
    setSelectedEvent(null)
  }

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
        <div className="relative bg-white rounded-xl sm:rounded-2xl shadow-2xl max-w-6xl w-full max-h-[95vh] sm:max-h-[90vh] overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <BookOpen className="w-6 h-6 text-white" />
              <div>
                <h2 className="text-2xl font-bold text-white">
                  {selectedEvent ? selectedEvent.event.name : 'Crisis Events Browser'}
                </h2>
                <p className="text-indigo-100 text-sm">
                  {selectedEvent
                    ? 'SHAP explanation for historical event'
                    : 'Explore model predictions during historical market crises'}
                </p>
              </div>
            </div>
            <button
              onClick={selectedEvent ? handleBackToList : onClose}
              className="text-white hover:text-gray-200 transition-colors"
              aria-label={selectedEvent ? 'Back to list' : 'Close browser'}
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Content */}
          <div className="p-4 sm:p-6 overflow-y-auto max-h-[calc(95vh-200px)] sm:max-h-[calc(90vh-180px)]">
            {loading ? (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[...Array(6)].map((_, i) => (
                  <LoadingSkeleton key={i} variant="card" />
                ))}
              </div>
            ) : error ? (
              <ErrorMessage
                error={error}
                onRetry={() => window.location.reload()}
                variant="inline"
              />
            ) : selectedEvent ? (
              // Event Detail View
              <div className="space-y-6">
                {/* Event Header */}
                <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg p-6 border border-indigo-200">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex-1">
                      <h3 className="text-2xl font-bold text-gray-900 mb-2">
                        {selectedEvent.event.name}
                      </h3>
                      <p className="text-gray-700 leading-relaxed mb-3">
                        {selectedEvent.event.description}
                      </p>
                      <div className="flex items-center gap-2 text-sm text-gray-600">
                        <Calendar className="w-4 h-4" />
                        <span className="font-medium">
                          {new Date(selectedEvent.event.date).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'long',
                            day: 'numeric',
                          })}
                        </span>
                      </div>
                    </div>
                    <div
                      className={`px-4 py-2 rounded-lg ${
                        regimeConfig[selectedEvent.explanation.predicted_regime].bgColor
                      } ${regimeConfig[selectedEvent.explanation.predicted_regime].borderColor} border-2`}
                    >
                      <p
                        className={`text-sm font-semibold ${
                          regimeConfig[selectedEvent.explanation.predicted_regime].color
                        }`}
                      >
                        {regimeConfig[selectedEvent.explanation.predicted_regime].label}
                      </p>
                      <p className="text-xs text-gray-500 text-center">
                        {(selectedEvent.explanation.confidence * 100).toFixed(1)}% confidence
                      </p>
                    </div>
                  </div>

                  {/* Crisis Metrics */}
                  <div className="grid grid-cols-2 gap-4">
                    <div className="bg-white rounded-lg p-4 border border-gray-200">
                      <div className="flex items-center gap-2 mb-2">
                        <TrendingUp className="w-5 h-5 text-red-600" />
                        <span className="text-sm font-medium text-gray-700">CISS Peak</span>
                        <Tooltip content="Composite Indicator of Systemic Stress at peak of crisis" />
                      </div>
                      <p className="text-2xl font-bold text-red-700">
                        {selectedEvent.event.ciss_peak.toFixed(3)}
                      </p>
                    </div>
                    <div className="bg-white rounded-lg p-4 border border-gray-200">
                      <div className="flex items-center gap-2 mb-2">
                        <Activity className="w-5 h-5 text-amber-600" />
                        <span className="text-sm font-medium text-gray-700">VIX Peak</span>
                        <Tooltip content="CBOE Volatility Index (fear gauge) at peak of crisis" />
                      </div>
                      <p className="text-2xl font-bold text-amber-700">
                        {selectedEvent.event.vix_peak.toFixed(2)}
                      </p>
                    </div>
                  </div>
                </div>

                {/* SHAP Explanation */}
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Waterfall Plot - 2/3 width */}
                  <div className="lg:col-span-2">
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                      <h4 className="text-lg font-semibold text-gray-900 mb-4">
                        Feature Contribution Waterfall
                      </h4>
                      {selectedEvent.explanation.waterfall_plot ? (
                        <div className="bg-white rounded border border-gray-200 p-4">
                          <img
                            src={selectedEvent.explanation.waterfall_plot}
                            alt="SHAP waterfall plot"
                            className="w-full h-auto"
                          />
                        </div>
                      ) : (
                        <div className="h-64 flex items-center justify-center bg-white rounded border border-gray-200 border-dashed">
                          <p className="text-gray-400">Waterfall plot not available</p>
                        </div>
                      )}
                    </div>
                  </div>

                  {/* Top Features - 1/3 width */}
                  <div className="lg:col-span-1">
                    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6">
                      <h4 className="text-lg font-semibold text-gray-900 mb-4">Top Features</h4>
                      <div className="space-y-3">
                        {selectedEvent.explanation.top_features.slice(0, 5).map((feature) => {
                          const isPositive = feature.shap_value >= 0
                          return (
                            <div
                              key={feature.feature_name}
                              className="bg-white rounded-lg p-3 border border-gray-200"
                            >
                              <div className="flex items-center gap-2 mb-1">
                                <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-gray-100 text-gray-600 text-xs font-medium">
                                  {feature.rank}
                                </span>
                                <p className="text-sm font-medium text-gray-900 truncate flex-1">
                                  {getFeatureDisplayName(feature.feature_name)}
                                </p>
                              </div>
                              <div className="ml-7">
                                <span
                                  className={`text-xs font-semibold ${
                                    isPositive ? 'text-green-700' : 'text-red-700'
                                  }`}
                                >
                                  {isPositive ? '+' : ''}
                                  {feature.shap_value.toFixed(4)}
                                </span>
                                <div className="h-2 bg-gray-100 rounded-full overflow-hidden mt-1">
                                  <div
                                    className={`h-full ${
                                      isPositive ? 'bg-green-500' : 'bg-red-500'
                                    }`}
                                    style={{
                                      width: `${
                                        (Math.abs(feature.shap_value) /
                                          Math.max(
                                            ...selectedEvent.explanation.top_features.map((f) =>
                                              Math.abs(f.shap_value)
                                            )
                                          )) *
                                        100
                                      }%`,
                                    }}
                                  />
                                </div>
                              </div>
                            </div>
                          )
                        })}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              // Events List View
              <div>
                <p className="text-gray-600 mb-6">
                  Select a historical crisis event to see how the model predicted regime during
                  that period using SHAP explainability.
                </p>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {events.map((event) => (
                    <button
                      key={event.event_id}
                      onClick={() => handleEventClick(event.event_id)}
                      disabled={loadingEventId === event.event_id}
                      className="text-left p-6 bg-white border border-gray-200 rounded-xl hover:border-indigo-300 hover:shadow-md transition-all disabled:opacity-50 disabled:cursor-not-allowed group"
                    >
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="text-lg font-bold text-gray-900 mb-2 group-hover:text-indigo-600 transition-colors">
                            {event.name}
                          </h3>
                          <div className="flex items-center gap-2 text-sm text-gray-500 mb-3">
                            <Calendar className="w-4 h-4" />
                            <span>
                              {new Date(event.date).toLocaleDateString('en-US', {
                                year: 'numeric',
                                month: 'short',
                                day: 'numeric',
                              })}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 leading-relaxed mb-4">
                            {event.description}
                          </p>
                        </div>
                        <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-indigo-600 transition-colors flex-shrink-0 ml-2" />
                      </div>

                      <div className="flex items-center gap-4 text-sm">
                        <div className="flex items-center gap-1.5">
                          <span className="text-gray-500">CISS:</span>
                          <span className="font-semibold text-red-700">
                            {event.ciss_peak.toFixed(3)}
                          </span>
                        </div>
                        <div className="flex items-center gap-1.5">
                          <span className="text-gray-500">VIX:</span>
                          <span className="font-semibold text-amber-700">
                            {event.vix_peak.toFixed(2)}
                          </span>
                        </div>
                      </div>

                      {loadingEventId === event.event_id && (
                        <div className="mt-3 flex items-center gap-2 text-sm text-indigo-600">
                          <LoadingSkeleton variant="inline" message="Loading explanation..." />
                        </div>
                      )}
                    </button>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="border-t border-gray-200 px-4 sm:px-6 py-3 sm:py-4 bg-gray-50 flex justify-end">
            <button
              type="button"
              onClick={selectedEvent ? handleBackToList : onClose}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors font-medium"
            >
              {selectedEvent ? 'Back to Events' : 'Close'}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
