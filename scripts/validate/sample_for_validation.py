#!/usr/bin/env python3
"""Sample inference outputs for manual gold-set validation.

3-class stratified sample by predicted_label, sampled across months to avoid
clustering on a single event window. Default: 60 doomer + 60 accelerationist +
80 neutral = 200 total.
"""
from __future__ import annotations

import argparse
import glob
from pathlib import Path

import pandas as pd


DEFAULT_QUOTA = {"doomer": 60, "accelerationist": 60, "neutral": 80}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-glob", default="data/inference/**/*.parquet")
    parser.add_argument("--output-csv", type=Path, default=Path("reports/gold_set_to_label.csv"))
    parser.add_argument("--seed", type=int, default=20260524)
    args = parser.parse_args()

    files = sorted(glob.glob(args.input_glob, recursive=True))
    if not files:
        raise SystemExit("no inference files matched %s" % args.input_glob)

    frames = []
    for path in files:
        try:
            df = pd.read_parquet(path, columns=[
                "comment_id", "year_month", "combined_text", "story_title",
                "predicted_label", "prob_doomer", "prob_accelerationist", "prob_neutral",
            ])
        except Exception:
            df = pd.read_parquet(path)
        if len(df) == 0:
            continue
        frames.append(df)
    if not frames:
        raise SystemExit("no rows found in inference shards")
    all_df = pd.concat(frames, ignore_index=True)
    all_df = all_df.dropna(subset=["combined_text"])
    all_df = all_df[all_df["combined_text"].str.len() > 20]

    rng = pd.Series(range(len(all_df))).sample(frac=1.0, random_state=args.seed).index

    out_parts = []
    for label, quota in DEFAULT_QUOTA.items():
        pool = all_df[all_df["predicted_label"] == label]
        if len(pool) == 0:
            print(f"warning: no rows for label={label}")
            continue
        take = min(quota, len(pool))
        sampled = pool.sample(n=take, random_state=args.seed)
        out_parts.append(sampled)
        print(f"sampled {take}/{quota} for label={label} (pool={len(pool)})")

    out = pd.concat(out_parts, ignore_index=True)
    out = out.sample(frac=1.0, random_state=args.seed).reset_index(drop=True)
    out["gold_label"] = ""

    keep_cols = [
        "comment_id", "year_month", "story_title", "combined_text",
        "predicted_label", "prob_doomer", "prob_accelerationist", "prob_neutral",
        "gold_label",
    ]
    out = out[[c for c in keep_cols if c in out.columns]]

    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.output_csv, index=False)
    print(f"wrote {len(out)} rows to {args.output_csv}")
    print("label this column: gold_label (doomer | accelerationist | neutral | wrong_other)")


if __name__ == "__main__":
    main()
