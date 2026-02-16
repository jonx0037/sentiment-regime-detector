/**
 * Data Export Utilities
 *
 * Functions to export dashboard data as CSV and JSON files.
 * Supports exporting sentiment scores, regime data, and GARCH results.
 */

import type { SentimentResponse, RegimeResponse } from '@/types/api'

/**
 * Converts an array of objects to CSV format
 *
 * @param data - Array of objects to convert
 * @param headers - Array of header names (object keys to include)
 * @returns CSV string
 */
function convertToCSV(data: any[], headers: string[]): string {
  const csvRows: string[] = []

  // Add header row
  csvRows.push(headers.join(','))

  // Add data rows
  data.forEach((row) => {
    const values = headers.map((header) => {
      const value = row[header]
      // Handle values that might contain commas or quotes
      if (value === null || value === undefined) {
        return ''
      }
      const stringValue = String(value)
      // Escape quotes and wrap in quotes if contains comma, quote, or newline
      if (stringValue.includes(',') || stringValue.includes('"') || stringValue.includes('\n')) {
        return `"${stringValue.replace(/"/g, '""')}"`
      }
      return stringValue
    })
    csvRows.push(values.join(','))
  })

  return csvRows.join('\n')
}

/**
 * Triggers a file download in the browser
 *
 * @param content - File content as string
 * @param filename - Base filename without extension
 * @param mimeType - MIME type of the file
 * @param extension - File extension
 */
function downloadFile(
  content: string,
  filename: string,
  mimeType: string,
  extension: string
): void {
  const blob = new Blob([content], { type: mimeType })
  const url = URL.createObjectURL(blob)
  const link = document.createElement('a')
  const date = new Date().toISOString().split('T')[0]

  link.download = `${filename}-${date}.${extension}`
  link.href = url
  link.click()

  // Cleanup
  URL.revokeObjectURL(url)
}

/**
 * Exports sentiment data as CSV
 *
 * @param data - Sentiment response data
 */
export function exportSentimentAsCSV(data: SentimentResponse): void {
  try {
    const rows = data.asset_classes.map((asset) => ({
      'Asset Class': asset.asset_class,
      'Compound Score': asset.compound_score.toFixed(4),
      'Positive Ratio': asset.positive_ratio.toFixed(4),
      'Negative Ratio': asset.negative_ratio.toFixed(4),
      'Sample Count': asset.sample_count,
    }))

    const csv = convertToCSV(rows, [
      'Asset Class',
      'Compound Score',
      'Positive Ratio',
      'Negative Ratio',
      'Sample Count',
    ])

    downloadFile(csv, 'sentiment-data', 'text/csv;charset=utf-8', 'csv')
  } catch (error) {
    console.error('Error exporting sentiment as CSV:', error)
    throw error
  }
}

/**
 * Exports sentiment data as JSON
 *
 * @param data - Sentiment response data
 */
export function exportSentimentAsJSON(data: SentimentResponse): void {
  try {
    const json = JSON.stringify(data, null, 2)
    downloadFile(json, 'sentiment-data', 'application/json', 'json')
  } catch (error) {
    console.error('Error exporting sentiment as JSON:', error)
    throw error
  }
}

/**
 * Exports regime data as CSV
 *
 * @param data - Regime response data
 */
export function exportRegimeAsCSV(data: RegimeResponse): void {
  try {
    const rows = [
      {
        Regime: data.regime,
        Confidence: data.confidence.toFixed(4),
        'CISS Level': data.features?.ciss_level?.toFixed(4) || 'N/A',
        'VIX Level': data.features?.vix_level?.toFixed(2) || 'N/A',
        'Cross Asset Mean': data.features?.cross_asset_mean?.toFixed(4) || 'N/A',
        Timestamp: data.timestamp || new Date().toISOString(),
      },
    ]

    const csv = convertToCSV(rows, [
      'Regime',
      'Confidence',
      'CISS Level',
      'VIX Level',
      'Cross Asset Mean',
      'Timestamp',
    ])

    downloadFile(csv, 'regime-data', 'text/csv;charset=utf-8', 'csv')
  } catch (error) {
    console.error('Error exporting regime as CSV:', error)
    throw error
  }
}

