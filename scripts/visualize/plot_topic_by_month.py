#!/usr/bin/env python3
"""Stacked-area chart of top BERTopic clusters by month.

Reads `outputs/topics/topic_by_month.parquet` (one row per
(year_month, topic, n_comments) from `scripts/bertopic_fit.py`),
joins on the per-topic top words from
`outputs/topics/topic_summary.csv`, and renders a self-contained
Bokeh HTML page with one stacked-area trace per top-N topic and
shaded event-month bands for ChatGPT / GPT-4 / board crisis.

Output:
  deliverables/hn-ai-discourse-topic-by-month.html
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd


EVENTS = [
    ("2022-11", "ChatGPT release"),
    ("2023-03", "GPT-4 release"),
    ("2023-11", "OpenAI board crisis"),
]

# Same palette as the atlas so the two dashboards line up visually.
TOPIC_PALETTE = [
    "#bf5700", "#007c80", "#8e44ad", "#27ae60", "#d35400",
    "#2980b9", "#c0392b", "#16a085", "#e67e22", "#9b59b6",
    "#34495e", "#f39c12", "#1abc9c", "#e74c3c", "#3498db",
]


def short_topic_label(name_field: str, fallback: str) -> str:
    if isinstance(name_field, str) and name_field:
        parts = name_field.split("_", 1)
        if len(parts) == 2:
            words = re.split(r"[_,]", parts[1])
            words = [w.strip() for w in words if w.strip()]
            return " · ".join(words[:3]) or fallback
    return fallback


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--topic-by-month",
        type=Path,
        default=Path("outputs/topics/topic_by_month.parquet"),
    )
    parser.add_argument(
        "--topic-summary",
        type=Path,
        default=Path("outputs/topics/topic_summary.csv"),
    )
    parser.add_argument("--top-n", type=int, default=12)
    parser.add_argument(
        "--output-html",
        type=Path,
        default=Path("deliverables/hn-ai-discourse-topic-by-month.html"),
    )
    args = parser.parse_args()

    from bokeh.embed import file_html
    from bokeh.layouts import column
    from bokeh.models import (
        ColumnDataSource, HoverTool, Span, Label, Div, BoxAnnotation,
    )
    from bokeh.plotting import figure
    from bokeh.resources import CDN

    print(f"loading {args.topic_by_month}")
    df = pd.read_parquet(args.topic_by_month)

    print(f"loading {args.topic_summary}")
    summary = pd.read_csv(args.topic_summary)
    topic_col = "Topic" if "Topic" in summary.columns else "topic"
    name_col = "Name" if "Name" in summary.columns else "name"
    summary["topic"] = summary[topic_col].astype(int)

    # Identify top-N topics by total count, excluding -1 noise cluster.
    total = (
        df[df["topic"] != -1]
        .groupby("topic")["n_comments"].sum()
        .sort_values(ascending=False)
    )
    top_topics = total.head(args.top_n).index.tolist()
    print(f"top {len(top_topics)} topics: {top_topics}")

    label_map = {
        int(r["topic"]): short_topic_label(r[name_col], f"topic {int(r['topic'])}")
        for _, r in summary.iterrows()
    }

    # Pivot to wide: rows=year_month, columns=topic, values=n_comments
    sub = df[df["topic"].isin(top_topics)].copy()
    wide = (
        sub.pivot_table(
            index="year_month", columns="topic", values="n_comments",
            aggfunc="sum", fill_value=0,
        )
        .sort_index()
    )
    wide = wide[top_topics]  # preserve top-N order
    months = wide.index.tolist()

    # Stacked-area series. Bokeh `varea_stack` expects a wide source.
    source_data: dict[str, list] = {"year_month": months}
    for t in top_topics:
        source_data[f"t{int(t):03d}"] = wide[t].tolist()
    source = ColumnDataSource(data=source_data)

    p = figure(
        x_range=months,
        height=520, width=1200,
        title="Top BERTopic clusters by month — what kinds of HN comments the "
              "lexicon actually retrieves",
        toolbar_location="above",
        tools="pan,box_zoom,wheel_zoom,reset,save",
    )
    stackers = [f"t{int(t):03d}" for t in top_topics]
    colors = [TOPIC_PALETTE[i % len(TOPIC_PALETTE)] for i in range(len(top_topics))]
    legend_labels = [label_map.get(int(t), f"topic {int(t)}") for t in top_topics]

    renderers = p.varea_stack(
        stackers=stackers, x="year_month", source=source,
        color=colors, legend_label=legend_labels, alpha=0.85,
    )

    # Hover (one tooltip per stacker — Bokeh's varea_stack convention).
    for r, label, col in zip(renderers, legend_labels, stackers):
        hover = HoverTool(renderers=[r], tooltips=[
            ("Month", "@year_month"),
            ("Topic", label),
            ("Comments", f"@{col}{{0,0}}"),
        ])
        p.add_tools(hover)

    p.xaxis.major_label_orientation = 1.0
    p.xaxis.major_label_text_font_size = "8pt"
    p.yaxis.axis_label = "Comments per month (stacked)"
    p.legend.location = "top_left"
    p.legend.click_policy = "mute"
    p.legend.label_text_font_size = "9pt"

    for ym, label in EVENTS:
        if ym in months:
            idx = months.index(ym)
            span = Span(location=idx, dimension="height",
                        line_color="#1c2736", line_dash="dashed",
                        line_width=1.5)
            p.add_layout(span)
            ymax = wide.sum(axis=1).max()
            lbl = Label(
                x=idx, y=ymax * 1.02, text=label,
                text_color="#1c2736", text_font_size="9pt",
                angle=1.4,
            )
            p.add_layout(lbl)

    header = Div(
        text=(
            "<h2>Topic activity over time</h2>"
            "<p>Each band is the monthly count of HN comments assigned to "
            "one of the top BERTopic clusters. Bands are stacked, so total "
            "height shows total in-AI-corpus volume. Dashed vertical lines "
            "mark the three events the project measures: ChatGPT, GPT-4, "
            "and the OpenAI board crisis. Click a legend entry to mute / "
            "unmute a topic; hover for monthly counts.</p>"
        ),
        width=1200,
    )
    layout = column(header, p)
    html = file_html(layout, CDN, title="HN AI — Topic by month")
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(html, encoding="utf-8")
    print(f"wrote {args.output_html} "
          f"({args.output_html.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
