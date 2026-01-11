# requirements-hpc.txt

```txt
# HPC-optimized versions
torch==2.0.1+cpu  # CPU version for HPC
transformers==4.30.2
pandas==2.0.3
numpy==1.24.3
scikit-learn==1.3.0
scipy==1.11.1
tqdm==4.65.0
```

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
   tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
   model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
```
