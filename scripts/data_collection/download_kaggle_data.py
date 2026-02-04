#!/usr/bin/env python3
"""
Download Kaggle datasets for financial sentiment analysis.

Automatically downloads popular Reddit financial datasets from Kaggle
for use with the sentiment regime detector.

Prerequisites:
    1. pip install kaggle
    2. Create Kaggle API token at: https://www.kaggle.com/settings
    3. Save kaggle.json to ~/.kaggle/kaggle.json
    4. chmod 600 ~/.kaggle/kaggle.json

Usage:
    python scripts/download_kaggle_data.py
    python scripts/download_kaggle_data.py --dataset wsb
    python scripts/download_kaggle_data.py --all
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# Available datasets
DATASETS = {
    "wsb": {
        "name": "WallStreetBets Posts",
        "slug": "gpreda/reddit-wallstreetsbets-posts",
        "size": "~50MB",
        "description": "Reddit r/wallstreetbets posts (2021-2023)",
    },
    "wsb-large": {
        "name": "WSB Full Dataset",
        "slug": "unanimad/reddit-rwallstreetbets",
        "size": "~200MB", 
        "description": "Comprehensive WSB posts with comments",
    },
    "crypto": {
        "name": "Crypto Sentiment",
        "slug": "kaushiksuresh147/cryptocurrency-sentiment-reddit",
        "size": "~30MB",
        "description": "Cryptocurrency subreddit sentiment data",
    },
    "stocks": {
        "name": "Stock Market Reddit",
        "slug": "pavellexyr/the-reddit-irl-dataset",
        "size": "~100MB",
        "description": "General stock market discussions",
    },
    "financial-news": {
        "name": "Financial News Sentiment",
        "slug": "ankurzing/sentiment-analysis-for-financial-news",
        "size": "~1MB",
        "description": "Labeled financial news headlines",
    },
}

# Default datasets to download
DEFAULT_DATASETS = ["wsb", "financial-news"]


def check_kaggle_setup():
    """Check if Kaggle is properly configured."""
    # Check if kaggle is installed
    try:
        import kaggle
    except ImportError:
        print("❌ Kaggle package not installed.")
        print("   Run: pip install kaggle")
        return False
    
    # Check for credentials
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    if not kaggle_json.exists():
        print("❌ Kaggle credentials not found!")
        print()
        print("To set up Kaggle API access:")
        print("1. Go to https://www.kaggle.com/settings")
        print("2. Scroll to 'API' section")
        print("3. Click 'Create New Token'")
        print("4. This downloads kaggle.json")
        print(f"5. Move it to: {kaggle_json}")
        print(f"6. Run: chmod 600 {kaggle_json}")
        return False
    
    # Check permissions
    if os.name != 'nt':  # Not Windows
        mode = oct(kaggle_json.stat().st_mode)[-3:]
        if mode != '600':
            print(f"⚠️  Fixing kaggle.json permissions...")
            os.chmod(kaggle_json, 0o600)
    
    print("✅ Kaggle credentials found")
    return True


def download_dataset(slug: str, output_dir: Path, name: str):
    """Download a single dataset from Kaggle."""
    print(f"\n📥 Downloading: {name}")
    print(f"   Dataset: {slug}")
    print(f"   Output: {output_dir}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Use kaggle CLI
        cmd = [
            "kaggle", "datasets", "download",
            "-d", slug,
            "-p", str(output_dir),
            "--unzip"
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )
        
        if result.returncode != 0:
            print(f"   ❌ Error: {result.stderr}")
            return False
        
        # Count downloaded files
        files = list(output_dir.glob("*"))
        total_size = sum(f.stat().st_size for f in files if f.is_file()) / (1024 * 1024)
        
        print(f"   ✅ Downloaded {len(files)} files ({total_size:.1f} MB)")
        return True
        
    except FileNotFoundError:
        print("   ❌ Kaggle CLI not found. Run: pip install kaggle")
        return False
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return False


def list_datasets():
    """Print available datasets."""
    print("\n📊 Available Kaggle Datasets:")
    print("=" * 70)
    for key, info in DATASETS.items():
        print(f"\n  {key}")
        print(f"    Name: {info['name']}")
        print(f"    Size: {info['size']}")
        print(f"    Description: {info['description']}")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Download Kaggle datasets for sentiment analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download default datasets (wsb + financial-news)
  python scripts/download_kaggle_data.py
  
  # Download specific dataset
  python scripts/download_kaggle_data.py --dataset wsb
  
  # Download all datasets
  python scripts/download_kaggle_data.py --all
  
  # List available datasets
  python scripts/download_kaggle_data.py --list
        """,
    )
    parser.add_argument(
        "--dataset", "-d",
        type=str,
        choices=list(DATASETS.keys()),
        help="Specific dataset to download"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Download all available datasets"
    )
    parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="List available datasets"
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default="data/kaggle",
        help="Output directory (default: data/kaggle)"
    )
    
    args = parser.parse_args()
    
    # List datasets
    if args.list:
        list_datasets()
        return
    
    print("=" * 60)
    print("📦 Kaggle Dataset Downloader")
    print("=" * 60)
    
    # Check Kaggle setup
    if not check_kaggle_setup():
        sys.exit(1)
    
    # Determine which datasets to download
    if args.all:
        to_download = list(DATASETS.keys())
    elif args.dataset:
        to_download = [args.dataset]
    else:
        to_download = DEFAULT_DATASETS
        print(f"\nDownloading default datasets: {', '.join(to_download)}")
        print("(Use --all for all datasets, or --dataset <name> for specific)")
    
    # Download each dataset
    base_dir = Path(args.output)
    success_count = 0
    
    for dataset_key in to_download:
        info = DATASETS[dataset_key]
        output_dir = base_dir / dataset_key
        
        if download_dataset(info["slug"], output_dir, info["name"]):
            success_count += 1
    
    # Summary
    print("\n" + "=" * 60)
    print(f"📊 Download Summary: {success_count}/{len(to_download)} successful")
    print("=" * 60)
    
    if success_count > 0:
        print(f"\nData saved to: {base_dir.absolute()}")
        print("\nTo load this data for processing:")
        print("  from sentiment_detector.collectors import KaggleDataLoader")
        print(f"  loader = KaggleDataLoader('{args.output}')")
        print("  items = loader.load_all(limit=1000)")
        print()
        print("Or run the multi-source collector:")
        print(f"  python scripts/collect_multi_source.py --sources kaggle --kaggle-dir {args.output}")


if __name__ == "__main__":
    main()
