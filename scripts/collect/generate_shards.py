#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import datetime as dt
from pathlib import Path

from hn_ai_discourse.io_utils import ensure_parent, load_terms
from hn_ai_discourse.text_utils import slugify


def month_bounds(year: int, month: int):
    start = dt.datetime(year, month, 1, tzinfo=dt.timezone.utc)
    if month == 12:
        end = dt.datetime(year + 1, 1, 1, tzinfo=dt.timezone.utc)
    else:
        end = dt.datetime(year, month + 1, 1, tzinfo=dt.timezone.utc)
    return int(start.timestamp()), int(end.timestamp()), start.date().isoformat(), end.date().isoformat()


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate month-by-query query list.")
    parser.add_argument("--start-year", type=int, default=2015)
    parser.add_argument("--end-year", type=int, default=2024)
    parser.add_argument("--terms-config", type=Path, default=Path("configs/terms.json"))
    parser.add_argument("--output", type=Path, default=Path("queries/shards.csv"))
    args = parser.parse_args()

    terms = load_terms(args.terms_config)
    ensure_parent(args.output)

    fieldnames = [
        "shard_id",
        "year",
        "month",
        "family",
        "query",
        "query_slug",
        "start_ts",
        "end_ts",
        "start_date",
        "end_date",
    ]

    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for year in range(args.start_year, args.end_year + 1):
            for month in range(1, 13):
                start_ts, end_ts, start_date, end_date = month_bounds(year, month)
                for family, queries in terms["query_families"].items():
                    for query in queries:
                        query_slug = slugify(query)
                        writer.writerow(
                            {
                                "shard_id": "%s-%04d-%02d-%s" % (family, year, month, query_slug),
                                "year": year,
                                "month": "%02d" % month,
                                "family": family,
                                "query": query,
                                "query_slug": query_slug,
                                "start_ts": start_ts,
                                "end_ts": end_ts,
                                "start_date": start_date,
                                "end_date": end_date,
                            }
                        )

    print("wrote query list to %s" % args.output)


if __name__ == "__main__":
    main()
