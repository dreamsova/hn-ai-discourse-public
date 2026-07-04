#!/usr/bin/env python3
"""PySpark monthly-panel aggregation.

Reads the same 1260 inference parquets as the pandas / Dask versions
and emits an identical panel schema (share_*_of_total +
share_*_of_ai). Run under `module load spark/3.3.2` via
`spark-submit --master local[8]`.
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from pyspark.sql import SparkSession, functions as F

STANCE_LABELS = ["doomer", "accelerationist", "neutral"]
NON_STANCE_LABELS = ["non_ai", "not_retrieved"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-glob",
        type=str,
        required=True,
        help="Glob of inference parquet files (Spark accepts globs in path).",
    )
    parser.add_argument(
        "--predicted-col",
        type=str,
        default="predicted_label",
        help="predicted_label (TF-IDF baseline) or predicted_label_zs (zero-shot).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/panel_spark"),
    )
    parser.add_argument(
        "--method-tag",
        type=str,
        default="spark",
    )
    parser.add_argument(
        "--master",
        type=str,
        default="local[8]",
        help="Spark master. 'local[N]' for N local cores; pass a Spark URL for a real cluster.",
    )
    args = parser.parse_args()

    t0 = time.time()
    spark = (
        SparkSession.builder
        .appName("hn-ai-discourse-aggregate")
        .master(args.master)
        .config("spark.sql.shuffle.partitions", "16")
        .config("spark.driver.memory", "8g")
        # The 1260 parquets were written at different pipeline versions
        # and comment_id appears as both INT and STRING across files.
        # Disable the strict vectorized reader so Spark falls back to a
        # row-based reader that tolerates the type-evolved column.
        .config("spark.sql.parquet.enableVectorizedReader", "false")
        .getOrCreate()
    )
    print(f"[{args.method_tag}] Spark {spark.version} session up; master={args.master}")

    pred_col = args.predicted_col
    # spark.read.parquet auto-discovers Hive-style partitions when given
    # the root path (data/inference/), so year/month/family/query become
    # virtual columns. mergeSchema=true is required because the 1260
    # shards were written at different times and comment_id appears as
    # both INT (early shards) and BINARY/string (later shards). Without
    # merge, the vectorized parquet reader throws SchemaColumnConvertNot-
    # SupportedException as soon as it hits the first cross-type file.
    raw = (
        spark.read
        .option("mergeSchema", "true")
        .parquet(args.input_glob)
    )
    # Coerce comment_id to string for stable dedupe across shards.
    raw = raw.withColumn("comment_id", F.col("comment_id").cast("string"))
    print(f"[{args.method_tag}] raw row count: {raw.count():,}")
    print(f"[{args.method_tag}] schema columns: {raw.columns}")
    df = raw.select("comment_id", "year_month", pred_col)
    # Drop_duplicates by comment_id (a comment can appear in multiple query shards)
    df = df.dropDuplicates(["comment_id"])
    print(f"[{args.method_tag}] after dropDuplicates: {df.count():,}")
    df = df.filter(F.col("year_month").isNotNull() & (F.col("year_month") != ""))
    print(f"[{args.method_tag}] after year_month filter: {df.count():,}")

    # n_comments per month
    monthly = df.groupBy("year_month").agg(F.count("comment_id").alias("n_comments"))

    # Per-label counts
    for label in STANCE_LABELS + NON_STANCE_LABELS:
        cnt = (
            df.filter(F.col(pred_col) == label)
            .groupBy("year_month")
            .agg(F.count("comment_id").alias(f"n_{label}"))
        )
        monthly = monthly.join(cnt, on="year_month", how="left").fillna(0, [f"n_{label}"])

    # n_ai_in_scope = sum of the three stance counts
    monthly = monthly.withColumn(
        "n_ai_in_scope",
        sum(F.col(f"n_{lab}") for lab in STANCE_LABELS),
    )

    for label in STANCE_LABELS:
        monthly = (
            monthly
            .withColumn(
                f"share_{label}_of_total",
                F.col(f"n_{label}") / F.greatest(F.col("n_comments"), F.lit(1)),
            )
            .withColumn(
                f"share_{label}_of_ai",
                F.col(f"n_{label}") / F.greatest(F.col("n_ai_in_scope"), F.lit(1)),
            )
        )

    monthly = monthly.orderBy("year_month")
    pdf = monthly.toPandas()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pdf.to_parquet(args.output_dir / "monthly_panel.parquet", index=False)
    pdf.to_csv(args.output_dir / "monthly_panel.csv", index=False)
    print(f"[{args.method_tag}] wrote {len(pdf)} months to {args.output_dir}")

    elapsed = time.time() - t0
    bench_path = args.output_dir / "spark_benchmark.json"
    bench_path.write_text(
        json.dumps(
            {
                "method_tag": args.method_tag,
                "spark_version": spark.version,
                "master": args.master,
                "elapsed_seconds": round(elapsed, 2),
                "n_months": int(len(pdf)),
                "shuffle_partitions": int(
                    spark.conf.get("spark.sql.shuffle.partitions")
                ),
            },
            indent=2,
        )
    )
    print(f"[{args.method_tag}] elapsed={elapsed:.2f}s, wrote {bench_path}")

    spark.stop()


if __name__ == "__main__":
    main()
