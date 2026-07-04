#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
from pathlib import Path

from hn_ai_discourse.io_utils import write_lines


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a line-based file manifest from a glob.")
    parser.add_argument("--glob", required=True, help="Input glob. Quote it to avoid shell expansion.")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    matches = sorted(Path(path).as_posix() for path in glob.glob(args.glob, recursive=True))
    if not matches:
        raise SystemExit("no files matched glob: %s" % args.glob)

    write_lines(matches, args.output)
    print("wrote %d paths to %s" % (len(matches), args.output))


if __name__ == "__main__":
    main()
