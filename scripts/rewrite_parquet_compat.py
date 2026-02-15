#!/usr/bin/env python3
"""Rewrite parquet files to pyarrow-compatible encoding using fastparquet reader."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from fastparquet import ParquetFile


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def rewrite_one(src: Path, tmp_dst: Path, compression: str = "snappy") -> int:
    pf = ParquetFile(src)
    writer = None
    total_rows = 0
    try:
        for rg_df in pf.iter_row_groups():
            table = pa.Table.from_pandas(rg_df, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(tmp_dst, table.schema, compression=compression)
            writer.write_table(table)
            total_rows += len(rg_df)
    finally:
        if writer is not None:
            writer.close()
    if writer is None:
        raise RuntimeError(f"No row groups found in {src}")
    return total_rows


def verify_pyarrow_read(path: Path) -> tuple[int, list[str]]:
    df = pd.read_parquet(path, engine="pyarrow")
    return len(df), list(df.columns)


def main() -> int:
    parser = argparse.ArgumentParser(description="Rewrite incompatible parquet files")
    parser.add_argument(
        "--input-dir",
        default="results/sentiment_processed",
        help="Root directory containing parquet partitions",
    )
    parser.add_argument(
        "--pattern",
        default="asset_class=*/part-00000.parquet",
        help="Glob pattern under input-dir",
    )
    parser.add_argument(
        "--backup-root",
        default="results/_archive",
        help="Root for backups of original files",
    )
    parser.add_argument(
        "--report",
        default="results/parquet_compat_migration_report.json",
        help="Path to write migration report JSON",
    )
    parser.add_argument(
        "--compression",
        default="snappy",
        choices=["snappy", "gzip", "brotli", "zstd", "none"],
    )
    parser.add_argument("--dry-run", action="store_true", help="Only test readable status")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    files = sorted(input_dir.glob(args.pattern))
    if not files:
        raise FileNotFoundError(f"No parquet files found in {input_dir}/{args.pattern}")

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    backup_dir = Path(args.backup_root) / f"sentiment_processed_pyarrow_migration_{timestamp}"
    report_rows = []

    print(f"Found {len(files)} parquet files")
    print(f"Input dir: {input_dir}")
    print(f"Dry run: {args.dry_run}")

    for src in files:
        row = {
            "path": str(src),
            "status": "unknown",
            "rows": 0,
            "old_size_bytes": src.stat().st_size,
            "old_sha256": sha256(src),
        }
        print(f"\nProcessing: {src}")
        try:
            if args.dry_run:
                # Verify current failure mode and fastparquet fallback.
                pyarrow_ok = True
                try:
                    pd.read_parquet(src, engine="pyarrow")
                except Exception:
                    pyarrow_ok = False
                fp_df = pd.read_parquet(src, engine="fastparquet")
                row["rows"] = int(len(fp_df))
                row["pyarrow_readable_before"] = pyarrow_ok
                row["status"] = "dry_run_ok"
                print(f"  rows={row['rows']} pyarrow_readable_before={pyarrow_ok}")
                report_rows.append(row)
                continue

            tmp_dst = src.with_suffix(".tmp_pyarrow.parquet")
            if tmp_dst.exists():
                tmp_dst.unlink()

            compression = None if args.compression == "none" else args.compression
            rows_written = rewrite_one(src, tmp_dst, compression=compression)
            rows_verified, cols_verified = verify_pyarrow_read(tmp_dst)
            if rows_verified != rows_written:
                raise RuntimeError(
                    f"row mismatch after rewrite: written={rows_written}, verified={rows_verified}"
                )

            backup_target = backup_dir / src.relative_to(input_dir.parent)
            backup_target.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(src), str(backup_target))
            shutil.move(str(tmp_dst), str(src))

            row.update(
                {
                    "status": "rewritten",
                    "rows": int(rows_verified),
                    "columns": cols_verified,
                    "backup_path": str(backup_target),
                    "new_size_bytes": src.stat().st_size,
                    "new_sha256": sha256(src),
                }
            )
            print(f"  rewritten rows={rows_verified}")
        except Exception as exc:
            row["status"] = "failed"
            row["error"] = str(exc)
            print(f"  failed: {exc}")
            # Best effort cleanup of temporary file.
            tmp = src.with_suffix(".tmp_pyarrow.parquet")
            if tmp.exists():
                tmp.unlink()
        report_rows.append(row)

    report = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_dir": str(input_dir),
        "pattern": args.pattern,
        "dry_run": args.dry_run,
        "backup_dir": str(backup_dir) if not args.dry_run else None,
        "files": report_rows,
    }
    report_path = Path(args.report)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2))
    print(f"\nMigration report: {report_path}")

    failures = sum(1 for r in report_rows if r["status"] == "failed")
    if failures:
        print(f"Completed with {failures} failure(s)")
        return 1
    print("Completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
