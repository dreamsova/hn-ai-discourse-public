#!/bin/bash
#SBATCH --job-name=hn-ai-infer
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --time=00:15:00
#SBATCH --output=logs/%x-%A_%a.out

set -euo pipefail

REPO_ROOT="${REPO_ROOT:-$HOME/final-project-final-project}"
PYTHON_BIN="${PYTHON_BIN:-python}"
CONDA_ENV_PATH="${CONDA_ENV_PATH:-$HOME/.conda/envs/hn-ai-discourse}"
VENV_PATH="${VENV_PATH:-$HOME/.venvs/hn-ai-discourse}"
MANIFEST_PATH="${MANIFEST_PATH:-$REPO_ROOT/queries/clean_files.txt}"
TASK_INDEX="${SLURM_ARRAY_TASK_ID:?SLURM_ARRAY_TASK_ID is required}"

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
INPUT_PATH="$(sed -n "${TASK_INDEX}p" "$MANIFEST_PATH")"
PYTHONPATH=src "$PYTHON_BIN" scripts/classify/infer_shard.py \
  --input-path "$INPUT_PATH" \
  --model-path outputs/model/tfidf_logreg.joblib \
  --output-root data/inference
