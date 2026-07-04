#!/usr/bin/env python3
"""Interrupted time series analysis of doomer/accelerationist framing shares.

Main specification: single-event ITS for the 2022-11-30 ChatGPT release with
level shift and slope change, weighted by monthly comment volume, with
Newey-West HAC standard errors. GPT-4 release (2023-03-14) and OpenAI board
crisis (2023-11-17) enter as pulse dummies in the main spec. Robustness:
separate single-event ITS for each event point.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm


EVENTS = {
    "chatgpt": "2022-11",
    "gpt4": "2023-03",
    "board_crisis": "2023-11",
}


def month_index(ym: str) -> int:
    year, month = ym.split("-")
    return int(year) * 12 + int(month)


def build_design(panel: pd.DataFrame, focal_event: str, pulse_events: list[str]) -> pd.DataFrame:
    df = panel.copy()
    df["t"] = df["year_month"].map(month_index)
    df["t"] = df["t"] - df["t"].min()

    focal_t = month_index(EVENTS[focal_event]) - (df["year_month"].map(month_index).min())
    df["post"] = (df["t"] >= focal_t).astype(int)
    df["t_post"] = df["post"] * (df["t"] - focal_t)

    for pulse in pulse_events:
        pulse_ym = EVENTS[pulse]
        df["pulse_%s" % pulse] = (df["year_month"] == pulse_ym).astype(int)

    return df


def fit_its(df: pd.DataFrame, outcome: str, weights: pd.Series, pulse_cols: list[str]) -> sm.regression.linear_model.RegressionResultsWrapper:
    exog_cols = ["t", "post", "t_post"] + pulse_cols
    X = sm.add_constant(df[exog_cols])
    y = df[outcome]
    model = sm.WLS(y, X, weights=weights)
    res = model.fit(cov_type="HAC", cov_kwds={"maxlags": 3})
    return res


def summarize(res, outcome: str, spec_name: str) -> dict:
    params = res.params.to_dict()
    bse = res.bse.to_dict()
    pvals = res.pvalues.to_dict()
    conf = res.conf_int(alpha=0.05)
    conf.columns = ["ci_low", "ci_high"]
    return {
        "spec": spec_name,
        "outcome": outcome,
        "n_obs": int(res.nobs),
        "r_squared": float(res.rsquared),
        "params": params,
        "se": bse,
        "p_values": pvals,
        "ci_low": conf["ci_low"].to_dict(),
        "ci_high": conf["ci_high"].to_dict(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--panel-csv", type=Path, default=Path("outputs/monthly_panel.csv"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs/event_study"))
    parser.add_argument(
        "--outcomes",
        type=str,
        default="share_doomer,share_accelerationist",
        help="Comma-separated list of outcome columns to fit ITS on. "
             "Use 'share_doomer_of_ai,share_accelerationist_of_ai' for "
             "panels produced by aggregate_monthly_v2.py.",
    )
    parser.add_argument(
        "--weight-col",
        type=str,
        default="n_comments",
        help="Column to use as WLS weights. v2 panels have 'n_ai_in_scope' "
             "which is the more principled choice for AI-conditional shares.",
    )
    args = parser.parse_args()

    panel = pd.read_csv(args.panel_csv)
    panel = panel.sort_values("year_month").reset_index(drop=True)
    if args.weight_col not in panel.columns:
        raise SystemExit(
            f"weight column {args.weight_col!r} not present in panel; "
            f"available: {list(panel.columns)}"
        )
    weights = panel[args.weight_col].clip(lower=1).astype(float)

    args.output_dir.mkdir(parents=True, exist_ok=True)

    all_results = []

    main_pulse = ["gpt4", "board_crisis"]
    main_pulse_cols = ["pulse_%s" % p for p in main_pulse]

    outcomes = [o.strip() for o in args.outcomes.split(",") if o.strip()]
    missing = [o for o in outcomes if o not in panel.columns]
    if missing:
        raise SystemExit(
            f"outcome columns missing from panel: {missing}; "
            f"available: {list(panel.columns)}"
        )

    for outcome in outcomes:
        df_main = build_design(panel, focal_event="chatgpt", pulse_events=main_pulse)
        res_main = fit_its(df_main, outcome, weights, main_pulse_cols)
        all_results.append(summarize(res_main, outcome, "main_chatgpt_with_pulses"))

        for focal in ["chatgpt", "gpt4", "board_crisis"]:
            df_r = build_design(panel, focal_event=focal, pulse_events=[])
            res_r = fit_its(df_r, outcome, weights, [])
            all_results.append(summarize(res_r, outcome, "robustness_%s_single" % focal))

    pre_chatgpt = panel[panel["year_month"] < EVENTS["chatgpt"]].copy()
    pre_summary = {}
    if len(pre_chatgpt) >= 4:
        pre_chatgpt["t"] = range(len(pre_chatgpt))
        for outcome in outcomes:
            X = sm.add_constant(pre_chatgpt[["t"]])
            y = pre_chatgpt[outcome]
            w = pre_chatgpt[args.weight_col].clip(lower=1).astype(float)
            res = sm.WLS(y, X, weights=w).fit(cov_type="HAC", cov_kwds={"maxlags": 2})
            pre_summary[outcome] = {
                "slope": float(res.params["t"]),
                "se": float(res.bse["t"]),
                "p_value": float(res.pvalues["t"]),
                "n_pre_months": int(len(pre_chatgpt)),
            }

    results_payload = {
        "events": EVENTS,
        "panel_range": [panel["year_month"].iloc[0], panel["year_month"].iloc[-1]],
        "n_months": int(len(panel)),
        "main_spec": "WLS with HAC(3) SE; weights=n_comments; pulses for GPT-4 and board crisis",
        "specifications": all_results,
        "pre_trend_test_chatgpt": pre_summary,
    }

    json_path = args.output_dir / "results.json"
    json_path.write_text(json.dumps(results_payload, indent=2))

    rows = []
    for spec in all_results:
        for name, value in spec["params"].items():
            rows.append({
                "spec": spec["spec"],
                "outcome": spec["outcome"],
                "term": name,
                "coef": value,
                "se": spec["se"].get(name),
                "p_value": spec["p_values"].get(name),
                "ci_low": spec["ci_low"].get(name),
                "ci_high": spec["ci_high"].get(name),
                "n_obs": spec["n_obs"],
                "r_squared": spec["r_squared"],
            })
    coef_df = pd.DataFrame(rows)
    coef_df.to_csv(args.output_dir / "coefficients.csv", index=False)

    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    n_plots = len(outcomes)
    fig, axes = plt.subplots(n_plots, 1, figsize=(11, 4 * n_plots), sharex=True)
    if n_plots == 1:
        axes = [axes]
    titles = [o.replace("_", " ").replace("share ", "").capitalize() + " (fitted)" for o in outcomes]
    for ax, outcome, title in zip(axes, outcomes, titles):
        df_plot = build_design(panel, focal_event="chatgpt", pulse_events=main_pulse)
        res = fit_its(df_plot, outcome, weights, main_pulse_cols)
        fitted = res.fittedvalues
        ax.plot(panel["year_month"], panel[outcome], "o-", label="observed", alpha=0.6)
        ax.plot(panel["year_month"], fitted, "-", label="ITS fit", color="red")
        for event_name, ym in EVENTS.items():
            if ym in panel["year_month"].values:
                ax.axvline(x=ym, color="gray", linestyle="--", alpha=0.5)
                ax.annotate(event_name, xy=(ym, ax.get_ylim()[1] * 0.95),
                            rotation=90, fontsize=8, va="top")
        ax.set_title(title)
        ax.set_ylabel("Share")
        ax.legend(loc="upper left", fontsize=8)
        ax.tick_params(axis="x", rotation=45, labelsize=7)
    plt.tight_layout()
    plot_path = args.output_dir / "its_plot.png"
    plt.savefig(plot_path, dpi=150)
    plt.close()

    print("wrote %s" % json_path)
    print("wrote %s" % (args.output_dir / "coefficients.csv"))
    print("wrote %s" % plot_path)


if __name__ == "__main__":
    main()
