#!/bin/bash
#SBATCH --job-name=hn-ai-bertopic
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --time=01:30:00
#SBATCH --output=logs/bertopic_%j.out
#SBATCH --error=logs/bertopic_%j.err

# BERTopic clustering on 411K HN AI-discourse comments.
# Inputs: outputs/umap_5d.parquet + outputs/corpus_embeddings.parquet
# Outputs: outputs/topics/*

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
export NUMBA_NUM_THREADS=$SLURM_CPUS_PER_TASK

python -c "import bertopic, hdbscan; print('bertopic OK')" \
    || { echo "ERROR: install on login node: pip install bertopic hdbscan"; exit 2; }

PYTHONPATH=src python -u scripts/analyze/bertopic_fit.py \
    --umap-parquet outputs/umap_5d.parquet \
    --embeddings-parquet outputs/corpus_embeddings.parquet \
    --clean-glob "data/clean/year=*/month=*/family=*/query=*/*.parquet" \
    --output-dir outputs/topics \
    --min-cluster-size 200 \
    "$@"
