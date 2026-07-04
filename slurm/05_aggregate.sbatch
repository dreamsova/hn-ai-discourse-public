#!/bin/bash
#SBATCH --job-name=hn-ai-aggregate
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:15:00
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
PYTHONPATH=src "$PYTHON_BIN" scripts/aggregate/aggregate_monthly.py \
  --input-glob 'data/inference/**/*.parquet' \
  --output-dir outputs
PYTHONPATH=src "$PYTHON_BIN" scripts/visualize/plot_monthly_shares.py \
  --panel-csv outputs/monthly_panel.csv \
  --events-csv outputs/event_markers.csv \
  --output-path outputs/monthly_shares.png
