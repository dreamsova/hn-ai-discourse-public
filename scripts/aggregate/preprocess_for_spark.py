#!/usr/bin/env python3
"""Homogenize the inference parquets so PySpark can read them.

The 1260 shards were written across pipeline iterations with
diverging types (`comment_id` INT vs STRING, `created_at` INT vs
STRING, etc.). Pandas and Dask tolerate this; Spark does not. The
script reads each shard with pandas, coerces to a fixed minimum
schema, and rewrites under a parallel tree. Runs as a Slurm CPU
array (one task per shard).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-path",
        type=Path,
        required=True,
        help="One parquet shard to homogenize.",
    )
    parser.add_argument(
        "--input-root",
        type=Path,
        default=Path("data/inference"),
        help="Root of the input tree (used to compute relative path).",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path("data/inference_normalized"),
        help="Root of the output tree (preserves relative path).",
    )
    args = parser.parse_args()

    if not args.input_path.exists():
        raise SystemExit(f"input path does not exist: {args.input_path}")

    df = pd.read_parquet(args.input_path)
    # Strip down to the minimum column set Spark and Dask actually need
    # for the monthly aggregation. The 1260 shards were written by
    # several pipeline iterations and we hit schema drift on roughly
    # every non-trivial column in turn (comment_id INT vs STRING,
    # created_at INT vs STRING, created_at_i INT32 vs INT64,
    # is_high_precision_label BOOL vs INT, query LARGE_STRING vs STRING).
    # Whack-a-mole'ing every offender is unstable; the reliable fix is
    # to write the normalized tree with only the columns the aggregator
    # consumes, all forced to one concrete dtype.
    keep = {"comment_id", "year_month", "predicted_label", "ai_hits"}
    df = df[[c for c in df.columns if c in keep]].copy()
    if "comment_id" in df.columns:
        df["comment_id"] = df["comment_id"].astype(str)
    if "year_month" in df.columns:
        df["year_month"] = df["year_month"].astype(str)
    if "predicted_label" in df.columns:
        df["predicted_label"] = df["predicted_label"].astype(str)
    if "ai_hits" in df.columns:
        df["ai_hits"] = df["ai_hits"].astype("int64", errors="ignore")

    relative = args.input_path.relative_to(args.input_root)
    out_path = args.output_root / relative
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out_path, index=False)
    print(f"wrote {len(df):,} rows: {out_path}")


if __name__ == "__main__":
    main()
