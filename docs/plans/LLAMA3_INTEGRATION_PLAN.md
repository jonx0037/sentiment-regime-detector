# Llama 3 Integration Plan

**Date:** February 6, 2026
**Status:** HIGH PRIORITY - 3 weeks overdue
**Goal:** Integrate Llama 3 into the sentiment ensemble pipeline

---

## 🎯 Current Status

### ✅ What's Already Done
- `src/sentiment_detector/models/llama_sentiment.py` - **Complete implementation** (419 lines)
- Support for multiple backends:
  - ✅ Transformers (HuggingFace)
  - ✅ llama.cpp (quantized GGUF)
  - ✅ External API (OpenRouter, Together AI)
  - ✅ Mock mode (for testing)
- ✅ `create_llama_for_ensemble()` helper function for integration
- ✅ Prompt templates for financial sentiment
- ✅ Output parsing with confidence scores

### ❌ What's Missing
- **NOT integrated into `SentimentEnsemble`**
- **NOT tested end-to-end**
- **NO HPC deployment scripts**
- **NO production model weights downloaded**

---

## 📋 Integration Checklist

### Phase 1: Local Testing (1-2 days)

#### Step 1.1: Test Llama Mock Mode
```bash
# Create test script
python -c "
from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

model = LlamaSentimentModel(backend='mock')
model.load()

result = model.predict('Bitcoin surges to new all-time high!')
print(f'Label: {result.label}, Confidence: {result.confidence}')
"
```

**Expected Output:**
```
Label: POSITIVE, Confidence: 0.7
```

#### Step 1.2: Add Llama to SentimentEnsemble
**File:** `src/sentiment_detector/models/sentiment_ensemble.py`

Add Llama as the 4th model:

```python
from sentiment_detector.models.llama_sentiment import create_llama_for_ensemble

def create_ensemble(
    use_finbert: bool = True,
    use_vader: bool = True,
    use_textblob: bool = True,
    use_llama: bool = False,  # NEW
    llama_backend: str = "mock",  # NEW
    asset_class: Optional[str] = None,
    weights: Optional[Dict[str, float]] = None
) -> SentimentEnsemble:
    """Create sentiment ensemble with optional Llama 3."""
    models = {}

    if use_finbert:
        models["finbert"] = create_finbert_model()

    if use_vader:
        models["vader"] = create_vader_model()

    if use_textblob:
        models["textblob"] = create_textblob_model()

    # NEW: Add Llama 3
    if use_llama:
        models["llama3"] = create_llama_for_ensemble(backend=llama_backend)

    return SentimentEnsemble(models=models, weights=weights)
```

#### Step 1.3: Write Integration Tests
**File:** `tests/test_models/test_llama_integration.py`

```python
import pytest
from sentiment_detector.models.llama_sentiment import LlamaSentimentModel
from sentiment_detector.models.sentiment_ensemble import create_ensemble

def test_llama_mock_backend():
    """Test Llama mock backend."""
    model = LlamaSentimentModel(backend="mock")
    model.load()

    result = model.predict("Stocks rally on positive earnings")
    assert result.label in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert 0.0 <= result.confidence <= 1.0

def test_llama_in_ensemble():
    """Test Llama integrated in ensemble."""
    ensemble = create_ensemble(
        use_finbert=False,
        use_vader=True,
        use_llama=True,
        llama_backend="mock"
    )

    result = ensemble.predict("Bitcoin crashes below $20k")
    assert result.label in ["POSITIVE", "NEGATIVE", "NEUTRAL"]
    assert "llama3" in result.model_predictions

@pytest.mark.slow
def test_llama_batch_processing():
    """Test batch processing with Llama."""
    model = LlamaSentimentModel(backend="mock")
    model.load()

    texts = [
        "Markets surge on Fed announcement",
        "Crypto winter continues",
        "Gold holds steady"
    ]

    results = model.predict_batch(texts)
    assert len(results) == 3
    assert all(r.confidence > 0 for r in results)
```

**Run tests:**
```bash
pytest tests/test_models/test_llama_integration.py -v
```

---

### Phase 2: Model Weights Download (2-3 hours)

#### Step 2.1: Download Llama 3.1 8B Instruct
```bash
# Option A: HuggingFace (requires authentication)
huggingface-cli login
huggingface-cli download meta-llama/Llama-3.1-8B-Instruct \
  --local-dir models/llama3.1-8b-instruct

# Option B: GGUF quantized (smaller, faster)
# Download from https://huggingface.co/TheBloke/Llama-3.1-8B-Instruct-GGUF
wget https://huggingface.co/TheBloke/Llama-3.1-8B-Instruct-GGUF/resolve/main/llama-3.1-8b-instruct.Q4_K_M.gguf \
  -O models/llama3.1-8b-instruct.Q4_K_M.gguf
```

