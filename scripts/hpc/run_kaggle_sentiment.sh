#!/bin/bash
#SBATCH -J kaggle_sentiment       # Job name
#SBATCH -o logs/kaggle_sentiment_%j.out  # Output file
#SBATCH -e logs/kaggle_sentiment_%j.err  # Error file
#SBATCH -p fp-gpgpu-3             # Production GPU partition (7 day limit)
#SBATCH -N 1                      # 1 node
#SBATCH -n 8                      # 8 CPU cores
#SBATCH --gres=gpu:1              # 1 GPU
#SBATCH --mem=48G                 # Memory (need more for ensemble)
#SBATCH -t 24:00:00               # 24 hour limit for 218K items
#SBATCH -A jcheun_ds6210_1262_401_0001
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --mail-user=jarocha@mail.smu.edu

# ============================================================
# Kaggle Sentiment Processing with Ensemble Models
# Processes all 218K Kaggle items through FinBERT + RoBERTa
# ============================================================

echo "=============================================="
echo "Kaggle Sentiment Processing (Full Dataset)"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start: $(date)"
echo "=============================================="

# Setup
PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector"
cd $PROJECT_DIR

# Load modules
module load cuda/11.8
module load python/3.12

# Activate virtual environment
source $PROJECT_DIR/.venv/bin/activate

# Create output directories
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/data/processed

# Show resources
echo -e "\n1. Resources allocated:"
echo "CPUs: $SLURM_CPUS_ON_NODE"
echo "Memory: $SLURM_MEM_PER_NODE"
nvidia-smi --query-gpu=name,memory.total,memory.free --format=csv,noheader

# Check Python environment
echo -e "\n2. Python environment:"
python --version
pip show transformers torch | grep -E "Name|Version"

# Run the Kaggle sentiment processing
echo -e "\n3. Starting Kaggle sentiment processing..."
echo "Processing all 218,702 items with ensemble (FinBERT + RoBERTa)"

python scripts/process_kaggle_sentiment.py \
    --kaggle-dir data/kaggle \
    --output data/processed/kaggle_sentiment_full.json \
    --batch-size 200 \
    2>&1 | tee logs/kaggle_sentiment_${SLURM_JOB_ID}.log

# Check output
echo -e "\n4. Output summary:"
if [ -f data/processed/kaggle_sentiment_full.json ]; then
    echo "Output file created successfully"
    ls -lh data/processed/kaggle_sentiment_full.json
    echo "First 50 lines:"
    head -50 data/processed/kaggle_sentiment_full.json
else
    echo "ERROR: Output file not created!"
fi

echo -e "\n=============================================="
echo "Kaggle Sentiment Processing Completed"
echo "End: $(date)"
echo "=============================================="
