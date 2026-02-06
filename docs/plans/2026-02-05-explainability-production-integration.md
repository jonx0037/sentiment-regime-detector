# SHAP Explainability Production Integration Design

**Date:** February 5, 2026
**Author:** Jonathan Rocha
**Status:** Approved - Ready for Implementation
**Priority:** High - Production feature for capstone demonstration

---

## Executive Summary

This document outlines the integration of the completed SHAP explainability system into the production dashboard. The system will allow users to understand "why" the model predicted a specific regime by visualizing SHAP feature contributions through an intuitive modal interface.

**Timeline:** 9-12 hours (2 phases)

**Deliverables:**

1. **Phase 1 (Required):** Current prediction explainability modal - 4-5 hours
2. **Phase 2 (Optional):** Historical crisis events explorer - 5-7 hours

**User Value:**

- Practitioners see "why risk-off now?" explanations
- Academic committee sees model interpretability in action
- Builds trust through transparency

---

## Background

The SHAP explainability system was built in `.worktrees/explainability-implementation` over 9 days and includes:

- ✅ Core explainer with SHAP TreeExplainer
- ✅ Two-tier caching (Redis L1 + PostgreSQL L2)
- ✅ 5 API endpoints at `/api/v1/explainability/*`
- ✅ Publication-quality visualization generation
- ✅ 6 crisis events analyzed (2008-2026)

**Current State:** Complete and tested in isolation, ready to merge into production.

**Goal:** Make explainability accessible to dashboard users through intuitive UI.

---

## Design Decisions

### Integration Scope

**Phase 1: Current Prediction Explainability (Required)**

- Add "Explain This Prediction" button to RegimePanel
- Modal shows SHAP waterfall plot + feature contributions table
- Answers "why did the model predict risk-off today?"
- Most valuable feature - explains what users are actively viewing

**Phase 2: Historical Events Explorer (Optional)**

- New page/route showing 6 crisis events
- Educational gallery: 2008 Crisis, COVID-19, GameStop, Luna, Celsius, Out-of-Sample
- Each event has detailed explanation showing model behavior during extremes
- Great for committee presentation and paper discussion

### UI Approach

**Modal Popup (Chosen)**

- Keeps main dashboard clean and uncluttered
- Shows detailed visualizations on demand
- Easy to dismiss and return to monitoring
- Follows common dashboard pattern

**Alternatives Rejected:**

- ❌ Expandable section - takes too much vertical space
- ❌ Dedicated tab only - requires navigation away from context

### Backend Integration

**Merge to Main Branch (Chosen)**

- Copy explainability module to main `src/sentiment_detector/explainability/`
- Use existing 5 API endpoints immediately
- Leverages existing caching infrastructure
- Clean integration with current architecture

**Alternatives Rejected:**

- ❌ Separate microservice - overkill for capstone, complex deployment
- ❌ Static pre-generated - inflexible, can't explain current prediction

---

## System Architecture

### Three-Layer Integration

```
┌─────────────────────────────────────────────────────────────┐
│                    Existing Dashboard                        │
│  - Sentiment monitoring                                      │
│  - Regime detection                                          │
│  - Real-time updates (60s)                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌──────────────────────────────────────┐
        │   NEW: Explainability Integration    │
        │  - ExplainabilityModal (UI)          │
        │  - "Explain" button in RegimePanel   │
        │  - Phase 2: Event Explorer (optional)│
        └──────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              Backend: Explainability Module                  │
│  - SHAP computation (TreeExplainer)                         │
│  - Two-tier cache (Redis L1, PostgreSQL L2)                 │
│  - Waterfall plot generation (matplotlib)                   │
│  - 5 REST endpoints                                          │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow: Current Prediction Explanation

1. **User Action:** Views RegimePanel → clicks "Explain This Prediction"
2. **Frontend Request:** `GET /api/v1/explainability/current`
3. **Backend Processing:**
   - Check Redis cache (L1) - hit: ~5ms
   - If miss, check PostgreSQL cache (L2) - hit: ~20ms
   - If miss, compute SHAP values - ~100-300ms
   - Generate waterfall plot as base64 PNG
   - Cache result (TTL: 5 minutes)
4. **Frontend Display:**
   - Open ExplainabilityModal
   - Show waterfall plot (left)
   - Show top 10 features table (right)
   - Display model metadata (version, timestamp)

**Performance Expectations:**

- Cached response: 5-20ms (99% of requests after warm-up)
- Cold computation: 100-300ms (acceptable for user-initiated action)
- Cache hit rate: >90% in steady state

---

## Phase 1: Current Prediction Explainability

### Backend Changes

**Files to Merge:**

```
Source: .worktrees/explainability-implementation/
Target: main branch

