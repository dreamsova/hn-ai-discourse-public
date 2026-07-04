#!/usr/bin/env python3
"""Multi-node Dask aggregation via `dask_jobqueue.SLURMCluster`.

Reads the normalized parquet tree produced by `preprocess_for_spark.py`
and computes the same monthly panel as `aggregate_monthly_v2.py`.
Workers are spawned as their own Slurm jobs across separate compute
nodes, giving a true multi-node Dask benchmark alongside the serial,
LocalCluster, and PySpark variants.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

STANCE_LABELS = ["doomer", "accelerationist", "neutral"]
NON_STANCE = ["non_ai", "not_retrieved"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--n-workers", type=int, default=4,
                        help="Number of distinct Slurm jobs to spawn as Dask workers.")
    parser.add_argument("--cores-per-worker", type=int, default=4)
    parser.add_argument("--memory-per-worker", type=str, default="8GB")
    parser.add_argument("--walltime-per-worker", type=str, default="00:30:00")
    parser.add_argument("--account", type=str, default="macs30123")
    parser.add_argument("--partition", type=str, default="caslake")
    parser.add_argument(
        "--input-glob",
        type=str,
        default="data/inference_normalized/year=*/month=*/family=*/query=*/*.parquet",
        help="Default points at the homogenized tree from "
             "scripts/preprocess_for_spark.py so dd.read_parquet doesn't "
             "hit the same schema-merge failure Spark hit on the raw tree.",
    )
    parser.add_argument("--predicted-col", type=str, default="predicted_label")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/panel_dask_multinode"),
    )
    parser.add_argument("--method-tag", type=str, default="dask_multinode")
    args = parser.parse_args()

    # Lazy imports so the script can be syntax-checked without these deps.
    import dask.dataframe as dd
    from dask_jobqueue import SLURMCluster
    from dask.distributed import Client

    args.output_dir.mkdir(parents=True, exist_ok=True)
    log_dir = args.output_dir / "worker_logs"
    log_dir.mkdir(exist_ok=True)

    cluster = SLURMCluster(
        queue=args.partition,
        account=args.account,
        cores=args.cores_per_worker,
        memory=args.memory_per_worker,
        walltime=args.walltime_per_worker,
        processes=args.cores_per_worker,
        log_directory=str(log_dir),
        job_extra_directives=[f"--output={log_dir}/worker_%j.out",
                              f"--error={log_dir}/worker_%j.err"],
    )
    print(f"[{args.method_tag}] cluster submission script preview:")
    print(cluster.job_script())

    print(f"[{args.method_tag}] requesting {args.n_workers} Slurm-job workers ...")
    cluster.scale(jobs=args.n_workers)
    client = Client(cluster)
    print(f"[{args.method_tag}] dashboard: {client.dashboard_link}")

    # Wait for at least N//2 workers to come up so the benchmark isn't
    # dominated by Slurm queue time.
    print(f"[{args.method_tag}] waiting for workers to register ...")
    deadline = time.time() + 600  # 10 min cap
    target = max(1, args.n_workers // 2)
    while time.time() < deadline:
        ready = len(client.scheduler_info()["workers"])
        if ready >= target:
            print(f"[{args.method_tag}] {ready} workers ready (target {target})")
            break
        time.sleep(10)
    else:
        print(f"[{args.method_tag}] WARNING: target {target} workers never registered")

    n_workers_active = len(client.scheduler_info()["workers"])
    t0 = time.time()

    pred_col = args.predicted_col
    # Hive partition discovery confuses dd.read_parquet on this tree
    # (some parquets carry year_month as a column but not year/month/
    # family/query individually). Bypass by handing Dask an explicit
    # list of file paths.
    import glob as _glob
    file_list = sorted(_glob.glob(args.input_glob))
    if not file_list:
        raise SystemExit(f"no parquets matched {args.input_glob}")
    print(f"[{args.method_tag}] reading {len(file_list)} parquets via explicit file list")
    df = dd.read_parquet(
        file_list,
        columns=["comment_id", "year_month", pred_col],
    )
    df["comment_id"] = df["comment_id"].astype(str)
    df = df.drop_duplicates(subset=["comment_id"])
    df = df[df["year_month"].notnull() & (df["year_month"] != "")]

    # Monthly counts
    n_comments = df.groupby("year_month")["comment_id"].count().rename("n_comments")
    per_label = {}
    for label in STANCE_LABELS + NON_STANCE:
        per_label[label] = (
            df[df[pred_col] == label]
            .groupby("year_month")["comment_id"]
            .count()
            .rename(f"n_{label}")
        )

    panel = n_comments.to_frame()
    for label, series in per_label.items():
        panel = panel.join(series, how="left")

    pdf = panel.compute().fillna(0).astype(int).reset_index().sort_values("year_month")

    pdf["n_ai_in_scope"] = pdf[[f"n_{l}" for l in STANCE_LABELS]].sum(axis=1)
    for label in STANCE_LABELS:
        pdf[f"share_{label}_of_total"] = pdf[f"n_{label}"] / pdf["n_comments"].clip(lower=1)
        pdf[f"share_{label}_of_ai"] = pdf[f"n_{label}"] / pdf["n_ai_in_scope"].clip(lower=1)

    pdf.to_parquet(args.output_dir / "monthly_panel.parquet", index=False)
    pdf.to_csv(args.output_dir / "monthly_panel.csv", index=False)
    elapsed = time.time() - t0

    bench = {
        "method_tag": args.method_tag,
        "n_workers_requested": args.n_workers,
        "n_workers_active_at_compute": n_workers_active,
        "cores_per_worker": args.cores_per_worker,
        "memory_per_worker": args.memory_per_worker,
        "elapsed_seconds": round(elapsed, 2),
        "n_months": int(len(pdf)),
        "n_rows_in": int(pdf["n_comments"].sum()),
    }
    (args.output_dir / "dask_multinode_benchmark.json").write_text(
        json.dumps(bench, indent=2)
    )
    print(f"[{args.method_tag}] wrote {len(pdf)} months in {elapsed:.2f}s "
          f"on {n_workers_active} active workers")
    print(json.dumps(bench, indent=2))

    client.close()
    cluster.close()


if __name__ == "__main__":
    main()
