#!/bin/bash
#SBATCH --job-name=hn-ai-embed
#SBATCH --account=macs30123
#SBATCH --partition=gpu
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=logs/embed_%j.out
#SBATCH --error=logs/embed_%j.err

# Embed the full HN AI-discourse corpus with sentence-transformers
# all-MiniLM-L6-v2 on a single Midway GPU. Output:
#   outputs/corpus_embeddings.parquet  (411K x 384, fp16, ~250 MB)
#
# Powers the Phase-7 semantic-atlas extension:
#   embed_corpus.py  →  umap_reduce.py  →  build_atlas_dashboard.py

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1
export TOKENIZERS_PARALLELISM=false
export HF_HOME="${HF_HOME:-$HOME/.cache/huggingface}"

echo "DIAG: venv python=$(which python)"
nvidia-smi --query-gpu=name,memory.free,memory.total --format=csv,noheader || true

# Hard fail if sentence-transformers isn't installed; do not pip-install
# from inside a Slurm job (race conditions + production hygiene).
python -c "import sentence_transformers; print('sentence-transformers OK')" \
    || { echo "ERROR: install sentence-transformers in the venv first (login node):"; \
         echo "  pip install sentence-transformers"; exit 2; }

PYTHONPATH=src python -u scripts/analyze/embed_corpus.py \
    --input-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --inference-glob "data/inference/year=*/month=*/family=*/query=*/*.parquet" \
    --output-parquet outputs/corpus_embeddings.parquet \
    --batch-size 128 \
    --max-length 256 \
    "$@"