Merge:
  src/sentiment_detector/explainability/
  ├── __init__.py
  ├── explainer.py      # SHAP computation engine
  ├── cache.py          # Two-tier caching
  ├── events.py         # Crisis event definitions
  └── viz.py            # Waterfall plot generation

Verify:
  src/sentiment_detector/api/routes/explainability.py (already exists)
  - GET /current
  - GET /events
  - GET /events/{event_id}
  - GET /global-importance
  - GET /feature-interactions
```

**Dependencies Check:**

```toml
# Ensure pyproject.toml includes:
shap = ">=0.44.0"
matplotlib = ">=3.8.0"
# Redis/PostgreSQL already configured
```

**No Router Changes Needed:**

- Explainability router already built in worktree
- Should be registered in main FastAPI app
- Endpoints follow existing `/api/v1/*` convention

### Frontend Changes

**New Files:**

**`frontend/src/types/explainability.ts`**

```typescript
export interface ExplanationResponse {
  predicted_regime: 'risk_on' | 'risk_off' | 'transition'
  confidence: number
  timestamp: string
  model_version: string
  waterfall_plot: string  // base64 PNG
  top_features: TopFeature[]
  shap_values: number[]
  feature_names: string[]
  base_value: number
  prediction: number
}

export interface TopFeature {
  name: string              // Technical name (e.g., "ciss_lag1")
  display_name: string      // Human-readable (e.g., "CISS (Previous Day)")
  value: number            // Feature value
  shap_value: number       // SHAP contribution
  contribution_pct: number // % of total |SHAP|
}

export interface CrisisEvent {
  event_id: string
  name: string
  date: string
  description: string
  ciss_peak: number
  vix_peak: number
}
```

**`frontend/src/components/ExplainabilityModal.tsx`**

**Component Structure:**

```tsx
interface Props {
  isOpen: boolean
  onClose: () => void
  regime: 'risk_on' | 'risk_off' | 'transition'
  confidence: number
}

export function ExplainabilityModal({ isOpen, onClose, regime, confidence }: Props)
```

**Layout:**

```
┌─────────────────────────────────────────────────────┐
│ Why Risk-Off? (Confidence: 87%)              [X]    │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌──────────────────────┐  ┌──────────────────┐   │
│  │                      │  │ Top Features     │   │
│  │  Waterfall Plot     │  │                  │   │
│  │  (base64 image)     │  │ 1. ciss_lag1 ↑  │   │
│  │                      │  │    0.45 (+0.23) │   │
│  │  Shows:              │  │                  │   │
│  │  - Base value        │  │ 2. vix ↑         │   │
│  │  - Feature           │  │    28.5 (+0.18) │   │
│  │    contributions     │  │                  │   │
│  │  - Final prediction  │  │ 3. sentiment ↓   │   │
│  │                      │  │    -0.15 (-0.12)│   │
│  └──────────────────────┘  │                  │   │
│                            │ [View Full List] │   │
│                            └──────────────────┘   │
│                                                      │
├─────────────────────────────────────────────────────┤
│ Model: v1.2.0 | Computed: 2026-02-05 14:23:15      │
│ [View Historical Events]                     [Close]│
└─────────────────────────────────────────────────────┘
```

**Features:**

- Responsive: 2-column on desktop, stacked on mobile
- Waterfall plot: Full-width image with loading skeleton
- Table: Sortable by contribution, color-coded (green/red)
- Tooltips: Explain technical feature names on hover
- Loading state: Show skeleton while fetching
- Error state: "Explanation temporarily unavailable"

**Modified Files:**

**`frontend/src/services/api.ts`**

```typescript
// Add new export
export const explainabilityApi = {
  /**
   * Get SHAP explanation for current regime prediction
   */
  async getCurrentExplanation(): Promise<ExplanationResponse> {
    return fetchApi<ExplanationResponse>('/explainability/current')
  },

  /**
   * Get list of historical crisis events
   */
  async getEventsList(): Promise<CrisisEvent[]> {
    return fetchApi<CrisisEvent[]>('/explainability/events')
  },

  /**
   * Get SHAP explanation for specific event
   */
  async getEventExplanation(eventId: string): Promise<ExplanationResponse> {
    return fetchApi<ExplanationResponse>(`/explainability/events/${eventId}`)
  },
}
```

**`frontend/src/components/RegimePanel.tsx`**

```typescript
// Add state
const [explainModalOpen, setExplainModalOpen] = useState(false)

