#!/bin/bash
#SBATCH --job-name=hn-ai-dask-aggregate
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=00:20:00
#SBATCH --output=logs/%x-%j.out

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/final-project-final-project}"
PYTHON_BIN="${PYTHON_BIN:-python}"
CONDA_ENV_PATH="${CONDA_ENV_PATH:-$HOME/.conda/envs/hn-ai-discourse}"
VENV_PATH="${VENV_PATH:-$HOME/.venvs/hn-ai-discourse}"

set +u
source /etc/bashrc
set -u
module load python/miniforge-25.3.0
if [ -f "$VENV_PATH/bin/activate" ]; then
  source "$VENV_PATH/bin/activate"
  PYTHON_BIN=python
elif command -v conda >/dev/null 2>&1; then
  eval "$(conda shell.bash hook)"
  conda activate "$CONDA_ENV_PATH" || true
fi

cd "$REPO_ROOT"
PYTHONPATH=src "$PYTHON_BIN" scripts/aggregate/dask_aggregate.py \
  --input-glob 'data/inference/**/*.parquet' \
  --output-dir outputs \
  --n-workers 8 \
  --memory-limit 2GB \
  --benchmark-out outputs/dask_benchmark.json
