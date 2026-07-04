#!/bin/bash
#SBATCH --job-name=hn-ai-ungated-ds
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=logs/ungated_downstream_%j.out
#SBATCH --error=logs/ungated_downstream_%j.err

# Build the monthly panel from the ungated 411K zero-shot output, fit
# the event study on it, and refresh the cross-method comparison table
# with a third column.

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1

echo "=== aggregate ungated zero-shot ==="
PYTHONPATH=src python -u scripts/aggregate/aggregate_monthly_v2.py \
    --input-glob "data/inference_zs_ungated/year=*/month=*/family=*/query=*/*.parquet" \
    --predicted-col predicted_label_zs \
    --output-dir outputs/panel_zs_ungated \
    --method-tag zs_ungated

echo "=== event study on ungated panel ==="
PYTHONPATH=src python -u scripts/analyze/event_study.py \
    --panel-csv outputs/panel_zs_ungated/monthly_panel.csv \
    --output-dir outputs/event_study_zs_ungated \
    --outcomes share_doomer_of_ai,share_accelerationist_of_ai \
    --weight-col n_ai_in_scope

echo "=== refresh cross-method comparison (3-column) ==="
PYTHONPATH=src python -u scripts/analyze/compare_its_coefficients.py \
    --tfidf-coef outputs/event_study_tfidf_v2/coefficients.csv \
    --zs-coef outputs/event_study_zs/coefficients.csv \
    --zs-ungated-coef outputs/event_study_zs_ungated/coefficients.csv \
    --output-md reports/generated/its_method_comparison.md
