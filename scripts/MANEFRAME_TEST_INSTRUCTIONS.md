# MANEFRAME Access Test Instructions

**Date**: January 30, 2026  
**User**: jarocha  
**Account**: jcheun_ds6210_1262_401_0001

## Quick Reference

- **Home Directory**: `/users/jarocha` (limited space, ~10GB)
- **Scratch Directory**: `/lustre/scratch/client/users/jarocha` (large workspace, use for data)
- **Web Portal**: <https://hpc.m3.smu.edu/>

## Step-by-Step Test Process

### Step 1: SSH Connection Test

```bash
# From your local machine
ssh jarocha@m3.smu.edu

# You should see a welcome message and be at the MANEFRAME prompt
# Something like: [jarocha@login001 ~]$
```

### Step 2: Initial Setup

Once logged in via SSH, run these commands:

```bash
# Check current location
pwd
# Should show: /users/jarocha

# List your files
ls -la

# Check scratch space
ls -la /lustre/scratch/client/users/jarocha

# Create project directory in scratch space
mkdir -p /lustre/scratch/client/users/jarocha/sentiment-detector
cd /lustre/scratch/client/users/jarocha/sentiment-detector

# Verify you're in the right place
pwd
```

### Step 3: Upload Test Scripts

From your **local machine** (open a new terminal tab):

```bash
# Navigate to the scripts directory
cd ~/Documents/SMU/DS_6210_Capstone/scripts

# Copy test scripts to MANEFRAME
scp test_maneframe.sh jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/
scp test_maneframe_gpu.sh jarocha@m3.smu.edu:/lustre/scratch/client/users/jarocha/sentiment-detector/

# Verify upload
ssh jarocha@m3.smu.edu "ls -lh /lustre/scratch/client/users/jarocha/sentiment-detector/"
```

### Step 4: Run Basic Test

Back in your SSH session on MANEFRAME:

```bash
# Navigate to project directory
cd /lustre/scratch/client/users/jarocha/sentiment-detector

# Make scripts executable
chmod +x test_maneframe.sh test_maneframe_gpu.sh

# Submit basic test job
sbatch test_maneframe.sh

# Check job status
squeue -u jarocha

# The job should complete quickly (1-2 minutes)
# Check output when done
ls -lt test_maneframe*.out test_maneframe*.err
cat test_maneframe_*.out
```

### Step 5: Run GPU Test

```bash
# Submit GPU test job
sbatch test_maneframe_gpu.sh

# Monitor job
squeue -u jarocha

# Check output when complete
cat test_gpu_*.out

# If there are errors, check error file
cat test_gpu_*.err
```

### Step 6: Check Module System

```bash
# List available modules
module avail

# Look for Python and CUDA
module avail python
module avail cuda

# Try loading modules
module load python/3.9
module load cuda/11.8

# Verify
python --version
nvcc --version
```

### Step 7: Test Conda (if available)

```bash
# Check if conda is available
which conda

# If not available, check if we can load it
module load anaconda3

# Create test environment
conda create -n test_env python=3.9 -y
conda activate test_env

# Test installation
pip install numpy pandas

# Deactivate
conda deactivate
```

## Common Commands Reference

### Job Management

```bash
# Submit job
sbatch script.sh

# Check job status
squeue -u jarocha

# Check detailed job info
scontrol show job <job_id>

# Cancel job
scancel <job_id>

# View completed jobs
sacct -u jarocha --format=JobID,JobName,Partition,State,ExitCode,Start,End

# Check account balance
sbalance -u jarocha
```

### File Management

```bash
# Check disk usage
du -sh /users/jarocha
du -sh /lustre/scratch/client/users/jarocha

# Check quotas
quota -s

# Find large files
find /users/jarocha -type f -size +100M -exec ls -lh {} \;
```

### Module System

```bash
# List loaded modules
module list

# Load module
module load <module_name>

# Unload module
module unload <module_name>

# Reset to defaults
module purge
```

## Expected Results

### Basic Test (test_maneframe.sh)

✓ Job completes successfully  
✓ Shows hostname and user info  
✓ Lists available Python/CUDA modules  
✓ Shows disk space  
✓ Creates test directory and file  
✓ All SLURM environment variables are set

### GPU Test (test_maneframe_gpu.sh)

✓ Job runs on GPU node  
✓ `nvidia-smi` shows GPU information  
✓ CUDA module loads successfully  
✓ `nvcc` is available

## Troubleshooting

### If SSH Fails

- Check VPN connection (SMU VPN required if off-campus)
- Verify username: `jarocha`
- Try: `ssh jarocha@m3.smu.edu` or `ssh jarocha@maneframe.smu.edu`

### If Job Fails

- Check error file: `cat test_maneframe_*.err`
- Verify account name in script matches: `jcheun_ds6210_1262_401_0001`
- Check job queue: `squeue -u jarocha`
- Look at job details: `scontrol show job <job_id>`

### If GPU Not Available

- Check partition names: `sinfo`
- Try different GPU partition: `#SBATCH -p gpu` or `#SBATCH -p gpgpu-1`
- Check GPU availability: `sinfo -p development-gpu`

### If No Modules Found

- Some HPC systems use different module names
- Try: `module spider python` to search all modules
- Check documentation: <https://www.smu.edu/OIT/Services/HPC>

## Next Steps After Successful Tests

1. ✓ Verify all tests pass
2. Set up Python environment for project
3. Upload project code and requirements
4. Test data pipeline components
5. Run small-scale sentiment analysis test
6. Scale up to full dataset

## Resources

- MANEFRAME Documentation: <https://www.smu.edu/OIT/Services/HPC>
- Allocation Portal: <https://hpcaccess.smu.edu/allocation/1448/>
- Web Interface: <https://hpc.m3.smu.edu/>
- Support: <help@smu.edu>
