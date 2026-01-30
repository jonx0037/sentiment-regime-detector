#!/bin/bash
#SBATCH -J setup_env              # Job name
#SBATCH -o setup_env_%j.out       # Output file
#SBATCH -e setup_env_%j.err       # Error file
#SBATCH -p dev                    # Use dev partition
#SBATCH -N 1                      # 1 node
#SBATCH -n 4                      # 4 cores for faster pip
#SBATCH --mem=16G                 # Memory
#SBATCH -t 00:30:00               # 30 min limit
#SBATCH -A jcheun_ds6210_1262_401_0001

# ============================================================
# MANEFRAME Environment Setup Script
# Sentiment Regime Detector Project
# Date: January 30, 2026
# ============================================================

echo "=============================================="
echo "Setting up Python Environment"
echo "Date: $(date)"
echo "=============================================="

# Set project directory
PROJECT_DIR="/lustre/scratch/client/users/jarocha/sentiment-detector"
cd $PROJECT_DIR

# Load PyTorch module (includes Python 3.11, PyTorch, CUDA support)
echo -e "\n1. Loading Python/PyTorch module..."
module purge
module load python/3.11.11/pytorch/2025.08.21
echo "Module loaded successfully"

# Check Python and PyTorch
echo -e "\n2. Verifying Python environment..."
python --version
python -c "import torch; print(f'PyTorch: {torch.__version__}')"
python -c "import torch; print(f'CUDA available: {torch.cuda.is_available()}')"

# Create virtual environment for additional packages
echo -e "\n3. Creating virtual environment..."
VENV_DIR="$PROJECT_DIR/venv"
if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment already exists, activating..."
else
    python -m venv $VENV_DIR --system-site-packages
    echo "Virtual environment created"
fi

source $VENV_DIR/bin/activate
echo "Virtual environment activated: $VIRTUAL_ENV"

# Upgrade pip
echo -e "\n4. Upgrading pip..."
pip install --upgrade pip --quiet

# Install additional requirements
echo -e "\n5. Installing project dependencies..."
pip install -r $PROJECT_DIR/requirements_hpc.txt --quiet

# Verify key packages
echo -e "\n6. Verifying installed packages..."
python -c "import transformers; print(f'Transformers: {transformers.__version__}')"
python -c "import pandas; print(f'Pandas: {pandas.__version__}')"
python -c "import sklearn; print(f'Scikit-learn: {sklearn.__version__}')"
python -c "import tqdm; print(f'tqdm: {tqdm.__version__}')"

# Download NLTK data (if needed)
echo -e "\n7. Downloading NLTK data..."
python -c "
import nltk
import os
nltk_data_dir = '$PROJECT_DIR/nltk_data'
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.download('punkt', download_dir=nltk_data_dir, quiet=True)
nltk.download('stopwords', download_dir=nltk_data_dir, quiet=True)
nltk.download('vader_lexicon', download_dir=nltk_data_dir, quiet=True)
print('NLTK data downloaded')
"

# Create directory structure
echo -e "\n8. Creating project directories..."
mkdir -p $PROJECT_DIR/data/raw
mkdir -p $PROJECT_DIR/data/processed
mkdir -p $PROJECT_DIR/models
mkdir -p $PROJECT_DIR/outputs
mkdir -p $PROJECT_DIR/logs
echo "Directories created"

# Create activation script for future use
echo -e "\n9. Creating activation helper..."
cat > $PROJECT_DIR/activate_env.sh << 'EOF'
#!/bin/bash
# Quick environment activation script
module purge
module load python/3.11.11/pytorch/2025.08.21
source /lustre/scratch/client/users/jarocha/sentiment-detector/venv/bin/activate
export NLTK_DATA=/lustre/scratch/client/users/jarocha/sentiment-detector/nltk_data
export PROJECT_DIR=/lustre/scratch/client/users/jarocha/sentiment-detector
cd $PROJECT_DIR
echo "Environment activated. Python: $(python --version)"
EOF
chmod +x $PROJECT_DIR/activate_env.sh

echo -e "\n=============================================="
echo "Environment Setup Complete!"
echo ""
echo "To activate in future sessions, run:"
echo "  source $PROJECT_DIR/activate_env.sh"
echo "=============================================="
