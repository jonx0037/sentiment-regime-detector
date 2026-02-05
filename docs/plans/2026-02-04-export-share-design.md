# Export/Share Functionality Design

**Date:** February 4, 2026
**Status:** Approved - Ready for Implementation
**Priority:** Nice-to-Have Enhancement

---

## Overview

Comprehensive export and share functionality for the Sentiment Regime Detector dashboard, enabling users to download charts, export data, generate PDF reports, and share dashboard states via URLs.

## Implementation Priorities

1. **Priority 1:** Chart downloads (PNG + SVG)
2. **Priority 2:** Data exports (CSV + JSON)
3. **Priority 3:** PDF report generator
4. **Priority 4:** Shareable URLs

---

## Architecture

### Core Components

1. **ExportButton Component** - Reusable button with icon + dropdown menu for format selection
2. **Chart Export Utilities** - Functions to capture and download charts as PNG/SVG
3. **Data Export Utilities** - Functions to convert API responses to CSV/JSON
4. **PDF Generator** - Comprehensive dashboard report generator
5. **URL Share Utilities** - Encode dashboard state in URL parameters

### Integration Points

- Add export buttons to each chart component (top-right corner)
- Add global "Export" dropdown button in header (next to Refresh)
- Export menu options: "Export All Charts", "Export Data", "Generate PDF Report", "Share Link"

### Technical Dependencies

```json
{
  "html2canvas": "^1.4.1",
  "jspdf": "^2.5.1"
}
```

- Browser native APIs: Download, Clipboard, SVG serialization

---

## Priority 1: Chart Downloads (PNG + SVG)

### User Experience

- Each chart has a download icon button in the top-right corner
- Clicking reveals dropdown: "Download PNG" | "Download SVG"
- Download triggers immediately with filename: `{chart-name}-{date}.{ext}`

### Charts to Enable

- `SentimentComparisonChart`
- `CISSHistoryChart`
- `SentimentHistoryChart`
- `RegimeTimeline`

### Implementation

**PNG Export** (using html2canvas):
```typescript
const exportChartAsPNG = async (elementId: string, filename: string) => {
  const element = document.getElementById(elementId)
  const canvas = await html2canvas(element, {
    scale: 2, // High DPI for paper quality
    backgroundColor: '#ffffff'
  })
  const link = document.createElement('a')
  link.download = `${filename}-${new Date().toISOString().split('T')[0]}.png`
  link.href = canvas.toDataURL('image/png')
  link.click()
}
```

**SVG Export** (direct extraction):
```typescript
const exportChartAsSVG = (svgElement: SVGElement, filename: string) => {
  const svgData = new XMLSerializer().serializeToString(svgElement)
  const blob = new Blob([svgData], { type: 'image/svg+xml' })
  const link = document.createElement('a')
  link.download = `${filename}-${new Date().toISOString().split('T')[0]}.svg`
  link.href = URL.createObjectURL(blob)
  link.click()
}
```

---

## Priority 2: Data Exports (CSV + JSON)

### User Experience

Global "Export Data" dropdown in header with options:
- "Current Sentiment (CSV)"
- "Current Sentiment (JSON)"
- "Regime Data (CSV)"
- "Regime Data (JSON)"
- "GARCH Results (CSV)"
- "Export All Data (ZIP)" - bundles everything

### Data Formats

**1. Sentiment Data CSV:**
```csv
Asset Class,Sentiment Score,Text Count,Last Updated
Crypto,0.245,1250,2026-02-04T19:30:00Z
Equity,0.123,3400,2026-02-04T19:30:00Z
Forex,0.089,890,2026-02-04T19:30:00Z
Commodities,0.156,670,2026-02-04T19:30:00Z
```

**2. Regime Data CSV:**
```csv
Regime,Confidence,CISS Level,VIX Level,Avg Sentiment,Timestamp
risk-on,0.87,0.15,14.2,0.18,2026-02-04T19:30:00Z
```

**3. GARCH Results CSV:**
```csv
Parameter,Value
Alpha,0.089
Beta,0.866
Persistence,0.955
Forecast Volatility,0.0234
Omega,0.000015
```

### Implementation

Utility functions for CSV/JSON conversion:
```typescript
const convertToCSV = (data: any[], headers: string[]) => {
  const csvRows = [headers.join(',')]
  data.forEach(row => {
    csvRows.push(headers.map(h => row[h]).join(','))
  })
  return csvRows.join('\n')
}

const downloadData = (data: string, filename: string, type: string) => {
  const blob = new Blob([data], { type })
  const link = document.createElement('a')
  link.download = `${filename}-${new Date().toISOString().split('T')[0]}.${type.split('/')[1]}`
  link.href = URL.createObjectURL(blob)
  link.click()
}
```

---

## Priority 3: PDF Report Generator

### User Experience

- "Generate PDF Report" option in export menu
- Shows loading overlay: "Generating report..."
- Auto-downloads: `sentiment-dashboard-report-{date}.pdf`

### Report Structure

**Page 1: Cover & Summary**
- Title: "Sentiment Regime Detector - Dashboard Report"
- Generation timestamp
- Current regime summary (CISS, VIX, avg sentiment)
- Executive summary box

**Page 2: Cross-Asset Sentiment**
- Sentiment comparison chart
- Table of sentiment scores
- Sentiment history chart

**Page 3: Market Stress & Volatility**
- CISS history chart
- GARCH results panel
- Regime timeline visualization

