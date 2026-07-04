#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd


def run_step(command, repo_root: Path) -> None:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root / "src")
    subprocess.run(command, check=True, cwd=repo_root, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a fixture-based end-to-end smoke test.")
    parser.add_argument("--workdir", type=Path, default=Path("scratch/smoke_test"))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    python_bin = sys.executable
    workdir = (repo_root / args.workdir).resolve()
    raw_out = workdir / "raw"
    clean_out = workdir / "clean"
    infer_out = workdir / "inference"
    output_dir = workdir / "outputs"
    manifests_dir = workdir / "manifests"
    for path in [raw_out, clean_out, infer_out, output_dir, manifests_dir]:
        path.mkdir(parents=True, exist_ok=True)

    sample_path = repo_root / "data/examples/smoke_raw.jsonl"
    raw_copy = raw_out / "smoke_raw.jsonl"
    raw_copy.write_text(sample_path.read_text(encoding="utf-8"), encoding="utf-8")

    run_step(
        [
            python_bin,
            "scripts/classify/clean_raw_shard.py",
            "--input-path",
            str(raw_copy),
            "--output-root",
            str(clean_out),
        ],
        repo_root,
    )

    clean_glob = str(clean_out / "**/*.parquet")
    run_step(
        [
            python_bin,
            "scripts/classify/train_classifier.py",
            "--input-glob",
            clean_glob,
            "--output-dir",
            str(output_dir / "model"),
            "--min-df",
            "1",
        ],
        repo_root,
    )

    run_step(
        [
            python_bin,
            "scripts/collect/build_file_manifest.py",
            "--glob",
            clean_glob,
            "--output",
            str(manifests_dir / "clean_files.txt"),
        ],
        repo_root,
    )

    clean_file = Path((manifests_dir / "clean_files.txt").read_text(encoding="utf-8").strip().splitlines()[0])
    run_step(
        [
            python_bin,
            "scripts/classify/infer_shard.py",
            "--input-path",
            str(clean_file),
            "--model-path",
            str(output_dir / "model/tfidf_logreg.joblib"),
            "--output-root",
            str(infer_out),
        ],
        repo_root,
    )

    infer_glob = str(infer_out / "**/*.parquet")
    run_step(
        [
            python_bin,
            "scripts/aggregate/aggregate_monthly.py",
            "--input-glob",
            infer_glob,
            "--output-dir",
            str(output_dir),
        ],
        repo_root,
    )
    run_step(
        [
            python_bin,
            "scripts/visualize/plot_monthly_shares.py",
            "--panel-csv",
            str(output_dir / "monthly_panel.csv"),
            "--events-csv",
            str(output_dir / "event_markers.csv"),
            "--output-path",
            str(output_dir / "monthly_shares.png"),
        ],
        repo_root,
    )

    panel = pd.read_csv(output_dir / "monthly_panel.csv")
    if panel.empty:
        raise SystemExit("smoke test failed: monthly panel is empty")
    required_files = [
        output_dir / "model/tfidf_logreg.joblib",
        output_dir / "model/metrics.json",
        output_dir / "monthly_panel.csv",
        output_dir / "monthly_shares.png",
    ]
    missing = [path for path in required_files if not path.exists()]
    if missing:
        raise SystemExit("smoke test failed: missing files %s" % missing)

    print("smoke test completed successfully")
    print(panel.to_string(index=False))


if __name__ == "__main__":
    main()
