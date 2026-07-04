#!/usr/bin/env python3
"""Distributed aggregation of inference shards via Dask.

Replaces the serial pandas aggregator with a dask.distributed
LocalCluster that reads all inference parquet files in parallel and
computes the monthly panel via dask.dataframe. Outputs are identical in
schema to scripts/aggregate_monthly.py so that the serial baseline and
the distributed version can be benchmarked head to head.
"""
from __future__ import annotations

import argparse
import glob
import time
from pathlib import Path

import dask
import dask.dataframe as dd
from dask import delayed
import pandas as pd
from dask.distributed import Client, LocalCluster


EVENT_MARKERS = [
    {"event_date": "2022-11", "event_label": "ChatGPT release"},
    {"event_date": "2023-03", "event_label": "GPT-4 release"},
    {"event_date": "2023-11", "event_label": "OpenAI board crisis"},
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Aggregate inferred shards into a monthly panel via Dask.")
    parser.add_argument("--input-glob", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--n-workers", type=int, default=8)
    parser.add_argument("--threads-per-worker", type=int, default=1)
    parser.add_argument("--memory-limit", default="2GB")
    parser.add_argument("--benchmark-out", type=Path, default=Path("outputs/dask_benchmark.json"))
    args = parser.parse_args()

    files = sorted(glob.glob(args.input_glob, recursive=True))
    if not files:
        raise SystemExit("no inference files matched %s" % args.input_glob)

    t0 = time.perf_counter()
    cluster = LocalCluster(
        n_workers=args.n_workers,
        threads_per_worker=args.threads_per_worker,
        memory_limit=args.memory_limit,
        dashboard_address=None,
    )
    client = Client(cluster)
    cluster_started = time.perf_counter()

    columns = ["comment_id", "story_id", "author", "year_month", "predicted_label"]

    @delayed
    def _read_one(path: str) -> pd.DataFrame:
        df = pd.read_parquet(path, columns=columns)
        df = df.dropna(subset=["year_month"])
        df = df[df["year_month"].astype(str) != ""]
        for col in ["comment_id", "story_id", "author", "year_month", "predicted_label"]:
            df[col] = df[col].astype("string")
        return df.reset_index(drop=True)

    parts = [_read_one(p) for p in files]
    meta = pd.DataFrame({
        "comment_id": pd.Series(dtype="string"),
        "story_id": pd.Series(dtype="string"),
        "author": pd.Series(dtype="string"),
        "year_month": pd.Series(dtype="string"),
        "predicted_label": pd.Series(dtype="string"),
    })
    ddf = dd.from_delayed(parts, meta=meta)
    ddf = ddf.drop_duplicates(subset=["comment_id"])

    n_comments = (
        ddf.groupby("year_month")["comment_id"].count()
        .compute()
        .rename("n_comments")
        .reset_index()
    )
    n_stories = (
        ddf[["year_month", "story_id"]]
        .drop_duplicates()
        .groupby("year_month")["story_id"].count()
        .compute()
        .rename("n_unique_stories")
        .reset_index()
    )
    n_authors = (
        ddf[["year_month", "author"]]
        .drop_duplicates()
        .groupby("year_month")["author"].count()
        .compute()
        .rename("n_unique_authors")
        .reset_index()
    )
    base = n_comments.merge(n_stories, on="year_month", how="left").merge(
        n_authors, on="year_month", how="left"
    ).sort_values("year_month")

    label_counts = (
        ddf.assign(_one=1)
        .groupby(["year_month", "predicted_label"])["_one"]
        .count()
        .compute()
        .reset_index(name="n")
    )
    pivot = label_counts.pivot(index="year_month", columns="predicted_label", values="n").fillna(0).astype(int)

    panel = base.merge(pivot.reset_index(), on="year_month", how="left").fillna(0)
    for label in ["doomer", "accelerationist", "neutral", "non_ai"]:
        col = label if label in panel.columns else None
        if col is None:
            panel[label] = 0
        panel = panel.rename(columns={label: "n_%s" % label})
        panel["share_%s" % label] = panel["n_%s" % label] / panel["n_comments"].clip(lower=1)

    aggregated = time.perf_counter()

    args.output_dir.mkdir(parents=True, exist_ok=True)
    panel_path = args.output_dir / "monthly_panel_dask.parquet"
    panel_csv = args.output_dir / "monthly_panel_dask.csv"
    events_csv = args.output_dir / "event_markers.csv"
    panel.to_parquet(panel_path, index=False)
    panel.to_csv(panel_csv, index=False)
    pd.DataFrame(EVENT_MARKERS).to_csv(events_csv, index=False)

    written = time.perf_counter()

    benchmark = {
        "n_files": len(files),
        "n_workers": args.n_workers,
        "threads_per_worker": args.threads_per_worker,
        "memory_limit": args.memory_limit,
        "cluster_setup_seconds": round(cluster_started - t0, 3),
        "aggregation_seconds": round(aggregated - cluster_started, 3),
        "write_seconds": round(written - aggregated, 3),
        "wall_clock_seconds": round(written - t0, 3),
        "n_months": int(len(panel)),
    }
    args.benchmark_out.parent.mkdir(parents=True, exist_ok=True)
    import json
    args.benchmark_out.write_text(json.dumps(benchmark, indent=2))

    print(f"wrote {panel_path}")
    print(f"benchmark: {benchmark}")

    client.close()
    cluster.close()


if __name__ == "__main__":
    main()
