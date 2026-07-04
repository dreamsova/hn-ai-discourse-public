#!/usr/bin/env python3
"""Monthly aggregation, v2 schema.

Emits both denominator variants explicitly so the dashboard can show
the right one:

    share_<label>_of_total = n_<label> / n_comments
    share_<label>_of_ai    = n_<label> / n_ai_in_scope

`n_ai_in_scope` counts only rows in the three on-topic stance classes
under the chosen classifier. `--predicted-col` switches between
`predicted_label` (TF-IDF) and `predicted_label_zs` (zero-shot
DeBERTa), so the same panel schema serves every measurement
instrument.
"""
from __future__ import annotations

import argparse
import glob
import sys
from pathlib import Path

import pandas as pd

# Stance labels we count toward "in-scope AI discourse"
STANCE_LABELS = ["doomer", "accelerationist", "neutral"]

# Default event markers (same as in v1)
EVENT_MARKERS = [
    {"event": "ChatGPT launch",        "date": "2022-11-30"},
    {"event": "GPT-4 release",         "date": "2023-03-14"},
    {"event": "OpenAI board crisis",   "date": "2023-11-17"},
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-glob",
        type=str,
        required=True,
        help="Glob of inference parquet files (e.g. 'data/inference_zs/year=*/month=*/family=*/query=*/*.parquet').",
    )
    parser.add_argument(
        "--predicted-col",
        type=str,
        default="predicted_label_zs",
        help="Which column to treat as the predicted stance label.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/panel_zs"),
        help="Where to write the monthly_panel.{parquet,csv} files.",
    )
    parser.add_argument(
        "--method-tag",
        type=str,
        default="zs",
        help="Short tag for this aggregation run (e.g. 'tfidf', 'zs'). Used in stdout only.",
    )
    args = parser.parse_args()

    paths = sorted(glob.glob(args.input_glob))
    if not paths:
        raise SystemExit("no parquet files matched glob: %s" % args.input_glob)
    print("[%s] reading %d shards" % (args.method_tag, len(paths)))

    frames = []
    for p in paths:
        df = pd.read_parquet(p)
        if args.predicted_col not in df.columns:
            raise SystemExit(
                "shard %s is missing column %s; available: %s"
                % (p, args.predicted_col, list(df.columns))
            )
        frames.append(df[["comment_id", "year_month", args.predicted_col]])
    frame = pd.concat(frames, ignore_index=True)
    # Defensive: drop duplicates by comment_id, keep first
    n_pre = len(frame)
    frame = frame.drop_duplicates(subset=["comment_id"], keep="first")
    if len(frame) < n_pre:
        print(
            "[%s] dropped %d duplicate comment_id rows" % (args.method_tag, n_pre - len(frame))
        )

    frame = frame[frame["year_month"].astype(str) != ""].copy()
    label_col = args.predicted_col

    # Monthly counts
    panel = (
        frame.groupby("year_month")
        .agg(n_comments=("comment_id", "count"))
        .reset_index()
        .sort_values("year_month")
    )

    # Per-label counts and BOTH denominators
    # n_ai_in_scope = sum of counts across the three stance labels
    label_counts = {}
    for label in STANCE_LABELS + ["non_ai", "not_retrieved"]:
        counts = (
            frame.assign(is_label=(frame[label_col] == label).astype(int))
            .groupby("year_month")["is_label"]
            .sum()
            .rename("n_%s" % label)
        )
        panel = panel.merge(counts, on="year_month", how="left")
        panel["n_%s" % label] = panel["n_%s" % label].fillna(0).astype(int)
        label_counts[label] = panel["n_%s" % label]

    panel["n_ai_in_scope"] = sum(label_counts[lab] for lab in STANCE_LABELS)

    for label in STANCE_LABELS:
        panel["share_%s_of_total" % label] = (
            panel["n_%s" % label] / panel["n_comments"].clip(lower=1)
        )
        panel["share_%s_of_ai" % label] = (
            panel["n_%s" % label] / panel["n_ai_in_scope"].clip(lower=1)
        )

    args.output_dir.mkdir(parents=True, exist_ok=True)
    panel_path = args.output_dir / "monthly_panel.parquet"
    panel_csv = args.output_dir / "monthly_panel.csv"
    events_csv = args.output_dir / "event_markers.csv"

    panel.to_parquet(panel_path, index=False)
    panel.to_csv(panel_csv, index=False)
    pd.DataFrame(EVENT_MARKERS).to_csv(events_csv, index=False)

    print(
        "[%s] wrote %s (%d months); column set: %s"
        % (args.method_tag, panel_path, len(panel), list(panel.columns))
    )
    # Quick sanity print
    show_cols = ["year_month", "n_comments", "n_ai_in_scope"] + [
        "share_%s_of_ai" % lab for lab in STANCE_LABELS
    ]
    print(panel[show_cols].tail(6).to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
