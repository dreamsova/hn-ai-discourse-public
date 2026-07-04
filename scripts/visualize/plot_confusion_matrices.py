#!/usr/bin/env python3
"""4-method × 3-class confusion-matrix grid + per-class F1 bar.

Reads the gold-set scoring outputs and produces one figure that
shows each classifier's confusion against the 200-row hand gold,
plus a final panel summarizing per-class F1 across the four methods.
This is the visual form of `reports/generated/gold_validation.md`.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

STANCE = ["accelerationist", "doomer", "neutral"]
METHODS = [
    ("Lexicon rule",          "Lexicon weak-label rule",            "#888888"),
    ("TF-IDF + LR",           "TF-IDF + LR (baseline)",             "#aaaaaa"),
    ("Zero-shot DeBERTa",     "Zero-shot DeBERTa-v3-large NLI",     "#007c80"),
    ("DistilBERT fine-tuned", "DistilBERT fine-tuned",              "#bf5700"),
]


def load_gold(path: Path) -> dict:
    return json.loads(path.read_text())


def load_distilbert_eval(path: Path) -> dict | None:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def find_method_block(payload: dict, pretty_label: str) -> dict | None:
    """The gold-set JSON nests per-method results under per_method."""
    per_method = payload.get("per_method", {})
    return per_method.get(pretty_label)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--gold-json",
        type=Path,
        default=Path("reports/generated/gold_validation.json"),
    )
    parser.add_argument(
        "--distilbert-json",
        type=Path,
        default=Path("outputs/distilbert_eval.json"),
        help="Standalone DistilBERT eval (held-out subset of gold).",
    )
    parser.add_argument(
        "--output-png",
        type=Path,
        default=Path("deliverables/confusion_matrices.png"),
    )
    args = parser.parse_args()

    gold = load_gold(args.gold_json)
    distil = load_distilbert_eval(args.distilbert_json)

    # Pull each method's confusion + per-class F1.
    method_payloads: list[tuple[str, np.ndarray | None, dict, str]] = []
    for short, pretty, color in METHODS:
        block = find_method_block(gold, pretty)
        if block is not None:
            cm = np.array(block["confusion_matrix"])
            f1s = {
                lab: block["classification_report"].get(lab, {}).get("f1-score", 0.0)
                for lab in STANCE
            }
            method_payloads.append((short, cm, f1s, color))
        elif short == "DistilBERT fine-tuned" and distil is not None:
            # The DistilBERT eval is on a held-out subset of the gold set
            # so we read it from its standalone json. Re-order to match
            # STANCE.
            label_order = distil.get("label_order", STANCE)
            cm_raw = np.array(distil["confusion_matrix"])
            idx_map = [label_order.index(lab) for lab in STANCE
                       if lab in label_order]
            cm = cm_raw[np.ix_(idx_map, idx_map)]
            f1s = {
                lab: distil["classification_report"].get(lab, {}).get("f1-score", 0.0)
                for lab in STANCE
            }
            method_payloads.append((short, cm, f1s, color))
        else:
            method_payloads.append((short, None, {lab: 0.0 for lab in STANCE}, color))

    # Figure
    fig, axes = plt.subplots(
        1, 5, figsize=(20, 4.4),
        constrained_layout=True,
        gridspec_kw={"width_ratios": [1, 1, 1, 1, 1.3]},
    )

    for ax, (short, cm, _, _) in zip(axes[:4], method_payloads):
        if cm is None:
            ax.set_axis_off()
            ax.set_title(f"{short}\n(no data)")
            continue
        cm_norm = cm.astype(float) / cm.sum(axis=1, keepdims=True).clip(1)
        im = ax.imshow(cm_norm, cmap="Oranges", vmin=0, vmax=1, aspect="auto")
        ax.set_xticks(range(len(STANCE)))
        ax.set_yticks(range(len(STANCE)))
        ax.set_xticklabels([s[:5] for s in STANCE], fontsize=9)
        ax.set_yticklabels(STANCE, fontsize=9)
        ax.set_xlabel("predicted", fontsize=9)
        ax.set_ylabel("gold", fontsize=9)
        ax.set_title(short, fontsize=11)
        for i in range(len(STANCE)):
            for j in range(len(STANCE)):
                count = int(cm[i, j])
                ax.text(j, i, str(count),
                        ha="center", va="center", fontsize=10,
                        color="white" if cm_norm[i, j] > 0.5 else "#1c2736")

    # F1 comparison panel
    f1_ax = axes[4]
    n_methods = len(method_payloads)
    bar_w = 0.22
    x = np.arange(len(STANCE))
    for i, (short, _, f1s, color) in enumerate(method_payloads):
        offsets = x + (i - n_methods / 2) * bar_w + bar_w / 2
        f1_ax.bar(
            offsets,
            [f1s[lab] for lab in STANCE],
            width=bar_w, color=color, edgecolor="#1c2736",
            linewidth=0.4, label=short,
        )
    f1_ax.set_xticks(x)
    f1_ax.set_xticklabels([s[:5] for s in STANCE], fontsize=9)
    f1_ax.set_ylim(0, 1.0)
    f1_ax.set_ylabel("F1", fontsize=10)
    f1_ax.set_title("Per-class F1 vs gold set", fontsize=11)
    f1_ax.legend(fontsize=8, loc="upper left", framealpha=0.9)
    f1_ax.grid(axis="y", linestyle="--", alpha=0.3)
    f1_ax.set_axisbelow(True)
    f1_ax.spines["top"].set_visible(False)
    f1_ax.spines["right"].set_visible(False)

    fig.suptitle(
        "Four-method gold-set evaluation — confusion matrices and per-class F1",
        fontsize=13, y=1.04,
    )

    args.output_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output_png, dpi=170, bbox_inches="tight")
    print(f"wrote {args.output_png}")


if __name__ == "__main__":
    main()
