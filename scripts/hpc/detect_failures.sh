#!/bin/bash
#
# Failure Detection Script for HPC Pipeline
# Identifies failed batches across all pipeline phases
#
# Usage:
#   bash scripts/hpc/detect_failures.sh collection
#   bash scripts/hpc/detect_failures.sh sentiment
#   bash scripts/hpc/detect_failures.sh garch
#   bash scripts/hpc/detect_failures.sh regime
#

set -euo pipefail

PHASE=$1
LOG_DIR="logs"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "========================================"
echo "Failure Detection Report"
echo "Phase: $PHASE"
echo "Timestamp: $(date)"
echo "========================================"

# Define patterns for each phase
case $PHASE in
  collection)
    PATTERN="collect_*.out"
    SUCCESS_MARKER="Collection complete for batch"
    RETRY_SCRIPT="run_collection_retry.sh"
    ;;
  sentiment)
    PATTERN="process_*.out"
    SUCCESS_MARKER="Sentiment processing complete"
    RETRY_SCRIPT="run_sentiment_retry.sh"
    ;;
  garch)
    PATTERN="garch_midas_*.out"
    SUCCESS_MARKER="GARCH-MIDAS complete"
    RETRY_SCRIPT="run_garch_midas.sh"
    ;;
  regime)
    PATTERN="regime_class_*.out"
    SUCCESS_MARKER="Regime classification complete"
    RETRY_SCRIPT="run_regime_classification.sh"
    ;;
  *)
    echo -e "${RED}Error: Unknown phase '$PHASE'${NC}"
    echo "Valid phases: collection, sentiment, garch, regime"
    exit 1
    ;;
esac

echo ""
echo "Checking logs in $LOG_DIR/$PATTERN..."
echo ""

# Arrays to track different failure types
declare -a failed_jobs=()
declare -a oom_jobs=()
declare -a network_jobs=()
declare -a disk_jobs=()
declare -a rate_limit_jobs=()
declare -a timeout_jobs=()
declare -a unknown_jobs=()

total_jobs=0
successful_jobs=0

# Check each log file
for log_file in $LOG_DIR/$PATTERN; do
  if [ ! -f "$log_file" ]; then
    continue
  fi

  ((total_jobs++))

  # Extract job/batch ID from filename
  batch_id=$(basename "$log_file" | grep -oP '\d+' | head -1)

  # Check if job completed successfully
  if grep -q "$SUCCESS_MARKER" "$log_file" 2>/dev/null; then
    ((successful_jobs++))
    continue
  fi

  # Job failed - determine failure type
  failed_jobs+=("$batch_id")

  # Check for specific error patterns
  error_log="${log_file%.out}.err"

  if [ -f "$error_log" ]; then
    if grep -qi "CUDA out of memory\|OOM killed" "$error_log"; then
      oom_jobs+=("$batch_id")
      echo -e "${RED}❌ Batch $batch_id: GPU Out of Memory${NC}"

    elif grep -qi "TimeoutError\|Connection.*timeout\|timed out" "$error_log"; then
      timeout_jobs+=("$batch_id")
      network_jobs+=("$batch_id")
      echo -e "${YELLOW}❌ Batch $batch_id: Network Timeout${NC}"

    elif grep -qi "Connection.*refused\|Connection.*reset\|Network.*unreachable" "$error_log"; then
      network_jobs+=("$batch_id")
      echo -e "${YELLOW}❌ Batch $batch_id: Network Connection Error${NC}"

    elif grep -qi "No space left\|Disk quota exceeded" "$error_log"; then
      disk_jobs+=("$batch_id")
      echo -e "${RED}❌ Batch $batch_id: Disk Space Error${NC}"

    elif grep -qi "rate limit\|429\|Too many requests" "$error_log"; then
      rate_limit_jobs+=("$batch_id")
      echo -e "${YELLOW}❌ Batch $batch_id: API Rate Limit${NC}"

    elif grep -qi "TIME LIMIT\|DUE TO TIME LIMIT" "$error_log"; then
      timeout_jobs+=("$batch_id")
      echo -e "${YELLOW}❌ Batch $batch_id: Job Time Limit Exceeded${NC}"

    elif grep -qi "ModuleNotFoundError\|ImportError\|No module named" "$error_log"; then
      unknown_jobs+=("$batch_id")
      echo -e "${RED}❌ Batch $batch_id: Missing Dependencies${NC}"

    else
      unknown_jobs+=("$batch_id")
      echo -e "${RED}❌ Batch $batch_id: Unknown Error${NC}"
      # Show first error line for unknown failures
      error_line=$(grep -i "error" "$error_log" | head -1)
      if [ -n "$error_line" ]; then
        echo -e "${RED}   └─ ${error_line:0:80}${NC}"
      fi
    fi
  else
    unknown_jobs+=("$batch_id")
    echo -e "${RED}❌ Batch $batch_id: No error log found${NC}"
  fi
done

# Summary statistics
echo ""
echo "========================================"
echo "Summary:"
echo "========================================"
echo -e "Total jobs:       $total_jobs"
echo -e "${GREEN}Successful:       $successful_jobs${NC}"
echo -e "${RED}Failed:           ${#failed_jobs[@]}${NC}"
echo ""

