#!/usr/bin/env python3
"""
Prepare WSB Echo Chamber data for HPC batch processing.

This script reads the JSON-formatted Reddit data from the WSB Echo Chamber
dataset and converts it into batches suitable for GPU-accelerated sentiment
processing on SMU ManeFrame M3.

Tickers: GME, AMC, TSLA, AAPL, MSFT, NOK
Format: JSON files with Reddit post structure
Output: JSON batches for HPC processing
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Default paths
DATA_BASE = Path(__file__).parent.parent / "data" / "kaggle" / "wsb-echo-chamber"
OUTPUT_BASE = Path(__file__).parent.parent / "data" / "hpc_batches"

# Tickers in the dataset
TICKERS = ["GME", "AMC", "TSLA", "AAPL", "MSFT", "NOK"]

# Batch size for HPC processing
DEFAULT_BATCH_SIZE = 1000


def load_ticker_data(ticker: str, data_base: Path) -> List[Dict[str, Any]]:
    """
    Load Reddit data for a specific ticker from JSON files.
    
    The WSB Echo Chamber data is in JSON format with posts stored as
    key-value pairs where keys are indices and values are content.
    
    Args:
        ticker: Stock ticker symbol
        data_base: Base path to wsb-echo-chamber directory
        
    Returns:
        List of post dictionaries
    """
    ticker_dir = data_base / f"reddit_raw_{ticker}" / ticker
    
    if not ticker_dir.exists():
        logger.warning(f"Directory not found: {ticker_dir}")
        return []
    
    posts = []
    json_files = list(ticker_dir.glob("*.json")) + list(ticker_dir.iterdir())
    
    # The files might not have extensions - check all files
    for file_path in ticker_dir.iterdir():
        if file_path.is_file():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                    
                if not content:
                    continue
                
                # Try to parse as JSON
                data = json.loads(content)
                
                if isinstance(data, dict):
                    # The data is structured as {field: {index: value}}
                    # We need to transpose it to [{field: value}, ...]
                    
                    # Get all field names
                    fields = list(data.keys())
                    if not fields:
                        continue
                    
                    # Get indices from first field
                    first_field = data[fields[0]]
                    if isinstance(first_field, dict):
                        indices = list(first_field.keys())
                    else:
                        # Single record
                        post = {field: data[field] for field in fields}
                        post["source_file"] = file_path.name
                        post["ticker"] = ticker
                        posts.append(post)
                        continue
                    
                    # Transpose to list of records
                    for idx in indices:
                        post = {}
                        for field in fields:
                            if isinstance(data[field], dict):
                                post[field] = data[field].get(str(idx), data[field].get(idx))
                            else:
                                post[field] = data[field]
                        post["source_file"] = file_path.name
                        post["ticker"] = ticker
                        posts.append(post)
                        
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict):
                            item["source_file"] = file_path.name
                            item["ticker"] = ticker
                            posts.append(item)
                            
            except json.JSONDecodeError:
                # Not JSON, try reading as text
                pass
            except Exception as e:
                logger.debug(f"Error reading {file_path}: {e}")
    
    logger.info(f"  {ticker}: Loaded {len(posts)} posts from {len(list(ticker_dir.iterdir()))} files")
    return posts


def extract_text_content(post: Dict[str, Any]) -> str:
    """
    Extract the text content from a Reddit post.
    
    Args:
        post: Dictionary containing post data
        
    Returns:
        Combined text content suitable for sentiment analysis
    """
    text_parts = []
    
    # Title
    title = post.get("title", post.get("title_submission", ""))
    if title and title != "[deleted]":
        text_parts.append(str(title))
    
    # Self text (post body)
    selftext = post.get("selftext", post.get("body", ""))
    if selftext and selftext != "[deleted]" and selftext != "[removed]":
        text_parts.append(str(selftext))
    
    # Combine
    combined = " ".join(text_parts).strip()
    
    # Clean up
    combined = combined.replace("\n", " ").replace("\r", " ")
    combined = " ".join(combined.split())  # Normalize whitespace
    
    return combined


def prepare_batches(
    posts: List[Dict[str, Any]],
    batch_size: int = DEFAULT_BATCH_SIZE,
) -> List[List[Dict[str, Any]]]:
    """
    Split posts into batches for HPC processing.
    
    Args:
        posts: List of all posts
        batch_size: Number of posts per batch
        
    Returns:
        List of batches, each containing batch_size posts
    """
    # Filter posts with valid text
    valid_posts = []
    for post in posts:
        text = extract_text_content(post)
        if len(text) >= 10:  # Minimum text length
            valid_posts.append({
                "id": hashlib.md5(text.encode()).hexdigest()[:16],
                "text": text[:5000],  # Limit text length for transformer
                "ticker": post.get("ticker", "unknown"),
                "timestamp": post.get("created_utc_submission", post.get("created_utc")),
                "score": post.get("score_submission", post.get("score", post.get("ups", 0))),
                "source_file": post.get("source_file"),
            })
    
    logger.info(f"Filtered to {len(valid_posts)} valid posts")
    
    # Split into batches
    batches = []
    for i in range(0, len(valid_posts), batch_size):
        batch = valid_posts[i:i + batch_size]
        batches.append(batch)
    
    logger.info(f"Created {len(batches)} batches of ~{batch_size} posts each")
    return batches


def save_batches(
    batches: List[List[Dict[str, Any]]],
    output_dir: Path,
    prefix: str = "wsb_echo_chamber",
) -> List[Path]:
    """
    Save batches as JSON files for HPC processing.
    
    Args:
        batches: List of post batches
        output_dir: Directory to save batch files
        prefix: Filename prefix
        
    Returns:
        List of saved file paths
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    saved_files = []
    for i, batch in enumerate(batches):
        filename = f"{prefix}_batch_{i:04d}.json"
        filepath = output_dir / filename
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump({
                "batch_id": i,
                "total_batches": len(batches),
                "num_items": len(batch),
                "created_at": datetime.now().isoformat(),
                "source": "wsb_echo_chamber",
                "items": batch,
            }, f, indent=2)
        
        saved_files.append(filepath)
    
    logger.info(f"Saved {len(saved_files)} batch files to {output_dir}")
    return saved_files


