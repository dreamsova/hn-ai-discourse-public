#!/bin/bash
#SBATCH --job-name=hn-ai-zs-ungated
#SBATCH --account=macs30123
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --array=0-3
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/zs_ungated_%A_%a.out
#SBATCH --error=logs/zs_ungated_%A_%a.err

# Ungated zero-shot NLI inference across the FULL 411K corpus on 4
# GPUs in parallel via Slurm array. Each task gets one GPU and one
# contiguous range of 315 shards.
#
# Pipeline meaning: scoring every comment (not just ai_hits>0) lets
# DeBERTa act as a proxy oracle for retrieval recall — any comment it
# confidently labels doomer/accelerationist with high probability while
# the lexicon said ai_hits=0 is a lexicon false-negative.
#
# Output: data/inference_zs_ungated/ (parallel to existing data/inference_zs/
# from the gated 156K run, so both versions coexist for direct comparison).

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

# Belt-and-suspenders diagnostics + line-buffer Python so progress
# flushes immediately instead of being held by the default block buffer.
export PYTHONUNBUFFERED=1
export PYTHONFAULTHANDLER=1

source ~/.venvs/hn-ai-discourse/bin/activate
echo "DIAG: venv activated, python=$(which python)"

export HF_HOME="${HF_HOME:-$HOME/.cache/huggingface}"
export TRANSFORMERS_OFFLINE=0
export TOKENIZERS_PARALLELISM=false

TOTAL_SHARDS=1260
N_TASKS=4
PER_TASK=$((TOTAL_SHARDS / N_TASKS))
START=$((SLURM_ARRAY_TASK_ID * PER_TASK))
END=$((START + PER_TASK))
# Last task absorbs any remainder (1260 % 4 == 0 so this is no-op here,
# but the pattern survives if TOTAL_SHARDS or N_TASKS ever changes).
if [ "$SLURM_ARRAY_TASK_ID" = "$((N_TASKS - 1))" ]; then
    END=$TOTAL_SHARDS
fi

echo "=== Array task $SLURM_ARRAY_TASK_ID handling shards [$START, $END) ==="
echo "DIAG: about to nvidia-smi"
nvidia-smi --query-gpu=name,memory.free,memory.total --format=csv,noheader || echo "nvidia-smi failed: $?"
echo "DIAG: about to launch python"

PYTHONPATH=src python -u scripts/classify/infer_zeroshot.py \
    --input-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --output-root data/inference_zs_ungated \
    --batch-size 64 \
    --max-length 256 \
    --shard-range "${START}:${END}" \
    --ungated \
    "$@"
