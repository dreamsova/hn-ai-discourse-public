#!/bin/bash
#SBATCH --job-name=hn-ai-spark-agg
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=logs/spark_agg_%j.out
#SBATCH --error=logs/spark_agg_%j.err

# PySpark monthly aggregation on Midway — third execution model in the
# pandas / Dask / Spark three-way benchmark.
#
# Default arguments:
#   --input-glob  data/inference/year=*/month=*/family=*/query=*/*.parquet
#   --predicted-col predicted_label    (TF-IDF baseline, matches the
#                                       other two benchmarks for apples-
#                                       to-apples comparison)
#   --output-dir  outputs/panel_spark
#   --master      local[8]              (use all 8 requested cores)

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

module load spark/3.3.2
# Use the project venv's python so pyspark-managed UDFs see our deps.
source ~/.venvs/hn-ai-discourse/bin/activate
# Midway's spark module preconfigures PYSPARK_DRIVER_PYTHON=jupyter for
# notebook users; override both for batch use.
export PYSPARK_PYTHON="$(which python)"
export PYSPARK_DRIVER_PYTHON="$(which python)"
unset PYSPARK_DRIVER_PYTHON_OPTS
# Make pyspark importable without a separate pip install.
export PYTHONPATH="${SPARK_HOME}/python:${SPARK_HOME}/python/lib/py4j-*-src.zip:${PYTHONPATH:-}"

echo "=== Spark version ==="
spark-submit --version 2>&1 | head -5

spark-submit \
    --master "local[${SLURM_CPUS_PER_TASK}]" \
    --driver-memory 8g \
    scripts/aggregate/spark_aggregate.py \
    --input-glob "data/inference" \
    --predicted-col predicted_label \
    --output-dir outputs/panel_spark \
    --method-tag spark \
    --master "local[${SLURM_CPUS_PER_TASK}]" \
    "$@"
