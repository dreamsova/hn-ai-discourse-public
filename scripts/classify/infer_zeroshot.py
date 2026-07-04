#!/usr/bin/env python3
"""Zero-shot NLI stance inference on the AI-retrieved subset.

Runs `MoritzLaurer/deberta-v3-large-zeroshot-v2.0` over rows with
`ai_hits > 0` and writes a parallel parquet with columns
`predicted_label_zs` ∈ {doomer, accelerationist, neutral, not_retrieved}
and per-class probabilities. Rows with `ai_hits == 0` get
`not_retrieved` so downstream aggregation can decide how to treat
them.
"""
from __future__ import annotations

import argparse
import math
import time
from pathlib import Path

import pandas as pd
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

DEFAULT_MODEL = "MoritzLaurer/deberta-v3-large-zeroshot-v2.0"

# Hypothesis templates. The label is what we tag back on the row; the
# hypothesis text is what the NLI model scores entailment against the
# (premise = comment text).
HYPOTHESES = {
    "doomer": "This comment expresses fear, pessimism, or alarm about AI risk, AI safety, AI misalignment, or catastrophic outcomes from AI.",
    "accelerationist": "This comment expresses excitement, optimism, or enthusiasm about rapidly building, deploying, or accelerating AI progress.",
    "neutral": "This comment is technical, descriptive, or product-oriented about AI without taking a normative stance for or against AI development.",
}

LABEL_ORDER = ["doomer", "accelerationist", "neutral"]


def build_premise(row: pd.Series) -> str:
    """One coherent premise that includes thread context.

    `combined_text` in this repo already prepends the story title to the
    comment body, so we use it directly. Truncation happens at the
    tokenizer level (max_length=512).
    """
    text = row.get("combined_text") or ""
    return str(text)


def score_batch(
    premises: list[str],
    model,
    tokenizer,
    device: torch.device,
    batch_size: int,
    max_length: int = 256,
) -> list[dict[str, float]]:
    """Score a list of premises against the three hypotheses.

    Returns list of dicts, one per premise, with keys ``prob_<label>``
    summing to 1 (renormalized over the three label hypotheses).
    """
    results: list[dict[str, float]] = []
    hypothesis_texts = [HYPOTHESES[label] for label in LABEL_ORDER]

    # We pair each premise with each of the three hypotheses, so the
    # effective batch sent to the model is `batch_size * 3` pairs.
    for start in range(0, len(premises), batch_size):
        chunk = premises[start : start + batch_size]
        premise_inputs: list[str] = []
        hypothesis_inputs: list[str] = []
        for p in chunk:
            for h in hypothesis_texts:
                premise_inputs.append(p)
                hypothesis_inputs.append(h)

        enc = tokenizer(
            premise_inputs,
            hypothesis_inputs,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=max_length,
        ).to(device)

        with torch.no_grad():
            logits = model(**enc).logits  # shape [B*3, num_labels]

        # NLI models output [contradiction, neutral, entailment] OR
        # [entailment, neutral, contradiction]. We look up which index
        # corresponds to "entailment" from id2label.
        ent_id = model.config.label2id.get("entailment")
        if ent_id is None:
            # Fall back to last column (zeroshot-v2 model convention)
            ent_id = logits.shape[-1] - 1
        entail_scores = logits[:, ent_id].view(-1, len(LABEL_ORDER))  # [B, 3]
        probs = torch.softmax(entail_scores, dim=-1).cpu().numpy()  # [B, 3]

        for row_probs in probs:
            results.append(
                {f"prob_{label}_zs": float(row_probs[i]) for i, label in enumerate(LABEL_ORDER)}
            )
    return results


