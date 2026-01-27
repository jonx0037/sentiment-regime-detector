# Sentiment Regime Detector - Frontend Dashboard

Modern React dashboard built with Next.js 14, TypeScript, and Tailwind CSS for visualizing cross-asset sentiment analysis.

## Features

- **Real-Time Sentiment Monitoring**: Live updates every 60 seconds
- **Cross-Asset Analysis**: Compare sentiment across Equities, Crypto, Forex, and Commodities
- **Interactive Visualizations**: Charts and cards showing sentiment breakdown
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **TypeScript**: Full type safety with API integration

## Tech Stack

- **Next.js 14** - React framework with App Router
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Recharts** - Data visualization
- **Lucide React** - Icon library

## Getting Started

### Prerequisites

- Node.js 18+ and npm/yarn
- Backend API running on `http://localhost:8000`

### Installation

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# or
yarn install
```

### Development

```bash
# Start development server
npm run dev

# or
yarn dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
# Create production build
npm run build

# Start production server
npm start
```

## Project Structure

```
frontend/
├── src/
│   ├── app/                 # Next.js App Router pages
│   │   ├── page.tsx         # Main dashboard page
│   │   ├── layout.tsx       # Root layout
│   │   └── globals.css      # Global styles
│   ├── components/          # React components
│   │   ├── SentimentCard.tsx
│   │   ├── CrossAssetSummary.tsx
│   │   └── SentimentComparisonChart.tsx
│   ├── services/            # API integration
│   │   └── api.ts           # API client
│   ├── types/               # TypeScript definitions
│   │   └── api.ts           # API response types
│   └── lib/                 # Utility functions
│       └── utils.ts         # Helper functions
├── public/                  # Static assets
├── tailwind.config.ts       # Tailwind configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies
```

## API Integration

The dashboard connects to the FastAPI backend at `http://localhost:8000/api/v1`. 

Key endpoints:
- `GET /sentiment/current` - Current sentiment for all asset classes
- `GET /sentiment/history` - Historical sentiment data
- `GET /regime/current` - Current market regime

## Components

### SentimentCard
Individual asset class sentiment card showing:
- Compound sentiment score
- Positive/Negative/Neutral breakdown
- Momentum indicator
- Sample count

### CrossAssetSummary
Aggregate statistics across all asset classes:
- Mean sentiment score
- Standard deviation (dispersion)
- Score spread
- Market condition interpretation

### SentimentComparisonChart
Interactive line chart comparing sentiment metrics across asset classes.

## Configuration

Environment variables (create `.env.local`):

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## Color Scheme

- **Bullish**: Green (`#059669`)
- **Bearish**: Red (`#dc2626`)
- **Neutral**: Gray (`#64748b`)

## Auto-Refresh

Dashboard automatically refreshes data every 60 seconds. Manual refresh available via button.

## License

Part of SMU MSDS Capstone Project (DS 6210)
