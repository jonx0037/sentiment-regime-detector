#!/usr/bin/env python3
"""
Master orchestrator for dataset import and HPC preparation.

This script coordinates the import of all new datasets from the 
February 1, 2026 research session, including:

1. Local imports (run immediately):
   - ECB CISS systemic stress index
   - COVID World Indices (46 global markets)
   - Pre-labeled sentiment datasets

2. HPC preparation (for evening session):
   - WSB Echo Chamber data batching

Usage:
    # Run all local imports
    python scripts/run_all_imports.py --local
    
    # Prepare HPC batches only
    python scripts/run_all_imports.py --hpc-prep
    
    # Run everything
    python scripts/run_all_imports.py --all
    
    # Dry run (no actual imports)
    python scripts/run_all_imports.py --all --dry-run
"""

import argparse
import logging
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Script directory
SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent


def run_script(script_name: str, args: List[str] = None, dry_run: bool = False) -> Tuple[bool, str]:
    """
    Run a Python script with optional arguments.
    
    Args:
        script_name: Name of the script in scripts/
        args: Additional command-line arguments
        dry_run: If True, don't actually run
        
    Returns:
        Tuple of (success, output/error message)
    """
    script_path = SCRIPTS_DIR / script_name
    
    if not script_path.exists():
        return False, f"Script not found: {script_path}"
    
    cmd = [sys.executable, str(script_path)]
    if args:
        cmd.extend(args)
    
    if dry_run:
        logger.info(f"[DRY RUN] Would run: {' '.join(cmd)}")
        return True, "Dry run - skipped"
    
    logger.info(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=PROJECT_ROOT,
        )
        
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, f"Exit code {result.returncode}: {result.stderr}"
            
    except Exception as e:
        return False, str(e)


def run_local_imports(db_url: str = None, dry_run: bool = False) -> dict:
    """
    Run all local import scripts.
    
    Args:
        db_url: Database connection URL
        dry_run: If True, analyze only
        
    Returns:
        Dictionary with import results
    """
    results = {
        "started_at": datetime.now().isoformat(),
        "imports": {},
    }
    
    # Common args
    common_args = []
    if db_url:
        common_args.extend(["--db-url", db_url])
    if dry_run:
        common_args.append("--dry-run")
    
    # 1. ECB CISS
    logger.info("\n" + "=" * 60)
    logger.info("1. Importing ECB CISS Systemic Stress Index")
    logger.info("=" * 60)
    
    success, output = run_script("import_ecb_ciss.py", common_args, dry_run=False)
    results["imports"]["ecb_ciss"] = {
        "success": success,
        "output": output[:500] if output else None,
    }
    if not success:
        logger.error(f"ECB CISS import failed: {output}")
    else:
        logger.info("ECB CISS import completed")
    
    # 2. COVID World Indices
    logger.info("\n" + "=" * 60)
    logger.info("2. Importing COVID World Indices (46 markets)")
    logger.info("=" * 60)
    
    success, output = run_script("import_covid_indices.py", common_args, dry_run=False)
    results["imports"]["covid_indices"] = {
        "success": success,
        "output": output[:500] if output else None,
    }
    if not success:
        logger.error(f"COVID Indices import failed: {output}")
    else:
        logger.info("COVID Indices import completed")
    
    # 3. Pre-labeled Sentiment Datasets
    logger.info("\n" + "=" * 60)
    logger.info("3. Importing Pre-labeled Sentiment Datasets")
    logger.info("=" * 60)
    
    success, output = run_script("import_prelabeled_sentiment.py", common_args, dry_run=False)
    results["imports"]["prelabeled_sentiment"] = {
        "success": success,
        "output": output[:500] if output else None,
    }
    if not success:
        logger.error(f"Pre-labeled sentiment import failed: {output}")
    else:
        logger.info("Pre-labeled sentiment import completed")
    
    results["completed_at"] = datetime.now().isoformat()
    
    return results


