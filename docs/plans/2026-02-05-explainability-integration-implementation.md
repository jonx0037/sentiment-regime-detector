# SHAP Explainability Production Integration Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Integrate the completed SHAP explainability system into the production dashboard with a modal UI showing why specific regime predictions were made.

**Architecture:** Two-phase integration: (1) Backend merge of explainability module + verify API endpoints, (2) Frontend modal component with "Explain" button in RegimePanel, (3) Optional historical events explorer page.

**Tech Stack:** Python (FastAPI, SHAP, matplotlib), TypeScript/React (Next.js 14, Tailwind CSS), Redis/PostgreSQL caching

---

## Phase 1: Backend Integration (30 minutes)

### Task 1: Merge Explainability Module

**Files:**
- Copy: `../explainability-implementation/src/sentiment_detector/explainability/` → `src/sentiment_detector/explainability/`
- Copy: `../explainability-implementation/src/sentiment_detector/api/routes/explainability.py` → `src/sentiment_detector/api/routes/explainability.py`
- Modify: `src/sentiment_detector/api/__init__.py` or `src/sentiment_detector/main.py`

**Step 1: Copy explainability module**

```bash
cp -r ../explainability-implementation/src/sentiment_detector/explainability src/sentiment_detector/
```

Expected: Directory `src/sentiment_detector/explainability/` created with 5 files (__init__.py, explainer.py, cache.py, events.py, viz.py)

**Step 2: Copy API router**

```bash
cp ../explainability-implementation/src/sentiment_detector/api/routes/explainability.py src/sentiment_detector/api/routes/
```

Expected: File `src/sentiment_detector/api/routes/explainability.py` created (13KB file)

**Step 3: Verify files copied correctly**

```bash
ls -la src/sentiment_detector/explainability/
ls -la src/sentiment_detector/api/routes/explainability.py
```

Expected: Shows all 5 explainability files + router file

**Step 4: Check API router registration**

Read `src/sentiment_detector/main.py` to see if explainability router already registered

Look for imports like: `from .api.routes import explainability`

**Step 5: Register router if needed**

If not already registered, add to `src/sentiment_detector/main.py`:

```python
from sentiment_detector.api.routes import explainability

# In app setup section (after other routers):
app.include_router(explainability.router, prefix="/api/v1", tags=["explainability"])
```

**Step 6: Commit backend merge**

```bash
git add src/sentiment_detector/explainability/ src/sentiment_detector/api/routes/explainability.py src/sentiment_detector/main.py
git commit -m "feat: merge SHAP explainability module

- Add core explainer with SHAP TreeExplainer
- Add two-tier caching (Redis L1, PostgreSQL L2)
- Add crisis event definitions (6 events)
- Add waterfall plot generation
- Add 5 API endpoints at /api/v1/explainability/*"
```

---

### Task 2: Verify Dependencies

**Files:**
- Read: `pyproject.toml`
- Modify: `pyproject.toml` (if needed)

**Step 1: Check for SHAP and matplotlib**

```bash
grep -E "(shap|matplotlib)" pyproject.toml
```

Expected: Should show `shap = ">=0.44.0"` and `matplotlib = ">=3.8.0"`

**Step 2: Add dependencies if missing**

If not found, add to `[project.dependencies]` in `pyproject.toml`:

```toml
shap = ">=0.44.0"
matplotlib = ">=3.8.0"
```

**Step 3: Install dependencies (if added)**

```bash
pip install -e .
```

Expected: Dependencies installed successfully

**Step 4: Commit if pyproject.toml changed**

```bash
git add pyproject.toml
git commit -m "chore: add SHAP and matplotlib dependencies"
```

---

### Task 3: Test API Endpoints

**Files:**
- Test: Backend API

**Step 1: Start API server**

```bash
python -m sentiment_detector.main &
sleep 5
```

Expected: Server starts on port 8000

**Step 2: Test /explainability/current**

```bash
curl -s http://localhost:8000/api/v1/explainability/current | python -m json.tool | head -30
```

Expected: JSON with predicted_regime, confidence, waterfall_plot, top_features

**Step 3: Test /explainability/events**

```bash
curl -s http://localhost:8000/api/v1/explainability/events | python -m json.tool
```

Expected: Array of 6 crisis events

**Step 4: Stop server**

```bash
pkill -f "sentiment_detector.main"
```

**Step 5: Create test documentation**

Create `docs/implementation/explainability-api-tests.md`:

```markdown
# API Test Results

Date: 2026-02-05

## Endpoints Verified

✅ GET /api/v1/explainability/current
✅ GET /api/v1/explainability/events
✅ GET /api/v1/explainability/events/{event_id}

## Performance
- Cold start: ~200ms
- Cached: ~5ms
```

