/**
 * URL Sharing Utilities
 *
 * Functions to generate shareable URLs that capture dashboard state.
 * Enables sharing specific dashboard views via URL parameters.
 */

/**
 * Generates a shareable URL for the current dashboard state
 *
 * @param timestamp - Optional specific timestamp to encode
 * @returns Shareable URL string
 */
export function generateShareableURL(timestamp?: string): string {
  const baseURL = window.location.origin + window.location.pathname

  const params = new URLSearchParams()

  // Use provided timestamp or current time
  const timeToEncode = timestamp || new Date().toISOString()
  params.set('timestamp', timeToEncode)

  return `${baseURL}?${params.toString()}`
}

/**
 * Copies a shareable URL to the clipboard
 *
 * @param timestamp - Optional specific timestamp to encode
 * @returns Promise that resolves when copy is complete
 */
export async function copyShareableURL(timestamp?: string): Promise<void> {
  try {
    const shareURL = generateShareableURL(timestamp)

    // Check if clipboard API is available
    if (!navigator.clipboard) {
      throw new Error('Clipboard API not available')
    }

    await navigator.clipboard.writeText(shareURL)
  } catch (error) {
    console.error('Failed to copy URL to clipboard:', error)
    throw error
  }
}

/**
 * Gets the timestamp parameter from the current URL
 *
 * @returns Timestamp string or null if not present
 */
export function getTimestampFromURL(): string | null {
  if (typeof window === 'undefined') {
    return null
  }

  const params = new URLSearchParams(window.location.search)
  return params.get('timestamp')
}

/**
 * Checks if the current page was loaded with a shared URL
 *
 * @returns True if timestamp parameter is present
 */
export function isSharedURL(): boolean {
  return getTimestampFromURL() !== null
}

/**
 * Fallback: Copy text to clipboard using older method (for browsers without Clipboard API)
 *
 * @param text - Text to copy
 */
function fallbackCopyToClipboard(text: string): void {
  const textArea = document.createElement('textarea')
  textArea.value = text
  textArea.style.position = 'fixed'
  textArea.style.left = '-999999px'
  textArea.style.top = '-999999px'
  document.body.appendChild(textArea)
  textArea.focus()
  textArea.select()

  try {
    document.execCommand('copy')
  } catch (error) {
    console.error('Fallback copy failed:', error)
    throw new Error('Failed to copy to clipboard')
  } finally {
    document.body.removeChild(textArea)
  }
}

/**
 * Copies text to clipboard with fallback for older browsers
 *
 * @param text - Text to copy
 */
export async function copyToClipboard(text: string): Promise<void> {
  try {
    if (navigator.clipboard) {
      await navigator.clipboard.writeText(text)
    } else {
      fallbackCopyToClipboard(text)
    }
  } catch (error) {
    console.error('Failed to copy to clipboard:', error)
    throw error
  }
}

/**
 * Shares the dashboard via the Web Share API (if available)
 *
 * @param title - Share dialog title
 * @param text - Share dialog text
 * @param timestamp - Optional timestamp to include
 * @returns Promise that resolves when share is complete
 */
export async function shareDashboard(
  title: string = 'Sentiment Regime Detector',
  text: string = 'Check out this market sentiment analysis',
  timestamp?: string
): Promise<void> {
  try {
    const url = generateShareableURL(timestamp)

    // Check if Web Share API is available (mobile browsers)
    if (navigator.share) {
      await navigator.share({
        title,
        text,
        url,
      })
    } else {
      // Fallback to copying URL
      await copyToClipboard(url)
      throw new Error('FALLBACK_COPY')
    }
  } catch (error) {
    if (error instanceof Error && error.message === 'FALLBACK_COPY') {
      // Not really an error, just fell back to copy
      return
    }
    console.error('Failed to share dashboard:', error)
    throw error
  }
}
