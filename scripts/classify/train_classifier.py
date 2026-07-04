#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline


ALLOWED_LABELS = ["doomer", "accelerationist", "neutral"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Train a framing classifier from weak labels.")
    parser.add_argument("--input-glob", required=True)
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/model"))
    parser.add_argument("--random-state", type=int, default=42)
    parser.add_argument("--min-df", type=int, default=2)
    args = parser.parse_args()

    files = sorted(glob.glob(args.input_glob, recursive=True))
    if not files:
        raise SystemExit("no parquet files matched %s" % args.input_glob)

    frame = pd.concat((pd.read_parquet(path) for path in files), ignore_index=True)
    frame = frame.drop_duplicates(subset=["comment_id"])
    frame = frame[frame["weak_label"].isin(ALLOWED_LABELS)].copy()
    frame = frame[frame["is_high_precision_label"].astype(bool)].copy()
    if frame.empty:
        raise SystemExit("no training rows remained after filtering")

    x = frame["combined_text"].fillna("")
    y = frame["weak_label"]

    pipeline = Pipeline(
        [
            ("tfidf", TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=args.min_df, max_features=50000)),
            ("clf", LogisticRegression(max_iter=1000)),
        ]
    )

    class_counts = y.value_counts().sort_index().to_dict()
    can_stratify = min(class_counts.values()) >= 2 and len(frame) >= 12

    if can_stratify:
        x_train, x_test, y_train, y_test = train_test_split(
            x,
            y,
            test_size=0.25,
            random_state=args.random_state,
            stratify=y,
        )
        pipeline.fit(x_train, y_train)
        preds = pipeline.predict(x_test)
        metrics = {
            "evaluation_type": "held_out",
            "accuracy": accuracy_score(y_test, preds),
            "classification_report": classification_report(y_test, preds, output_dict=True, zero_division=0),
            "confusion_matrix": confusion_matrix(y_test, preds, labels=ALLOWED_LABELS).tolist(),
            "n_docs": int(len(frame)),
            "n_train": int(len(x_train)),
            "n_test": int(len(x_test)),
            "class_counts": class_counts,
        }
    else:
        pipeline.fit(x, y)
        preds = pipeline.predict(x)
        metrics = {
            "evaluation_type": "training_only",
            "accuracy": accuracy_score(y, preds),
            "classification_report": classification_report(y, preds, output_dict=True, zero_division=0),
            "confusion_matrix": confusion_matrix(y, preds, labels=ALLOWED_LABELS).tolist(),
            "n_docs": int(len(frame)),
            "n_train": int(len(frame)),
            "n_test": 0,
            "class_counts": class_counts,
        }

    args.output_dir.mkdir(parents=True, exist_ok=True)
    model_path = args.output_dir / "tfidf_logreg.joblib"
    metrics_path = args.output_dir / "metrics.json"
    counts_path = args.output_dir / "class_counts.csv"

    joblib.dump(pipeline, model_path)
    metrics_path.write_text(json.dumps(metrics, indent=2, sort_keys=True), encoding="utf-8")
    pd.DataFrame(
        [{"label": label, "count": class_counts.get(label, 0)} for label in ALLOWED_LABELS]
    ).to_csv(counts_path, index=False)

    print("trained model on %d docs" % len(frame))
    print("saved model to %s" % model_path)
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
