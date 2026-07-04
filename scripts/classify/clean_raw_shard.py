#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from hn_ai_discourse.io_utils import drop_known_suffixes, iter_jsonl, load_terms
from hn_ai_discourse.text_utils import (
    assign_weak_label,
    combined_text,
    count_term_hits,
    find_partition_relative_path,
    is_high_precision_label,
    month_key_from_timestamp,
)

CLEAN_COLUMNS = [
    "comment_id",
    "created_at",
    "created_at_i",
    "year_month",
    "author",
    "story_id",
    "parent_id",
    "story_title",
    "comment_text",
    "combined_text",
    "query_family",
    "query",
    "shard_id",
    "broad_ai_hits",
    "doomer_hits",
    "accel_hits",
    "ai_hits",
    "weak_label",
    "is_high_precision_label",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean one raw shard and assign weak labels.")
    parser.add_argument("--input-path", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=Path("data/clean"))
    parser.add_argument("--terms-config", type=Path, default=Path("configs/terms.json"))
    args = parser.parse_args()

    terms = load_terms(args.terms_config)["lexicons"]
    rows = []
    for record in iter_jsonl(args.input_path):
        comment_id = str(record.get("objectID", "")).strip()
        created_at_i = int(record.get("created_at_i") or 0)
        comment_text = record.get("comment_text") or record.get("text") or ""
        story_title = record.get("story_title") or ""
        text = combined_text(comment_text, story_title)
        broad_ai_hits = count_term_hits(text, terms["broad_ai"])
        doomer_hits = count_term_hits(text, terms["doomer"])
        accel_hits = count_term_hits(text, terms["accelerationist"])
        ai_hits = broad_ai_hits + doomer_hits + accel_hits
        weak_label = assign_weak_label(ai_hits=ai_hits, doomer_hits=doomer_hits, accel_hits=accel_hits)

        rows.append(
            {
                "comment_id": comment_id,
                "created_at": record.get("created_at"),
                "created_at_i": created_at_i,
                "year_month": month_key_from_timestamp(created_at_i) if created_at_i else "",
                "author": record.get("author"),
                "story_id": record.get("story_id"),
                "parent_id": record.get("parent_id"),
                "story_title": story_title,
                "comment_text": comment_text,
                "combined_text": text,
                "query_family": record.get("query_family"),
                "query": record.get("query"),
                "shard_id": record.get("shard_id"),
                "broad_ai_hits": broad_ai_hits,
                "doomer_hits": doomer_hits,
                "accel_hits": accel_hits,
                "ai_hits": ai_hits,
                "weak_label": weak_label,
                "is_high_precision_label": is_high_precision_label(weak_label),
            }
        )

    relative = find_partition_relative_path(args.input_path)
    out_name = "%s.parquet" % drop_known_suffixes(relative)
    out_path = args.output_root / relative.parent / out_name if relative.parent != Path(".") else args.output_root / out_name
    out_path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        pd.DataFrame(columns=CLEAN_COLUMNS).to_parquet(out_path, index=False)
        print("wrote 0 cleaned rows to %s" % out_path)
        return

    frame = pd.DataFrame(rows).drop_duplicates(subset=["comment_id", "shard_id"])
    frame.to_parquet(out_path, index=False)
    print("wrote %d cleaned rows to %s" % (len(frame), out_path))


if __name__ == "__main__":
    main()
