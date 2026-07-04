#!/bin/bash
#SBATCH --job-name=hn-ai-umap
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --time=01:00:00
#SBATCH --output=logs/umap_%j.out
#SBATCH --error=logs/umap_%j.err

# Reduce sentence-transformer embeddings to 2-D (atlas) or 5-D (BERTopic).
# Pass --output-parquet + --n-components on the sbatch command line.
#
# Examples:
#   sbatch slurm/10_umap_reduce.sbatch \
#       --output-parquet outputs/umap_2d.parquet \
#       --n-components 2 --min-dist 0.1
#
#   sbatch slurm/10_umap_reduce.sbatch \
#       --output-parquet outputs/umap_5d.parquet \
#       --n-components 5 --min-dist 0.0

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMBA_NUM_THREADS=$SLURM_CPUS_PER_TASK

python -c "import umap; print('umap-learn', umap.__version__)" \
    || { echo "ERROR: install umap-learn on login node: pip install umap-learn"; exit 2; }

PYTHONPATH=src python -u scripts/analyze/umap_reduce.py \
    --input-parquet outputs/corpus_embeddings.parquet \
    --fit-sample 50000 \
    "$@"
