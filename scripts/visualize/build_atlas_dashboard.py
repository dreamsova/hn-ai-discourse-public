#!/usr/bin/env python3
"""Render the 411K-point semantic atlas, colored by BERTopic cluster.

Joins:
  - outputs/umap_2d.parquet                    (2-D UMAP coordinates per comment_id)
  - outputs/topics/topics_per_comment.parquet  (BERTopic cluster id)
  - outputs/topics/topic_summary.csv           (top words per cluster)

The default coloring is by `topic`, which makes the structural finding
visible: AI-specific clusters (AI safety / x-risk, ChatGPT / chatbots,
NVIDIA / GPUs) sit in distinct regions from clusters the lexicon
dragged in but that aren't actually about AI (HN hiring, COVID,
bitcoin, music). That's the same 51% lexicon noise the gold-set audit
quantified, here visualized spatially.

The previous version colored by predicted_label, but
`not_retrieved` and `neutral` together account for ~95% of points,
so the plot rendered nearly monochrome. The topic-colored version is
where the structure actually lives.

Output:
  deliverables/hn-ai-discourse-semantic-atlas.html
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

# A categorical palette of distinguishable colors for the top topics.
TOPIC_PALETTE = [
    "#bf5700",  # burnt orange
    "#007c80",  # teal
    "#8e44ad",  # purple
    "#27ae60",  # emerald
    "#d35400",  # carrot
    "#2980b9",  # belize blue
    "#c0392b",  # pomegranate
    "#16a085",  # green sea
    "#e67e22",  # tangerine
    "#9b59b6",  # amethyst
    "#34495e",  # wet asphalt
    "#f39c12",  # orange
    "#1abc9c",  # turquoise
    "#e74c3c",  # alizarin
    "#3498db",  # peter river
]
NOISE_COLOR = "#dddddd"   # very light grey for noise / non-top topics


def short_topic_label(name_field: str, top_words_field: str, fallback: str) -> str:
    """Derive a 2-3 word label for a topic from BERTopic's `Name`/`Representation` columns."""
    if isinstance(name_field, str) and name_field:
        # BERTopic Names look like "9_ai safety_ai risk_xrisk_existential risk"
        parts = name_field.split("_", 1)
        if len(parts) == 2:
            tail = parts[1]
            words = re.split(r"[_,]", tail)
            words = [w.strip() for w in words if w.strip()]
            return " · ".join(words[:3]) or fallback
    return fallback


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--umap-parquet", type=Path,
                        default=Path("outputs/umap_2d.parquet"))
    parser.add_argument("--topics-parquet", type=Path,
                        default=Path("outputs/topics/topics_per_comment.parquet"))
    parser.add_argument("--topic-summary-csv", type=Path,
                        default=Path("outputs/topics/topic_summary.csv"))
    parser.add_argument("--top-n", type=int, default=15,
                        help="How many top topics to color distinctly. "
                             "Everything else (and the -1 noise cluster) "
                             "goes to the light-grey 'other' bucket.")
    parser.add_argument("--output-html", type=Path,
                        default=Path("deliverables/hn-ai-discourse-semantic-atlas.html"))
    parser.add_argument("--plot-width", type=int, default=1100)
    parser.add_argument("--plot-height", type=int, default=750)
    args = parser.parse_args()

    # Lazy imports.
    import datashader as ds
    import datashader.transfer_functions as tf
    import numpy as np
    from bokeh.embed import file_html
    from bokeh.layouts import column, row
    from bokeh.models import Div
    from bokeh.plotting import figure
    from bokeh.resources import CDN

    print(f"loading {args.umap_parquet}")
    umap = pd.read_parquet(args.umap_parquet)
    umap["comment_id"] = umap["comment_id"].astype(str)
    print(f"  {len(umap):,} UMAP rows")

    print(f"loading {args.topics_parquet}")
    topics = pd.read_parquet(args.topics_parquet)
    topics["comment_id"] = topics["comment_id"].astype(str)
    umap = umap.merge(topics[["comment_id", "topic"]],
                      on="comment_id", how="left")
    umap["topic"] = umap["topic"].fillna(-1).astype(int)

    # Identify top-N topics by count (excluding the -1 noise cluster)
    counts = umap[umap["topic"] != -1]["topic"].value_counts()
    top_topics = counts.head(args.top_n).index.tolist()
    print(f"  top {len(top_topics)} topics by count: {top_topics}")

    # Build a categorical column with stable level names. Everything not
    # in the top-N collapses into 'other' so DataShader doesn't try to
    # color 204 distinct clusters.
    topic_labels: dict[int, str] = {-1: "other"}
    for i, t in enumerate(top_topics):
        topic_labels[int(t)] = f"t{int(t):03d}"
    umap["topic_bucket"] = (
        umap["topic"].map(topic_labels).fillna("other").astype("category")
    )

    # Build the color_key DataShader will use.
    color_key: dict[str, str] = {"other": NOISE_COLOR}
    for i, t in enumerate(top_topics):
        color_key[f"t{int(t):03d}"] = TOPIC_PALETTE[i % len(TOPIC_PALETTE)]

    # Read topic_summary to pretty-print legend
    label_pretty: dict[int, str] = {}
    if args.topic_summary_csv.exists():
        summary = pd.read_csv(args.topic_summary_csv)
        name_col = "Name" if "Name" in summary.columns else "name"
        topic_col = "Topic" if "Topic" in summary.columns else "topic"
        for _, r in summary.iterrows():
            tid = int(r[topic_col])
            label_pretty[tid] = short_topic_label(
                r.get(name_col, ""),
                "",
                fallback=f"topic {tid}",
            )

    # DataShader rasterization
    canvas = ds.Canvas(plot_width=args.plot_width, plot_height=args.plot_height)
    agg = canvas.points(umap, x="umap_0", y="umap_1",
                        agg=ds.count_cat("topic_bucket"))
    img = tf.shade(agg, color_key=color_key, how="log")
    img = tf.set_background(img, "white")
    rgba = img.to_pil()
    arr = np.array(rgba.convert("RGBA"))[::-1]
    arr_flat = arr.view(dtype=np.uint32).reshape(arr.shape[:2])

    x_min, x_max = float(umap["umap_0"].min()), float(umap["umap_0"].max())
    y_min, y_max = float(umap["umap_1"].min()), float(umap["umap_1"].max())

    p = figure(
        width=args.plot_width, height=args.plot_height,
        title=f"HN AI-discourse semantic atlas — "
              f"{len(umap):,} comments, colored by BERTopic cluster",
        toolbar_location="above",
        tools="pan,box_zoom,wheel_zoom,reset,save",
        x_range=(x_min, x_max), y_range=(y_min, y_max),
    )
    p.image_rgba(image=[arr_flat], x=x_min, y=y_min,
                 dw=x_max - x_min, dh=y_max - y_min)
    p.xaxis.axis_label = "UMAP-0 (semantic axis 1)"
    p.yaxis.axis_label = "UMAP-1 (semantic axis 2)"

    # Legend table: top-N topics with color swatch, count, top-3 words.
    legend_rows: list[str] = []
    other_count = int((umap["topic_bucket"] == "other").sum())
    for t in top_topics:
        key = f"t{int(t):03d}"
        color = color_key[key]
        n = int(counts.loc[t])
        words = label_pretty.get(int(t), f"topic {int(t)}")
        legend_rows.append(
            f"<tr>"
            f"<td style='width:14px;background:{color};border-radius:3px'>&nbsp;</td>"
            f"<td style='padding-left:6px'>{words}</td>"
            f"<td align='right' style='padding-left:10px'>{n:,}</td>"
            f"</tr>"
        )
    legend_rows.append(
        f"<tr>"
        f"<td style='width:14px;background:{NOISE_COLOR};border-radius:3px'>&nbsp;</td>"
        f"<td style='padding-left:6px;color:#888'>other / noise (-1 cluster + small topics)</td>"
        f"<td align='right' style='padding-left:10px'>{other_count:,}</td>"
        f"</tr>"
    )
    legend_html = (
        "<table style='font-family:sans-serif;font-size:11pt;"
        "border-collapse:collapse;border:0'>"
        "<thead><tr>"
        "<th></th><th align='left'>top words</th><th align='right'>n</th>"
        "</tr></thead>"
        f"<tbody>{''.join(legend_rows)}</tbody></table>"
    )

    header = Div(
        text=(
            "<h2>HN AI-discourse semantic atlas</h2>"
            "<p>Each pixel is a density of HN comments. Embeddings come "
            "from <code>sentence-transformers/all-MiniLM-L6-v2</code>, "
            "reduced to 2-D via UMAP, rasterized with DataShader. Color "
            "encodes BERTopic cluster: the top "
            f"{len(top_topics)} clusters get distinct colors, the rest "
            "(including HDBSCAN's noise bucket) collapse to light grey. "
            "AI-specific clusters and clusters the lexicon dragged in "
            "from non-AI topics are visible as distinct regions of the "
            "manifold.</p>"
        ),
        width=args.plot_width,
    )
    side = Div(text=legend_html, width=320)

    layout = column(header, row(p, side))
    html = file_html(layout, CDN, title="HN AI semantic atlas")
    args.output_html.parent.mkdir(parents=True, exist_ok=True)
    args.output_html.write_text(html, encoding="utf-8")
    size_kb = args.output_html.stat().st_size / 1024
    print(f"wrote {args.output_html} ({size_kb:.0f} KB)")


if __name__ == "__main__":
    main()
