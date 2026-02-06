#!/bin/bash
# Seed production database with essential market data for explainability
#
# Usage:
#   ./scripts/admin/seed_production.sh
#
# This script populates the Railway production database with:
# 1. ECB CISS stress indices (2006-2026)
# 2. VIX volatility data (2006-2026)
# 3. SPY market data for regime classification
#
# Prerequisites:
# - Railway CLI configured and linked to project
# - Data files in data/kaggle/ecb-ciss/ directory
# - Python dependencies installed

set -e  # Exit on error

echo "🚀 Seeding Production Database for SHAP Explainability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Get production database URL from Railway
echo "📡 Getting production database URL from Railway..."
PROD_DATABASE_URL=$(railway variables get DATABASE_URL 2>&1)

if [ $? -ne 0 ] || [ -z "$PROD_DATABASE_URL" ]; then
    echo "❌ Error: Could not get DATABASE_URL from Railway"
    echo "   Make sure you're logged in with: railway login"
    echo "   And linked to the project with: railway link"
    exit 1
fi

echo "✅ Connected to production database"
echo ""

# Export for Python scripts
export DATABASE_URL="$PROD_DATABASE_URL"

echo "Step 1: Importing ECB CISS data..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "scripts/data_import/import_ecb_ciss.py" ]; then
    python scripts/data_import/import_ecb_ciss.py
    echo "✅ CISS data imported"
else
    echo "⚠️  Warning: import_ecb_ciss.py not found, skipping"
fi
echo ""

echo "Step 2: Collecting VIX data..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "scripts/data_collection/collect_vix_data.py" ]; then
    python scripts/data_collection/collect_vix_data.py \
        --start-date 2006-01-01 \
        --end-date 2026-02-06 \
        --output data/vix_historical.json
    echo "✅ VIX data collected"
else
    echo "⚠️  Warning: collect_vix_data.py not found, skipping"
fi
echo ""

echo "Step 3: Downloading SPY market data..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "scripts/data_collection/download_spy_data.py" ]; then
    python scripts/data_collection/download_spy_data.py
    echo "✅ SPY data downloaded"
else
    echo "⚠️  Warning: download_spy_data.py not found, skipping"
fi
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Production Database Seeded!"
echo ""
echo "✅ Next Steps:"
echo "   1. Test explainability endpoints:"
echo "      curl https://sentiment-regime-detector-production.up.railway.app/api/v1/explainability/current"
echo ""
echo "   2. Open the frontend and click Explain/History buttons"
echo "      https://sentiment-regime-detector.vercel.app"
echo ""
echo "   3. Verify the SHAP waterfall plots appear correctly"
echo ""