/**
 * Exports regime data as JSON
 *
 * @param data - Regime response data
 */
export function exportRegimeAsJSON(data: RegimeResponse): void {
  try {
    const json = JSON.stringify(data, null, 2)
    downloadFile(json, 'regime-data', 'application/json', 'json')
  } catch (error) {
    console.error('Error exporting regime as JSON:', error)
    throw error
  }
}

/**
 * Exports GARCH results as CSV
 *
 * @param data - GARCH results data (should match the API structure)
 */
export function exportGARCHAsCSV(data: any): void {
  try {
    const normalized = normalizeGARCHForExport(data)
    const rows = [
      { Parameter: 'Alpha (ARCH effect)', Value: normalized.alpha?.toFixed(6) || 'N/A' },
      { Parameter: 'Beta (GARCH effect)', Value: normalized.beta?.toFixed(6) || 'N/A' },
      {
        Parameter: 'Persistence (α+β)',
        Value: normalized.persistence?.toFixed(6) || 'N/A',
      },
      { Parameter: 'Omega (constant)', Value: normalized.omega?.toFixed(8) || 'N/A' },
      {
        Parameter: 'Forecast Volatility (mean)',
        Value: normalized.forecast_volatility?.toFixed(6) || 'N/A',
      },
      {
        Parameter: 'Log Likelihood',
        Value: normalized.log_likelihood?.toFixed(2) || 'N/A',
      },
      { Parameter: 'AIC', Value: normalized.aic?.toFixed(2) || 'N/A' },
      { Parameter: 'BIC', Value: normalized.bic?.toFixed(2) || 'N/A' },
    ]

    const csv = convertToCSV(rows, ['Parameter', 'Value'])
    downloadFile(csv, 'garch-results', 'text/csv;charset=utf-8', 'csv')
  } catch (error) {
    console.error('Error exporting GARCH as CSV:', error)
    throw error
  }
}

/**
 * Exports GARCH results as JSON
 *
 * @param data - GARCH results data
 */
export function exportGARCHAsJSON(data: any): void {
  try {
    const json = JSON.stringify(data, null, 2)
    downloadFile(json, 'garch-results', 'application/json', 'json')
  } catch (error) {
    console.error('Error exporting GARCH as JSON:', error)
    throw error
  }
}

/**
 * Exports all dashboard data as a single JSON file
 *
 * @param sentiment - Sentiment response data
 * @param regime - Regime response data
 * @param garch - GARCH results data
 */
export function exportAllDataAsJSON(
  sentiment: SentimentResponse,
  regime: RegimeResponse,
  garch: any
): void {
  try {
    const allData = {
      exported_at: new Date().toISOString(),
      sentiment,
      regime,
      garch,
    }

    const json = JSON.stringify(allData, null, 2)
    downloadFile(json, 'dashboard-complete-data', 'application/json', 'json')
  } catch (error) {
    console.error('Error exporting all data as JSON:', error)
    throw error
  }
}

function normalizeGARCHForExport(data: any): {
  alpha?: number
  beta?: number
  persistence?: number
  omega?: number
  forecast_volatility?: number
  log_likelihood?: number
  aic?: number
  bic?: number
} {
  if (data?.parameters?.parameters && data?.forecast?.statistics) {
    return {
      alpha: data.parameters.parameters['alpha[1]'],
      beta: data.parameters.parameters['beta[1]'],
      persistence: data.parameters.persistence,
      omega: data.parameters.parameters.omega,
      forecast_volatility: data.forecast.statistics.mean,
      log_likelihood: data.parameters.loglikelihood,
      aic: data.parameters.aic,
      bic: data.parameters.bic,
    }
  }

  return {
    alpha: data?.alpha,
    beta: data?.beta,
    persistence: data?.persistence,
    omega: data?.omega,
    forecast_volatility: data?.forecast_volatility,
    log_likelihood: data?.log_likelihood,
    aic: data?.aic,
    bic: data?.bic,
  }
}
