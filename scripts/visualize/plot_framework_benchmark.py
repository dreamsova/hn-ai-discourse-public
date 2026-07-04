#!/usr/bin/env python3
"""Bar chart of the four aggregation backends' wall-clock times.

Reads the benchmark JSON files written by each aggregation script
and writes a PNG comparing pandas serial, Dask LocalCluster,
Dask SLURMCluster (multi-node), and PySpark on Midway.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


# Hard-coded reference values for the two backends whose benchmark
# JSON files are not always saved by the production scripts (pandas
# baseline lives in dask_benchmark.json's "pandas_elapsed" or in the
# report; LocalCluster lives in the same file).
PANDAS_BASELINE_SECONDS = 62.0
DASK_LOCALCLUSTER_SECONDS = 152.0


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--spark-bench",
        type=Path,
        default=Path("outputs/panel_spark/spark_benchmark.json"),
    )
    parser.add_argument(
        "--dask-multinode-bench",
        type=Path,
        default=Path("outputs/panel_dask_multinode/dask_multinode_benchmark.json"),
    )
    parser.add_argument(
        "--output-png",
        type=Path,
        default=Path("deliverables/framework_benchmark.png"),
    )
    args = parser.parse_args()

    # Load the two we have JSON for; fall back to the canonical
    # baselines for the rest.
    spark_secs = json.loads(args.spark_bench.read_text())["elapsed_seconds"]
    dask_mn_secs = json.loads(args.dask_multinode_bench.read_text())["elapsed_seconds"]

    rows = [
        ("Dask\nLocalCluster", DASK_LOCALCLUSTER_SECONDS, "#aaaaaa"),
        ("pandas\nserial",      PANDAS_BASELINE_SECONDS,  "#888888"),
        ("Dask\nSLURMCluster",  dask_mn_secs,             "#007c80"),
        ("PySpark\nMidway",     spark_secs,               "#bf5700"),
    ]

    labels = [r[0] for r in rows]
    secs = [r[1] for r in rows]
    colors = [r[2] for r in rows]
    speedup = [PANDAS_BASELINE_SECONDS / s for s in secs]

    fig, ax = plt.subplots(figsize=(10, 5.5), constrained_layout=True)
    bars = ax.bar(labels, secs, color=colors, edgecolor="#1c2736",
                  linewidth=0.5, width=0.6)

    for bar, sec, sp in zip(bars, secs, speedup):
        y = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2, y + 2,
            f"{sec:.1f}s\n({sp:.1f}× pandas)",
            ha="center", va="bottom", fontsize=10, color="#1c2736",
        )

    ax.set_ylabel("Wall-clock time (seconds)", fontsize=12)
    ax.set_title(
        "Monthly-panel aggregation across four execution backends\n"
        "(same 1260 inference parquets, 411K rows, on Midway 3)",
        fontsize=13, pad=10,
    )
    ax.set_ylim(0, max(secs) * 1.18)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="y", linestyle="--", alpha=0.3)
    ax.set_axisbelow(True)

    args.output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_png, dpi=170)
    print(f"wrote {args.output_png}")


if __name__ == "__main__":
    main()