### Implementation

```typescript
const generatePDFReport = async () => {
  const pdf = new jsPDF('p', 'mm', 'a4')

  // Page 1: Cover
  pdf.setFontSize(20)
  pdf.text('Sentiment Regime Detector Report', 20, 20)
  pdf.setFontSize(12)
  pdf.text(`Generated: ${new Date().toLocaleString()}`, 20, 30)

  // Add regime summary
  pdf.text(`Current Regime: ${regime?.regime || 'N/A'}`, 20, 45)
  pdf.text(`CISS Level: ${regime?.features?.ciss_level || 'N/A'}`, 20, 55)
  pdf.text(`VIX Level: ${regime?.features?.vix_level || 'N/A'}`, 20, 65)

  // Page 2+: Capture charts
  const charts = [
    { id: 'sentiment-comparison', title: 'Cross-Asset Sentiment' },
    { id: 'ciss-history', title: 'CISS History' },
    { id: 'regime-timeline', title: 'Regime Timeline' }
  ]

  for (let i = 0; i < charts.length; i++) {
    pdf.addPage()
    pdf.setFontSize(16)
    pdf.text(charts[i].title, 20, 20)

    const element = document.getElementById(charts[i].id)
    const canvas = await html2canvas(element, { scale: 2 })
    pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 10, 30, 190, 120)
  }

  pdf.save(`dashboard-report-${new Date().toISOString().split('T')[0]}.pdf`)
}
```

---

## Priority 4: Shareable URLs

### User Experience

- "Share Dashboard" button in export menu
- Copies URL to clipboard
- Toast notification: "Link copied! Share this URL to show the current dashboard view."

### URL Format

```
https://sentiment-regime-detector.vercel.app/?timestamp=2026-02-04T19:30:00Z
```

### Implementation

```typescript
const generateShareableURL = () => {
  const currentTime = new Date().toISOString()
  const baseURL = window.location.origin
  const shareURL = `${baseURL}?timestamp=${currentTime}`

  navigator.clipboard.writeText(shareURL)
  showToast('Link copied to clipboard!')

  return shareURL
}

// On page load, check for timestamp parameter
useEffect(() => {
  const params = new URLSearchParams(window.location.search)
  const timestamp = params.get('timestamp')

  if (timestamp) {
    // Note: Requires backend support for historical data
    fetchDataForTimestamp(timestamp)
  } else {
    fetchData() // Fetch current data
  }
}, [])
```

**Note:** Shareable URLs with historical data playback require backend API support for timestamp-based queries. Initial implementation may encode only current view state.

---

## UI Components

### ExportButton Component

Reusable dropdown button for export options:

```tsx
interface ExportButtonProps {
  onExportPNG: () => void
  onExportSVG: () => void
  label?: string
}

const ExportButton: React.FC<ExportButtonProps> = ({
  onExportPNG,
  onExportSVG,
  label = 'Export'
}) => {
  const [isOpen, setIsOpen] = useState(false)

  return (
    <div className="relative">
      <button onClick={() => setIsOpen(!isOpen)}>
        <Download className="w-4 h-4" />
        {label}
      </button>
      {isOpen && (
        <div className="absolute right-0 mt-2 bg-white shadow-lg rounded-lg">
          <button onClick={onExportPNG}>Download PNG</button>
          <button onClick={onExportSVG}>Download SVG</button>
        </div>
      )}
    </div>
  )
}
```

### Global Export Menu

Add to header next to Refresh button:

```tsx
<button className="export-menu-button">
  <Download className="w-4 h-4" />
  Export
  <ChevronDown className="w-4 h-4" />
</button>
```

Dropdown options:
- Export All Charts (ZIP)
- Export Data →
  - Sentiment (CSV/JSON)
  - Regime (CSV/JSON)
  - GARCH (CSV/JSON)
- Generate PDF Report
- Share Dashboard

---

## Success Criteria

- [x] Design documented and approved
- [ ] All 4 chart types support PNG + SVG export
- [ ] Data export for sentiment, regime, and GARCH results
- [ ] PDF report generator produces multi-page professional report
- [ ] Shareable URLs encode dashboard state
- [ ] Toast notifications for user feedback
- [ ] Error handling for failed exports
- [ ] Tested in production deployment

---

## Implementation Notes

### File Organization

```
frontend/src/
├── components/
│   ├── ExportButton.tsx          # Reusable export button component
│   ├── ExportMenu.tsx             # Global export dropdown menu
│   └── Toast.tsx                  # Toast notification component
└── utils/
    ├── exportChart.ts             # Chart export utilities
    ├── exportData.ts              # Data export utilities
    ├── exportPDF.ts               # PDF generation
    └── shareURL.ts                # URL sharing utilities
```

### Error Handling

- Catch and display user-friendly errors for failed exports
- Fallback messages if browser doesn't support clipboard API
- Validation for empty/missing data before export

### Accessibility

- Keyboard navigation for export menus
- ARIA labels for export buttons
- Screen reader announcements for export success/failure

---

## Future Enhancements

- Batch export all charts as ZIP file
- Custom date range selection for historical data exports
- Email/Slack integration for sharing reports
- Scheduled automated report generation
- Export customization (select which charts/data to include)

---

**Design Status:** ✅ Approved - Ready for Implementation
**Next Steps:** Install dependencies → Create utilities → Add UI components → Test
