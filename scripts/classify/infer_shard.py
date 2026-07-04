#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd

from hn_ai_discourse.io_utils import drop_known_suffixes
from hn_ai_discourse.text_utils import find_partition_relative_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Run inference on one cleaned shard.")
    parser.add_argument("--input-path", type=Path, required=True)
    parser.add_argument("--model-path", type=Path, default=Path("outputs/model/tfidf_logreg.joblib"))
    parser.add_argument("--output-root", type=Path, default=Path("data/inference"))
    args = parser.parse_args()

    frame = pd.read_parquet(args.input_path).copy()
    model = joblib.load(args.model_path)

    frame["predicted_label"] = "non_ai"
    frame["prob_accelerationist"] = 0.0
    frame["prob_doomer"] = 0.0
    frame["prob_neutral"] = 0.0

    ai_mask = frame["ai_hits"].fillna(0).astype(int) > 0
    if ai_mask.any():
        ai_text = frame.loc[ai_mask, "combined_text"].fillna("")
        probs = model.predict_proba(ai_text)
        labels = model.predict(ai_text)
        prob_frame = pd.DataFrame(probs, columns=["prob_%s" % label for label in model.classes_], index=frame.index[ai_mask])
        for column in prob_frame.columns:
            frame.loc[ai_mask, column] = prob_frame[column]
        frame.loc[ai_mask, "predicted_label"] = labels

    relative = find_partition_relative_path(args.input_path)
    out_name = "%s.parquet" % drop_known_suffixes(relative)
    out_path = args.output_root / relative.parent / out_name if relative.parent != Path(".") else args.output_root / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(out_path, index=False)
    print("wrote %d inference rows to %s" % (len(frame), out_path))


if __name__ == "__main__":
    main()
