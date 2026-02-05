# MANEFRAME HPC Workflow

```bash
# Email: help@smu.edu
# Subject: MANEFRAME Access Request - MSDS Capstone
# Body: [Attach proposal, request GPU node access, estimate 50-100 GPU hours]
```

```bash
# SSH into MANEFRAME
ssh <your_smu_id>@maneframe.smu.edu

# Check available modules
module avail

# Load Python/CUDA modules
module load python/3.9 cuda/11.8

# Create conda environment
conda create -n sentiment python=3.9
conda activate sentiment

# Install key packages
pip install torch transformers datasets pandas scikit-learn
```