**Step 6: Commit test docs**

```bash
git add docs/implementation/explainability-api-tests.md
git commit -m "docs: add API endpoint test results"
```

---

## Phase 2: Frontend Types (15 minutes)

### Task 4: Create TypeScript Types

**Files:**
- Create: `frontend/src/types/explainability.ts`

**Step 1: Create types file**

```typescript
export interface ExplanationResponse {
  predicted_regime: 'risk_on' | 'risk_off' | 'transition'
  confidence: number
  timestamp: string
  model_version: string
  waterfall_plot: string
  top_features: TopFeature[]
  shap_values: number[]
  feature_names: string[]
  base_value: number
  prediction: number
}

export interface TopFeature {
  name: string
  display_name: string
  value: number
  shap_value: number
  contribution_pct: number
}

export interface CrisisEvent {
  event_id: string
  name: string
  date: string
  description: string
  ciss_peak: number
  vix_peak: number
}

export interface EventsListResponse {
  events: CrisisEvent[]
}

export interface EventDetailResponse {
  event: CrisisEvent
  explanation: ExplanationResponse
}
```

**Step 2: Verify TypeScript compiles**

```bash
cd frontend && npx tsc --noEmit
```

Expected: No errors

**Step 3: Commit types**

```bash
git add frontend/src/types/explainability.ts
git commit -m "feat(frontend): add explainability TypeScript types"
```

---

### Task 5: Extend API Client

**Files:**
- Modify: `frontend/src/services/api.ts`

**Step 1: Add imports**

Add to import section at top:

```typescript
import type {
  ExplanationResponse,
  CrisisEvent,
  EventsListResponse,
  EventDetailResponse,
} from '@/types/explainability'
```

**Step 2: Add explainabilityApi**

Add at end of file (after healthApi):

```typescript
export const explainabilityApi = {
  async getCurrentExplanation(): Promise<ExplanationResponse> {
    return fetchApi<ExplanationResponse>('/explainability/current')
  },

  async getEventsList(): Promise<CrisisEvent[]> {
    const response = await fetchApi<EventsListResponse>('/explainability/events')
    return response.events
  },

  async getEventExplanation(eventId: string): Promise<EventDetailResponse> {
    return fetchApi<EventDetailResponse>(`/explainability/events/${eventId}`)
  },
}
```

**Step 3: Verify TypeScript compiles**

```bash
cd frontend && npx tsc --noEmit
```

Expected: No errors

**Step 4: Commit API client**

```bash
git add frontend/src/services/api.ts
git commit -m "feat(frontend): add explainability API client methods"
```

---

## Phase 3: Modal Component (2 hours)

### Task 6: Create Modal Shell

**Files:**
- Create: `frontend/src/components/ExplainabilityModal.tsx`

**Step 1: Create component with basic structure**

See full component code in design document section "Task 6"

Key sections:
- Props interface (isOpen, onClose, regime, confidence)
- State for explanation, loading, error
- useEffect to fetch on open
- Modal backdrop and container
- Header with regime and confidence
- Content area with placeholders
- Footer with model info

**Step 2: Verify compiles**

```bash
cd frontend && npx tsc --noEmit
```

**Step 3: Commit shell**

```bash
git add frontend/src/components/ExplainabilityModal.tsx
git commit -m "feat(frontend): create ExplainabilityModal shell component"
```

---

### Task 7: Add Waterfall Plot

**Files:**
- Modify: `frontend/src/components/ExplainabilityModal.tsx`

**Step 1: Replace waterfall plot placeholder**

Replace the placeholder div with:

```typescript
<div className="lg:col-span-2">
  <h3 className="text-lg font-semibold text-gray-900 mb-4">
    Feature Contributions
  </h3>
  <div className="bg-white rounded-lg border border-gray-200 overflow-hidden">
    {explanation.waterfall_plot ? (
      <img
        src={explanation.waterfall_plot}
        alt="SHAP Waterfall Plot"
        className="w-full h-auto"
      />
    ) : (
      <div className="p-8 text-center text-gray-500">
        No visualization available
      </div>
    )}
  </div>
  <p className="mt-2 text-sm text-gray-600">
    Shows how features push prediction from base value to final value
  </p>
</div>
```

**Step 2: Verify compiles**

```bash
cd frontend && npx tsc --noEmit
```

**Step 3: Commit waterfall plot**

```bash
git add frontend/src/components/ExplainabilityModal.tsx
git commit -m "feat(frontend): add waterfall plot image display"
```

---

### Task 8: Add Features Table

