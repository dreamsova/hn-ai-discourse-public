#!/bin/bash
#SBATCH --job-name=hn-ai-atlas
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --output=logs/atlas_%j.out
#SBATCH --error=logs/atlas_%j.err

# Render the DataShader + Bokeh semantic atlas from outputs/umap_2d.parquet
# (and optionally outputs/topics/topics_per_comment.parquet).

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs deliverables

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1

PYTHONPATH=src python -u scripts/visualize/build_atlas_dashboard.py \
    --umap-parquet outputs/umap_2d.parquet \
    --topics-parquet outputs/topics/topics_per_comment.parquet \
    --embeddings-parquet outputs/corpus_embeddings.parquet \
    --output-html deliverables/hn-ai-discourse-semantic-atlas.html
