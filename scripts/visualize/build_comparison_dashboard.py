#!/usr/bin/env python3
"""Side-by-side dashboard comparing the TF-IDF baseline panel and the
zero-shot NLI panel on the same Y axis.

The key validity question for this project is whether the headline ITS
finding (doomer share rises around AI events; accelerationist share has
distinctive event-window behavior) is robust to the choice of
measurement instrument. Eyeballing the two trajectories on the same
plot is the cheapest way to answer that.

Reads two monthly panels with `share_<label>_of_ai` columns produced by
`scripts/aggregate_monthly_v2.py` and renders a self-contained HTML page
with one Bokeh figure per stance class (doomer / accelerationist /
neutral), each holding both methods' time series, plus event markers.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from bokeh.embed import file_html
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool, Span, Label, Div
from bokeh.plotting import figure
from bokeh.resources import CDN

EVENTS = [
    ("2022-11", "ChatGPT release", "#bf5700"),
    ("2023-03", "GPT-4 release", "#007c80"),
    ("2023-11", "OpenAI board crisis", "#1c2736"),
]

STANCES = ["doomer", "accelerationist", "neutral"]


def make_method_compare_plot(merged: pd.DataFrame, stance: str) -> figure:
    """One plot per stance class, showing all available methods on the same axis."""
    source = ColumnDataSource(merged)
    p = figure(
        x_range=merged["year_month"].tolist(),
        height=320,
        width=1100,
        title=f"Monthly share of '{stance}' framing across measurement instruments",
        toolbar_location="above",
        tools="pan,box_zoom,reset,save,wheel_zoom",
    )

    # Each method tuple: (column_suffix, legend_label, color, line_width)
    methods = [
        ("tfidf", "TF-IDF + LR (lexicon-trained)", "#888888", 2.2),
        ("zs", "Zero-shot DeBERTa (lexicon-gated)", "#007c80", 2.4),
        ("zs_ungated", "Zero-shot DeBERTa (ungated, full 411K)", "#bf5700", 2.6),
    ]

    tooltip_items = [("Month", "@year_month")]
    plotted_cols = []
    for suffix, label, color, lw in methods:
        col = f"share_{stance}_of_ai_{suffix}"
        if col not in merged.columns:
            continue
        p.line(x="year_month", y=col, source=source, color=color,
               line_width=lw, legend_label=label)
        p.scatter(x="year_month", y=col, source=source, size=5, color=color)
        tooltip_items.append((f"{stance} ({suffix})", f"@{col}{{0.000}}"))
        plotted_cols.append(col)

    p.xaxis.major_label_orientation = 1.0
    p.xaxis.major_label_text_font_size = "8pt"
    p.yaxis.axis_label = "Share of AI-in-scope comments"
    p.legend.location = "top_left"
    p.legend.click_policy = "hide"
    p.add_tools(HoverTool(tooltips=tooltip_items))

    for ym, label, color in EVENTS:
        if ym in merged["year_month"].values:
            idx = merged["year_month"].tolist().index(ym)
            span = Span(location=idx, dimension="height", line_color=color,
                        line_dash="dashed", line_width=1.5)
            p.add_layout(span)
            ymax = max((merged[c].max() for c in plotted_cols), default=0.1)
            lbl = Label(x=idx, y=ymax * 1.05, text=label, text_color=color,
                        text_font_size="9pt", angle=1.4)
            p.add_layout(lbl)

    return p


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--tfidf-panel",
        type=Path,
        default=Path("outputs/panel_tfidf/monthly_panel.parquet"),
        help="Output of aggregate_monthly_v2.py with --predicted-col predicted_label.",
    )
    parser.add_argument(
        "--zs-panel",
        type=Path,
        default=Path("outputs/panel_zs/monthly_panel.parquet"),
        help="Output of aggregate_monthly_v2.py with --predicted-col predicted_label_zs.",
    )
    parser.add_argument(
        "--zs-ungated-panel",
        type=Path,
        default=Path("outputs/panel_zs_ungated/monthly_panel.parquet"),
        help="Output of aggregate_monthly_v2.py with --predicted-col predicted_label_zs "
             "applied to the ungated 411K corpus (optional).",
    )
    parser.add_argument(
        "--output-html",
        type=Path,
        default=Path("deliverables/hn-ai-discourse-method-comparison.html"),
    )
    args = parser.parse_args()

    keep = ["year_month", "n_ai_in_scope"] + [f"share_{s}_of_ai" for s in STANCES]

    def load_and_rename(path: Path, suffix: str) -> pd.DataFrame:
        df = pd.read_parquet(path)[keep].rename(columns={
            "n_ai_in_scope": f"n_ai_{suffix}",
            **{f"share_{s}_of_ai": f"share_{s}_of_ai_{suffix}" for s in STANCES},
        })
        return df

    tfidf = load_and_rename(args.tfidf_panel, "tfidf")
    zs = load_and_rename(args.zs_panel, "zs")
    merged = tfidf.merge(zs, on="year_month", how="inner")
    print(f"merged TF-IDF + zero-shot gated: {len(merged)} months")

    if args.zs_ungated_panel.exists():
        zs_ungated = load_and_rename(args.zs_ungated_panel, "zs_ungated")
        merged = merged.merge(zs_ungated, on="year_month", how="left")
        print(f"merged in zero-shot ungated: {len(merged)} months")

    merged = merged.sort_values("year_month")

    header_methods = "TF-IDF + LR; zero-shot DeBERTa NLI (lexicon-gated)"
    if "share_doomer_of_ai_zs_ungated" in merged.columns:
        header_methods += "; zero-shot DeBERTa NLI (ungated, 411K)"
    header = Div(
        text=(
            "<h2>Measurement-method comparison</h2>"
            f"<p>Each panel plots monthly framing shares produced by "
            f"independent measurement instruments on the same 411K-comment "
            f"corpus: {header_methods}. The denominator in all series is "
            "<code>n_doomer + n_accelerationist + n_neutral</code> (AI-in-scope "
            "comments only). Click a legend entry to hide a series; hover to "
            "see exact monthly values.</p>"
        ),
        width=1100,
    )
    plots = [make_method_compare_plot(merged, s) for s in STANCES]
    layout = column(header, *plots)
    html = file_html(layout, CDN, title="HN AI discourse — method comparison")

    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(html, encoding="utf-8")
    print("wrote %s (%.1f KB)" % (args.output_html, args.output_html.stat().st_size / 1024))


if __name__ == "__main__":
    main()
