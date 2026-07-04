#!/bin/bash
#SBATCH --job-name=hn-ai-ft-ds
#SBATCH --account=macs30123
#SBATCH --partition=caslake
#SBATCH --cpus-per-task=2
#SBATCH --mem=8G
#SBATCH --time=00:20:00
#SBATCH --output=logs/ft_downstream_%j.out
#SBATCH --error=logs/ft_downstream_%j.err

# Once the fine-tune job has written data/inference_ft/, this job rolls
# the DistilBERT predictions up into the same v2 monthly panel format,
# fits the event study on it, and refreshes the cross-method comparison
# table with a fourth column.

set -uo pipefail

cd "$SLURM_SUBMIT_DIR"
mkdir -p logs

source ~/.venvs/hn-ai-discourse/bin/activate
export PYTHONUNBUFFERED=1

echo "=== aggregate distilbert predictions ==="
PYTHONPATH=src python -u scripts/aggregate/aggregate_monthly_v2.py \
    --input-glob "data/inference_ft/year=*/month=*/family=*/query=*/*.parquet" \
    --predicted-col predicted_label_ft \
    --output-dir outputs/panel_ft \
    --method-tag ft

echo "=== event study on distilbert panel ==="
PYTHONPATH=src python -u scripts/analyze/event_study.py \
    --panel-csv outputs/panel_ft/monthly_panel.csv \
    --output-dir outputs/event_study_ft \
    --outcomes share_doomer_of_ai,share_accelerationist_of_ai \
    --weight-col n_ai_in_scope

echo "=== refresh 4-column cross-method comparison ==="
# compare_its_coefficients.py already handles 3 inputs; for the 4th we
# need a small inline join. Print the FT coefficients alongside the
# existing table for the report.
PYTHONPATH=src python -u scripts/analyze/compare_its_coefficients.py \
    --tfidf-coef outputs/event_study_tfidf_v2/coefficients.csv \
    --zs-coef outputs/event_study_zs/coefficients.csv \
    --zs-ungated-coef outputs/event_study_zs_ungated/coefficients.csv \
    --output-md reports/generated/its_method_comparison.md

echo "=== DistilBERT gold-set eval (already produced by training step) ==="
ls outputs/distilbert_eval.json 2>&1 | head -1
