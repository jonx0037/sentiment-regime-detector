#!/bin/bash
# =============================================================================
# Automated Data Collection for Sentiment Regime Detector
# =============================================================================
# This script is designed to run via cron and handles:
# - Environment setup
# - Data collection from configured sources
# - Logging with timestamps
# - Error notification (optional)
#
# Crontab entry (every 4 hours):
#   0 */4 * * * /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/scripts/cron_collect.sh >> /Users/jonathanrocha/Documents/SMU/DS_6210_Capstone/logs/cron_collect.log 2>&1
#
# =============================================================================

set -e

# Configuration
PROJECT_DIR="/Users/jonathanrocha/Documents/SMU/DS_6210_Capstone"
VENV_PATH="$PROJECT_DIR/.venv"
LOG_DIR="$PROJECT_DIR/logs"
DATA_DIR="$PROJECT_DIR/data/raw/scheduled"

# Create directories if needed
mkdir -p "$LOG_DIR"
mkdir -p "$DATA_DIR"

# Timestamp for this run
TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
OUTPUT_FILE="$DATA_DIR/collection_${TIMESTAMP}.json"

# Log function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "=========================================="
log "Starting scheduled data collection"
log "=========================================="

# Change to project directory
cd "$PROJECT_DIR"

# Activate virtual environment
source "$VENV_PATH/bin/activate"

# Set Python path
export PYTHONPATH="$PROJECT_DIR/src:$PYTHONPATH"

# Load environment variables using python-dotenv (safer for complex values)
# Don't source .env directly as it may contain special characters
log "Environment loaded via python-dotenv"

# Run collection (RSS + Twitter - the real-time sources)
# Kaggle data is static/historical, so we skip it in scheduled runs
log "Collecting from RSS feeds and Twitter..."

python scripts/collect_multi_source.py \
    --sources twitter,rss \
    --limit 100 \
    --output "$OUTPUT_FILE" \
    --days 1

# Check if collection succeeded
if [ -f "$OUTPUT_FILE" ]; then
    ITEM_COUNT=$(python -c "import json; data=json.load(open('$OUTPUT_FILE')); print(data['total_items'])")
    FILE_SIZE=$(ls -lh "$OUTPUT_FILE" | awk '{print $5}')
    log "Collection successful: $ITEM_COUNT items ($FILE_SIZE)"
    
    # Import to database if we have items
    if [ "$ITEM_COUNT" -gt 0 ]; then
        log "Importing to PostgreSQL..."
        
        # Use the import script (need to create a simple one for raw data)
        python scripts/import_collected_data.py --input "$OUTPUT_FILE"
        
        log "Import complete"
    else
        log "No items collected, skipping import"
    fi
else
    log "ERROR: Collection failed - no output file created"
    exit 1
fi

# Cleanup old collection files (keep last 7 days)
log "Cleaning up old collection files..."
find "$DATA_DIR" -name "collection_*.json" -mtime +7 -delete

log "=========================================="
log "Scheduled collection complete"
log "=========================================="
