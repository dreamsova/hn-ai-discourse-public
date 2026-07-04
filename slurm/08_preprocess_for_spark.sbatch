#!/bin/bash
#SBATCH --job-name=hn-ai-pp-spark
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --array=0-7
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:20:00
#SBATCH --output=logs/pp_spark_%A_%a.out
#SBATCH --error=logs/pp_spark_%A_%a.err

# Normalize parquet schemas across the 1260 inference shards so PySpark
# can read them with a single schema. Each array task handles one shard.
#
# Submit: sbatch slurm/08_preprocess_for_spark.sbatch
# Then:   sbatch slurm/06_spark_aggregate.sbatch  (with --input-glob data/inference_normalized/...)

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1

# Build a 1260-entry path manifest once per array submission; each array
# task picks its own shard by SLURM_ARRAY_TASK_ID. flock + atomic rename
# so concurrent array tasks don't race on the manifest write.
MANIFEST=/tmp/inference_shards_${SLURM_ARRAY_JOB_ID}.txt
LOCK="${MANIFEST}.lock"
exec 9>"$LOCK"
flock 9
if [ ! -f "$MANIFEST" ]; then
    TMP_MANIFEST="${MANIFEST}.tmp.$$"
    find data/inference -type f -name '*.parquet' | sort > "$TMP_MANIFEST"
    mv "$TMP_MANIFEST" "$MANIFEST"
fi
exec 9>&-
TOTAL=$(wc -l < "$MANIFEST")
echo "DIAG: manifest=$MANIFEST total=$TOTAL task=$SLURM_ARRAY_TASK_ID"

# Batch mode: each of the 8 array tasks processes ~158 shards. We
# divide the manifest into N_TASKS contiguous slices keyed by
# SLURM_ARRAY_TASK_ID.
N_TASKS=8
PER_TASK=$(( (TOTAL + N_TASKS - 1) / N_TASKS ))  # ceiling division
START=$(( SLURM_ARRAY_TASK_ID * PER_TASK + 1 ))   # sed lines are 1-indexed
END=$(( START + PER_TASK - 1 ))
[ "$END" -gt "$TOTAL" ] && END=$TOTAL
echo "DIAG: task $SLURM_ARRAY_TASK_ID processing lines $START..$END of $TOTAL"

sed -n "${START},${END}p" "$MANIFEST" | while read -r INPUT; do
    PYTHONPATH=src python -u scripts/aggregate/preprocess_for_spark.py \
        --input-path "$INPUT" \
        --input-root data/inference \
        --output-root data/inference_normalized
done
