/**
 * Export Menu Component
 *
 * Global dropdown menu for exporting all dashboard data, charts, and reports.
 * Provides comprehensive export options including PDF reports and shareable URLs.
 */

'use client'

import { useState, useRef, useEffect } from 'react'
import {
  Download,
  FileText,
  FileJson,
  FileImage,
  Share2,
  ChevronDown,
  Loader2,
} from 'lucide-react'
import type { SentimentResponse, RegimeResponse } from '@/types/api'
import {
  exportSentimentAsCSV,
  exportSentimentAsJSON,
  exportRegimeAsCSV,
  exportRegimeAsJSON,
  exportGARCHAsCSV,
  exportGARCHAsJSON,
  exportAllDataAsJSON,
} from '@/utils/exportData'
import { exportAllChartsAsPNG, exportAllChartsAsSVG } from '@/utils/exportChart'
import { generatePDFReport } from '@/utils/exportPDF'
import { copyShareableURL } from '@/utils/shareURL'

export interface ExportMenuProps {
  sentiment: SentimentResponse | null
  regime: RegimeResponse | null
  garch: any | null
  onToast: (message: string, type: 'success' | 'error' | 'info') => void
}

export default function ExportMenu({
  sentiment,
  regime,
  garch,
  onToast,
}: ExportMenuProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [isExporting, setIsExporting] = useState(false)
  const [exportProgress, setExportProgress] = useState<string>('')
  const dropdownRef = useRef<HTMLDivElement>(null)

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false)
      }
    }

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside)
    }

    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [isOpen])

  const handleExport = async (
    exportFn: () => void | Promise<void>,
    successMessage: string
  ) => {
    try {
      setIsExporting(true)
      setExportProgress('')
      await exportFn()
      onToast(successMessage, 'success')
      setIsOpen(false)
    } catch (error) {
      console.error('Export failed:', error)
      onToast('Export failed. Please try again.', 'error')
    } finally {
      setIsExporting(false)
      setExportProgress('')
    }
  }

  const handleExportAllCharts = async (format: 'PNG' | 'SVG') => {
    const charts = [
      { elementId: 'sentiment-comparison-chart', filename: 'sentiment-comparison' },
      { elementId: 'ciss-history-chart', filename: 'ciss-history' },
      { elementId: 'sentiment-history-chart', filename: 'sentiment-history' },
      { elementId: 'regime-timeline-chart', filename: 'regime-timeline' },
    ]

    if (format === 'PNG') {
      await exportAllChartsAsPNG(charts)
    } else {
      exportAllChartsAsSVG(charts)
    }
  }

  const handleGeneratePDF = async () => {
    try {
      setIsExporting(true)
      await generatePDFReport(sentiment, regime, (message) => {
        setExportProgress(message)
      })
      onToast('PDF report generated successfully!', 'success')
      setIsOpen(false)
    } catch (error) {
      console.error('PDF generation failed:', error)
      onToast('PDF generation failed. Please try again.', 'error')
    } finally {
      setIsExporting(false)
      setExportProgress('')
    }
  }

  const handleShareURL = async () => {
    try {
      await copyShareableURL()
      onToast('Link copied to clipboard!', 'success')
      setIsOpen(false)
    } catch (error) {
      console.error('Failed to copy URL:', error)
      onToast('Failed to copy link. Please try again.', 'error')
    }
  }

  return (
    <div className="relative" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        disabled={isExporting}
        className="
          flex items-center gap-2 px-4 py-2
          bg-white border border-gray-300 rounded-lg
          hover:bg-gray-50 hover:border-gray-400
          disabled:opacity-50 disabled:cursor-not-allowed
          transition-colors
        "
        aria-label="Export menu"
        aria-expanded={isOpen}
        aria-haspopup="true"
      >
        {isExporting ? (
          <Loader2 className="w-4 h-4 animate-spin" />
        ) : (
          <Download className="w-4 h-4" />
        )}
        <span className="hidden sm:inline">Export</span>
        <ChevronDown className={`w-4 h-4 transition-transform ${isOpen ? 'rotate-180' : ''}`} />
      </button>

      {isOpen && (
        <div
          className="
            absolute right-0 mt-2 w-64
            bg-white border border-gray-200 rounded-lg shadow-lg
            z-10
            animate-in fade-in slide-in-from-top-2 duration-200
          "
          role="menu"
        >
          {/* Charts Section */}
          <div className="p-2 border-b border-gray-100">
            <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wide">
              Charts
            </div>
            <button
              onClick={() =>
                handleExport(
                  () => handleExportAllCharts('PNG'),
                  'All charts exported as PNG'
                )
              }
              disabled={isExporting}
              className="menu-item"
              role="menuitem"
            >
              <FileImage className="w-4 h-4 text-gray-600" />
              <span>Export All Charts (PNG)</span>
            </button>
            <button
              onClick={() =>
                handleExport(
                  () => handleExportAllCharts('SVG'),
                  'All charts exported as SVG'
                )
              }
              disabled={isExporting}
              className="menu-item"
              role="menuitem"
            >
              <FileImage className="w-4 h-4 text-gray-600" />
              <span>Export All Charts (SVG)</span>
            </button>
          </div>

          {/* Data Section */}
          <div className="p-2 border-b border-gray-100">
            <div className="px-2 py-1 text-xs font-semibold text-gray-500 uppercase tracking-wide">
              Data
            </div>
            <button
              onClick={() =>
                handleExport(
                  () => { if (sentiment) exportSentimentAsCSV(sentiment) },
                  'Sentiment data exported as CSV'
                )
              }
              disabled={isExporting || !sentiment}
              className="menu-item"
              role="menuitem"
            >
              <FileText className="w-4 h-4 text-gray-600" />
              <span>Sentiment Data (CSV)</span>
            </button>
            <button
              onClick={() =>
                handleExport(
                  () => { if (regime) exportRegimeAsCSV(regime) },
                  'Regime data exported as CSV'
                )
              }
              disabled={isExporting || !regime}
              className="menu-item"
              role="menuitem"
            >
              <FileText className="w-4 h-4 text-gray-600" />
              <span>Regime Data (CSV)</span>
            </button>
            <button
              onClick={() =>
                handleExport(
                  () => { if (garch) exportGARCHAsCSV(garch) },
                  'GARCH results exported as CSV'
                )
              }
              disabled={isExporting || !garch}
              className="menu-item"
              role="menuitem"
            >
              <FileText className="w-4 h-4 text-gray-600" />
              <span>GARCH Results (CSV)</span>
            </button>
            <button
              onClick={() =>
                handleExport(
                  () => {
                    if (sentiment && regime && garch) {
                      exportAllDataAsJSON(sentiment, regime, garch)
                    }
                  },
                  'All data exported as JSON'
                )
              }
              disabled={isExporting || !sentiment || !regime}
              className="menu-item"
              role="menuitem"
            >
              <FileJson className="w-4 h-4 text-gray-600" />
              <span>All Data (JSON)</span>
            </button>
          </div>

          {/* Report & Share Section */}
          <div className="p-2">
            <button
              onClick={handleGeneratePDF}
              disabled={isExporting}
              className="menu-item"
              role="menuitem"
            >
              <FileText className="w-4 h-4 text-gray-600" />
              <span>Generate PDF Report</span>
            </button>
            <button
              onClick={handleShareURL}
              disabled={isExporting}
              className="menu-item"
              role="menuitem"
            >
              <Share2 className="w-4 h-4 text-gray-600" />
              <span>Share Dashboard Link</span>
            </button>
          </div>

          {/* Progress Indicator */}
          {exportProgress && (
            <div className="px-4 py-2 border-t border-gray-200 bg-blue-50">
              <div className="flex items-center gap-2 text-xs text-blue-700">
                <Loader2 className="w-3 h-3 animate-spin" />
                <span>{exportProgress}</span>
              </div>
            </div>
          )}
        </div>
      )}

      <style jsx>{`
        .menu-item {
          @apply w-full flex items-center gap-3 px-3 py-2 text-sm text-left;
          @apply hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed;
          @apply transition-colors rounded;
        }
      `}</style>
    </div>
  )
}
