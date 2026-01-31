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

# Setup - Use the actual uploaded directory name
PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector-hpc-20260131"
cd $PROJECT_DIR

# Load modules - using the pytorch environment which has CUDA and all dependencies
module load python/3.11.11/pytorch

# Add user-installed packages to path
export PATH="$HOME/.local/bin:$PATH"
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

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
python3 --version
python3 -c "import torch; print(f'PyTorch: {torch.__version__}, CUDA: {torch.cuda.is_available()}')"
pip show transformers | grep -E "Name|Version"

# Verify files exist
echo -e "\n2b. Verifying files..."
ls -la scripts/process_kaggle_sentiment.py || echo "ERROR: process_kaggle_sentiment.py not found!"
ls -la data/kaggle/ | head -5 || echo "ERROR: data/kaggle not found!"

# Run the Kaggle sentiment processing
echo -e "\n3. Starting Kaggle sentiment processing..."
echo "Processing all 218,702 items with ensemble (FinBERT + RoBERTa)"

python3 scripts/process_kaggle_sentiment.py \
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