def create_manifest(
    batches: List[List[Dict[str, Any]]],
    output_dir: Path,
    batch_files: List[Path],
) -> Path:
    """
    Create a manifest file for HPC job tracking.
    
    Args:
        batches: List of post batches
        output_dir: Output directory
        batch_files: List of saved batch file paths
        
    Returns:
        Path to manifest file
    """
    manifest = {
        "created_at": datetime.now().isoformat(),
        "source": "wsb_echo_chamber",
        "total_batches": len(batches),
        "total_items": sum(len(b) for b in batches),
        "batch_size": len(batches[0]) if batches else 0,
        "tickers": TICKERS,
        "batch_files": [str(f.name) for f in batch_files],
        "status": "ready",
        "hpc_job_id": None,
    }
    
    manifest_path = output_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    
    logger.info(f"Created manifest: {manifest_path}")
    return manifest_path


def analyze_data(posts: List[Dict[str, Any]]) -> dict:
    """
    Analyze the loaded data for summary statistics.
    
    Returns:
        Dictionary with analysis results
    """
    analysis = {
        "total_posts": len(posts),
        "posts_by_ticker": {},
        "text_length_stats": {},
        "timestamp_range": {},
    }
    
    # Group by ticker
    for ticker in TICKERS:
        ticker_posts = [p for p in posts if p.get("ticker") == ticker]
        analysis["posts_by_ticker"][ticker] = len(ticker_posts)
    
    # Text length stats
    text_lengths = [len(extract_text_content(p)) for p in posts]
    valid_lengths = [l for l in text_lengths if l > 0]
    
    if valid_lengths:
        analysis["text_length_stats"] = {
            "min": min(valid_lengths),
            "max": max(valid_lengths),
            "mean": sum(valid_lengths) / len(valid_lengths),
            "valid_count": len(valid_lengths),
            "empty_count": len(text_lengths) - len(valid_lengths),
        }
    
    # Timestamp range
    timestamps = [p.get("created_utc_submission", p.get("created_utc")) for p in posts]
    valid_timestamps = [t for t in timestamps if t and isinstance(t, (int, float))]
    
    if valid_timestamps:
        min_ts = min(valid_timestamps)
        max_ts = max(valid_timestamps)
        analysis["timestamp_range"] = {
            "earliest": datetime.fromtimestamp(min_ts).isoformat(),
            "latest": datetime.fromtimestamp(max_ts).isoformat(),
        }
    
    return analysis


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Prepare WSB Echo Chamber data for HPC processing"
    )
    parser.add_argument(
        "--data-path",
        type=Path,
        default=DATA_BASE,
        help="Path to WSB Echo Chamber data directory",
    )
    parser.add_argument(
        "--output-path",
        type=Path,
        default=OUTPUT_BASE,
        help="Path to save batch files",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help="Number of posts per batch",
    )
    parser.add_argument(
        "--tickers",
        type=str,
        nargs="+",
        default=TICKERS,
        help="Specific tickers to process",
    )
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only analyze data, don't create batches",
    )
    
    args = parser.parse_args()
    
    logger.info("=" * 60)
    logger.info("WSB Echo Chamber HPC Batch Preparation")
    logger.info("=" * 60)
    
    # Load data for all tickers
    all_posts = []
    for ticker in args.tickers:
        posts = load_ticker_data(ticker, args.data_path)
        all_posts.extend(posts)
    
    if not all_posts:
        logger.error("No posts loaded!")
        return
    
    # Analyze data
    analysis = analyze_data(all_posts)
    
    logger.info(f"\nData Summary:")
    logger.info(f"  Total posts: {analysis['total_posts']:,}")
    logger.info(f"  Posts by ticker:")
    for ticker, count in analysis["posts_by_ticker"].items():
        logger.info(f"    {ticker}: {count:,}")
    
    if analysis.get("text_length_stats"):
        stats = analysis["text_length_stats"]
        logger.info(f"  Text length: min={stats['min']}, max={stats['max']}, mean={stats['mean']:.0f}")
        logger.info(f"  Valid posts: {stats['valid_count']:,}, Empty: {stats['empty_count']:,}")
    
    if analysis.get("timestamp_range"):
        ts = analysis["timestamp_range"]
        logger.info(f"  Date range: {ts['earliest']} to {ts['latest']}")
    
    if args.analyze_only:
        logger.info("\nAnalysis complete (--analyze-only)")
        return
    
    # Prepare batches
    batches = prepare_batches(all_posts, args.batch_size)
    
    # Save batches
    output_dir = args.output_path / "wsb_echo_chamber"
    batch_files = save_batches(batches, output_dir)
    
    # Create manifest
    manifest_path = create_manifest(batches, output_dir, batch_files)
    
    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("HPC Batch Preparation Complete")
    logger.info("=" * 60)
    logger.info(f"Output directory: {output_dir}")
    logger.info(f"Batch files: {len(batch_files)}")
    logger.info(f"Total items: {sum(len(b) for b in batches):,}")
    logger.info(f"Manifest: {manifest_path}")
    logger.info("\nNext steps:")
    logger.info("  1. Transfer to ManeFrame: scp -r data/hpc_batches/wsb_echo_chamber m3.smu.edu:~/capstone/data/")
    logger.info("  2. Submit SLURM job: sbatch scripts/hpc/wsb_echo_chamber.slurm")


if __name__ == "__main__":
    main()
