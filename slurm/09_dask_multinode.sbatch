#!/bin/bash
#SBATCH --job-name=hn-ai-dask-mn
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:45:00
#SBATCH --output=logs/dask_mn_%j.out
#SBATCH --error=logs/dask_mn_%j.err

# Multi-node Dask aggregation benchmark via dask-jobqueue.SLURMCluster.
#
# This job is just the Dask CLIENT + SCHEDULER (lightweight). It launches
# additional Slurm worker jobs via dask-jobqueue, which run on their own
# nodes. Each worker is a separate Slurm job.
#
# Total cluster footprint when scaled up:
#   - this job:    1 caslake CPU,  8G,   45 min (scheduler + client)
#   - 4 workers:   4 caslake jobs, 8G ea, 30 min ea (parallel)
#
# Adds a third row to the existing pandas/Dask LocalCluster benchmark
# table:
#   pandas serial:        ~62s
#   Dask LocalCluster:    ~152s
#   Dask SLURMCluster:    (this run)

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1

# dask-jobqueue may not be in the venv yet.
python -c "import dask_jobqueue; print('dask_jobqueue OK')" \
    || { echo "ERROR: install dask-jobqueue in venv first on login node:"; \
         echo "  pip install dask-jobqueue"; exit 2; }

PYTHONPATH=src python -u scripts/aggregate/dask_multinode_aggregate.py \
    --n-workers 4 \
    --cores-per-worker 4 \
    --memory-per-worker 8GB \
    --walltime-per-worker 00:30:00 \
    --account macs30123 \
    --partition caslake \
    --input-glob "data/inference_normalized/year=*/month=*/family=*/query=*/*.parquet" \
    --predicted-col predicted_label \
    --output-dir outputs/panel_dask_multinode \
    "$@"
