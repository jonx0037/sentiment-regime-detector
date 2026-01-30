#!/bin/bash
#SBATCH -J test_maneframe          # Job name
#SBATCH -o test_maneframe_%j.out   # Output file (%j = job ID)
#SBATCH -e test_maneframe_%j.err   # Error file
#SBATCH -p dev                     # Partition (dev is default, 2hr limit)
#SBATCH -N 1                       # Number of nodes
#SBATCH -n 1                       # Number of tasks
#SBATCH --mem=4G                   # Memory allocation
#SBATCH -t 00:05:00                # Time limit (5 minutes)
#SBATCH -A jcheun_ds6210_1262_401_0001  # Your slurm account

# Test Script for MANEFRAME Access
# Date: January 30, 2026
# Purpose: Verify basic MANEFRAME functionality

echo "=========================================="
echo "MANEFRAME Test Job Started"
echo "Date: $(date)"
echo "=========================================="

# 1. Check basic system info
echo -e "\n1. System Information:"
echo "Hostname: $(hostname)"
echo "User: $(whoami)"
echo "Working Directory: $(pwd)"

# 2. Check available modules
echo -e "\n2. Available Python Modules:"
module avail python 2>&1 | grep -i python

# 3. Check CUDA availability
echo -e "\n3. Available CUDA Modules:"
module avail cuda 2>&1 | grep -i cuda

# 4. Check disk space
echo -e "\n4. Disk Space:"
echo "Home directory:"
du -sh /users/jarocha 2>/dev/null || echo "Cannot access home directory"
echo "Scratch directory:"
du -sh /lustre/scratch/client/users/jarocha 2>/dev/null || echo "Cannot access scratch directory"

# 5. Check environment
echo -e "\n5. Environment Variables:"
echo "SLURM_JOB_ID: $SLURM_JOB_ID"
echo "SLURM_JOB_NAME: $SLURM_JOB_NAME"
echo "SLURM_SUBMIT_DIR: $SLURM_SUBMIT_DIR"
echo "SLURM_JOB_NODELIST: $SLURM_JOB_NODELIST"
echo "SLURM_ACCOUNT: $SLURM_ACCOUNT"

# 6. Test Python availability
echo -e "\n6. Python Version Check:"
python3 --version 2>/dev/null || echo "Python3 not found in default path"

# 7. Create test file in scratch space
echo -e "\n7. Testing File System Write:"
TEST_DIR="/lustre/scratch/client/users/jarocha/test_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$TEST_DIR" && echo "✓ Created test directory: $TEST_DIR" || echo "✗ Failed to create test directory"

if [ -d "$TEST_DIR" ]; then
    echo "Test file content" > "$TEST_DIR/test_file.txt"
    if [ -f "$TEST_DIR/test_file.txt" ]; then
        echo "✓ Successfully wrote test file"
        cat "$TEST_DIR/test_file.txt"
    else
        echo "✗ Failed to write test file"
    fi
fi

echo -e "\n=========================================="
echo "MANEFRAME Test Job Completed"
echo "Check the output file for results"
echo "=========================================="
