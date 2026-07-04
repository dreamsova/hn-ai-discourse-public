#!/usr/bin/env python3
"""Score classifier predictions against human-labeled gold set.

Reads the labeled CSV produced by sample_for_validation.py (after manual
labeling fills in the gold_label column), computes per-class precision,
recall, F1, and a confusion matrix per method, and writes a markdown
report that compares each method.

By default it evaluates the TF-IDF + LR baseline (`predicted_label`). If
zero-shot NLI inference has been run and merged into the labeled CSV via
`scripts/merge_zs_into_gold.py`, the `predicted_label_zs` column is
auto-detected and evaluated side-by-side.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix

VALID_GOLD = {"doomer", "accelerationist", "neutral"}


def evaluate(df: pd.DataFrame, pred_col: str) -> dict:
    """Run classification_report + confusion_matrix for one predicted-label column."""
    sub = df[df[pred_col].notna() & (df[pred_col] != "")].copy()
    sub["pred_norm"] = sub[pred_col].astype(str).str.strip().str.lower()
    # Drop rows where pred is one of the non-stance classes (not_retrieved / non_ai)
    sub = sub[sub["pred_norm"].isin(VALID_GOLD)]
    labels = sorted(VALID_GOLD)
    if sub.empty:
        return {"n_evaluable": 0, "classification_report": {}, "confusion_matrix": []}
    report = classification_report(
        sub["gold_norm"], sub["pred_norm"],
        labels=labels, output_dict=True, zero_division=0,
    )
    cm = confusion_matrix(sub["gold_norm"], sub["pred_norm"], labels=labels)
    return {
        "n_evaluable_for_method": int(len(sub)),
        "labels": labels,
        "classification_report": report,
        "confusion_matrix": cm.tolist(),
    }


def render_method_block(name: str, payload: dict) -> list[str]:
    if payload.get("n_evaluable_for_method", 0) == 0:
        return [f"## {name}", "", f"_No evaluable rows for `{name}` — column missing or empty._", ""]

    labels = payload["labels"]
    report = payload["classification_report"]
    cm = payload["confusion_matrix"]
    lines: list[str] = []
    lines.append(f"## {name}")
    lines.append("")
    lines.append(f"_Evaluable rows for this method: {payload['n_evaluable_for_method']}_")
    lines.append("")
    lines.append("| Class | Precision | Recall | F1 | Support |")
    lines.append("| --- | --- | --- | --- | --- |")
    for label in labels:
        row = report.get(label, {})
        lines.append(
            f"| {label} | {row.get('precision', 0):.3f} | {row.get('recall', 0):.3f} | "
            f"{row.get('f1-score', 0):.3f} | {int(row.get('support', 0))} |"
        )
    macro = report.get("macro avg", {})
    lines.append(
        f"| **macro avg** | {macro.get('precision', 0):.3f} | {macro.get('recall', 0):.3f} | "
        f"{macro.get('f1-score', 0):.3f} | {int(macro.get('support', 0))} |"
    )
    lines.append("")
    lines.append(f"Overall accuracy: **{report.get('accuracy', 0):.3f}**")
    lines.append("")
    lines.append("Confusion matrix (rows = gold, cols = predicted):")
    lines.append("")
    header = "| gold \\ pred | " + " | ".join(labels) + " |"
    sep = "| --- |" + " --- |" * len(labels)
    lines.append(header)
    lines.append(sep)
    for i, label in enumerate(labels):
        row = "| " + label + " | " + " | ".join(str(int(x)) for x in cm[i]) + " |"
        lines.append(row)
    lines.append("")
    return lines


def render_summary_table(per_method: dict[str, dict]) -> list[str]:
    """Side-by-side macro-F1 table for quick reading."""
    lines: list[str] = []
    methods = [m for m, p in per_method.items() if p.get("n_evaluable_for_method", 0) > 0]
    if len(methods) < 2:
        return lines
    lines.append("## Method comparison")
    lines.append("")
    lines.append("Macro F1 per class, across all evaluated methods:")
    lines.append("")
    classes = sorted(VALID_GOLD)
    header = "| Class | " + " | ".join(methods) + " |"
    sep = "| --- |" + " --- |" * len(methods)
    lines.append(header)
    lines.append(sep)
    for cls in classes:
        cells: list[str] = []
        for m in methods:
            f1 = per_method[m]["classification_report"].get(cls, {}).get("f1-score", 0)
            cells.append(f"{f1:.3f}")
        lines.append(f"| {cls} | " + " | ".join(cells) + " |")
    macro_cells = [
        f"{per_method[m]['classification_report'].get('macro avg', {}).get('f1-score', 0):.3f}"
        for m in methods
    ]
    lines.append(f"| **macro F1** | " + " | ".join(macro_cells) + " |")
    acc_cells = [
        f"{per_method[m]['classification_report'].get('accuracy', 0):.3f}"
        for m in methods
    ]
    lines.append(f"| **accuracy** | " + " | ".join(acc_cells) + " |")
    lines.append("")
    return lines


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-csv", type=Path, default=Path("reports/gold_set_labeled.csv"))
    parser.add_argument("--output-md", type=Path, default=Path("reports/generated/gold_validation.md"))
    parser.add_argument("--output-json", type=Path, default=Path("reports/generated/gold_validation.json"))
    parser.add_argument(
        "--pred-cols",
        type=str,
        default="predicted_label,predicted_label_zs,weak_label",
        help="Comma-separated list of predicted-label columns to evaluate (silently skipped if absent).",
    )
    args = parser.parse_args()

    df = pd.read_csv(args.input_csv)
    df = df[df["gold_label"].notna() & (df["gold_label"].astype(str).str.strip() != "")]
    if len(df) == 0:
        raise SystemExit("no labeled rows in %s" % args.input_csv)

    df["gold_norm"] = df["gold_label"].astype(str).str.strip().str.lower()
    df = df[df["gold_norm"].isin(VALID_GOLD | {"wrong_other"})]
    eval_df = df[df["gold_norm"].isin(VALID_GOLD)].copy()

    method_pretty = {
        "predicted_label": "TF-IDF + LR (baseline)",
        "predicted_label_zs": "Zero-shot DeBERTa-v3-large NLI",
        "weak_label": "Lexicon weak-label rule",
    }

    per_method: dict[str, dict] = {}
    requested_cols = [c.strip() for c in args.pred_cols.split(",") if c.strip()]
    for col in requested_cols:
        if col not in eval_df.columns:
            print(f"skipping {col!r}: column not present in CSV")
            continue
        name = method_pretty.get(col, col)
        per_method[name] = evaluate(eval_df, col)

    n_wrong_other = int((df["gold_norm"] == "wrong_other").sum())
    payload = {
        "n_labeled_total": int(len(df)),
        "n_evaluable_gold": int(len(eval_df)),
        "n_wrong_other": n_wrong_other,
        "wrong_other_share": (n_wrong_other / max(len(df), 1)),
        "per_method": per_method,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2))

    lines: list[str] = []
    lines.append("# Gold-set validation")
    lines.append("")
    lines.append(f"- Total labeled rows: {payload['n_labeled_total']}")
    lines.append(
        f"- Evaluable rows (gold ∈ {{doomer, accelerationist, neutral}}): "
        f"{payload['n_evaluable_gold']}"
    )
    lines.append(
        f"- Marked `wrong_other` (lexicon false positive or off-topic): "
        f"{payload['n_wrong_other']} "
        f"({100 * payload['wrong_other_share']:.1f}% of labeled rows)"
    )
    lines.append("")
    lines.append(
        "> **Note on the wrong_other rate**: this is the empirical lexicon "
        "false-positive rate. If this number is non-trivial (>5%), the AI "
        "retrieval gate is noisier than the pipeline assumes."
    )
    lines.append("")

    lines.extend(render_summary_table(per_method))
    for name, payload_m in per_method.items():
        lines.extend(render_method_block(name, payload_m))

    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(lines))
    print("wrote %s and %s" % (args.output_md, args.output_json))


if __name__ == "__main__":
    main()
