/**
 * Chart Export Utilities
 *
 * Functions to export charts as PNG or SVG images for use in papers and presentations.
 */

import html2canvas from 'html2canvas'

/**
 * Export a chart element as a PNG image
 *
 * @param elementId - The DOM element ID containing the chart
 * @param filename - Base filename (date will be appended automatically)
 * @returns Promise that resolves when download completes
 */
export async function exportChartAsPNG(
  elementId: string,
  filename: string
): Promise<void> {
  try {
    const element = document.getElementById(elementId)
    if (!element) {
      throw new Error(`Element with ID "${elementId}" not found`)
    }

    // Capture element as canvas with high DPI for paper quality
    const canvas = await html2canvas(element, {
      scale: 2, // 2x resolution for crisp images
      backgroundColor: '#ffffff',
      logging: false,
      useCORS: true, // Allow cross-origin images
    })

    // Convert to blob and trigger download
    canvas.toBlob((blob) => {
      if (!blob) {
        throw new Error('Failed to create image blob')
      }

      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      const date = new Date().toISOString().split('T')[0]
      link.download = `${filename}-${date}.png`
      link.href = url
      link.click()

      // Cleanup
      URL.revokeObjectURL(url)
    }, 'image/png')
  } catch (error) {
    console.error('Error exporting chart as PNG:', error)
    throw error
  }
}

/**
 * Export a chart's SVG element as an SVG file
 *
 * @param elementId - The DOM element ID containing the SVG chart
 * @param filename - Base filename (date will be appended automatically)
 */
export function exportChartAsSVG(
  elementId: string,
  filename: string
): void {
  try {
    const element = document.getElementById(elementId)
    if (!element) {
      throw new Error(`Element with ID "${elementId}" not found`)
    }

    // Find SVG element (could be the element itself or a child)
    const svgElement = element.tagName === 'svg'
      ? element
      : element.querySelector('svg')

    if (!svgElement) {
      throw new Error(`No SVG element found in "${elementId}"`)
    }

    // Serialize SVG to string
    const svgData = new XMLSerializer().serializeToString(svgElement)

    // Add XML declaration and ensure proper namespace
    const svgBlob = new Blob(
      ['<?xml version="1.0" encoding="UTF-8"?>\n' + svgData],
      { type: 'image/svg+xml;charset=utf-8' }
    )

    // Trigger download
    const url = URL.createObjectURL(svgBlob)
    const link = document.createElement('a')
    const date = new Date().toISOString().split('T')[0]
    link.download = `${filename}-${date}.svg`
    link.href = url
    link.click()

    // Cleanup
    URL.revokeObjectURL(url)
  } catch (error) {
    console.error('Error exporting chart as SVG:', error)
    throw error
  }
}

/**
 * Export all charts on the page as PNG images in a batch
 *
 * @param charts - Array of {elementId, filename} pairs
 */
export async function exportAllChartsAsPNG(
  charts: Array<{ elementId: string; filename: string }>
): Promise<void> {
  for (const chart of charts) {
    await exportChartAsPNG(chart.elementId, chart.filename)
    // Small delay between downloads to avoid browser blocking
    await new Promise(resolve => setTimeout(resolve, 300))
  }
}

/**
 * Export all charts on the page as SVG files in a batch
 *
 * @param charts - Array of {elementId, filename} pairs
 */
export function exportAllChartsAsSVG(
  charts: Array<{ elementId: string; filename: string }>
): void {
  charts.forEach((chart, index) => {
    // Stagger downloads slightly to avoid browser blocking
    setTimeout(() => {
      exportChartAsSVG(chart.elementId, chart.filename)
    }, index * 300)
  })
}
