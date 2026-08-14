#!/usr/bin/env python3
"""Build all synthetic data and dashboard outputs from one seed."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from presence_pathways.pipeline import build_demo  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=20260814)
    parser.add_argument("--check-reproducibility", action="store_true")
    args = parser.parse_args()
    output = build_demo(ROOT, seed=args.seed, check_reproducibility=args.check_reproducibility)
    meta = output["analysis"]["metadata"]
    print(
        f"Built synthetic demo: {meta['participants']} participants, "
        f"{meta['observations']} observations, {meta['study_days']} study days."
    )
    print(f"EMA SHA-256: {output['manifest']['ema_sha256']}")


if __name__ == "__main__":
    main()
