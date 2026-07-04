#!/usr/bin/env python3
"""Fine-tune DistilBERT-base for three-class stance classification.

Trains on the union of:
  - 200 hand-labeled gold rows (`reports/gold_set_labeled.csv`),
    filtered to those whose `gold_label` is in {doomer, accelerationist,
    neutral}. These are the high-quality anchors.
  - The ~6K weak-label rows used by `scripts/train_classifier.py`
    (the cleaned shards' `weak_label` filtered to the same three
    classes). These provide volume but with known label noise.

The gold rows are oversampled (or up-weighted) so they aren't drowned
out by the larger weak-label set.

After training, runs inference on all 411K rows and writes a parallel
`predicted_label_ft` column for the cross-method ITS comparison.

Output:
  outputs/model/distilbert_stance/        (model weights + tokenizer)
  data/inference_ft/year=*/.../*.parquet  (same partition tree, with predicted_label_ft)
  outputs/distilbert_eval.json            (gold-set metrics)
"""
from __future__ import annotations

import argparse
import glob
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

STANCE_LABELS = ["accelerationist", "doomer", "neutral"]
LABEL_TO_ID = {lab: i for i, lab in enumerate(STANCE_LABELS)}
ID_TO_LABEL = {i: lab for lab, i in LABEL_TO_ID.items()}


