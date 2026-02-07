#!/bin/bash
#
# HPC Pipeline Progress Dashboard
# Real-time monitoring of job status, file output, and resource usage
#
# Usage:
#   bash scripts/hpc/monitor_progress.sh collection
#   bash scripts/hpc/monitor_progress.sh sentiment
#   watch -n 60 'bash scripts/hpc/monitor_progress.sh collection'
#

set -euo pipefail

PHASE=${1:-"collection"}

# Color codes
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

clear
echo "========================================"
echo -e "${BLUE}HPC Pipeline Progress Dashboard${NC}"
echo "Phase: $PHASE"
echo "Timestamp: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"
echo ""

# Job status
echo "📊 Job Status:"
job_states=$(squeue -u $USER -h -o "%T" 2>/dev/null | sort | uniq -c)

if [ -n "$job_states" ]; then
  echo "$job_states" | while read count state; do
    case $state in
      RUNNING)   echo -e "  ${GREEN}🟢 Running:${NC}    $count" ;;
      PENDING)   echo -e "  ${YELLOW}🟡 Pending:${NC}    $count" ;;
      COMPLETED) echo -e "  ${GREEN}✅ Completed:${NC}  $count" ;;
      FAILED)    echo -e "  ${RED}❌ Failed:${NC}     $count" ;;
      TIMEOUT)   echo -e "  ${RED}⏱️  Timeout:${NC}    $count" ;;
      *)         echo "  ⚪ $state:     $count" ;;
    esac
  done

  total_jobs=$(squeue -u $USER -h 2>/dev/null | wc -l)
  echo "  📈 Total active: $total_jobs"
else
  echo "  No active jobs"
fi

echo ""

# File output progress
case $PHASE in
  collection)
    output_dir="/scratch/$USER/sentiment_regime_data/raw_data"
    expected_files=72
    pattern="*.parquet"
    ;;
  sentiment)
    output_dir="/scratch/$USER/sentiment_regime_data/sentiment_results"
    expected_files=72
    pattern="daily_batch_*.csv"
    ;;
  garch)
    output_dir="/scratch/$USER/sentiment_regime_data"
    expected_files=1
    pattern="volatility_forecasts.csv"
    ;;
  regime)
    output_dir="/scratch/$USER/sentiment_regime_data"
    expected_files=1
    pattern="regime_predictions.csv"
    ;;
  *)
    output_dir=""
    expected_files=0
    pattern=""
    ;;
esac

if [ -d "$output_dir" ] && [ -n "$pattern" ]; then
  completed_files=$(find "$output_dir" -name "$pattern" 2>/dev/null | wc -l)
  percent=$((completed_files * 100 / expected_files))

  echo "📁 Output Files:"
  echo "  Completed: $completed_files / $expected_files ($percent%)"

  # Progress bar
  bar_length=40
  filled=$((completed_files * bar_length / expected_files))
  empty=$((bar_length - filled))

  # Build progress bar
  bar=""
  for ((i=0; i<filled; i++)); do bar+="█"; done
  for ((i=0; i<empty; i++)); do bar+="░"; done

  # Color code based on progress
  if [ $percent -ge 100 ]; then
    echo -e "  [${GREEN}${bar}${NC}] $percent%"
  elif [ $percent -ge 50 ]; then
    echo -e "  [${YELLOW}${bar}${NC}] $percent%"
  else
    echo -e "  [${RED}${bar}${NC}] $percent%"
  fi

  # Sample recent file
  recent_file=$(find "$output_dir" -name "$pattern" -type f 2>/dev/null | head -1)
  if [ -n "$recent_file" ]; then
    file_size=$(du -h "$recent_file" | cut -f1)
    file_time=$(stat -f "%Sm" -t "%Y-%m-%d %H:%M" "$recent_file" 2>/dev/null || stat -c "%y" "$recent_file" 2>/dev/null | cut -d. -f1)
    echo "  Latest: $(basename $recent_file) ($file_size, $file_time)"
  fi
else
  echo "📁 Output Files:"
  echo "  Directory not found or phase unknown"
fi

echo ""

# Disk usage
echo "💾 Disk Usage:"
if [ -d "$output_dir" ]; then
  data_size=$(du -sh "$output_dir" 2>/dev/null | cut -f1)
  echo "  Data: $data_size"
fi

if [ -d "logs" ]; then
  log_size=$(du -sh logs 2>/dev/null | cut -f1)
  echo "  Logs: $log_size"
fi

