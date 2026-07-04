#!/bin/bash
#SBATCH --job-name=hn-ai-ft
#SBATCH --account=macs30123
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=02:00:00
#SBATCH --output=logs/ft_distilbert_%j.out
#SBATCH --error=logs/ft_distilbert_%j.err

# Fine-tune DistilBERT on 200 gold + 6K weak labels, then run inference
# over the full 411K corpus into data/inference_ft/.

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false

nvidia-smi --query-gpu=name,memory.free --format=csv,noheader || true

PYTHONPATH=src python -u scripts/classify/finetune_distilbert.py \
    --gold-csv reports/gold_set_labeled.csv \
    --clean-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --inference-glob "data/inference/year=*/month=*/family=*/query=*/*.parquet" \
    --output-model-dir outputs/model/distilbert_stance \
    --output-inference-root data/inference_ft \
    --epochs 3 \
    --batch-size 32 \
    --max-length 256 \
    "$@"
