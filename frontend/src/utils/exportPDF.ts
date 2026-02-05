/**
 * PDF Export Utilities
 *
 * Generates comprehensive PDF reports of the dashboard state.
 * Combines text summaries with chart captures for professional reports.
 */

import { jsPDF } from 'jspdf'
import html2canvas from 'html2canvas'
import type { SentimentResponse, RegimeResponse } from '@/types/api'

/**
 * Captures a DOM element as a canvas
 *
 * @param elementId - The DOM element ID to capture
 * @returns Canvas element
 */
async function captureElement(elementId: string): Promise<HTMLCanvasElement> {
  const element = document.getElementById(elementId)

  if (!element) {
    throw new Error(`Element with ID "${elementId}" not found`)
  }

  const canvas = await html2canvas(element, {
    scale: 2,
    backgroundColor: '#ffffff',
    logging: false,
    useCORS: true,
  })

  return canvas
}

/**
 * Adds text to PDF with word wrapping
 *
 * @param pdf - jsPDF instance
 * @param text - Text to add
 * @param x - X coordinate
 * @param y - Y coordinate
 * @param maxWidth - Maximum width before wrapping
 * @returns New Y coordinate after text
 */
function addWrappedText(
  pdf: jsPDF,
  text: string,
  x: number,
  y: number,
  maxWidth: number
): number {
  const lines = pdf.splitTextToSize(text, maxWidth)
  pdf.text(lines, x, y)
  const lineHeight = pdf.getLineHeight() / pdf.internal.scaleFactor
  return y + lines.length * lineHeight
}

/**
 * Generates a comprehensive PDF report of the dashboard
 *
 * @param sentiment - Current sentiment data
 * @param regime - Current regime data
 * @param onProgress - Optional callback for progress updates
 */
