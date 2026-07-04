#!/usr/bin/env python3
"""Cluster the 411K HN AI-discourse comments into topics with BERTopic.

Reads the 5-D UMAP output (`outputs/umap_5d.parquet`) plus the raw
sentence-transformer embeddings, fits HDBSCAN clusters in the 5-D
space, and uses class-based TF-IDF to surface each topic's top words.
Output:

  outputs/topics_per_comment.parquet    [comment_id, topic, topic_prob]
  outputs/topic_words.csv               [topic, rank, word, score]
  outputs/topic_summary.csv             [topic, n_comments, top_words, ...]
  outputs/topic_by_month.parquet        [year_month, topic, n_comments]

The topic-by-month table is the substantive payoff: it shows how
specific clusters (e.g. governance/alignment discourse, GPT-product
chatter, AI-replacing-jobs framing) wax and wane across the event
windows, providing semantic structure that the simple
doomer/accelerationist/neutral split collapses.
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
        "--umap-parquet",
        type=Path,
        default=Path("outputs/umap_5d.parquet"),
    )
    parser.add_argument(
        "--embeddings-parquet",
        type=Path,
        default=Path("outputs/corpus_embeddings.parquet"),
        help="Original 384-d embeddings; BERTopic uses them for class-tfidf "
             "representation even when clustering is on the reduced UMAP.",
    )
    parser.add_argument(
        "--clean-glob",
        type=str,
        default="data/clean/year=*/month=*/family=*/query=*/*.parquet",
        help="Used to pull combined_text for per-topic exemplars and "
             "class-based TF-IDF.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("outputs/topics"),
    )
    parser.add_argument(
        "--min-cluster-size",
        type=int,
        default=200,
        help="HDBSCAN min_cluster_size — controls topic granularity.",
    )
    parser.add_argument(
        "--top-n-words",
        type=int,
        default=15,
    )
    parser.add_argument("--seed", type=int, default=20260526)
    args = parser.parse_args()

    # Lazy imports.
    import hdbscan
    from bertopic import BERTopic
    from bertopic.vectorizers import ClassTfidfTransformer
    from sklearn.feature_extraction.text import CountVectorizer

    args.output_dir.mkdir(parents=True, exist_ok=True)
    t0 = time.time()

    # Load reduced coordinates + raw embeddings
    print(f"loading {args.umap_parquet} ...")
    umap_df = pd.read_parquet(args.umap_parquet)
    umap_cols = [c for c in umap_df.columns if c.startswith("umap_")]
    print(f"UMAP columns: {umap_cols}")
    coords_5d = umap_df[umap_cols].to_numpy(dtype=np.float32)
    print(f"coords_5d: {coords_5d.shape}")

    print(f"loading {args.embeddings_parquet} ...")
    emb_df = pd.read_parquet(args.embeddings_parquet)
    # Align ordering by comment_id (UMAP preserves order from embed step but
    # be defensive — join on comment_id to guarantee).
    umap_df["comment_id"] = umap_df["comment_id"].astype(str)
    emb_df["comment_id"] = emb_df["comment_id"].astype(str)
    merged = umap_df.merge(
        emb_df[["comment_id", "embedding"]],
        on="comment_id", how="left",
    )
    assert merged["embedding"].notna().all(), "embedding join failed"
    coords_5d = merged[umap_cols].to_numpy(dtype=np.float32)
    emb_384 = np.asarray(merged["embedding"].tolist(), dtype=np.float32)
    print(f"aligned matrices: 5d={coords_5d.shape}, 384d={emb_384.shape}")

    # Load combined_text for class-tfidf
    import glob
    text_frames = []
    for p in sorted(glob.glob(args.clean_glob)):
        text_frames.append(
            pd.read_parquet(p, columns=["comment_id", "combined_text"])
        )
    text_df = pd.concat(text_frames, ignore_index=True)
    text_df["comment_id"] = text_df["comment_id"].astype(str)
    text_df = text_df.drop_duplicates(subset=["comment_id"], keep="first")
    merged = merged.merge(text_df, on="comment_id", how="left")
    merged["combined_text"] = merged["combined_text"].fillna("")
    docs = merged["combined_text"].tolist()
    print(f"loaded {len(docs):,} text rows")

    # HDBSCAN cluster on the 5-D UMAP space
    print(f"clustering with HDBSCAN min_cluster_size={args.min_cluster_size} ...")
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=args.min_cluster_size,
        metric="euclidean",
        cluster_selection_method="eom",
        prediction_data=True,
    )
    clusterer.fit(coords_5d)
    topic_labels = clusterer.labels_
    n_topics = int(topic_labels.max()) + 1
    n_noise = int((topic_labels == -1).sum())
    print(f"HDBSCAN: {n_topics} topics + {n_noise:,} noise points "
          f"({100 * n_noise / len(topic_labels):.1f}%)")

    # Run BERTopic with pre-computed embeddings + pre-computed clusters
    print("fitting BERTopic with custom clusters ...")
    vectorizer = CountVectorizer(
        ngram_range=(1, 2), min_df=10, max_df=0.5,
        stop_words="english",
    )
    ctfidf = ClassTfidfTransformer(reduce_frequent_words=True)
    topic_model = BERTopic(
        umap_model=None,         # we pre-reduced
        hdbscan_model=clusterer, # pre-fit
        vectorizer_model=vectorizer,
        ctfidf_model=ctfidf,
        calculate_probabilities=False,
        verbose=True,
    )
    # BERTopic expects to "fit" but with pre-computed embeddings + pre-fit
    # clusterer it will skip the heavy steps.
    topics, _ = topic_model.fit_transform(docs, embeddings=emb_384)

    # Save outputs
    out_topics = pd.DataFrame({
        "comment_id": merged["comment_id"].to_numpy(),
        "year_month": merged["year_month"].to_numpy(),
        "topic": topics,
    })
    out_topics.to_parquet(args.output_dir / "topics_per_comment.parquet",
                          index=False)

    info = topic_model.get_topic_info()
    info.to_csv(args.output_dir / "topic_summary.csv", index=False)

    # Top words per topic
    rows = []
    for t in info["Topic"]:
        words = topic_model.get_topic(t) or []
        for r, (w, s) in enumerate(words[: args.top_n_words]):
            rows.append({"topic": t, "rank": r, "word": w, "score": float(s)})
    pd.DataFrame(rows).to_csv(args.output_dir / "topic_words.csv", index=False)

    # Topic-by-month panel for the report's substantive section
    tbm = (
        out_topics.groupby(["year_month", "topic"])
        .size()
        .rename("n_comments")
        .reset_index()
    )
    tbm.to_parquet(args.output_dir / "topic_by_month.parquet", index=False)
    tbm.to_csv(args.output_dir / "topic_by_month.csv", index=False)

    elapsed = time.time() - t0
    print(f"BERTopic done in {elapsed:.1f}s; wrote {args.output_dir}/")
    print(info.head(20).to_string(index=False))


if __name__ == "__main__":
    main()
