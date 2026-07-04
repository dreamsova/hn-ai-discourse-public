from __future__ import annotations

import datetime as dt
import html
import re
from functools import lru_cache
from pathlib import Path
from typing import Iterable


TAG_RE = re.compile(r"<[^>]+>")
WHITESPACE_RE = re.compile(r"\s+")
NON_SLUG_RE = re.compile(r"[^a-z0-9]+")


def strip_html(value: str) -> str:
    return TAG_RE.sub(" ", html.unescape(value or ""))


def normalize_text(value: str) -> str:
    stripped = strip_html(value).lower()
    return WHITESPACE_RE.sub(" ", stripped).strip()


def combined_text(comment_text: str, story_title: str) -> str:
    parts = [story_title or "", comment_text or ""]
    return normalize_text(" ".join(part for part in parts if part))


def month_key_from_timestamp(timestamp: int) -> str:
    return dt.datetime.utcfromtimestamp(int(timestamp)).strftime("%Y-%m")


@lru_cache(maxsize=None)
def term_pattern(term: str) -> re.Pattern:
    escaped = re.escape(term.lower())
    return re.compile(r"(?<!\w)%s(?!\w)" % escaped)


def count_term_hits(text: str, terms: Iterable[str]) -> int:
    return sum(len(term_pattern(term).findall(text)) for term in terms)


def assign_weak_label(ai_hits: int, doomer_hits: int, accel_hits: int) -> str:
    if ai_hits <= 0:
        return "non_ai"
    if doomer_hits > accel_hits and doomer_hits > 0:
        return "doomer"
    if accel_hits > doomer_hits and accel_hits > 0:
        return "accelerationist"
    if doomer_hits == 0 and accel_hits == 0:
        return "neutral"
    return "mixed"


def is_high_precision_label(label: str) -> bool:
    return label in {"doomer", "accelerationist", "neutral"}


def slugify(value: str) -> str:
    slug = NON_SLUG_RE.sub("-", value.lower()).strip("-")
    return slug or "na"


def find_partition_relative_path(path: Path) -> Path:
    parts = list(path.parts)
    for idx, part in enumerate(parts):
        if part.startswith("year="):
            return Path(*parts[idx:])
    return Path(path.name)