**Disk Space Required:**
- Full model: ~16GB
- 4-bit quantized: ~4.5GB
- 8-bit quantized: ~8.5GB

**Recommendation:** Use 4-bit quantized for development, full model for HPC.

#### Step 2.2: Test with Real Weights
```python
# Test transformers backend
from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

model = LlamaSentimentModel(
    model_id="models/llama3.1-8b-instruct",
    backend="transformers",
    quantization="4bit"  # Use 4bit for local testing
)
model.load()

result = model.predict("Tesla stock soars after Q4 earnings beat")
print(result.label, result.confidence, result.reasoning)
```

---

### Phase 3: HPC Deployment (1 day)

#### Step 3.1: Create HPC Batch Script
**File:** `scripts/hpc/run_llama_sentiment.sh`

```bash
#!/bin/bash
#SBATCH --job-name=llama_sentiment
#SBATCH --partition=gpu-a100
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --gres=gpu:a100:1
#SBATCH --time=4:00:00
#SBATCH --output=logs/llama_sentiment_%j.out
#SBATCH --error=logs/llama_sentiment_%j.err

module load python/3.11
module load cuda/12.1

# Activate virtual environment
source venv/bin/activate

# Run Llama sentiment analysis on batch
python scripts/hpc/process_batch_llama.py \
  --input data/hpc_batches/batch_$SLURM_ARRAY_TASK_ID.json \
  --output results/llama_sentiment/batch_$SLURM_ARRAY_TASK_ID.json \
  --model-path models/llama3.1-8b-instruct \
  --backend transformers \
  --quantization 4bit \
  --batch-size 8
```

#### Step 3.2: Create Processing Script
**File:** `scripts/hpc/process_batch_llama.py`

```python
#!/usr/bin/env python3
"""Process sentiment batch with Llama 3 on HPC."""

import argparse
import json
from pathlib import Path
from tqdm import tqdm

from sentiment_detector.models.llama_sentiment import LlamaSentimentModel

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input batch JSON")
    parser.add_argument("--output", required=True, help="Output results JSON")
    parser.add_argument("--model-path", required=True, help="Model path")
    parser.add_argument("--backend", default="transformers")
    parser.add_argument("--quantization", default="4bit")
    parser.add_argument("--batch-size", type=int, default=8)
    args = parser.parse_args()

    # Load model
    model = LlamaSentimentModel(
        model_id=args.model_path,
        backend=args.backend,
        quantization=args.quantization
    )
    model.load()

    # Load input batch
    with open(args.input) as f:
        texts = json.load(f)

    # Process batch
    results = []
    for text_obj in tqdm(texts, desc="Processing"):
        result = model.predict(text_obj["text"])
        results.append({
            "text_id": text_obj["id"],
            "label": result.label,
            "confidence": result.confidence,
            "reasoning": result.reasoning
        })

    # Save results
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()
```

#### Step 3.3: Submit HPC Jobs
```bash
# On ManeFrame III
sbatch --array=0-29 scripts/hpc/run_llama_sentiment.sh

# Monitor progress
squeue -u $USER
```

---

### Phase 4: Production Integration (2-3 days)

#### Step 4.1: Update API Endpoint
**File:** `src/sentiment_detector/api/routes/sentiment.py`

Add `use_llama` parameter:

```python
@router.post("/analyze")
async def analyze_sentiment(
    text: str,
    use_finbert: bool = True,
    use_vader: bool = True,
    use_textblob: bool = True,
    use_llama: bool = False,  # NEW
    session: AsyncSession = Depends(get_session)
):
    """Analyze sentiment with ensemble (optionally including Llama 3)."""
    ensemble = create_ensemble(
        use_finbert=use_finbert,
        use_vader=use_vader,
        use_textblob=use_textblob,
        use_llama=use_llama,
        llama_backend="api" if use_llama else "mock"  # Use API in production
    )

    result = ensemble.predict(text)
    return result.to_dict()
```

#### Step 4.2: Update Frontend UI
**File:** `frontend/src/components/SentimentAnalyzer.tsx`

Add Llama toggle:

```typescript
const [useLlama, setUseLlama] = useState(false);

// In the UI:
<label>
  <input
    type="checkbox"
    checked={useLlama}
    onChange={(e) => setUseLlama(e.target.checked)}
  />
  Use Llama 3 (slower, more nuanced)
</label>
```

#### Step 4.3: Configure External API (Fallback)
For production without GPU:

```bash
# .env
LLAMA_API_KEY=your_openrouter_key
LLAMA_API_URL=https://openrouter.ai/api/v1/chat/completions
```

