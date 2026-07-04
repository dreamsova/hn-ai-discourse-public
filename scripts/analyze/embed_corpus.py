#!/usr/bin/env python3
"""Embed the full HN AI-discourse corpus with sentence-transformers.

Reads cleaned shards, embeds `combined_text` with
`sentence-transformers/all-MiniLM-L6-v2` on a single GPU in fp16
batches, and writes a single parquet keyed by `comment_id` with
columns `[comment_id, year_month, predicted_label, emb_0, ..., emb_383]`
(or `embedding` as a list column — see --layout).

This is the upstream half of the Phase-7 semantic-atlas extension:
embeddings feed UMAP 2D reduction (`scripts/umap_reduce.py`, separate)
and then a DataShader + Bokeh interactive atlas
(`scripts/build_atlas_dashboard.py`, separate). The embedding step is
the GPU-bound part; keeping it as a standalone job means UMAP can be
re-fit on CPU without re-touching the GPU.

Compute profile on Midway:
  - Model: ~80 MB, loads in <10 s on a Quadro RTX 6000 / V100 / A100
  - Throughput on 411K AI-retrieved comments at batch=128, max_length=256:
      ~300-600 samples/sec on a V100, ~1000+ on A100
      Wall clock: 10-20 min single GPU
  - Output size: 411K × 384 float16 ≈ 250 MB parquet
"""
from __future__ import annotations

import argparse
import glob
import time
from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--input-glob",
        type=str,
        default="data/clean/year=*/month=*/family=*/query=*/*.parquet",
        help="Glob of cleaned shards. Read via pandas (small enough to fit).",
    )
    parser.add_argument(
        "--inference-glob",
        type=str,
        default="data/inference/year=*/month=*/family=*/query=*/*.parquet",
        help="Glob of TF-IDF inference shards (only used to attach predicted_label).",
    )
    parser.add_argument(
        "--output-parquet",
        type=Path,
        default=Path("outputs/corpus_embeddings.parquet"),
    )
    parser.add_argument("--model-name", type=str,
                        default="sentence-transformers/all-MiniLM-L6-v2")
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--max-length", type=int, default=256,
                        help="Tokenizer truncation length passed to "
                             "SentenceTransformer.max_seq_length.")
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="If set, embed only the first N rows (for smoke tests).",
    )
    args = parser.parse_args()

    # Lazy import so the script can be syntax-checked without torch installed.
    import torch
    from sentence_transformers import SentenceTransformer

    # Load cleaned text
    paths = sorted(glob.glob(args.input_glob))
    if not paths:
        raise SystemExit(f"no shards matched: {args.input_glob}")
    print(f"loading {len(paths)} cleaned shards ...")
    frames = []
    for p in paths:
        frames.append(pd.read_parquet(p, columns=[
            "comment_id", "year_month", "combined_text",
        ]))
    df = pd.concat(frames, ignore_index=True)
    # Coerce comment_id to string for stable joins (different shards wrote it
    # as int vs string — same issue that broke Spark).
    df["comment_id"] = df["comment_id"].astype(str)
    df = df.drop_duplicates(subset=["comment_id"], keep="first").reset_index(drop=True)
    print(f"unique comment_ids after dedup: {len(df):,}")

    if args.limit:
        df = df.head(args.limit).copy()
        print(f"limit applied: embedding {len(df)} rows")

    # Attach predicted_label from TF-IDF inference (for atlas coloring)
    inf_paths = sorted(glob.glob(args.inference_glob))
    if inf_paths:
        print(f"loading {len(inf_paths)} inference shards (for predicted_label) ...")
        inf_frames = []
        for p in inf_paths:
            inf_frames.append(pd.read_parquet(p, columns=[
                "comment_id", "predicted_label",
            ]))
        inf = pd.concat(inf_frames, ignore_index=True)
        inf["comment_id"] = inf["comment_id"].astype(str)
        inf = inf.drop_duplicates(subset=["comment_id"], keep="first")
        df = df.merge(inf, on="comment_id", how="left")
        df["predicted_label"] = df["predicted_label"].fillna("not_retrieved")
    else:
        df["predicted_label"] = "not_retrieved"
    print("predicted_label distribution:")
    print(df["predicted_label"].value_counts().to_string())

    # Embed on GPU
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"loading {args.model_name} on {device} ...")
    model = SentenceTransformer(args.model_name, device=device)
    # MiniLM (22M params) is small enough that fp32 is fine on V100/A100;
    # fp16 saves <100 MB at the cost of touching a private attribute that
    # changes across sentence-transformers releases. Stay in fp32.
    model.max_seq_length = args.max_length

    texts = df["combined_text"].fillna("").astype(str).tolist()
    t0 = time.time()
    emb = model.encode(
        texts,
        batch_size=args.batch_size,
        show_progress_bar=True,
        convert_to_numpy=True,
        normalize_embeddings=True,  # cosine sim downstream
    )
    elapsed = time.time() - t0
    print(
        f"embedded {len(texts):,} rows in {elapsed:.1f}s "
        f"({len(texts) / max(elapsed, 1e-6):.1f} samples/s)"
    )

    # Write parquet
    # Store the 384-d vector as a list column. fp16 to halve disk size; UMAP
    # downstream will cast back to float32 on load.
    out = df[["comment_id", "year_month", "predicted_label"]].copy()
    out["embedding"] = list(emb.astype(np.float16))
    args.output_parquet.parent.mkdir(parents=True, exist_ok=True)
    out.to_parquet(args.output_parquet, index=False)
    size_mb = args.output_parquet.stat().st_size / (1024 * 1024)
    print(f"wrote {args.output_parquet} ({size_mb:.1f} MB, {len(out):,} rows)")


if __name__ == "__main__":
    main()
