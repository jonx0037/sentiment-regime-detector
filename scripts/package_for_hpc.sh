#!/bin/bash
# Package project for MANEFRAME HPC transfer
# Creates a tarball with code and data for upload

set -e

PROJECT_DIR="/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone"
PACKAGE_NAME="sentiment-detector-hpc-$(date +%Y%m%d)"
PACKAGE_DIR="/tmp/${PACKAGE_NAME}"
TARBALL="${PROJECT_DIR}/${PACKAGE_NAME}.tar.gz"

echo "=============================================="
echo "Packaging Project for MANEFRAME"
echo "=============================================="

# Create package directory
rm -rf "$PACKAGE_DIR"
mkdir -p "$PACKAGE_DIR"

echo "1. Copying source code..."
cp -r "$PROJECT_DIR/src" "$PACKAGE_DIR/"
cp -r "$PROJECT_DIR/scripts" "$PACKAGE_DIR/"
cp "$PROJECT_DIR/pyproject.toml" "$PACKAGE_DIR/"
cp "$PROJECT_DIR/requirements.txt" "$PACKAGE_DIR/"

echo "2. Copying Kaggle data..."
mkdir -p "$PACKAGE_DIR/data/kaggle"
cp -r "$PROJECT_DIR/data/kaggle"/* "$PACKAGE_DIR/data/kaggle/" 2>/dev/null || true

echo "3. Copying processed data (if exists)..."
mkdir -p "$PACKAGE_DIR/data/processed"
cp "$PROJECT_DIR/data/processed/vix_regimes.json" "$PACKAGE_DIR/data/processed/" 2>/dev/null || true

echo "4. Creating HPC setup script..."
cat > "$PACKAGE_DIR/setup_hpc.sh" << 'EOF'
#!/bin/bash
# Setup script for MANEFRAME HPC
# Run this after extracting the tarball on MANEFRAME

set -e

echo "=============================================="
echo "Setting up Sentiment Regime Detector on MANEFRAME"
echo "=============================================="

# Show available Python versions
echo ""
echo "1. Finding Python modules..."
module spider python 2>&1 | grep -E "python/[0-9]" | head -10 || true

# Try to load Python (try multiple versions)
echo ""
echo "2. Loading Python module..."
if module load python/3.11 2>/dev/null; then
    echo "   Loaded python/3.11"
elif module load python/3.10 2>/dev/null; then
    echo "   Loaded python/3.10"
elif module load python/3.9 2>/dev/null; then
    echo "   Loaded python/3.9"
else
    echo "   Using system Python"
fi

# Load CUDA
echo ""
echo "3. Loading CUDA module..."
module load cuda/11.8 2>/dev/null || module load cuda 2>/dev/null || echo "   CUDA not loaded (will use CPU)"

# Show what we loaded
echo ""
echo "4. Environment:"
python3 --version
which python3

# Create virtual environment
echo ""
echo "5. Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
echo ""
echo "6. Installing dependencies..."
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install transformers pandas numpy scipy scikit-learn arch yfinance

echo ""
echo "=============================================="
echo "Setup complete!"
echo "=============================================="
echo ""
echo "To activate: source .venv/bin/activate"
echo "To run job:  sbatch scripts/hpc/run_kaggle_sentiment.sh"
EOF
chmod +x "$PACKAGE_DIR/setup_hpc.sh"

echo "5. Creating tarball..."
cd /tmp
tar -czf "$TARBALL" "$PACKAGE_NAME"

echo ""
echo "=============================================="
echo "Package created: $TARBALL"
echo "=============================================="
echo ""
echo "To upload to MANEFRAME:"
echo "  scp $TARBALL jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/"
echo ""
echo "On MANEFRAME:"
echo "  cd /lustre/scratch/client/users/jarocha"
echo "  tar -xzf ${PACKAGE_NAME}.tar.gz"
echo "  cd ${PACKAGE_NAME}"
echo "  ./setup_hpc.sh"
echo ""

# Show package size
ls -lh "$TARBALL"

# Cleanup
rm -rf "$PACKAGE_DIR"
