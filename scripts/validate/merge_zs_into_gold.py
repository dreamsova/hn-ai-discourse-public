#!/usr/bin/env python3
"""Merge zero-shot predictions into the labeled gold-set CSV.

After the user labels reports/gold_set_to_label.md and we extract those
labels into reports/gold_set_labeled.csv, we still need to pull in the
zero-shot predictions for the same comment_ids so score_gold_set.py can
evaluate both methods side-by-side.

Reads predicted_label_zs (and its probabilities + weak_label) from the
data/inference_zs/ shards by comment_id, joins them onto the labeled
CSV, and overwrites it in place.
"""
from __future__ import annotations

import argparse
import glob
from pathlib import Path

import pandas as pd

ZS_COLS = [
    "predicted_label_zs",
    "prob_doomer_zs",
    "prob_accelerationist_zs",
    "prob_neutral_zs",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-csv",
        type=Path,
        default=Path("reports/gold_set_labeled.csv"),
        help="Labeled gold-set CSV to enrich (modified in place).",
    )
    parser.add_argument(
        "--zs-glob",
        type=str,
        default="data/inference_zs/year=*/month=*/family=*/query=*/*.parquet",
        help="Glob of zero-shot inference shards.",
    )
    parser.add_argument(
        "--clean-glob",
        type=str,
        default="data/clean/year=*/month=*/family=*/query=*/*.parquet",
        help="Glob of cleaned shards (used to pull weak_label).",
    )
    args = parser.parse_args()

    gold = pd.read_csv(args.input_csv, dtype={"comment_id": str})
    wanted_ids = set(gold["comment_id"].astype(str))

    # Pull zero-shot predictions for just the gold comment_ids.
    zs_paths = sorted(glob.glob(args.zs_glob))
    if not zs_paths:
        raise SystemExit("no zero-shot shards matched: %s" % args.zs_glob)
    zs_rows: list[pd.DataFrame] = []
    for p in zs_paths:
        df = pd.read_parquet(p, columns=["comment_id"] + ZS_COLS)
        df["comment_id"] = df["comment_id"].astype(str)
        df = df[df["comment_id"].isin(wanted_ids)]
        if not df.empty:
            zs_rows.append(df)
    zs_df = pd.concat(zs_rows, ignore_index=True) if zs_rows else pd.DataFrame(
        columns=["comment_id"] + ZS_COLS
    )
    print("matched %d / %d gold rows in zero-shot output" % (len(zs_df), len(gold)))

    # Pull weak_label from cleaned shards too, so the gold validation can
    # also report agreement against the deployed lexicon rule itself.
    clean_paths = sorted(glob.glob(args.clean_glob))
    weak_rows: list[pd.DataFrame] = []
    for p in clean_paths:
        df = pd.read_parquet(p, columns=["comment_id", "weak_label"])
        df["comment_id"] = df["comment_id"].astype(str)
        df = df[df["comment_id"].isin(wanted_ids)]
        if not df.empty:
            weak_rows.append(df)
    weak_df = pd.concat(weak_rows, ignore_index=True) if weak_rows else pd.DataFrame(
        columns=["comment_id", "weak_label"]
    )
    print("matched %d / %d gold rows in cleaned shards (weak_label)" % (len(weak_df), len(gold)))

    # Drop pre-existing columns in gold so we get the latest values.
    drop_cols = [c for c in ZS_COLS + ["weak_label"] if c in gold.columns]
    if drop_cols:
        gold = gold.drop(columns=drop_cols)

    merged = gold.merge(zs_df, on="comment_id", how="left")
    merged = merged.merge(weak_df, on="comment_id", how="left")

    merged.to_csv(args.input_csv, index=False)
    print(
        "wrote %s with %d rows and columns: %s"
        % (args.input_csv, len(merged), list(merged.columns))
    )


if __name__ == "__main__":
    main()
