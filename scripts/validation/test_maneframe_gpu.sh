#!/bin/bash
#SBATCH -J test_gpu                # Job name
#SBATCH -o test_gpu_%j.out         # Output file
#SBATCH -e test_gpu_%j.err         # Error file
#SBATCH -p gpu-dev                 # GPU partition (gpu-dev for testing, 4hr limit)
#SBATCH -N 1                       # Number of nodes
#SBATCH -n 1                       # Number of tasks
#SBATCH --gres=gpu:1               # Request 1 GPU
#SBATCH --mem=8G                   # Memory allocation
#SBATCH -t 00:05:00                # Time limit (5 minutes)
#SBATCH -A jcheun_ds6210_1262_401_0001  # Your slurm account

# GPU Test Script for MANEFRAME
# Purpose: Verify GPU access and CUDA functionality

echo "=========================================="
echo "MANEFRAME GPU Test Job Started"
echo "Date: $(date)"
echo "=========================================="

# 1. Check GPU visibility
echo -e "\n1. GPU Information:"
nvidia-smi 2>/dev/null || echo "nvidia-smi not available"

# 2. Load CUDA module
echo -e "\n2. Loading CUDA Module:"
module load cuda/11.8
echo "CUDA module loaded"

# 3. Check CUDA compiler
echo -e "\n3. NVCC Version:"
nvcc --version 2>/dev/null || echo "nvcc not found"

# 4. Environment variables
echo -e "\n4. CUDA Environment:"
echo "CUDA_HOME: $CUDA_HOME"
echo "CUDA_PATH: $CUDA_PATH"

echo -e "\n=========================================="
echo "GPU Test Job Completed"
echo "=========================================="
