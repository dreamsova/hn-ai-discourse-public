#!/bin/bash
#SBATCH --job-name=hn-ai-smoke
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:10:00
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

mkdir -p "$REPO_ROOT/logs" "$REPO_ROOT/scratch"
cd "$REPO_ROOT"
PYTHONPATH=src "$PYTHON_BIN" scripts/smoke_test_pipeline.py \
  --workdir "scratch/smoke_test_${SLURM_JOB_ID}"
