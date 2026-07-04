#!/usr/bin/env python3
"""Per-author concentration analysis of doomer/accelerationist framing.

Reads the cleaned + TF-IDF inferred corpus, joins predicted_label with
author, and reports:

  - Top-N most prolific authors per stance class (counts + share of class total)
  - Gini coefficient on per-author class counts (how concentrated is each class?)
  - Repeat-doomer / repeat-accel rate (what % of authors writing 1 doomer comment
    write 2+? — are the trends driven by a long tail or a small core?)
  - Author-month panel (top-N authors x month) for stacked-area chart later

The substantive question: is the rise in "doomer share" around event windows
driven by lots of new participants OR by a small number of prolific authors
writing more?
"""
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import numpy as np
import pandas as pd

STANCE_LABELS = ["doomer", "accelerationist", "neutral"]


def gini(arr: np.ndarray) -> float:
    """Gini coefficient on a non-negative array."""
    arr = np.asarray(arr, dtype=np.float64).flatten()
    if arr.size == 0 or arr.sum() == 0:
        return 0.0
    arr = np.sort(arr)
    n = arr.size
    idx = np.arange(1, n + 1)
    return float((2 * (idx * arr).sum() - (n + 1) * arr.sum()) / (n * arr.sum()))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--clean-glob",
        type=str,
        default="data/clean/year=*/month=*/family=*/query=*/*.parquet",
    )
    parser.add_argument(
        "--inference-glob",
        type=str,
        default="data/inference/year=*/month=*/family=*/query=*/*.parquet",
    )
    parser.add_argument("--top-n", type=int, default=20)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/author_analysis"),
    )
    args = parser.parse_args()

    args.output_dir.mkdir(parents=True, exist_ok=True)

    # Load author + year_month from clean shards
    print("loading author/year_month from cleaned shards ...")
    clean_frames = []
    for p in sorted(glob.glob(args.clean_glob)):
        clean_frames.append(pd.read_parquet(p, columns=[
            "comment_id", "author", "year_month",
        ]))
    clean = pd.concat(clean_frames, ignore_index=True)
    clean["comment_id"] = clean["comment_id"].astype(str)
    clean = clean.drop_duplicates(subset=["comment_id"], keep="first")
    clean = clean[clean["author"].notna() & (clean["author"] != "")]
    print(f"  unique comment_ids with author: {len(clean):,}")

    # Load predicted_label from inference shards
    print("loading predicted_label from inference shards ...")
    inf_frames = []
    for p in sorted(glob.glob(args.inference_glob)):
        inf_frames.append(pd.read_parquet(p, columns=[
            "comment_id", "predicted_label",
        ]))
    inf = pd.concat(inf_frames, ignore_index=True)
    inf["comment_id"] = inf["comment_id"].astype(str)
    inf = inf.drop_duplicates(subset=["comment_id"], keep="first")

    df = clean.merge(inf, on="comment_id", how="left")
    df["predicted_label"] = df["predicted_label"].fillna("not_retrieved")

    summary = {}

    # Top-N authors per class
    print("computing per-author counts ...")
    per_author = df.groupby(["author", "predicted_label"]).size().unstack(fill_value=0)
    for lab in STANCE_LABELS + ["non_ai", "not_retrieved"]:
        if lab not in per_author.columns:
            per_author[lab] = 0
    per_author["total"] = per_author.sum(axis=1)
    per_author.to_csv(args.output_dir / "per_author_class_counts.csv")

    top_per_class = {}
    for lab in STANCE_LABELS:
        topn = per_author.sort_values(lab, ascending=False).head(args.top_n)
        topn_share = topn[lab].sum() / max(per_author[lab].sum(), 1)
        topn_table = topn[[lab, "total"]].reset_index().rename(
            columns={lab: f"n_{lab}"})
        topn_table["share_of_class"] = topn_table[f"n_{lab}"] / max(per_author[lab].sum(), 1)
        topn_table.to_csv(args.output_dir / f"top{args.top_n}_{lab}_authors.csv",
                          index=False)
        summary[f"top{args.top_n}_{lab}_share_of_class"] = float(topn_share)
        summary[f"n_authors_with_{lab}>0"] = int((per_author[lab] > 0).sum())
        summary[f"gini_{lab}"] = gini(per_author[lab].to_numpy())

    # Repeat-author rate per class
    for lab in STANCE_LABELS:
        with_one = int((per_author[lab] >= 1).sum())
        with_two_plus = int((per_author[lab] >= 2).sum())
        summary[f"repeat_rate_{lab}"] = (
            with_two_plus / max(with_one, 1)
        )

    # Cross-class authors (people who wrote BOTH doomer and accel comments)
    summary["n_authors_doomer_only"] = int(
        ((per_author["doomer"] > 0) & (per_author["accelerationist"] == 0)).sum()
    )
    summary["n_authors_accel_only"] = int(
        ((per_author["accelerationist"] > 0) & (per_author["doomer"] == 0)).sum()
    )
    summary["n_authors_both"] = int(
        ((per_author["doomer"] > 0) & (per_author["accelerationist"] > 0)).sum()
    )

    (args.output_dir / "author_summary.json").write_text(
        json.dumps(summary, indent=2)
    )
    print(json.dumps(summary, indent=2))

    # Top-N author-month panel for stacked-area chart
    top_authors = set()
    for lab in STANCE_LABELS:
        top_authors |= set(per_author.sort_values(lab, ascending=False)
                           .head(args.top_n).index.tolist())
    am = (
        df[df["author"].isin(top_authors)]
        .groupby(["author", "year_month", "predicted_label"])
        .size()
        .rename("n")
        .reset_index()
    )
    am.to_parquet(args.output_dir / "top_author_month_panel.parquet", index=False)
    am.to_csv(args.output_dir / "top_author_month_panel.csv", index=False)

    print(f"wrote {args.output_dir}/ — author analysis complete")


if __name__ == "__main__":
    main()