// Add button below confidence display
<button
  onClick={() => setExplainModalOpen(true)}
  className="mt-3 inline-flex items-center px-3 py-2 border border-gray-300
             shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700
             bg-white hover:bg-gray-50 focus:outline-none focus:ring-2
             focus:ring-offset-2 focus:ring-indigo-500"
>
  <Lightbulb className="h-4 w-4 mr-2" />
  Explain This Prediction
</button>

// Add modal
<ExplainabilityModal
  isOpen={explainModalOpen}
  onClose={() => setExplainModalOpen(false)}
  regime={regime.current_regime}
  confidence={regime.confidence}
/>
```

### Caching Strategy

**Frontend:**

- Cache current explanation for 60 seconds (matches dashboard refresh)
- Invalidate on regime change detection
- Use React Query or simple state management

**Backend:**

- Already implemented in merged code
- Redis L1: 5-minute TTL
- PostgreSQL L2: Permanent with model version key
- Cache key: `explain:{date}:{model_version}`

### Error Handling

**API Call Failures:**

- If `/explainability/current` returns 503: Show toast "Explanation temporarily unavailable"
- If returns 404: Disable "Explain" button (model not ready)
- If returns 500: Log error, show generic message
- Retry logic: 2 attempts with exponential backoff (1s, 2s)

**Graceful Degradation:**

- Dashboard continues working if explainability fails
- "Explain" button shows loading state during fetch
- Clear error messages guide user (not technical jargon)

**Edge Cases:**

- Model not loaded: Disable button with tooltip "Explainability loading..."
- No recent prediction: Gray out button
- Very old prediction (>1 hour): Warning in modal "Explaining outdated prediction"

---

## Phase 2: Historical Events Explorer (Optional)

### New Route/Page

**URL:** `/explainability` or new tab in dashboard navigation

**Purpose:**

- Educational: Show how model behaved during historical crises
- Committee demo: Quick access to interesting events
- Paper figures: Same visualizations shown in dashboard

### UI Design

**Gallery View:**

```
┌────────────────────────────────────────────────────────┐
│  Historical Crisis Events                              │
│  Explore how the model interpreted major market events │
├────────────────────────────────────────────────────────┤
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ 2008 Crisis │  │ COVID Crash │  │  GameStop   │   │
│  │ Nov 20 2008 │  │ Mar 16 2020 │  │ Jan 27 2021 │   │
│  │             │  │             │  │             │   │
│  │ Risk-Off ⚠️ │  │ Risk-Off ⚠️ │  │ Risk-On ✓   │   │
│  │ CISS: 0.98  │  │ VIX: 82.69  │  │ CISS: 0.42  │   │
│  │             │  │             │  │             │   │
│  │  [Explain]  │  │  [Explain]  │  │  [Explain]  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐   │
│  │ Luna Crash  │  │  Celsius    │  │Out-of-Sample│   │
│  │ May 9 2022  │  │ Jun 15 2022 │  │  2024-2026  │   │
│  │             │  │             │  │             │   │
│  │ Risk-Off ⚠️ │  │ Risk-Off ⚠️ │  │   Various   │   │
│  │ VIX: 35.2   │  │ CISS: 0.55  │  │ Testing     │   │
│  │             │  │             │  │             │   │
│  │  [Explain]  │  │  [Explain]  │  │  [Explain]  │   │
│  └─────────────┘  └─────────────┘  └─────────────┘   │
│                                                         │
└────────────────────────────────────────────────────────┘
```

**Event Card Design:**

- Event name and date (prominent)
- Key indicators badge: CISS peak, VIX peak
- Predicted regime with icon (✓ correct, ⚠️ stress detected)
- Brief 1-line description
- "Explain" button

**Event Detail Modal:**

Similar to Phase 1 modal but enhanced:

```
┌─────────────────────────────────────────────────────┐
│ COVID-19 Market Crash (March 16, 2020)        [X]   │
├─────────────────────────────────────────────────────┤
│ What Happened:                                       │
│ Global markets crashed as COVID-19 pandemic spread.  │
│ VIX hit all-time high of 82.69. Model correctly     │
│ predicted extreme risk-off regime.                   │
├─────────────────────────────────────────────────────┤
│  [Waterfall Plot]         [Top Features Table]      │
│  (same as Phase 1)        (same as Phase 1)        │
├─────────────────────────────────────────────────────┤
│ Predicted: Risk-Off (95% confidence)                │
│ Model: v1.2.0 | Event Date: March 16, 2020         │
│                                              [Close] │
└─────────────────────────────────────────────────────┘
```

**Differences from Phase 1:**

- Add "What Happened?" context section (from events.py descriptions)
- Show event date instead of "Computed" timestamp
- Optional: Compare predicted vs. actual regime if ground truth available

### Implementation

**New Files:**

- `frontend/src/app/explainability/page.tsx` (Next.js page)
- `frontend/src/components/EventCard.tsx` (event card component)
- `frontend/src/components/EventDetailModal.tsx` (or reuse ExplainabilityModal)

**Backend:**

- Already built: `GET /api/v1/explainability/events`
- Already built: `GET /api/v1/explainability/events/{event_id}`
- Events defined in `events.py`:
  - financial_crisis_2008
  - covid_crash_2020
  - gamestop_2021
  - luna_collapse_2022
  - celsius_contagion_2022
  - out_of_sample_validation

**Navigation:**

- Add link in dashboard header or sidebar
- Footer link: "View Historical Events" in Phase 1 modal

---

## Testing Strategy

### Backend Testing

**Unit Tests (`tests/test_explainability/`):**

```python
# test_explainer.py
def test_explain_prediction_with_mock_data():
    """Test SHAP computation produces valid results."""

