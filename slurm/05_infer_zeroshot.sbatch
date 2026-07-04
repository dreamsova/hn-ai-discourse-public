#!/bin/bash
#SBATCH --job-name=hn-ai-zs-infer
#SBATCH --account=macs30123
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/zs_infer_%j.out
#SBATCH --error=logs/zs_infer_%j.err

# Zero-shot NLI stance inference: DeBERTa-v3-large over the 156K
# AI-retrieved corpus on a single GPU. Output mirrors data/clean/
# under data/inference_zs/.

set -euo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate

# Pin HF cache to a writable location with plenty of space.
export HF_HOME="${HF_HOME:-$HOME/.cache/huggingface}"
export TRANSFORMERS_OFFLINE=0
export TOKENIZERS_PARALLELISM=false

nvidia-smi | head -20

PYTHONPATH=src python scripts/classify/infer_zeroshot.py \
    --input-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --output-root data/inference_zs \
    --batch-size 64 \
    --max-length 256 \
    "$@"
