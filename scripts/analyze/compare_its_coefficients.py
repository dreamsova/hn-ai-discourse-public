#!/usr/bin/env python3
"""Side-by-side comparison of ITS coefficients across measurement instruments.

Reads the `coefficients.csv` produced by `scripts/event_study.py` for each
classifier (TF-IDF baseline, zero-shot DeBERTa, and optionally the raw
lexicon weak-label panel) and emits a single markdown table that the
final report and the slide deck can copy verbatim.

For each (spec, outcome, term) row, the output shows the point estimate
and the p-value in parentheses for each method, plus a flag column that
flags rows whose conclusion differs across methods (sign change or one
significant + one not significant at α=0.05).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

SIG_ALPHA = 0.05

# The four "interesting" terms — others (const, t) are estimation
# nuisance and rarely belong in the headline table.
HEADLINE_TERMS = ["post", "t_post", "pulse_gpt4", "pulse_board_crisis"]

PRETTY = {
    "post": "Level shift @ ChatGPT",
    "t_post": "Slope change @ ChatGPT",
    "pulse_gpt4": "GPT-4 pulse",
    "pulse_board_crisis": "Board crisis pulse",
}


def _load(method_name: str, csv_path: Path) -> pd.DataFrame:
    if not csv_path.exists():
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    df = df[df["spec"] == "main_chatgpt_with_pulses"]
    df = df[df["term"].isin(HEADLINE_TERMS)]
    df = df[["outcome", "term", "coef", "p_value"]].copy()
    df["method"] = method_name
    return df


def _format_cell(coef: float, p: float) -> str:
    if pd.isna(coef):
        return "—"
    star = " ✱" if p < SIG_ALPHA else ""
    return f"{coef:+.4f} (p={p:.3f}){star}"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tfidf-coef",
        type=Path,
        default=Path("outputs/event_study_tfidf_v2/coefficients.csv"),
    )
    parser.add_argument(
        "--zs-coef",
        type=Path,
        default=Path("outputs/event_study_zs/coefficients.csv"),
        help="Zero-shot gated (lexicon ai_hits>0 only).",
    )
    parser.add_argument(
        "--zs-ungated-coef",
        type=Path,
        default=Path("outputs/event_study_zs_ungated/coefficients.csv"),
        help="Zero-shot ungated (all 411K, no retrieval gate).",
    )
    parser.add_argument(
        "--ft-coef",
        type=Path,
        default=Path("outputs/event_study_ft/coefficients.csv"),
        help="DistilBERT fine-tuned on 200 gold + 6K weak labels.",
    )
    parser.add_argument(
        "--output-md",
        type=Path,
        default=Path("reports/generated/its_method_comparison.md"),
    )
    args = parser.parse_args()

    method_specs = [
        ("TF-IDF baseline", args.tfidf_coef),
        ("Zero-shot DeBERTa (gated)", args.zs_coef),
        ("Zero-shot DeBERTa (ungated)", args.zs_ungated_coef),
        ("DistilBERT fine-tuned", args.ft_coef),
    ]
    frames = []
    for name, p in method_specs:
        df = _load(name, p)
        if df.empty:
            print(f"skipping {name}: no rows found at {p}")
        else:
            frames.append(df)
    if not frames:
        raise SystemExit("no coefficient files found")

    long = pd.concat(frames, ignore_index=True)
    # Pivot to (outcome, term) rows × method columns; keep coef + p_value side-by-side.
    pivot_coef = long.pivot_table(
        index=["outcome", "term"], columns="method", values="coef", aggfunc="first"
    )
    pivot_p = long.pivot_table(
        index=["outcome", "term"], columns="method", values="p_value", aggfunc="first"
    )
    methods = list(pivot_coef.columns)

    rows = []
    for (outcome, term), _ in pivot_coef.iterrows():
        record = {
            "Outcome": outcome,
            "Term": PRETTY.get(term, term),
        }
        sig_flags: list[bool] = []
        sign_set: set[int] = set()
        for m in methods:
            c = pivot_coef.loc[(outcome, term), m]
            p = pivot_p.loc[(outcome, term), m]
            record[m] = _format_cell(c, p)
            if not pd.isna(c):
                sig_flags.append(bool(p < SIG_ALPHA))
                sign_set.add(1 if c > 0 else (-1 if c < 0 else 0))
        # Flag rows where methods disagree
        disagrees = (len(set(sig_flags)) > 1) or (len(sign_set) > 1 and 0 not in sign_set)
        record["Methods agree?"] = "—" if disagrees is False else ("**disagree**" if disagrees else "")
        record["Methods agree?"] = "**disagree**" if disagrees else "agree"
        rows.append(record)

    out = pd.DataFrame(rows)
    # Order: doomer first, then accelerationist, then anything else
    def _outcome_sort(s: str) -> int:
        if "doomer" in s:
            return 0
        if "accelerationist" in s:
            return 1
        return 2
    out["_sort"] = out["Outcome"].map(_outcome_sort)
    out = out.sort_values(["_sort", "Outcome", "Term"]).drop(columns="_sort").reset_index(drop=True)

    md_lines = [
        "# ITS coefficient comparison across measurement instruments",
        "",
        "Main specification: `share_<label> ~ t + post + t_post + "
        "pulse_gpt4 + pulse_board_crisis`, fit by WLS with Newey-West HAC(3) "
        "standard errors. Weights: `n_ai_in_scope` for the v2 panels.",
        "",
        f"Coefficients flagged with ✱ are significant at α={SIG_ALPHA}.",
        "",
    ]
    md_lines.append("| " + " | ".join(out.columns) + " |")
    md_lines.append("| " + " | ".join(["---"] * len(out.columns)) + " |")
    for _, r in out.iterrows():
        md_lines.append("| " + " | ".join(str(r[c]) for c in out.columns) + " |")
    md_lines.append("")
    md_lines.append(
        "**Reading guide.** Methods 'agree' if the coefficient has the same sign "
        "AND the same significance verdict (both p<α or both p≥α). 'Disagree' "
        "rows are the ones whose headline interpretation depends on the "
        "measurement instrument and therefore deserve the most scrutiny in any "
        "narrative summary."
    )
    args.output_md.parent.mkdir(parents=True, exist_ok=True)
    args.output_md.write_text("\n".join(md_lines))
    print(f"wrote {args.output_md}")


if __name__ == "__main__":
    main()