def process_shard(
    input_path: Path,
    output_root: Path,
    model,
    tokenizer,
    device: torch.device,
    batch_size: int,
    max_length: int = 256,
    ungated: bool = False,
) -> tuple[int, int, float]:
    """Score one cleaned shard and write predictions parquet.

    Returns (n_total, n_scored, seconds).
    """
    frame = pd.read_parquet(input_path).copy()
    n_total = len(frame)

    # Defaults
    frame["predicted_label_zs"] = "not_retrieved"
    for label in LABEL_ORDER:
        frame[f"prob_{label}_zs"] = 0.0

    if ungated:
        # Score every comment; lexicon ai_hits is ignored. Zero-shot
        # DeBERTa then acts as proxy oracle for retrieval recall: any
        # comment it confidently labels doomer/accel/neutral while the
        # lexicon said ai_hits=0 is a lexicon false-negative.
        ai_mask = pd.Series(True, index=frame.index)
    else:
        ai_mask = frame["ai_hits"].fillna(0).astype(int) > 0
    n_scored = int(ai_mask.sum())
    t0 = time.time()
    if n_scored > 0:
        sub = frame.loc[ai_mask]
        premises = [build_premise(row) for _, row in sub.iterrows()]
        scored = score_batch(premises, model, tokenizer, device, batch_size, max_length=max_length)

        for i, label in enumerate(LABEL_ORDER):
            col = f"prob_{label}_zs"
            frame.loc[ai_mask, col] = [s[col] for s in scored]

        prob_cols = [f"prob_{label}_zs" for label in LABEL_ORDER]
        best = frame.loc[ai_mask, prob_cols].values.argmax(axis=1)
        frame.loc[ai_mask, "predicted_label_zs"] = [LABEL_ORDER[i] for i in best]

    elapsed = time.time() - t0

    # Mirror the cleaned directory tree under the output root.
    parts = input_path.parts
    try:
        idx = parts.index("clean")
        relative = Path(*parts[idx + 1 :])
    except ValueError:
        relative = Path(input_path.name)
    out_path = output_root / relative
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(out_path, index=False)
    return n_total, n_scored, elapsed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-glob", type=str, required=True,
                        help="Glob of cleaned shard parquets to score.")
    parser.add_argument("--output-root", type=Path,
                        default=Path("data/inference_zs"))
    parser.add_argument("--model-name", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--batch-size", type=int, default=32,
                        help="Comments per batch (effective batch sent to GPU is 3x this).")
    parser.add_argument("--max-length", type=int, default=256,
                        help="Tokenizer truncation length. Most HN comments fit in 256; "
                             "raise to 512 if you need full-context but expect 4x memory.")
    parser.add_argument("--limit-shards", type=int, default=None,
                        help="If set, process only the first N shards (smoke test).")
    parser.add_argument("--shard-range", type=str, default=None,
                        help="e.g. '0:315' to process shards [0,315). Used by 4-GPU Slurm array.")
    parser.add_argument("--ungated", action="store_true",
                        help="Score ALL comments, not just ai_hits>0. Uses zero-shot DeBERTa "
                             "as proxy oracle for retrieval recall: comments the lexicon "
                             "missed will still be classified into doomer/accel/neutral.")
    parser.add_argument("--device", type=str, default="auto",
                        help="auto | cuda | cpu")
    args = parser.parse_args()

    import glob

    paths = sorted(Path(p) for p in glob.glob(args.input_glob))
    if args.shard_range:
        start_s, end_s = args.shard_range.split(":")
        paths = paths[int(start_s) : int(end_s)]
    if args.limit_shards:
        paths = paths[: args.limit_shards]
    if not paths:
        raise SystemExit("no shards matched glob: %s" % args.input_glob)

    device_str = args.device
    if device_str == "auto":
        device_str = "cuda" if torch.cuda.is_available() else "cpu"
    device = torch.device(device_str)
    print("loading model %s on %s ..." % (args.model_name, device_str))

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    model = AutoModelForSequenceClassification.from_pretrained(args.model_name)
    if device.type == "cuda":
        model = model.to(device).half()  # fp16 for A100 throughput
    else:
        model = model.to(device)
    model.eval()
    print("model loaded; processing %d shards" % len(paths))

    args.output_root.mkdir(parents=True, exist_ok=True)
    t_start = time.time()
    total_rows = 0
    total_scored = 0
    for i, p in enumerate(paths):
        n_total, n_scored, secs = process_shard(
            p, args.output_root, model, tokenizer, device, args.batch_size,
            max_length=args.max_length,
            ungated=args.ungated,
        )
        total_rows += n_total
        total_scored += n_scored
        rate = (n_scored / secs) if (n_scored and secs > 0) else 0.0
        print(
            "[%d/%d] %s  rows=%d  scored=%d  %.1fs  (%.1f scored/s)"
            % (i + 1, len(paths), p.name, n_total, n_scored, secs, rate),
            flush=True,
        )

    elapsed = time.time() - t_start
    overall_rate = total_scored / elapsed if elapsed > 0 else 0.0
    print(
        "DONE in %.1fs: %d shards, %d total rows, %d scored (%.1f scored/s overall)"
        % (elapsed, len(paths), total_rows, total_scored, overall_rate)
    )


if __name__ == "__main__":
    main()
