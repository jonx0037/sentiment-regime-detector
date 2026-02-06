#!/bin/bash
# Seed production database with essential market data for explainability
#
# Usage:
#   ./scripts/admin/seed_production_v2.sh
#
# This uses 'railway run' to execute scripts with production env vars

set -e  # Exit on error

echo "🚀 Seeding Production Database for SHAP Explainability"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Verify Railway CLI is ready
echo "📡 Verifying Railway CLI setup..."
railway status > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "❌ Error: Not linked to Railway project"
    echo "   Run: railway link"
    exit 1
fi
echo "✅ Railway CLI ready"
echo ""

# Step 1: Import CISS data
echo "Step 1: Importing ECB CISS stress indices (2006-2026)..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ -f "scripts/data_import/import_ecb_ciss.py" ]; then
    railway run python scripts/data_import/import_ecb_ciss.py
    if [ $? -eq 0 ]; then
        echo "✅ CISS data imported successfully"
    else
        echo "⚠️  CISS import had issues (may be already imported)"
    fi
else
    echo "⚠️  Script not found: scripts/data_import/import_ecb_ciss.py"
fi
echo ""

# Step 2: Check if VIX data collection works
echo "Step 2: Checking VIX data availability..."
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Note: VIX data needs to be collected and imported separately"
echo "The production database should populate VIX from market_data table"
echo ""

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 CISS Data Seeded!"
echo ""
echo "✅ Next Steps:"
echo ""
echo "1. Test if data is available:"
echo "   railway run python -c \"from sentiment_detector.core.database import get_db; import asyncio; from sqlalchemy import text; async def check(): db = get_db(); async with db() as session: result = await session.execute(text('SELECT COUNT(*) FROM stress_indices')); print(f'CISS records: {result.scalar()}'); asyncio.run(check())\""
echo ""
echo "2. Test explainability endpoint:"
echo "   curl https://sentiment-regime-detector-production.up.railway.app/api/v1/explainability/current"
echo ""
echo "3. If endpoint still fails, you may need to populate VIX data separately"
echo ""
