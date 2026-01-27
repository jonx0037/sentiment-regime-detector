import type { Config } from 'tailwindcss'

const config: Config = {
  content: [
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        bullish: {
          light: '#10b981',
          DEFAULT: '#059669',
          dark: '#047857',
        },
        bearish: {
          light: '#ef4444',
          DEFAULT: '#dc2626',
          dark: '#b91c1c',
        },
        neutral: {
          light: '#94a3b8',
          DEFAULT: '#64748b',
          dark: '#475569',
        },
      },
    },
  },
  plugins: [],
}
export default config
