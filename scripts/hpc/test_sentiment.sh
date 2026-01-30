#!/bin/bash
#SBATCH -J sentiment_test         # Job name
#SBATCH -o sentiment_test_%j.out  # Output file
#SBATCH -e sentiment_test_%j.err  # Error file
#SBATCH -p gpu-dev                # GPU dev partition for testing
#SBATCH -N 1                      # 1 node
#SBATCH -n 4                      # 4 CPU cores
#SBATCH --gres=gpu:1              # 1 GPU
#SBATCH --mem=16G                 # Memory
#SBATCH -t 00:30:00               # 30 min for testing
#SBATCH -A jcheun_ds6210_1262_401_0001

# ============================================================
# Sentiment Analysis Test Job
# Tests the sentiment engine on sample data
# ============================================================

echo "=============================================="
echo "Sentiment Analysis Test Job"
echo "Date: $(date)"
echo "=============================================="

# Setup environment
PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector"
source $PROJECT_DIR/activate_env.sh

# Show GPU info
echo -e "\n1. GPU Information:"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv

# Test sentiment engine
echo -e "\n2. Testing Sentiment Engine..."
python << 'PYTHON_SCRIPT'
import torch
import time
from transformers import pipeline

print(f"PyTorch version: {torch.__version__}")
print(f"CUDA available: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")

# Test texts
test_texts = [
    "The stock market surged today with record-breaking gains across all sectors.",
    "Investors are worried about the economic downturn and rising inflation.",
    "The Federal Reserve announced it will maintain current interest rates.",
    "Breaking: Major bank reports significant losses in Q4 earnings.",
    "Tech stocks rally as AI investments continue to drive growth.",
]

# Load FinBERT (finance-specific)
print("\n3. Loading FinBERT model...")
start = time.time()
device = 0 if torch.cuda.is_available() else -1
classifier = pipeline(
    "sentiment-analysis", 
    model="ProsusAI/finbert",
    device=device,
    truncation=True,
    max_length=512
)
print(f"Model loaded in {time.time() - start:.2f} seconds")

# Run inference
print("\n4. Running sentiment analysis...")
start = time.time()
results = classifier(test_texts)
inference_time = time.time() - start

print(f"Inference completed in {inference_time:.2f} seconds")
print(f"Throughput: {len(test_texts) / inference_time:.1f} texts/second")

# Display results
print("\n5. Results:")
print("-" * 60)
for text, result in zip(test_texts, results):
    label = result['label']
    score = result['score']
    print(f"[{label:>8}] ({score:.3f}) {text[:50]}...")
print("-" * 60)

# Memory stats
if torch.cuda.is_available():
    print(f"\nGPU Memory used: {torch.cuda.memory_allocated(0) / 1e9:.2f} GB")
    print(f"GPU Memory cached: {torch.cuda.memory_reserved(0) / 1e9:.2f} GB")

print("\n✓ Sentiment analysis test completed successfully!")
PYTHON_SCRIPT

echo -e "\n=============================================="
echo "Test Job Completed"
echo "=============================================="
