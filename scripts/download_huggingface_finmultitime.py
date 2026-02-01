#!/usr/bin/env python3
"""
Download FinMultiTime dataset from HuggingFace.

NOTE (2026-02-01): The FinMultiTime dataset requires special handling due to 
its multimodal nature (images, text, tables, time series). The dataset is 
available at:
- HuggingFace: Wenyan0110/Multimodal-Dataset-Image_Text_Table_TimeSeries-for-Financial-Time-Series-Forecasting
- Paper: arXiv:2506.05019

For manual download, visit the HuggingFace page directly and use Git LFS:
    git lfs install
    git clone https://huggingface.co/datasets/Wenyan0110/Multimodal-Dataset-Image_Text_Table_TimeSeries-for-Financial-Time-Series-Forecasting

Coverage: S&P 500 and HS 300 stocks, 2009-2025, ~112.6 GB total
"""

import os
import sys

try:
    from huggingface_hub import snapshot_download
    
    finmulti_dir = 'data/kaggle/huggingface/finmultitime'
    os.makedirs(finmulti_dir, exist_ok=True)
    
    print('Attempting to download FinMultiTime dataset via snapshot_download...')
    print('Note: This is a large multimodal dataset (~112GB), may require significant time and space.')
    
    # Try snapshot download which handles large files better
    path = snapshot_download(
        repo_id="Wenyan0110/Multimodal-Dataset-Image_Text_Table_TimeSeries-for-Financial-Time-Series-Forecasting",
        repo_type="dataset",
        local_dir=finmulti_dir,
        ignore_patterns=["*.png", "*.jpg", "*.jpeg"],  # Skip images to reduce download size
    )
    print(f'Downloaded to: {path}')
    
except Exception as e:
    print(f'Error downloading FinMultiTime: {e}')
    print('\nManual download instructions:')
    print('  1. Install Git LFS: brew install git-lfs && git lfs install')
    print('  2. Clone: git clone https://huggingface.co/datasets/Wenyan0110/Multimodal-Dataset-Image_Text_Table_TimeSeries-for-Financial-Time-Series-Forecasting')
    print('  3. Move to: data/kaggle/huggingface/finmultitime/')
    sys.exit(1)

if __name__ == '__main__':
    pass
