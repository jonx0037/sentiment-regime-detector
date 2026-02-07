#!/bin/bash
# =============================================================================
# FINBERT HPC DEPLOYMENT SCRIPT
# Upload batch files and submit FinBERT job to ManeFrame III
# =============================================================================
# Usage: ./deploy_finbert_hpc.sh
# =============================================================================

set -e

# Configuration
LOCAL_PROJECT="/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone"
HPC_USER="jarocha"
HPC_HOST="m3.smu.edu"  # CORRECT HOSTNAME
HPC_BASE="/lustre/scratch/client/users/jarocha/sentiment-detector"

echo "=============================================="
echo "FinBERT HPC Deployment to ManeFrame III"
echo "=============================================="
echo "Local project: $LOCAL_PROJECT"
echo "HPC target: $HPC_USER@$HPC_HOST:$HPC_BASE"
echo ""

# Step 1: Test connection
echo "📡 Step 1: Testing SSH connection..."
if ssh -o ConnectTimeout=10 "$HPC_USER@$HPC_HOST" "echo 'Connection successful'" 2>/dev/null; then
    echo "✅ SSH connection successful"
else
    echo "❌ SSH connection failed"
    echo ""
    echo "Troubleshooting tips:"
    echo "  1. Connect to SMU VPN (GlobalProtect) if off-campus"
    echo "  2. Use Duo push authentication when prompted"
    echo "  3. Try: ssh $HPC_USER@$HPC_HOST"
    exit 1
fi
echo ""

# Step 2: Create directories on HPC
echo "📁 Step 2: Creating directories on HPC..."
ssh "$HPC_USER@$HPC_HOST" "
    mkdir -p $HPC_BASE/data/batches
    mkdir -p $HPC_BASE/data/processed
    mkdir -p $HPC_BASE/scripts
    mkdir -p $HPC_BASE/logs
    mkdir -p $HPC_BASE/checkpoints
"
echo "✅ Directories created"
echo ""

# Step 3: Upload batch files
echo "📤 Step 3: Uploading batch files (30 files, ~450MB)..."
echo "   This may take a few minutes..."
rsync -avz --progress \
    "$LOCAL_PROJECT/data/hpc_batches/"*.json \
    "$HPC_USER@$HPC_HOST:$HPC_BASE/data/batches/"
echo "✅ Batch files uploaded"
echo ""

# Step 4: Upload scripts
echo "📤 Step 4: Uploading HPC scripts..."
rsync -avz \
    "$LOCAL_PROJECT/scripts/hpc/batch_sentiment.py" \
    "$LOCAL_PROJECT/scripts/hpc/run_finbert_batch.sh" \
    "$LOCAL_PROJECT/scripts/hpc/requirements_hpc.txt" \
    "$HPC_USER@$HPC_HOST:$HPC_BASE/scripts/"
echo "✅ Scripts uploaded"
echo ""

# Step 5: Set up environment
echo "🔧 Step 5: Setting up Python environment..."
ssh "$HPC_USER@$HPC_HOST" "
    cd $HPC_BASE
    
    # Load modules
    module purge
    module load python/3.10
    module load cuda/11.8
    
    # Create venv if not exists
    if [ ! -d 'venv' ]; then
        echo 'Creating virtual environment...'
        python -m venv venv
    fi
    
    # Activate and install dependencies
    source venv/bin/activate
    pip install --upgrade pip
    pip install torch transformers pandas tqdm numpy
"
echo "✅ Environment ready"
echo ""

# Step 6: Verify batch files
echo "📊 Step 6: Verifying uploaded data..."
ssh "$HPC_USER@$HPC_HOST" "
    echo 'Batch files:'
    ls -lh $HPC_BASE/data/batches/*.json | wc -l
    echo 'Total size:'
    du -sh $HPC_BASE/data/batches/
"
echo ""

echo "=============================================="
echo "🎉 Deployment Complete!"
echo "=============================================="
echo ""
echo "Next steps:"
echo ""
echo "1. SSH to ManeFrame:"
echo "   ssh $HPC_USER@$HPC_HOST"
echo ""
echo "2. Navigate to project:"
echo "   cd $HPC_BASE"
echo ""
echo "3. Submit FinBERT job:"
echo "   sbatch scripts/run_finbert_batch.sh"
echo ""
echo "4. Monitor job:"
echo "   squeue -u $HPC_USER"
echo "   tail -f logs/finbert_batch_*.out"
echo ""
echo "5. Download results when complete:"
echo "   scp -r $HPC_USER@$HPC_HOST:$HPC_BASE/data/processed ."
echo ""
