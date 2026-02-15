#!/usr/bin/env python3
"""Validate canonical results artifacts against docs/RESULTS_MANIFEST.json."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def validate(manifest_path: Path) -> int:
    manifest = json.loads(manifest_path.read_text())
    failures = 0

    for section in ("active_artifacts", "archived_artifacts", "invalid_artifacts"):
        artifacts = manifest.get(section, [])
        for artifact in artifacts:
            path = Path(artifact["path"])
            expected = artifact["sha256"]

            if not path.exists():
                print(f"MISSING [{section}]: {path}")
                failures += 1
                continue

            actual = sha256(path)
            if actual != expected:
                print(f"HASH MISMATCH [{section}]: {path}")
                print(f"  expected={expected}")
                print(f"  actual  ={actual}")
                failures += 1
            else:
                print(f"OK [{section}]: {path}")

    if failures:
        print(f"\nFAILED: {failures} manifest validation error(s)")
        return 1

    print("\nPASSED: manifest validated")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate results manifest")
    parser.add_argument(
        "--manifest",
        default="docs/RESULTS_MANIFEST.json",
        help="Path to manifest JSON",
    )
    args = parser.parse_args()
    return validate(Path(args.manifest))


if __name__ == "__main__":
    raise SystemExit(main())