# Check scratch space
scratch_info=$(df -h /scratch/$USER 2>/dev/null | tail -1)
if [ -n "$scratch_info" ]; then
  free_space=$(echo "$scratch_info" | awk '{print $4}')
  used_pct=$(echo "$scratch_info" | awk '{print $5}')

  # Warn if space is low
  used_num=$(echo "$used_pct" | tr -d '%')
  if [ "$used_num" -ge 90 ]; then
    echo -e "  ${RED}Free: $free_space ($used_pct used) ⚠️  LOW SPACE${NC}"
  else
    echo "  Free: $free_space ($used_pct used)"
  fi
fi

echo ""

# Recent errors (last 5)
echo "⚠️  Recent Errors:"
if [ -d "logs" ]; then
  recent_errors=$(grep -i "error\|fail\|exception" logs/*.err 2>/dev/null | \
                  grep -v "No error\|0 errors\|without error" | \
                  tail -5)

  if [ -n "$recent_errors" ]; then
    echo "$recent_errors" | while IFS= read -r line; do
      # Truncate long lines
      truncated=$(echo "$line" | cut -c1-80)
      echo -e "  ${RED}${truncated}${NC}"
    done
  else
    echo -e "  ${GREEN}None in recent logs ✓${NC}"
  fi
else
  echo "  No logs directory"
fi

echo ""

# Performance metrics (if available)
if [ "$PHASE" = "sentiment" ] && [ -d "logs" ]; then
  echo "⚡ Performance Metrics:"

  # Extract processing rate from recent logs
  rate=$(grep -h "texts/sec" logs/process_*.out 2>/dev/null | tail -1 | grep -oP '\d+\.\d+(?= texts/sec)' || echo "")
  if [ -n "$rate" ]; then
    echo "  Processing rate: ${rate} texts/sec"
  fi

  # GPU utilization (if available in logs)
  gpu_util=$(grep -h "GPU Utilization" logs/process_*.out 2>/dev/null | tail -1 | grep -oP '\d+(?=%)' || echo "")
  if [ -n "$gpu_util" ]; then
    if [ "$gpu_util" -ge 80 ]; then
      echo -e "  ${GREEN}GPU utilization: ${gpu_util}% ✓${NC}"
    elif [ "$gpu_util" -ge 50 ]; then
      echo -e "  ${YELLOW}GPU utilization: ${gpu_util}%${NC}"
    else
      echo -e "  ${RED}GPU utilization: ${gpu_util}% ⚠️${NC}"
    fi
  fi

  echo ""
fi

# Estimated completion time
if [ -d "$output_dir" ] && [ $expected_files -gt 0 ] && [ $completed_files -gt 0 ]; then
  echo "⏱️  Estimated Completion:"

  # Get oldest checkpoint to estimate start time
  oldest_checkpoint=$(find logs -name "checkpoint_*.json" -type f 2>/dev/null | head -1)
  if [ -f "$oldest_checkpoint" ]; then
    start_epoch=$(stat -f "%B" "$oldest_checkpoint" 2>/dev/null || stat -c "%Y" "$oldest_checkpoint" 2>/dev/null)
    current_epoch=$(date +%s)
    elapsed=$((current_epoch - start_epoch))

    # Calculate rate and ETA
    if [ $elapsed -gt 0 ]; then
      rate_per_sec=$(echo "scale=6; $completed_files / $elapsed" | bc)
      remaining=$((expected_files - completed_files))
      eta_seconds=$(echo "$remaining / $rate_per_sec" | bc)

      # Format ETA
      eta_hours=$((eta_seconds / 3600))
      eta_mins=$(((eta_seconds % 3600) / 60))

      completion_epoch=$((current_epoch + eta_seconds))
      completion_time=$(date -r $completion_epoch '+%Y-%m-%d %H:%M' 2>/dev/null || date -d "@$completion_epoch" '+%Y-%m-%d %H:%M' 2>/dev/null)

      echo "  Elapsed: $((elapsed / 3600))h $((elapsed % 3600 / 60))m"
      echo "  Remaining: ~${eta_hours}h ${eta_mins}m"
      echo "  ETA: $completion_time"
    fi
  fi

  echo ""
fi

# Action commands
echo "========================================"
echo "Commands:"
echo "  Detailed errors:  bash scripts/hpc/detect_failures.sh $PHASE"
echo "  Check logs:       tail -f logs/${PHASE}_*.out"
echo "  Validate:         python scripts/hpc/validate_pipeline_phase.py --phase $PHASE --path $output_dir"

if [ "$PHASE" = "sentiment" ]; then
  echo "  GPU status:       srun --partition=gpu-a100 --gres=gpu:1 nvidia-smi"
fi

echo "========================================"
