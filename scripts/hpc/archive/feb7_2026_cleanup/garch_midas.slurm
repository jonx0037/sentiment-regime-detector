#!/bin/bash
#SBATCH --job-name=garch_midas
#SBATCH --output=garch_midas_%j.out
#SBATCH --error=garch_midas_%j.err
#SBATCH --time=02:00:00
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --partition=standard-s
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=jarocha@smu.edu

# ============================================================
# GARCH-MIDAS with Sentiment/CISS - ManeFrame III
# ============================================================
# This script runs the full GARCH-MIDAS model with arch library
# for volatility decomposition and regime detection.
# ============================================================

echo "============================================================"
echo "GARCH-MIDAS Estimation on ManeFrame III"
echo "============================================================"
echo "Job ID: $SLURM_JOB_ID"
echo "Node: $SLURM_NODELIST"
echo "Start time: $(date)"
echo "Working directory: $(pwd)"
echo "============================================================"

# Load required modules
module purge
module load conda

# Activate base conda environment (has numpy, pandas, scipy)
source activate base

# Set up environment
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Navigate to work directory
cd $SLURM_SUBMIT_DIR

# Check for data directory
if [ ! -d "hpc_data" ]; then
    echo "ERROR: hpc_data directory not found!"
    echo "Please ensure data files are present in hpc_data/"
    exit 1
fi

# List data files
echo ""
echo "Data files available:"
ls -lh hpc_data/

# Check if arch is installed
echo ""
echo "Checking Python environment..."
python --version
which python

# Install arch if not present
python -c "import arch" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installing arch library..."
    pip install --user arch
fi

# Run the GARCH-MIDAS estimation
echo ""
echo "============================================================"
echo "Starting GARCH-MIDAS Estimation..."
echo "============================================================"

python run_garch_midas_hpc.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "============================================================"
    echo "GARCH-MIDAS Estimation Complete!"
    echo "============================================================"
    
    # List output files
    echo ""
    echo "Output files:"
    ls -lh garch_midas_results*.json 2>/dev/null || echo "No JSON output files found"
    ls -lh *.csv 2>/dev/null | head -10 || echo "No CSV output files found"
    
else
    echo ""
    echo "============================================================"
    echo "ERROR: GARCH-MIDAS Estimation Failed!"
    echo "============================================================"
    exit 1
fi

echo ""
echo "End time: $(date)"
echo "============================================================"
