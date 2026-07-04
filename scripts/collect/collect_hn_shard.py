#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

from hn_ai_discourse.io_utils import ensure_parent, open_text, read_manifest_row


BASE_URL = "https://hn.algolia.com/api/v1/search_by_date"


def fetch_page(query: str, start_ts: int, end_ts: int, page: int, hits_per_page: int) -> dict:
    params = {
        "query": query,
        "tags": "comment",
        "page": page,
        "hitsPerPage": hits_per_page,
        "numericFilters": "created_at_i>=%s,created_at_i<%s" % (start_ts, end_ts),
    }
    url = "%s?%s" % (BASE_URL, urllib.parse.urlencode(params))
    request = urllib.request.Request(url, headers={"User-Agent": "macs30123-final-project/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(description="Collect one Algolia shard from a manifest row.")
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--task-index", type=int, default=0)
    parser.add_argument("--output-root", type=Path, default=Path("data/raw"))
    parser.add_argument("--hits-per-page", type=int, default=100)
    parser.add_argument("--max-pages", type=int, default=1000)
    parser.add_argument("--pause-seconds", type=float, default=0.1)
    args = parser.parse_args()

    task_index = args.task_index or int(__import__("os").environ.get("SLURM_ARRAY_TASK_ID", "0"))
    if task_index <= 0:
        raise SystemExit("provide --task-index or set SLURM_ARRAY_TASK_ID")

    row = read_manifest_row(args.manifest, task_index)
    out_dir = (
        args.output_root
        / ("year=%s" % row["year"])
        / ("month=%s" % row["month"])
        / ("family=%s" % row["family"])
        / ("query=%s" % row["query_slug"])
    )
    out_path = out_dir / ("part-%s.jsonl.gz" % row["shard_id"])
    meta_path = out_dir / ("part-%s.meta.json" % row["shard_id"])
    ensure_parent(out_path)

    total_hits = 0
    pages_written = 0
    nb_pages = 0

    with open_text(out_path, "wt") as handle:
        page = 0
        while page < args.max_pages:
            payload = fetch_page(
                query=row["query"],
                start_ts=int(row["start_ts"]),
                end_ts=int(row["end_ts"]),
                page=page,
                hits_per_page=args.hits_per_page,
            )
            if page == 0:
                nb_pages = int(payload.get("nbPages", 0))
            hits = payload.get("hits", [])
            if not hits:
                break
            for hit in hits:
                hit["query_family"] = row["family"]
                hit["query"] = row["query"]
                hit["shard_id"] = row["shard_id"]
                handle.write(json.dumps(hit, sort_keys=True))
                handle.write("\n")
            total_hits += len(hits)
            pages_written += 1
            page += 1
            if page >= nb_pages:
                break
            time.sleep(args.pause_seconds)

    meta = {
        "shard_id": row["shard_id"],
        "query": row["query"],
        "family": row["family"],
        "output_path": out_path.as_posix(),
        "pages_written": pages_written,
        "nb_pages_reported": nb_pages,
        "max_pages": args.max_pages,
        "total_hits_written": total_hits,
        "truncated": nb_pages > args.max_pages,
    }
    ensure_parent(meta_path)
    meta_path.write_text(json.dumps(meta, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(meta, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
