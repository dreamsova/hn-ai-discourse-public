#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
from pathlib import Path

import pandas as pd


EVENT_MARKERS = [
    {"event_date": "2022-11", "event_label": "ChatGPT release"},
    {"event_date": "2023-03", "event_label": "GPT-4 release"},
    {"event_date": "2023-11", "event_label": "OpenAI board crisis"},
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate inferred shards into a monthly panel.")
    parser.add_argument("--input-glob", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    args = parser.parse_args()

    files = sorted(glob.glob(args.input_glob, recursive=True))
    if not files:
        raise SystemExit("no inference files matched %s" % args.input_glob)

    frame = pd.concat((pd.read_parquet(path) for path in files), ignore_index=True)
    frame = frame.drop_duplicates(subset=["comment_id"])
    frame = frame[frame["year_month"].astype(str) != ""].copy()

    panel = (
        frame.groupby("year_month")
        .agg(
            n_comments=("comment_id", "count"),
            n_unique_stories=("story_id", pd.Series.nunique),
            n_unique_authors=("author", pd.Series.nunique),
        )
        .reset_index()
        .sort_values("year_month")
    )

    for label in ["doomer", "accelerationist", "neutral", "non_ai"]:
        counts = (
            frame.assign(is_label=(frame["predicted_label"] == label).astype(int))
            .groupby("year_month")["is_label"]
            .sum()
            .rename("n_%s" % label)
        )
        panel = panel.merge(counts, on="year_month", how="left")
        panel["n_%s" % label] = panel["n_%s" % label].fillna(0).astype(int)
        panel["share_%s" % label] = panel["n_%s" % label] / panel["n_comments"]

    args.output_dir.mkdir(parents=True, exist_ok=True)
    panel_path = args.output_dir / "monthly_panel.parquet"
    panel_csv = args.output_dir / "monthly_panel.csv"
    events_csv = args.output_dir / "event_markers.csv"

    panel.to_parquet(panel_path, index=False)
    panel.to_csv(panel_csv, index=False)
    pd.DataFrame(EVENT_MARKERS).to_csv(events_csv, index=False)

    print("wrote monthly panel to %s" % panel_path)
    print(panel.to_string(index=False))


if __name__ == "__main__":
    main()