def test_waterfall_plot_generation():
    """Test base64 PNG generation."""

def test_top_features_sorting():
    """Test features sorted by |SHAP|."""

# test_cache.py
def test_redis_cache_hit():
    """Test L1 cache returns cached result."""

def test_postgres_cache_fallback():
    """Test L2 cache when Redis misses."""

def test_cache_invalidation_on_version_change():
    """Test cache key includes model version."""

# test_explainability_routes.py
def test_current_endpoint_returns_valid_response():
    """Test /explainability/current endpoint."""

def test_events_list_returns_six_events():
    """Test /explainability/events returns all events."""

def test_event_detail_returns_explanation():
    """Test /explainability/events/{id} returns explanation."""
```

**Integration Tests:**

```python
def test_end_to_end_explanation():
    """Test full flow: API call → SHAP → plot → response."""
    # Use real model file
    # Verify response structure matches ExplanationResponse type
    # Check base64 string is valid image
```

### Frontend Testing

**Component Tests (`frontend/src/components/__tests__/`):**

```typescript
// ExplainabilityModal.test.tsx
describe('ExplainabilityModal', () => {
  it('renders waterfall plot when data loaded')
  it('shows loading skeleton while fetching')
  it('displays error message on API failure')
  it('sorts table by SHAP contribution')
  it('closes on backdrop click')
})

// RegimePanel.test.tsx (additions)
describe('RegimePanel with Explainability', () => {
  it('shows Explain button when regime available')
  it('opens modal on button click')
  it('disables button when explanation unavailable')
})
```

**Integration Tests:**

```typescript
describe('Explainability Integration', () => {
  it('fetches explanation on button click')
  it('displays explanation in modal')
  it('handles API errors gracefully')
  it('caches explanation for 60 seconds')
})
```

### Manual Testing Checklist

**Phase 1:**

- [ ] Click "Explain" button in RegimePanel
- [ ] Verify modal opens with loading state
- [ ] Verify waterfall plot displays (check image not broken)
- [ ] Verify top 10 features table shows correct data
- [ ] Verify table sorting works
- [ ] Test on mobile (responsive layout)
- [ ] Test with slow network (loading states)
- [ ] Test API failure (error message displays)
- [ ] Close modal and reopen (cached response)

**Phase 2:**

- [ ] Navigate to /explainability page
- [ ] Verify 6 event cards display
- [ ] Click each event's "Explain" button
- [ ] Verify event-specific explanations
- [ ] Test mobile gallery layout
- [ ] Test navigation between events

---

## Deployment Considerations

### Railway Production Environment

**Requirements:**

- Memory: ~500MB for model + SHAP computation (current Railway plan: adequate)
- Redis: Already configured via Railway plugin
- PostgreSQL: Already configured with DATABASE_URL
- Model file: `models/regime_classifier_rf.pkl` must be in deployment

**Environment Variables:**

```bash
# Already configured:
REDIS_URL=redis://...
DATABASE_URL=postgresql://...

