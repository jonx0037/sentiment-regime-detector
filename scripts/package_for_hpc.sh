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

echo "Setting up Sentiment Regime Detector on MANEFRAME"

# Load modules
module load python/3.12
module load cuda/11.8

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt

echo "Setup complete! Activate with: source .venv/bin/activate"
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