def prepare_hpc_batches(dry_run: bool = False) -> dict:
    """
    Prepare HPC batches for WSB Echo Chamber processing.
    
    Args:
        dry_run: If True, analyze only
        
    Returns:
        Dictionary with preparation results
    """
    results = {
        "started_at": datetime.now().isoformat(),
    }
    
    logger.info("\n" + "=" * 60)
    logger.info("4. Preparing WSB Echo Chamber HPC Batches")
    logger.info("=" * 60)
    
    args = []
    if dry_run:
        args.append("--analyze-only")
    
    success, output = run_script("prepare_wsb_echo_chamber.py", args, dry_run=False)
    results["wsb_echo_chamber"] = {
        "success": success,
        "output": output[:1000] if output else None,
    }
    
    if not success:
        logger.error(f"WSB Echo Chamber preparation failed: {output}")
    else:
        logger.info("WSB Echo Chamber preparation completed")
    
    results["completed_at"] = datetime.now().isoformat()
    
    return results


def print_summary(local_results: dict = None, hpc_results: dict = None):
    """Print a summary of all operations."""
    logger.info("\n" + "=" * 60)
    logger.info("PROCESSING SUMMARY")
    logger.info("=" * 60)
    
    if local_results:
        logger.info("\nLocal Imports:")
        for name, result in local_results.get("imports", {}).items():
            status = "✓" if result["success"] else "✗"
            logger.info(f"  {status} {name}")
    
    if hpc_results:
        logger.info("\nHPC Preparation:")
        wsb = hpc_results.get("wsb_echo_chamber", {})
        status = "✓" if wsb.get("success") else "✗"
        logger.info(f"  {status} WSB Echo Chamber batches")
    
    logger.info("\n" + "=" * 60)
    logger.info("Next Steps:")
    logger.info("=" * 60)
    
    if hpc_results and hpc_results.get("wsb_echo_chamber", {}).get("success"):
        logger.info("""
For Evening Session (HPC Processing):
1. Package data for transfer:
   tar -czvf hpc_wsb_$(date +%Y%m%d).tar.gz data/hpc_batches/wsb_echo_chamber scripts/hpc/

2. Transfer to ManeFrame:
   scp hpc_wsb_*.tar.gz m3.smu.edu:~/capstone/

3. SSH and submit job:
   ssh m3.smu.edu
   cd ~/capstone && tar -xzf hpc_wsb_*.tar.gz
   sbatch scripts/hpc/wsb_echo_chamber.slurm

4. Monitor progress:
   squeue -u $USER
   tail -f logs/wsb_echo_chamber_*.log

5. After completion, retrieve results:
   scp -r m3.smu.edu:~/capstone/results/wsb_echo_chamber_* ./data/hpc_results/

6. Import HPC results:
   python scripts/import_hpc_sentiment.py --input data/hpc_results/
""")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Master orchestrator for dataset imports"
    )
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run local imports only (ECB CISS, COVID Indices, Pre-labeled)",
    )
    parser.add_argument(
        "--hpc-prep",
        action="store_true",
        help="Prepare HPC batches only (WSB Echo Chamber)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all imports and HPC preparation",
    )
    parser.add_argument(
        "--db-url",
        type=str,
        default=None,
        help="Database URL (defaults to settings)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Analyze data without importing",
    )
    
    args = parser.parse_args()
    
    # Default to --all if no specific option given
    if not (args.local or args.hpc_prep or args.all):
        args.all = True
    
    logger.info("=" * 60)
    logger.info("DATASET IMPORT ORCHESTRATOR")
    logger.info(f"Started: {datetime.now().isoformat()}")
    logger.info("=" * 60)
    
    local_results = None
    hpc_results = None
    
    if args.local or args.all:
        local_results = run_local_imports(
            db_url=args.db_url,
            dry_run=args.dry_run,
        )
    
    if args.hpc_prep or args.all:
        hpc_results = prepare_hpc_batches(dry_run=args.dry_run)
    
    # Print summary
    print_summary(local_results, hpc_results)
    
    logger.info(f"\nCompleted: {datetime.now().isoformat()}")


if __name__ == "__main__":
    main()
