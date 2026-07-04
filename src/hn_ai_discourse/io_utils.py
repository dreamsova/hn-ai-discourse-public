from __future__ import annotations

import csv
import gzip
import json
from pathlib import Path
from typing import Dict, Iterable, Iterator, List


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def ensure_parent(path: Path) -> None:
    ensure_dir(path.parent)


def open_text(path: Path, mode: str = "rt"):
    if path.suffix == ".gz":
        return gzip.open(path, mode, encoding="utf-8")
    return path.open(mode, encoding="utf-8")


def iter_jsonl(path: Path) -> Iterator[Dict]:
    with open_text(path, "rt") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def write_jsonl(records: Iterable[Dict], path: Path) -> None:
    ensure_parent(path)
    with open_text(path, "wt") as handle:
        for record in records:
            handle.write(json.dumps(record, sort_keys=True))
            handle.write("\n")


def load_terms(path: Path) -> Dict:
    return json.loads(path.read_text(encoding="utf-8"))


def read_manifest_row(path: Path, task_index: int) -> Dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for idx, row in enumerate(reader, start=1):
            if idx == task_index:
                return row
    raise IndexError("task index %s not found in %s" % (task_index, path))


def drop_known_suffixes(path: Path) -> str:
    name = path.name
    for suffix in (".jsonl.gz", ".jsonl", ".parquet", ".csv", ".txt"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return path.stem


def write_lines(lines: List[str], path: Path) -> None:
    ensure_parent(path)
    with path.open("w", encoding="utf-8") as handle:
        for line in lines:
            handle.write(line)
            handle.write("\n")
