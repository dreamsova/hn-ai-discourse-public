#!/bin/bash
#SBATCH --job-name=hn-ai-audits
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=logs/audits_%j.out
#SBATCH --error=logs/audits_%j.err

# Run author concentration analysis + embedding-based retrieval audit
# in one CPU job (both small, both produce reportable tables).

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1

echo "=== author_analysis.py ==="
PYTHONPATH=src python -u scripts/analyze/author_analysis.py \
    --clean-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --inference-glob "data/inference/year=*/month=*/family=*/query=*/*.parquet" \
    --output-dir outputs/author_analysis \
    --top-n 20

echo "=== embedding_retrieval_audit.py ==="
PYTHONPATH=src python -u scripts/analyze/embedding_retrieval_audit.py \
    --embeddings-parquet outputs/corpus_embeddings.parquet \
    --clean-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --similarity-threshold 0.55 \
    --output-csv outputs/retrieval_audit_embedding.csv \
    --output-md reports/generated/retrieval_audit_embedding.md