**Files:**
- Modify: `frontend/src/components/ExplainabilityModal.tsx`

**Step 1: Add sorted features helper**

After state declarations:

```typescript
const sortedFeatures = explanation?.top_features
  ? [...explanation.top_features].sort((a, b) =>
      Math.abs(b.shap_value) - Math.abs(a.shap_value)
    )
  : []
```

**Step 2: Replace features table placeholder**

Replace with full table implementation (see design doc Task 8)

Key elements:
- Sticky header
- Top 10 features only
- Display name + technical name
- Value column
- SHAP impact with green/red color coding

**Step 3: Verify compiles**

```bash
cd frontend && npx tsc --noEmit
```

**Step 4: Commit table**

```bash
git add frontend/src/components/ExplainabilityModal.tsx
git commit -m "feat(frontend): add top features table with color-coded impacts"
```

---

### Task 9: Add Loading Skeleton

**Files:**
- Modify: `frontend/src/components/ExplainabilityModal.tsx`

**Step 1: Improve loading state**

Replace loading div with skeleton:

```typescript
{loading && (
  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
    <div className="lg:col-span-2">
      <div className="h-4 bg-gray-200 rounded w-48 mb-4 animate-pulse"></div>
      <div className="bg-gray-100 rounded-lg h-96 animate-pulse"></div>
    </div>
    <div>
      <div className="h-4 bg-gray-200 rounded w-32 mb-4 animate-pulse"></div>
      <div className="bg-gray-100 rounded-lg h-96 animate-pulse"></div>
    </div>
  </div>
)}
```

**Step 2: Commit skeleton**

```bash
git add frontend/src/components/ExplainabilityModal.tsx
git commit -m "feat(frontend): add skeleton loading state to modal"
```

---

## Phase 4: RegimePanel Integration (30 minutes)

### Task 10: Add Explain Button

**Files:**
- Modify: `frontend/src/components/RegimePanel.tsx`

**Step 1: Add imports**

```typescript
import { useState } from 'react'
import { Lightbulb } from 'lucide-react'
import ExplainabilityModal from './ExplainabilityModal'
```

**Step 2: Add state**

After existing useState:

```typescript
const [explainModalOpen, setExplainModalOpen] = useState(false)
```

**Step 3: Add button after confidence display**

Find confidence percentage display, add button after:

```typescript
<button
  onClick={() => setExplainModalOpen(true)}
  className="mt-4 w-full inline-flex items-center justify-center px-4 py-2
             border border-gray-300 shadow-sm text-sm font-medium rounded-md
             text-gray-700 bg-white hover:bg-gray-50
             focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500
             transition-colors"
>
  <Lightbulb className="w-4 h-4 mr-2" />
  Explain This Prediction
</button>
```

**Step 4: Add modal component**

Before closing return tag:

```typescript
<ExplainabilityModal
  isOpen={explainModalOpen}
  onClose={() => setExplainModalOpen(false)}
  regime={data?.current_regime || ''}
  confidence={data?.confidence || 0}
/>
```

**Step 5: Verify compiles**

```bash
cd frontend && npx tsc --noEmit
```

**Step 6: Commit integration**

```bash
git add frontend/src/components/RegimePanel.tsx
git commit -m "feat(frontend): integrate Explain button into RegimePanel"
```

---

## Phase 5: Testing (1 hour)

### Task 11: Manual Testing

**Files:**
- Test: Full integration

**Step 1: Start backend**

```bash
python -m sentiment_detector.main
```

**Step 2: Start frontend**

```bash
cd frontend && npm run dev
```

**Step 3: Test in browser**

Navigate to http://localhost:3000

Test checklist:
- [ ] RegimePanel shows Explain button
- [ ] Click button opens modal
- [ ] Modal shows loading skeleton
- [ ] Waterfall plot displays
- [ ] Features table shows 10 items
- [ ] SHAP values are color-coded
- [ ] Close modal with X button
- [ ] Close modal with backdrop
- [ ] Close modal with Close button
- [ ] Reopen modal (should be cached/fast)

**Step 4: Test responsive**

Resize to mobile width, verify layout stacks correctly

**Step 5: Test error handling**

Stop backend, click Explain, verify error message

**Step 6: Document results**

Create `docs/implementation/manual-testing-results.md` with checklist results

**Step 7: Commit test docs**

```bash
git add docs/implementation/manual-testing-results.md
git commit -m "docs: add manual testing results"
```

---

### Task 12: Polish & Accessibility

**Files:**
- Modify: `frontend/src/components/ExplainabilityModal.tsx`

**Step 1: Add tooltips**

Wrap feature display_name with title attribute

