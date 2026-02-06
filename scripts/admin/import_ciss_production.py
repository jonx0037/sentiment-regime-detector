#!/usr/bin/env python3
"""
Import CISS data directly to production database.
Wraps the import_ecb_ciss.py script with correct database URL handling.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root / "src"))

# Get DATABASE_URL from environment (injected by Railway)
database_url = os.getenv("DATABASE_URL")
if not database_url:
    print("❌ Error: DATABASE_URL not set")
    print("   This script should be run with: railway run python scripts/admin/import_ciss_production.py")
    sys.exit(1)

# Convert async URL to sync URL if needed
if "+asyncpg" in database_url:
    # Replace postgresql+asyncpg:// with postgresql://
    database_url = database_url.replace("postgresql+asyncpg://", "postgresql://")
    print(f"✅ Converted async URL to sync URL for import")

# Set the sync URL for the import script
os.environ["DATABASE_URL"] = database_url

# Import and run the CISS import
sys.path.insert(0, str(project_root / "scripts" / "data_import"))

print("🚀 Starting CISS data import to production...")
print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

try:
    # Import the module
    import import_ecb_ciss

    # Find the data file
    data_path = project_root / "data" / "kaggle" / "ecb-ciss"

    # Load data
    print(f"📂 Loading CISS data from: {data_path}")
    df = import_ecb_ciss.load_ecb_ciss_data(data_path)

    # Analyze
    print("\n📊 Analyzing crisis periods...")
    analysis = import_ecb_ciss.analyze_crisis_periods(df)
    print(f"   Total observations: {analysis['total_observations']}")
    print(f"   High stress days: {analysis['high_stress_days']} ({analysis['high_stress_pct']:.1f}%)")
    print(f"   Crisis days: {analysis['crisis_days']} ({analysis['crisis_pct']:.1f}%)")
    print(f"   Max CISS: {analysis['max_ciss']:.3f} on {analysis['max_ciss_date']}")

    # Import to database
    print("\n💾 Importing to production database...")
    result = import_ecb_ciss.import_to_database(df, database_url)

    if result == 0:
        print("\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print("✅ CISS data successfully imported to production!")
        print(f"   Records: {len(df)}")
        print(f"   Date range: {df['date'].min()} to {df['date'].max()}")
        print("\n🎯 Next: Test the explainability endpoint")
        print("   curl https://sentiment-regime-detector-production.up.railway.app/api/v1/explainability/current")
    else:
        print(f"\n⚠️  Import completed with status code: {result}")
        sys.exit(result)

except Exception as e:
    print(f"\n❌ Error during import: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
