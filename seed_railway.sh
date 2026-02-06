#!/bin/bash
# This script will be uploaded and run on Railway
# It imports CISS data directly from within the Railway environment

set -e

echo "🚀 Importing CISS data to Railway database..."

# Install pandas if not already installed
pip install pandas psycopg2-binary > /dev/null 2>&1

# Run the import
python scripts/admin/import_ciss_production.py

echo "✅ Import complete!"