**Step 2: Add responsive text**

Change h2 to `text-xl sm:text-2xl`

**Step 3: Add aria-labels**

Add to close button: `aria-label="Close explanation modal"`

**Step 4: Commit polish**

```bash
git add frontend/src/components/ExplainabilityModal.tsx
git commit -m "refactor(frontend): add tooltips and accessibility improvements"
```

---

## Phase 6: Optional - Historical Events (5-7 hours)

### Task 13: Create Events Page

**Files:**
- Create: `frontend/src/app/explainability/page.tsx`

**Step 1: Create directory**

```bash
mkdir -p frontend/src/app/explainability
```

**Step 2: Create page component**

See full code in design doc Task 13

Key features:
- Fetch events list on mount
- Grid layout (3 columns desktop, 1 mobile)
- Event cards with name, date, description
- CISS/VIX peaks display
- "View Explanation" button per card

**Step 3: Test page**

Navigate to http://localhost:3000/explainability

**Step 4: Commit page**

```bash
git add frontend/src/app/explainability/
git commit -m "feat(frontend): create historical events explorer page"
```

---

### Task 14: Create Event Detail Modal

**Files:**
- Create: `frontend/src/components/EventDetailModal.tsx`

**Step 1: Create component**

Similar to ExplainabilityModal but:
- Takes eventId prop
- Fetches event detail on open
- Shows "What Happened?" section
- Shows event date instead of computed time

See full code in design doc Task 14

**Step 2: Commit modal**

```bash
git add frontend/src/components/EventDetailModal.tsx
git commit -m "feat(frontend): create EventDetailModal component"
```

---

### Task 15: Wire Up Events to Modal

**Files:**
- Modify: `frontend/src/app/explainability/page.tsx`

**Step 1: Add state**

```typescript
const [selectedEventId, setSelectedEventId] = useState<string | null>(null)
const [modalOpen, setModalOpen] = useState(false)
```

**Step 2: Update button handler**

```typescript
onClick={() => {
  setSelectedEventId(event.event_id)
  setModalOpen(true)
}}
```

**Step 3: Add modal**

```typescript
<EventDetailModal
  isOpen={modalOpen}
  onClose={() => {
    setModalOpen(false)
    setSelectedEventId(null)
  }}
  eventId={selectedEventId}
/>
```

**Step 4: Test clicking events**

**Step 5: Commit wiring**

```bash
git add frontend/src/app/explainability/page.tsx
git commit -m "feat(frontend): wire event cards to detail modal"
```

---

### Task 16: Add Navigation

**Files:**
- Modify: `frontend/src/components/ExplainabilityModal.tsx`

**Step 1: Add link in modal footer**

Before Close button:

```typescript
<a href="/explainability" className="text-sm text-indigo-600 hover:underline">
  View Historical Events
</a>
```

**Step 2: Commit navigation**

```bash
git add frontend/src/components/ExplainabilityModal.tsx
git commit -m "feat(frontend): add navigation to historical events"
```

---

## Final Tasks

### Task 17: Final Verification

**Files:**
- Create: `docs/implementation/final-checklist.md`

**Step 1: Run all checks**

```bash
# TypeScript
cd frontend && npx tsc --noEmit

# Backend tests (if available)
pytest tests/ -k explainability -v

# Git status
git status
```

**Step 2: Create final checklist**

Document all completed features and test results

**Step 3: Commit checklist**

```bash
git add docs/implementation/final-checklist.md
git commit -m "docs: add final integration checklist"
```

---

### Task 18: Prepare for Merge

**Files:**
- None

**Step 1: Verify clean state**

```bash
git status
```

Expected: "working tree clean"

**Step 2: Push branch**

```bash
git push -u origin feature/explainability-production-integration
```

**Step 3: Use finishing-a-development-branch skill**

```
@superpowers:finishing-a-development-branch
```

This will guide you through:
- Creating PR vs direct merge
- Worktree cleanup
- Next steps

---

## Summary

**Total Time Estimate:**
- Phase 1 (Backend): 30 min
- Phase 2 (Types): 15 min
- Phase 3 (Modal): 2 hours
- Phase 4 (Integration): 30 min
- Phase 5 (Testing): 1 hour
- **Phase 1-5 Total: 4.25 hours**
- Phase 6 (Optional Events): 5-7 hours
- **Complete Total: 9-11 hours**

**Key Success Criteria:**
- ✅ Explainability module merged
- ✅ API endpoints working
- ✅ Modal displays waterfall + features
- ✅ Explain button in RegimePanel
- ✅ All tests passing
- ✅ TypeScript compiles
- ✅ Manual testing complete