if [ ${#failed_jobs[@]} -gt 0 ]; then
  echo "Failure breakdown:"
  [ ${#oom_jobs[@]} -gt 0 ] && echo -e "  ${RED}GPU OOM:          ${#oom_jobs[@]}${NC}"
  [ ${#network_jobs[@]} -gt 0 ] && echo -e "  ${YELLOW}Network errors:   ${#network_jobs[@]}${NC}"
  [ ${#disk_jobs[@]} -gt 0 ] && echo -e "  ${RED}Disk space:       ${#disk_jobs[@]}${NC}"
  [ ${#rate_limit_jobs[@]} -gt 0 ] && echo -e "  ${YELLOW}Rate limits:      ${#rate_limit_jobs[@]}${NC}"
  [ ${#timeout_jobs[@]} -gt 0 ] && echo -e "  ${YELLOW}Timeouts:         ${#timeout_jobs[@]}${NC}"
  [ ${#unknown_jobs[@]} -gt 0 ] && echo -e "  ${RED}Unknown:          ${#unknown_jobs[@]}${NC}"
fi

echo "========================================"

# Provide recovery instructions
if [ ${#failed_jobs[@]} -gt 0 ]; then
  echo ""
  echo "Recovery Actions:"
  echo "========================================"

  # Convert array to comma-separated string
  failed_batch_ids=$(IFS=,; echo "${failed_jobs[*]}")

  echo ""
  echo "1. Review specific errors:"
  echo "   cat logs/${PHASE}_*.err | grep -i error"
  echo ""

  # Specific recommendations based on error types
  if [ ${#oom_jobs[@]} -gt 0 ]; then
    echo "2. For GPU OOM errors:"
    echo "   - Reduce batch size in processing script"
    echo "   - Edit scripts/hpc/process_sentiment_batch.py"
    echo "   - Change: BATCH_SIZE = 32  # Was 64"
    echo ""
  fi

  if [ ${#rate_limit_jobs[@]} -gt 0 ]; then
    echo "2. For API rate limit errors:"
    echo "   - Reduce parallelism (max 10 concurrent jobs):"
    echo "   - sbatch --array=${failed_batch_ids}%10 scripts/hpc/$RETRY_SCRIPT"
    echo ""
  fi

  if [ ${#disk_jobs[@]} -gt 0 ]; then
    echo "2. For disk space errors:"
    echo "   - Check space: df -h /scratch/jarocha"
    echo "   - Clean temp files: find /scratch/jarocha -name '*.tmp' -delete"
    echo "   - Archive logs: tar -czf logs_backup.tar.gz logs/*.out logs/*.err"
    echo ""
  fi

  if [ ${#timeout_jobs[@]} -gt 0 ]; then
    echo "2. For timeout errors:"
    echo "   - Jobs will resume from checkpoint automatically"
    echo "   - If needed, increase time limit in retry script"
    echo ""
  fi

  echo "3. Retry all failed batches:"
  echo "   sbatch --array=${failed_batch_ids} scripts/hpc/$RETRY_SCRIPT"
  echo ""

  echo "4. Or retry with reduced parallelism:"
  echo "   sbatch --array=${failed_batch_ids}%5 scripts/hpc/$RETRY_SCRIPT"
  echo ""

  echo "5. Monitor retry progress:"
  echo "   watch -n 30 'squeue -u \$USER'"
  echo ""

  # Output failed batch IDs for programmatic use
  echo "Failed batch IDs: ${failed_batch_ids}"

  exit 1
else
  echo ""
  echo -e "${GREEN}✅ All batches completed successfully!${NC}"
  echo ""
  echo "Next steps:"
  case $PHASE in
    collection)
      echo "  1. Validate collected data:"
      echo "     python scripts/hpc/validate_pipeline_phase.py --phase collection --path /scratch/jarocha/sentiment_regime_data/raw_data"
      echo ""
      echo "  2. Start sentiment processing:"
      echo "     sbatch scripts/hpc/run_sentiment_processing.sh"
      ;;
    sentiment)
      echo "  1. Validate sentiment results:"
      echo "     python scripts/hpc/validate_pipeline_phase.py --phase sentiment --path /scratch/jarocha/sentiment_regime_data/sentiment_results"
      echo ""
      echo "  2. Aggregate results:"
      echo "     python scripts/hpc/aggregate_all_sentiment.py"
      ;;
    garch)
      echo "  1. Validate GARCH-MIDAS results:"
      echo "     head -20 /scratch/jarocha/sentiment_regime_data/volatility_forecasts.csv"
      echo ""
      echo "  2. Run regime classification:"
      echo "     sbatch scripts/hpc/run_regime_classification.sh"
      ;;
    regime)
      echo "  1. Validate regime predictions:"
      echo "     python scripts/hpc/validate_pipeline_phase.py --phase final --path /scratch/jarocha/sentiment_regime_data/regime_predictions.csv"
      echo ""
      echo "  2. Start backtesting:"
      echo "     python scripts/backtesting/run_historical_backtests_ml.py"
      ;;
  esac

  exit 0
fi
