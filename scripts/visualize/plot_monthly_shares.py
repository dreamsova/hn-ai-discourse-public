#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def main() -> None:
    parser = argparse.ArgumentParser(description="Plot monthly framing shares from the aggregated panel.")
    parser.add_argument("--panel-csv", type=Path, default=Path("outputs/monthly_panel.csv"))
    parser.add_argument("--events-csv", type=Path, default=Path("outputs/event_markers.csv"))
    parser.add_argument("--output-path", type=Path, default=Path("outputs/monthly_shares.png"))
    args = parser.parse_args()

    panel = pd.read_csv(args.panel_csv)
    events = pd.read_csv(args.events_csv)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(panel["year_month"], panel["share_doomer"], marker="o", label="Doomer share")
    ax.plot(panel["year_month"], panel["share_accelerationist"], marker="o", label="Accelerationist share")
    ax.plot(panel["year_month"], panel["share_neutral"], marker="o", label="Neutral share", alpha=0.5)

    event_positions = {label: idx for idx, label in enumerate(panel["year_month"])}
    for _, event in events.iterrows():
        if event["event_date"] in event_positions:
            xpos = event_positions[event["event_date"]]
            ax.axvline(x=xpos, linestyle="--", alpha=0.35, color="gray")
            ax.text(xpos + 0.05, 0.98, event["event_label"], rotation=90, va="top", ha="left", fontsize=8, transform=ax.get_xaxis_transform())

    ax.set_title("Monthly Hacker News AI framing shares")
    ax.set_ylabel("Share of comments")
    ax.set_xlabel("Year-month")
    ax.set_ylim(0, 1)
    ax.legend(loc="upper right")
    ax.grid(alpha=0.2)
    ax.set_xticks(range(len(panel)))
    ax.set_xticklabels(panel["year_month"], rotation=45, ha="right")

    args.output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    fig.savefig(args.output_path, dpi=160)
    print("wrote plot to %s" % args.output_path)


if __name__ == "__main__":
    main()
