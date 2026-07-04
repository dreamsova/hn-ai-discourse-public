#!/usr/bin/env python3
"""Reduce 384-dim sentence-transformer embeddings to lower dimensions via UMAP.

Runs twice in the pipeline with different parameters:
  - n_components=2, min_dist=0.1  →  for the DataShader semantic atlas
  - n_components=5, min_dist=0.0  →  for BERTopic clustering input

UMAP fit on a stratified subsample (default 50K rows balanced over
year_month + predicted_label) for speed, then `transform` the rest. The
2-D output is ~3.3 MB on 411K rows (two float32 columns); the 5-D output
is ~8.3 MB.
"""
from __future__ import annotations

import argparse
import time
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-parquet",
        type=Path,
        default=Path("outputs/corpus_embeddings.parquet"),
        help="Parquet with `comment_id`, `year_month`, `predicted_label`, "
             "`embedding` (list of 384 fp16 floats) — produced by "
             "scripts/embed_corpus.py.",
    )
    parser.add_argument("--output-parquet", type=Path, required=True,
                        help="Output parquet path.")
    parser.add_argument("--n-components", type=int, default=2)
    parser.add_argument("--n-neighbors", type=int, default=15)
    parser.add_argument("--min-dist", type=float, default=0.1)
    parser.add_argument("--metric", type=str, default="cosine")
    parser.add_argument("--fit-sample", type=int, default=50000,
                        help="UMAP fit on this many stratified rows; "
                             "transform applies to the full corpus.")
    parser.add_argument("--seed", type=int, default=20260526)
    args = parser.parse_args()

    # Lazy imports so syntax check passes without optional deps installed.
    import umap

    t0 = time.time()
    print(f"loading {args.input_parquet} ...")
    df = pd.read_parquet(args.input_parquet)
    n_total = len(df)
    print(f"loaded {n_total:,} rows; embedding column dtype: "
          f"{type(df['embedding'].iloc[0]).__name__}")

    # Materialize embedding column as a (N, 384) float32 matrix.
    emb = np.asarray(df["embedding"].tolist(), dtype=np.float32)
    print(f"embedding matrix: {emb.shape} {emb.dtype}")

    # Stratified subsample for fit: balanced across (year_month,
    # predicted_label) so UMAP doesn't overfit dominant months/classes.
    fit_n = min(args.fit_sample, n_total)
    if fit_n < n_total:
        rng = np.random.default_rng(args.seed)
        # Per-(year_month, predicted_label) quota = fit_n divided by the
        # actual number of observed cells, not by an assumed label count.
        n_strata = df.groupby(
            ["year_month", "predicted_label"], observed=True
        ).ngroups
        per_cell = max(1, fit_n // max(1, n_strata))
        df_sample_idx = (
            df.groupby(["year_month", "predicted_label"], observed=True)
            .apply(lambda g: g.sample(
                n=min(len(g), per_cell),
                random_state=rng.integers(0, 1_000_000),
            ))
            .index.get_level_values(-1)
            .unique()
            .tolist()
        )
        # If stratified sample is too small or too large, pad/truncate
        # via a uniform supplement to hit fit_n exactly.
        sample_idx = list(df_sample_idx)[:fit_n]
        if len(sample_idx) < fit_n:
            remaining = list(set(range(n_total)) - set(sample_idx))
            extra = rng.choice(remaining, size=fit_n - len(sample_idx),
                               replace=False)
            sample_idx = sample_idx + list(extra)
        fit_emb = emb[sample_idx]
        print(f"stratified fit sample: {len(fit_emb):,} rows")
    else:
        fit_emb = emb
        print(f"fitting on full corpus ({n_total:,} rows)")

    print(f"fitting UMAP n_components={args.n_components} "
          f"n_neighbors={args.n_neighbors} min_dist={args.min_dist} "
          f"metric={args.metric} ...")
    reducer = umap.UMAP(
        n_components=args.n_components,
        n_neighbors=args.n_neighbors,
        min_dist=args.min_dist,
        metric=args.metric,
        random_state=args.seed,
        verbose=True,
    )
    reducer.fit(fit_emb)
    print(f"fit done in {time.time() - t0:.1f}s; transforming full corpus ...")
    t1 = time.time()
    coords = reducer.transform(emb)
    print(f"transform done in {time.time() - t1:.1f}s; coords shape {coords.shape}")

    out = df[["comment_id", "year_month", "predicted_label"]].copy()
    for k in range(args.n_components):
        out[f"umap_{k}"] = coords[:, k].astype(np.float32)
    args.output_parquet.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args.output_parquet, index=False)
    size_mb = args.output_parquet.stat().st_size / (1024 * 1024)
    elapsed = time.time() - t0
    print(f"wrote {args.output_parquet} ({size_mb:.1f} MB, "
          f"{len(out):,} rows); total elapsed {elapsed:.1f}s")


if __name__ == "__main__":
    main()