# New (optional):
ENABLE_EXPLAINABILITY=true  # Feature flag for rollback
SHAP_CACHE_TTL=300          # Cache TTL in seconds (default: 300)
```

**Deployment Steps:**

1. Merge explainability code to main branch
2. Verify model file in `models/` directory (check .gitignore)
3. Run database migrations if cache schema added
4. Deploy to Railway
5. Test `/api/v1/explainability/current` endpoint
6. Monitor logs for any SHAP computation errors

**Performance Monitoring:**

- Track API response time for `/explainability/current`
- Target: <50ms (cached), <500ms (cold)
- Monitor cache hit rate via Redis INFO
- Alert if >10% requests take >1 second

**Rollback Plan:**

```python
# In FastAPI app startup:
if os.getenv('ENABLE_EXPLAINABILITY', 'true') == 'false':
    # Don't register explainability routes
    logger.info("Explainability disabled via env var")
```

---

## Implementation Timeline

### Phase 1: Current Prediction Explainability (4-5 hours)

**Backend (30 minutes):**

- [ ] Copy explainability module to main branch (5 min)
- [ ] Verify imports and paths (5 min)
- [ ] Test API endpoints locally (10 min)
- [ ] Write/run unit tests (10 min)

**Frontend (3-4 hours):**

- [ ] Create TypeScript types (15 min)
- [ ] Extend api.ts with explainabilityApi (15 min)
- [ ] Build ExplainabilityModal component (2 hours)
  - Modal shell and layout
  - Waterfall plot display
  - Top features table
  - Loading and error states
- [ ] Integrate "Explain" button into RegimePanel (30 min)
- [ ] Styling and responsive design (30 min)
- [ ] Testing and refinement (1 hour)

### Phase 2: Historical Events Explorer (5-7 hours)

**Backend (Already Complete):**

- ✅ API endpoints exist
- ✅ Event definitions exist
- ✅ Mock feature generation exists

**Frontend (5-7 hours):**

- [ ] Create /explainability page route (30 min)
- [ ] Build EventCard component (1 hour)
- [ ] Build event gallery layout (1 hour)
- [ ] Create/adapt EventDetailModal (2 hours)
- [ ] Add navigation links (30 min)
- [ ] Styling and responsive design (1 hour)
- [ ] Testing and refinement (1-2 hours)

**Total Estimated Time: 9-12 hours**

---

## Success Metrics

### Technical Metrics

**Performance:**

- Cache hit rate >90% after 5 minutes of warm-up
- Median response time <50ms (cached)
- 95th percentile response time <500ms (cold)
- Zero 500 errors from explainability endpoints

**Reliability:**

- Dashboard works even if explainability unavailable
- Graceful degradation on API failures
- Clear error messages (not technical stack traces)

### User Experience Metrics

**Engagement:**

- Track "Explain" button click rate (expect 20-40% of users)
- Modal view duration (should be >10 seconds if engaged)
- Historical events page views (Phase 2)

**Qualitative:**

- Committee feedback: "Model is clearly interpretable"
- User feedback: "I understand why it predicted risk-off"
- No confusion about feature contributions

### Academic Metrics

**Paper Integration:**

- Include modal screenshot in paper
- Reference waterfall plots from Phase 2 events
- Discuss feature importance findings from global analysis

**Committee Demonstration:**

- Live demo: Click "Explain" and walk through waterfall plot
- Show historical event (e.g., COVID-19) with extreme features
- Answer questions using live SHAP values

---

## Known Limitations & Future Work

### Current Limitations

**Model-Specific:**

- Only works with tree-based models (Random Forest, XGBoost)
- SHAP TreeExplainer used (optimized for trees)
- If model changes to neural network, would need different explainer

**Feature Names:**

- Technical names like "ciss_lag1" need tooltips for clarity
- Display names manually mapped (not auto-generated)

**Visualization:**

- Waterfall plot generated server-side (not interactive)
- No drill-down into feature details from plot
- Fixed layout (can't reorder features in UI)

**Data:**

- Mock features used in demo (not connected to real-time DB yet)
- Historical events use representative feature values
- Production needs actual feature pipeline integration

### Future Enhancements

**Interactivity:**

- Allow users to toggle features on/off to see impact
- "What-if" analysis: Change feature values, see prediction change
- Compare multiple time periods side-by-side

**Additional Visualizations:**

- SHAP summary plot (beeswarm) for global importance
- Dependency plots showing feature relationships
- Force plots (alternative to waterfall)

**Real-Time Integration:**

- Connect to actual feature database
- Show explanation for any historical date (not just crisis events)
- Time-series view of feature importance over time

**Model Comparison:**

- Compare Random Forest vs. XGBoost explanations
- Highlight where models disagree
- Show ensemble reasoning

---

## Appendix: API Response Examples

### GET /api/v1/explainability/current

**Response (200 OK):**

```json
{
  "predicted_regime": "risk_off",
  "confidence": 0.87,
  "timestamp": "2026-02-05T14:23:15Z",
  "model_version": "v1.2.0",
  "waterfall_plot": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
  "top_features": [
    {
      "name": "ciss_lag1",
      "display_name": "CISS (Previous Day)",
      "value": 0.45,
      "shap_value": 0.23,
      "contribution_pct": 28.5
    },
    {
      "name": "vix",
      "display_name": "VIX Volatility Index",
      "value": 28.5,
      "shap_value": 0.18,
      "contribution_pct": 22.3
    },
    {
      "name": "sentiment",
      "display_name": "Cross-Asset Sentiment",
      "value": -0.15,
      "shap_value": -0.12,
      "contribution_pct": 14.9
    }
  ],
  "shap_values": [0.23, 0.18, -0.12, 0.08, ...],
  "feature_names": ["ciss_lag1", "vix", "sentiment", ...],
  "base_value": 0.33,
  "prediction": 0.87
}
```

### GET /api/v1/explainability/events

**Response (200 OK):**

```json
{
  "events": [
    {
      "event_id": "financial_crisis_2008",
      "name": "Financial Crisis 2008",
      "date": "2008-11-20",
      "description": "CISS reached all-time high of 0.98 during Lehman Brothers collapse aftermath.",
      "ciss_peak": 0.98,
      "vix_peak": 80.86
    },
    {
      "event_id": "covid_crash_2020",
      "name": "COVID-19 Market Crash",
      "date": "2020-03-16",
      "description": "VIX spiked to 82.69 as pandemic fears triggered global sell-off.",
      "ciss_peak": 0.66,
      "vix_peak": 82.69
    }
  ]
}
```

### GET /api/v1/explainability/events/covid_crash_2020

**Response (200 OK):**

```json
{
  "event": {
    "event_id": "covid_crash_2020",
    "name": "COVID-19 Market Crash",
    "date": "2020-03-16",
    "description": "VIX spiked to 82.69 as pandemic fears triggered global sell-off.",
    "ciss_peak": 0.66,
    "vix_peak": 82.69
  },
  "explanation": {
    "predicted_regime": "risk_off",
    "confidence": 0.95,
    "timestamp": "2020-03-16T16:00:00Z",
    "model_version": "v1.2.0",
    "waterfall_plot": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...",
    "top_features": [
      {
        "name": "vix",
        "display_name": "VIX Volatility Index",
        "value": 82.69,
        "shap_value": 0.45,
        "contribution_pct": 42.1
      },
      {
        "name": "vix_spike",
        "display_name": "VIX Spike Indicator",
        "value": 1.0,
        "shap_value": 0.28,
        "contribution_pct": 26.2
      },
      {
        "name": "sentiment",
        "display_name": "Cross-Asset Sentiment",
        "value": -0.40,
        "shap_value": -0.18,
        "contribution_pct": 16.8
      }
    ],
    "shap_values": [0.45, 0.28, -0.18, ...],
    "feature_names": ["vix", "vix_spike", "sentiment", ...],
    "base_value": 0.33,
    "prediction": 0.95
  }
}
```

---

## Conclusion

This integration brings the completed SHAP explainability system to production users through an intuitive modal interface. Phase 1 provides immediate value by explaining current predictions, while Phase 2 adds educational historical context for committee demonstrations.

The design leverages existing infrastructure (caching, API architecture) and follows established patterns in the codebase. Total implementation time is 9-12 hours split across two phases.

**Next Steps:**

1. Review and approve this design
2. Create implementation plan with detailed tasks
3. Consider using git worktree for isolated development
4. Execute Phase 1 first, validate with users
5. Optionally implement Phase 2 based on time and feedback

---

**Design Status:** ✅ Complete and approved - ready for implementation planning