**Cost estimate:** $0.30 per 1M tokens (OpenRouter)

---

## 🧪 Validation Plan

### Validation 1: Accuracy Comparison
Compare Llama 3 vs. existing ensemble on 1,000 labeled samples:

```python
# Script: scripts/validation/compare_llama_accuracy.py
results = {
    "finbert_only": test_ensemble(use_finbert=True, use_llama=False),
    "vader_only": test_ensemble(use_vader=True, use_llama=False),
    "llama_only": test_ensemble(use_llama=True),
    "ensemble_no_llama": test_ensemble(use_finbert=True, use_vader=True),
    "ensemble_with_llama": test_ensemble(use_finbert=True, use_vader=True, use_llama=True)
}
```

**Expected improvement:** +2-5% accuracy on nuanced/sarcastic texts (per Dakalbab et al. 2024)

### Validation 2: Performance Benchmarking
Measure inference speed:

```python
# Test on 100 texts
import time

start = time.time()
results = model.predict_batch(test_texts)
elapsed = time.time() - start

print(f"Texts/sec: {len(test_texts) / elapsed:.2f}")
```

**Target performance:**
- Mock backend: 1000+ texts/sec
- 4-bit quantized (GPU): 50-100 texts/sec
- Full model (GPU): 20-40 texts/sec
- API fallback: 5-10 texts/sec (rate limited)

### Validation 3: Crisis Event Reanalysis
Re-run 2008, COVID-19, GameStop backtests with Llama:

```bash
python scripts/backtesting/run_historical_backtests_llama.py \
  --events 2008_crisis,covid19,gamestop \
  --use-llama \
  --backend transformers
```

**Compare:** Does Llama improve regime prediction accuracy?

---

## 📊 Success Metrics

| Metric | Target | Priority |
|--------|--------|----------|
| **Integration Tests Pass** | 100% | CRITICAL |
| **Accuracy Improvement** | +2-5% | HIGH |
| **Inference Speed** | >20 texts/sec (GPU) | HIGH |
| **API Cost** | <$10/month (if using API) | MEDIUM |
| **HPC Job Success Rate** | >95% | HIGH |

---

## 🚧 Known Issues & Blockers

### Issue 1: Model Download Size
- **Problem:** 16GB model too large for local development
- **Solution:** Use 4-bit quantized GGUF (4.5GB)

### Issue 2: GPU Memory
- **Problem:** A100 has 40GB, but batch processing may OOM
- **Solution:** Set batch_size=4 with gradient checkpointing

### Issue 3: API Rate Limits
- **Problem:** OpenRouter limits to 10 req/sec
- **Solution:** Implement queue with retry logic

### Issue 4: Prompt Engineering
- **Problem:** Current prompt may not work well for all texts
- **Solution:** A/B test multiple prompt templates:
  - `SENTIMENT_PROMPT_TEMPLATE` (current)
  - `SENTIMENT_PROMPT_SIMPLE` (fallback)
  - Custom prompts for crypto vs. equity texts

---

## 📅 Timeline

| Phase | Duration | Blocker? |
|-------|----------|----------|
| **Phase 1: Local Testing** | 1-2 days | None |
| **Phase 2: Model Weights** | 2-3 hours | Download speed |
| **Phase 3: HPC Deployment** | 1 day | ManeFrame access |
| **Phase 4: Production** | 2-3 days | API costs |

**Total:** 4-6 days to full production integration

---

## 🎯 Next Actions (Priority Order)

1. ✅ **TODAY:** Run local tests with mock backend
2. ✅ **TODAY:** Write integration tests
3. 🔜 **TOMORROW:** Download 4-bit quantized model
4. 🔜 **TOMORROW:** Test with real weights locally
5. 🔜 **WEEKEND:** HPC batch processing
6. 🔜 **NEXT WEEK:** Production API integration

---

## 📚 References

### Academic Papers
- **Dakalbab et al. (2024):** "Advancing Forex Prediction Through Multimodal Text-Driven Model"
  - LLMs improve financial sentiment accuracy by 3-7%
  - Recommendation: Use Llama 3 for nuanced financial discourse

### Existing Research Summaries
- `course_files/research/summaries/finllama-financial-sentiment-classification-for-algorithmic-trading-applications_ScholarcySummary.md`
- `course_files/research/summaries/luo-w-and-gong-d-2024-pre-trained-large-language-models-for-financial-sentiment-analysis_ScholarcySummary.md`

### Technical Documentation
- Meta Llama 3 Model Card: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
- llama.cpp: https://github.com/ggerganov/llama.cpp

---

**Contact:** Jonathan Rocha (jrocha@smu.edu)
**Advisor:** David (King Ip) Lin, Ph.D. (kdlin@smu.edu)