def load_training_data(
    gold_csv: Path, clean_glob: str, weak_oversample: int = 1,
) -> tuple[list[str], list[int], list[float]]:
    """Return (texts, label_ids, sample_weights)."""
    # Gold rows
    gold = pd.read_csv(gold_csv)
    gold = gold[gold["gold_label"].isin(STANCE_LABELS)].copy()
    gold["text"] = gold["combined_text"].fillna("").astype(str)
    gold["label_id"] = gold["gold_label"].map(LABEL_TO_ID)
    gold_texts = gold["text"].tolist()
    gold_labels = gold["label_id"].tolist()
    gold_weights = [3.0] * len(gold_texts)  # 3x weight vs weak labels

    # Weak rows (from cleaned shards, is_high_precision_label = True)
    weak_frames = []
    for p in sorted(glob.glob(clean_glob)):
        weak_frames.append(pd.read_parquet(p, columns=[
            "comment_id", "combined_text", "weak_label", "is_high_precision_label",
        ]))
    weak = pd.concat(weak_frames, ignore_index=True)
    weak = weak[
        weak["is_high_precision_label"].astype(bool)
        & weak["weak_label"].isin(STANCE_LABELS)
    ].copy()
    weak["comment_id"] = weak["comment_id"].astype(str)
    weak = weak.drop_duplicates(subset=["comment_id"], keep="first")
    # Drop any weak row whose comment_id is already in the gold set to
    # avoid leakage.
    gold_ids = set(gold["comment_id"].astype(str))
    weak = weak[~weak["comment_id"].astype(str).isin(gold_ids)]
    weak["text"] = weak["combined_text"].fillna("").astype(str)
    weak["label_id"] = weak["weak_label"].map(LABEL_TO_ID)
    weak_texts = weak["text"].tolist()
    weak_labels = weak["label_id"].tolist()
    weak_weights = [1.0] * len(weak_texts)

    print(f"training pool: gold={len(gold_texts)} (weight 3.0), "
          f"weak={len(weak_texts)} (weight 1.0)")
    return (
        gold_texts + weak_texts,
        gold_labels + weak_labels,
        gold_weights + weak_weights,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gold-csv", type=Path,
                        default=Path("reports/gold_set_labeled.csv"))
    parser.add_argument("--clean-glob", type=str,
                        default="data/clean/year=*/month=*/family=*/query=*/*.parquet")
    parser.add_argument("--inference-glob", type=str,
                        default="data/inference/year=*/month=*/family=*/query=*/*.parquet",
                        help="Used to get the same partition tree for the FT output.")
    parser.add_argument("--model-name", type=str,
                        default="distilbert-base-uncased")
    parser.add_argument("--output-model-dir", type=Path,
                        default=Path("outputs/model/distilbert_stance"))
    parser.add_argument("--output-inference-root", type=Path,
                        default=Path("data/inference_ft"))
    parser.add_argument("--output-eval-json", type=Path,
                        default=Path("outputs/distilbert_eval.json"))
    parser.add_argument("--max-length", type=int, default=256)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--epochs", type=int, default=3)
    parser.add_argument("--lr", type=float, default=2e-5)
    parser.add_argument("--eval-only", action="store_true",
                        help="Skip training; just run inference using the existing model dir.")
    parser.add_argument("--skip-inference", action="store_true")
    parser.add_argument("--seed", type=int, default=20260526)
    args = parser.parse_args()

    import torch
    from torch.utils.data import DataLoader, Dataset
    from transformers import (
        AutoModelForSequenceClassification, AutoTokenizer,
        get_linear_schedule_with_warmup,
    )
    from sklearn.metrics import classification_report, confusion_matrix

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"device: {device}")
    torch.manual_seed(args.seed)
    np.random.seed(args.seed)

    tokenizer = AutoTokenizer.from_pretrained(args.model_name)

    class StanceDataset(Dataset):
        def __init__(self, texts, labels, weights, tok, max_length):
            self.encodings = tok(
                texts, truncation=True, padding="max_length",
                max_length=max_length, return_tensors="pt",
            )
            self.labels = torch.tensor(labels, dtype=torch.long)
            self.weights = torch.tensor(weights, dtype=torch.float)

        def __len__(self):
            return len(self.labels)

        def __getitem__(self, i):
            return {
                "input_ids": self.encodings["input_ids"][i],
                "attention_mask": self.encodings["attention_mask"][i],
                "labels": self.labels[i],
                "weight": self.weights[i],
            }

    # Training
    if not args.eval_only:
        texts, labels, weights = load_training_data(
            args.gold_csv, args.clean_glob,
        )
        # Split off 10% of gold for eval (the gold set itself, since
        # weak labels are noisy and not a meaningful eval).
        gold_df = pd.read_csv(args.gold_csv)
        eval_df = gold_df[gold_df["gold_label"].isin(STANCE_LABELS)].sample(
            frac=0.2, random_state=args.seed,
        )
        eval_texts = eval_df["combined_text"].fillna("").astype(str).tolist()
        eval_labels = eval_df["gold_label"].map(LABEL_TO_ID).tolist()

        # Drop eval comment_ids from training pool to avoid leakage.
        eval_ids = set(eval_df["comment_id"].astype(str))
        keep_mask = []
        gold_csv_ids = pd.read_csv(args.gold_csv)["comment_id"].astype(str).tolist()
        # Reload gold to align ids with texts/labels we already have
        # (cheap; gold is 200 rows)
        gold_full = pd.read_csv(args.gold_csv)
        gold_full = gold_full[gold_full["gold_label"].isin(STANCE_LABELS)]
        gold_ids_in_train_order = gold_full["comment_id"].astype(str).tolist()
        keep_train = [i for i, cid in enumerate(gold_ids_in_train_order)
                      if cid not in eval_ids]
        # texts / labels / weights are gold-then-weak; only filter the
        # gold portion.
        n_gold = len(gold_ids_in_train_order)
        texts_kept = (
            [texts[i] for i in keep_train] + texts[n_gold:]
        )
        labels_kept = (
            [labels[i] for i in keep_train] + labels[n_gold:]
        )
        weights_kept = (
            [weights[i] for i in keep_train] + weights[n_gold:]
        )

        train_ds = StanceDataset(
            texts_kept, labels_kept, weights_kept, tokenizer, args.max_length,
        )
        eval_ds = StanceDataset(
            eval_texts, eval_labels, [1.0] * len(eval_texts),
            tokenizer, args.max_length,
        )

        train_loader = DataLoader(train_ds, batch_size=args.batch_size, shuffle=True)
        eval_loader = DataLoader(eval_ds, batch_size=args.batch_size, shuffle=False)

        model = AutoModelForSequenceClassification.from_pretrained(
            args.model_name, num_labels=len(STANCE_LABELS),
        ).to(device)

        optim = torch.optim.AdamW(model.parameters(), lr=args.lr)
        num_steps = len(train_loader) * args.epochs
        sched = get_linear_schedule_with_warmup(
            optim, num_warmup_steps=int(0.1 * num_steps),
            num_training_steps=num_steps,
        )
        loss_fn = torch.nn.CrossEntropyLoss(reduction="none")

        print(f"training {args.epochs} epochs over {len(train_ds)} examples")
        t0 = time.time()
        for epoch in range(args.epochs):
            model.train()
            running = 0.0
            n_batches = 0
            for batch in train_loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                logits = model(
                    input_ids=batch["input_ids"],
                    attention_mask=batch["attention_mask"],
                ).logits
                per_ex = loss_fn(logits, batch["labels"])
                loss = (per_ex * batch["weight"]).mean()
                optim.zero_grad()
                loss.backward()
                optim.step()
                sched.step()
                running += float(loss)
                n_batches += 1
            print(f"epoch {epoch + 1}/{args.epochs} avg loss "
                  f"{running / max(n_batches, 1):.4f} "
                  f"({time.time() - t0:.1f}s elapsed)")

        # Eval on held-out gold
        model.eval()
        all_preds, all_labels = [], []
        with torch.no_grad():
            for batch in eval_loader:
                batch = {k: v.to(device) for k, v in batch.items()}
                logits = model(
                    input_ids=batch["input_ids"],
                    attention_mask=batch["attention_mask"],
                ).logits
                preds = logits.argmax(-1).cpu().tolist()
                all_preds.extend(preds)
                all_labels.extend(batch["labels"].cpu().tolist())
        report = classification_report(
            all_labels, all_preds,
            labels=list(range(len(STANCE_LABELS))),
            target_names=STANCE_LABELS,
            output_dict=True, zero_division=0,
        )
        cm = confusion_matrix(all_labels, all_preds,
                              labels=list(range(len(STANCE_LABELS))))
        args.output_eval_json.parent.mkdir(parents=True, exist_ok=True)
        args.output_eval_json.write_text(json.dumps({
            "n_train": len(train_ds), "n_eval": len(eval_ds),
            "classification_report": report,
            "confusion_matrix": cm.tolist(),
            "label_order": STANCE_LABELS,
        }, indent=2))
        print(f"eval on held-out gold ({len(eval_ds)} rows):")
        print(json.dumps(report, indent=2))

        args.output_model_dir.mkdir(parents=True, exist_ok=True)
        model.save_pretrained(args.output_model_dir)
        tokenizer.save_pretrained(args.output_model_dir)
        print(f"saved model to {args.output_model_dir}")

    # Inference on the full 411K corpus
    if args.skip_inference:
        return

    model = AutoModelForSequenceClassification.from_pretrained(
        args.output_model_dir,
    ).to(device)
    model.eval()
    tokenizer = AutoTokenizer.from_pretrained(args.output_model_dir)

    args.output_inference_root.mkdir(parents=True, exist_ok=True)
    inf_paths = sorted(glob.glob(args.inference_glob))
    t0 = time.time()
    for i, p in enumerate(inf_paths):
        df = pd.read_parquet(p)
        df["combined_text"] = df.get("combined_text", "").fillna("").astype(str)
        texts = df["combined_text"].tolist()
        preds = []
        for start in range(0, len(texts), args.batch_size):
            chunk = texts[start : start + args.batch_size]
            enc = tokenizer(
                chunk, truncation=True, padding=True,
                max_length=args.max_length, return_tensors="pt",
            ).to(device)
            with torch.no_grad():
                logits = model(**enc).logits
            preds.extend(logits.argmax(-1).cpu().tolist())
        df["predicted_label_ft"] = [ID_TO_LABEL[p] for p in preds]
        rel = Path(p).relative_to("data/inference")
        out = args.output_inference_root / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out, index=False)
        if (i + 1) % 50 == 0 or i == len(inf_paths) - 1:
            elapsed = time.time() - t0
            print(f"[{i + 1}/{len(inf_paths)}] shards inferred "
                  f"({elapsed:.1f}s, "
                  f"{1000 * elapsed / (i + 1):.0f} ms/shard)")


if __name__ == "__main__":
    main()
