#!/bin/bash
#SBATCH --job-name=build-sif
#SBATCH --partition=caslake
#SBATCH --account=macs30123
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=logs/build-sif-%j.out
#SBATCH --error=logs/build-sif-%j.err

set -euo pipefail

module load apptainer/1.4.1

cd "$SLURM_SUBMIT_DIR"
mkdir -p containers logs

# Use scratch for build cache to avoid filling $HOME.
SCRATCH_USER="/scratch/midway3/$USER"
export APPTAINER_CACHEDIR="$SCRATCH_USER/apptainer-cache"
export APPTAINER_TMPDIR="$SCRATCH_USER/apptainer-tmp"
mkdir -p "$APPTAINER_CACHEDIR" "$APPTAINER_TMPDIR"

echo "[build-sif] start at $(date -Iseconds)"
echo "[build-sif] apptainer: $(apptainer --version)"

apptainer build --force \
  containers/hn-ai-discourse.sif \
  containers/Singularity.def

echo "[build-sif] image size:"
ls -lh containers/hn-ai-discourse.sif

echo "[build-sif] smoke-test python + key imports:"
apptainer exec containers/hn-ai-discourse.sif python -c "
import importlib, sys
mods = ['pandas','numpy','pyarrow','sklearn','statsmodels',
        'dask','dask_jobqueue','bokeh','umap','hdbscan',
        'sentence_transformers','transformers','bertopic',
        'datashader','holoviews','torch']
for m in mods:
    importlib.import_module(m)
    print(f'  ok  {m}')
print('python:', sys.version.split()[0])
"

echo "[build-sif] done at $(date -Iseconds)"
