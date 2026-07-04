#!/usr/bin/env python3
"""Automated retrieval-recall audit using sentence-transformer embeddings.

The lexicon-based retrieval gate (`ai_hits > 0`) decides which comments
even reach the stance classifier. The earlier 50-row hand audit gave a
Wilson CI on retrieval recall that was too wide to be useful. This
script scales that audit to the full corpus using semantic similarity:

  1. Embed a small set of AI-discussion "anchor" sentences.
  2. For every cleaned comment (including those the lexicon discarded),
     compute the maximum cosine similarity to any anchor.
  3. Flag comments above a similarity threshold as "AI-by-semantics".
  4. Cross-tab against `ai_hits > 0` to estimate retrieval false
     negatives at scale.

Output:
  outputs/retrieval_audit_embedding.csv     per-month FN-rate estimate
  outputs/retrieval_audit_summary.md        narrative summary

Implementation notes: anchors are encoded once on CPU (cheap), the
full 411K × 384 embedding matrix is loaded from
`outputs/corpus_embeddings.parquet` (produced by the earlier embed
GPU job), and cosine similarities are computed in a single matmul.
"""
from __future__ import annotations

import argparse
import glob
from pathlib import Path

import numpy as np
import pandas as pd


# Hand-written anchor sentences. The matrix-max-similarity captures
# "any of these notions" rather than averaging.
AI_ANCHORS = [
    "This comment discusses artificial intelligence systems.",
    "This comment discusses a large language model.",
    "This comment expresses concern about AI safety or AI alignment.",
    "This comment discusses machine learning research or deep learning.",
    "This comment discusses deploying GPT, Claude, Gemini, or another foundation model.",
    "This comment discusses how AI will change jobs, the economy, or society.",
]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--embeddings-parquet",
        type=Path,
        default=Path("outputs/corpus_embeddings.parquet"),
    )
    parser.add_argument(
        "--clean-glob",
        type=str,
        default="data/clean/year=*/month=*/family=*/query=*/*.parquet",
    )
    parser.add_argument(
        "--similarity-threshold",
        type=float,
        default=0.55,
        help="Cosine-similarity cutoff for 'semantically AI'. "
             "0.55 is a conservative default for normalized MiniLM embeddings.",
    )
    parser.add_argument(
        "--model-name",
        type=str,
        default="sentence-transformers/all-MiniLM-L6-v2",
        help="Same model used for the corpus embeddings.",
    )
    parser.add_argument(
        "--output-csv",
        type=Path,
        default=Path("outputs/retrieval_audit_embedding.csv"),
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("reports/generated/retrieval_audit_embedding.md"),
    )
    args = parser.parse_args()

    import torch
    from sentence_transformers import SentenceTransformer

    # Encode anchors (CPU is fine; only 6 sentences)
    print(f"loading model {args.model_name} (anchors only) ...")
    model = SentenceTransformer(args.model_name, device="cpu")
    anchor_emb = model.encode(
        AI_ANCHORS, normalize_embeddings=True, convert_to_numpy=True,
    ).astype(np.float32)  # shape (n_anchors, 384)
    print(f"encoded {len(AI_ANCHORS)} anchors -> {anchor_emb.shape}")

    # Load corpus embeddings
    print(f"loading {args.embeddings_parquet} ...")
    emb_df = pd.read_parquet(args.embeddings_parquet)
    emb_df["comment_id"] = emb_df["comment_id"].astype(str)
    corpus = np.asarray(emb_df["embedding"].tolist(), dtype=np.float32)
    # Embeddings from embed_corpus.py were normalized at encode time,
    # but re-normalize defensively in case the parquet roundtrip changed
    # anything.
    norms = np.linalg.norm(corpus, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    corpus = corpus / norms
    print(f"corpus: {corpus.shape}")

    # Cosine similarity (matmul on normalized vectors)
    print("computing max cosine similarity per row ...")
    sims = corpus @ anchor_emb.T  # (N, n_anchors)
    max_sim = sims.max(axis=1)
    emb_df["max_anchor_sim"] = max_sim
    emb_df["semantically_ai"] = max_sim >= args.similarity_threshold

    # Join with lexicon ai_hits to compute FN rate
    clean_frames = []
    for p in sorted(glob.glob(args.clean_glob)):
        clean_frames.append(pd.read_parquet(p, columns=["comment_id", "ai_hits"]))
    clean = pd.concat(clean_frames, ignore_index=True)
    clean["comment_id"] = clean["comment_id"].astype(str)
    clean = clean.drop_duplicates(subset=["comment_id"], keep="first")
    clean["lexicon_retrieved"] = (clean["ai_hits"].fillna(0).astype(int) > 0)
    merged = emb_df.merge(
        clean[["comment_id", "ai_hits", "lexicon_retrieved"]],
        on="comment_id", how="left",
    )
    print(f"joined: {len(merged):,} rows")

    # Confusion (lexicon_retrieved × semantically_ai)
    tot = len(merged)
    a = int(((merged["lexicon_retrieved"]) & (merged["semantically_ai"])).sum())
    b = int(((merged["lexicon_retrieved"]) & (~merged["semantically_ai"])).sum())
    c = int(((~merged["lexicon_retrieved"]) & (merged["semantically_ai"])).sum())
    d = int(((~merged["lexicon_retrieved"]) & (~merged["semantically_ai"])).sum())
    fn_rate = c / max(c + a, 1)  # FN / (FN + TP_lexicon)
    recall = a / max(a + c, 1)

    # Per-month false-negative rate
    per_month = (
        merged.groupby("year_month")
        .agg(
            n_total=("comment_id", "count"),
            n_lex_in=("lexicon_retrieved", "sum"),
            n_sem_ai=("semantically_ai", "sum"),
            n_lex_out_sem_in=(
                "comment_id",
                lambda s: int(((~merged.loc[s.index, "lexicon_retrieved"]) &
                               (merged.loc[s.index, "semantically_ai"])).sum()),
            ),
        )
        .reset_index()
    )
    per_month["est_retrieval_recall"] = per_month["n_lex_in"] / (
        per_month["n_lex_in"] + per_month["n_lex_out_sem_in"]
    ).clip(lower=1)
    args.output_csv.parent.mkdir(parents=True, exist_ok=True)
    per_month.to_csv(args.output_csv, index=False)

    # Markdown summary
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text(
        f"""# Embedding-based retrieval audit

Anchor sentences encoded with `{args.model_name}`. A comment is
labeled **semantically AI** if its embedding has cosine similarity
≥ {args.similarity_threshold:.2f} to at least one of the {len(AI_ANCHORS)}
anchors.

## Corpus-wide confusion

| | semantically_ai = True | semantically_ai = False |
| --- | --- | --- |
| lexicon_retrieved = True  | **{a:,}** (true positive) | {b:,} |
| lexicon_retrieved = False | **{c:,}** (lexicon false negative) | {d:,} |

- Estimated retrieval recall: **{100 * recall:.1f}%**
- Estimated false-negative rate: **{100 * fn_rate:.1f}%**

Full per-month table: `{args.output_csv}`.

## Interpretation

This number complements the 200-row gold-set audit. The gold set
measured **lexicon precision** (51% of lexicon-retrieved comments
were `wrong_other` / off-topic). This embedding audit measures
**lexicon recall** (what fraction of semantically-AI comments did the
lexicon miss?). Together they bound the lexicon's signal/noise floor
in both directions.
"""
    )
    print(f"wrote {args.output_csv} and {args.output_md}")
    print(f"corpus-wide retrieval recall ≈ {100 * recall:.1f}%")
    print(f"corpus-wide lexicon false-negative rate ≈ {100 * fn_rate:.1f}%")


if __name__ == "__main__":
    main()
