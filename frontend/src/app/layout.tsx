import type { Metadata } from 'next'
import { ThemeProvider } from '@/components/ThemeProvider'
import './globals.css'

export const metadata: Metadata = {
  title: 'Sentiment Regime Detector',
  description: 'Cross-Asset Sentiment Analysis Dashboard',
}

// Static inline script to prevent flash of wrong theme on load.
// This is a standard Next.js pattern (used by next-themes, Tailwind docs, etc.)
// The content is a hardcoded string literal — no user input involved.
const themeScript = `(function(){
  var t = localStorage.getItem('theme');
  if (t === 'dark' || (!t && matchMedia('(prefers-color-scheme:dark)').matches))
    document.documentElement.classList.add('dark');
})()`

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeScript }} />
      </head>
      <body>
        <ThemeProvider>{children}</ThemeProvider>
      </body>
    </html>
  )
}