export async function generatePDFReport(
  sentiment: SentimentResponse | null,
  regime: RegimeResponse | null,
  onProgress?: (message: string) => void
): Promise<void> {
  try {
    onProgress?.('Initializing PDF...')

    const pdf = new jsPDF('p', 'mm', 'a4')
    const pageWidth = pdf.internal.pageSize.getWidth()
    const pageHeight = pdf.internal.pageSize.getHeight()
    const margin = 20
    const contentWidth = pageWidth - 2 * margin

    // ==================== Page 1: Cover & Summary ====================
    onProgress?.('Creating cover page...')

    // Title
    pdf.setFontSize(24)
    pdf.setFont('helvetica', 'bold')
    pdf.text('Sentiment Regime Detector', margin, 30)

    pdf.setFontSize(16)
    pdf.setFont('helvetica', 'normal')
    pdf.text('Dashboard Report', margin, 40)

    // Generation timestamp
    pdf.setFontSize(10)
    pdf.setTextColor(100, 100, 100)
    const generatedTime = new Date().toLocaleString('en-US', {
      dateStyle: 'full',
      timeStyle: 'long',
    })
    pdf.text(`Generated: ${generatedTime}`, margin, 50)

    // Reset text color
    pdf.setTextColor(0, 0, 0)

    // Executive Summary Box
    pdf.setFillColor(240, 248, 255) // Light blue background
    pdf.rect(margin, 60, contentWidth, 50, 'F')

    pdf.setFontSize(14)
    pdf.setFont('helvetica', 'bold')
    pdf.text('Executive Summary', margin + 5, 70)

    pdf.setFontSize(11)
    pdf.setFont('helvetica', 'normal')

    let summaryY = 78

    if (regime) {
      summaryY = addWrappedText(
        pdf,
        `Current Market Regime: ${regime.regime.toUpperCase()}`,
        margin + 5,
        summaryY,
        contentWidth - 10
      )
      summaryY += 2

      if (regime.confidence !== undefined) {
        summaryY = addWrappedText(
          pdf,
          `Confidence: ${(regime.confidence * 100).toFixed(2)}%`,
          margin + 5,
          summaryY,
          contentWidth - 10
        )
        summaryY += 2
      }

      if (regime.features) {
        if (regime.features.ciss_level !== undefined && regime.features.ciss_level !== null) {
          summaryY = addWrappedText(
            pdf,
            `CISS Level: ${regime.features.ciss_level.toFixed(4)}`,
            margin + 5,
            summaryY,
            contentWidth - 10
          )
          summaryY += 2
        }

        if (regime.features.vix_level !== undefined && regime.features.vix_level !== null) {
          summaryY = addWrappedText(
            pdf,
            `VIX Level: ${regime.features.vix_level.toFixed(2)}`,
            margin + 5,
            summaryY,
            contentWidth - 10
          )
          summaryY += 2
        }

        if (regime.features.cross_asset_mean !== undefined && regime.features.cross_asset_mean !== null) {
          summaryY = addWrappedText(
            pdf,
            `Cross Asset Mean: ${regime.features.cross_asset_mean.toFixed(4)}`,
            margin + 5,
            summaryY,
            contentWidth - 10
          )
        }
      }
    } else {
      pdf.text('Regime data unavailable', margin + 5, summaryY)
    }

    // Sentiment Summary Table
    if (sentiment && sentiment.asset_classes.length > 0) {
      let tableY = 120

      pdf.setFontSize(12)
      pdf.setFont('helvetica', 'bold')
      pdf.text('Cross-Asset Sentiment Overview', margin, tableY)

      tableY += 8

      // Table headers
      pdf.setFontSize(10)
      pdf.setFont('helvetica', 'bold')
      pdf.text('Asset Class', margin, tableY)
      pdf.text('Sentiment', margin + 50, tableY)
      pdf.text('Texts', margin + 90, tableY)

      tableY += 2
      pdf.line(margin, tableY, pageWidth - margin, tableY)
      tableY += 5

      // Table rows
      pdf.setFont('helvetica', 'normal')
      sentiment.asset_classes
        .sort((a, b) => a.asset_class.localeCompare(b.asset_class))
        .forEach((asset) => {
          pdf.text(asset.asset_class, margin, tableY)
          pdf.text(asset.compound_score.toFixed(4), margin + 50, tableY)
          pdf.text(asset.sample_count.toString(), margin + 90, tableY)
          tableY += 6
        })
    }

    // Footer
    pdf.setFontSize(8)
    pdf.setTextColor(150, 150, 150)
    pdf.text(
      'Generated by Sentiment Regime Detector',
      pageWidth / 2,
      pageHeight - 10,
      { align: 'center' }
    )
    pdf.setTextColor(0, 0, 0)

    // ==================== Page 2: Charts ====================
    const charts = [
      { id: 'sentiment-comparison-chart', title: 'Cross-Asset Sentiment Comparison' },
      { id: 'ciss-history-chart', title: 'CISS History' },
      { id: 'sentiment-history-chart', title: 'Sentiment History' },
      { id: 'regime-timeline-chart', title: 'Regime Timeline' },
    ]

    for (let i = 0; i < charts.length; i++) {
      onProgress?.(`Capturing chart ${i + 1} of ${charts.length}...`)

      try {
        const canvas = await captureElement(charts[i].id)

        // Add new page
        pdf.addPage()

        // Chart title
        pdf.setFontSize(14)
        pdf.setFont('helvetica', 'bold')
        pdf.text(charts[i].title, margin, 20)

        // Calculate dimensions to fit chart on page
        const maxChartWidth = contentWidth
        const maxChartHeight = pageHeight - 50 // Leave space for title and footer

        const canvasRatio = canvas.width / canvas.height
        let chartWidth = maxChartWidth
        let chartHeight = chartWidth / canvasRatio

        if (chartHeight > maxChartHeight) {
          chartHeight = maxChartHeight
          chartWidth = chartHeight * canvasRatio
        }

        // Center chart horizontally
        const chartX = (pageWidth - chartWidth) / 2

        // Add chart image
        pdf.addImage(
          canvas.toDataURL('image/png'),
          'PNG',
          chartX,
          30,
          chartWidth,
          chartHeight
        )

        // Page number
        pdf.setFontSize(8)
        pdf.setTextColor(150, 150, 150)
        pdf.text(
          `Page ${i + 2}`,
          pageWidth / 2,
          pageHeight - 10,
          { align: 'center' }
        )
        pdf.setTextColor(0, 0, 0)
      } catch (error) {
        console.warn(`Failed to capture chart ${charts[i].id}:`, error)
        // Continue with other charts even if one fails
      }
    }

    // ==================== Save PDF ====================
    onProgress?.('Saving PDF...')

    const date = new Date().toISOString().split('T')[0]
    pdf.save(`dashboard-report-${date}.pdf`)

    onProgress?.('PDF generated successfully!')
  } catch (error) {
    console.error('Error generating PDF report:', error)
    throw error
  }
}
