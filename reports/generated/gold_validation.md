# Gold-set validation

- Total labeled rows: 200
- Evaluable rows (gold ∈ {doomer, accelerationist, neutral}): 98
- Marked `wrong_other` (lexicon false positive or off-topic): 102 (51.0% of labeled rows)

> **Note on the wrong_other rate**: this is the empirical lexicon false-positive rate. If this number is non-trivial (>5%), the AI retrieval gate is noisier than the pipeline assumes.

## Method comparison

Macro F1 per class, across all evaluated methods:

| Class | Lexicon weak-label rule | TF-IDF + LR (baseline) | Zero-shot DeBERTa-v3-large NLI |
| --- | --- | --- | --- |
| accelerationist | 0.200 | 0.200 | 0.000 |
| doomer | 0.585 | 0.513 | 0.513 |
| neutral | 0.855 | 0.844 | 0.851 |
| **macro F1** | 0.547 | 0.519 | 0.455 |
| **accuracy** | 0.765 | 0.745 | 0.745 |

## Lexicon weak-label rule

_Evaluable rows for this method: 98_

| Class | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| accelerationist | 0.500 | 0.125 | 0.200 | 8 |
| doomer | 0.444 | 0.857 | 0.585 | 14 |
| neutral | 0.899 | 0.816 | 0.855 | 76 |
| **macro avg** | 0.614 | 0.599 | 0.547 | 98 |

Overall accuracy: **0.765**

Confusion matrix (rows = gold, cols = predicted):

| gold \ pred | accelerationist | doomer | neutral |
| --- | --- | --- | --- |
| accelerationist | 1 | 2 | 5 |
| doomer | 0 | 12 | 2 |
| neutral | 1 | 13 | 62 |

## TF-IDF + LR (baseline)

_Evaluable rows for this method: 98_

| Class | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| accelerationist | 0.500 | 0.125 | 0.200 | 8 |
| doomer | 0.400 | 0.714 | 0.513 | 14 |
| neutral | 0.873 | 0.816 | 0.844 | 76 |
| **macro avg** | 0.591 | 0.552 | 0.519 | 98 |

Overall accuracy: **0.745**

Confusion matrix (rows = gold, cols = predicted):

| gold \ pred | accelerationist | doomer | neutral |
| --- | --- | --- | --- |
| accelerationist | 1 | 2 | 5 |
| doomer | 0 | 10 | 4 |
| neutral | 1 | 13 | 62 |

## Zero-shot DeBERTa-v3-large NLI

_Evaluable rows for this method: 98_

| Class | Precision | Recall | F1 | Support |
| --- | --- | --- | --- | --- |
| accelerationist | 0.000 | 0.000 | 0.000 | 8 |
| doomer | 0.400 | 0.714 | 0.513 | 14 |
| neutral | 0.875 | 0.829 | 0.851 | 76 |
| **macro avg** | 0.425 | 0.514 | 0.455 | 98 |

Overall accuracy: **0.745**

Confusion matrix (rows = gold, cols = predicted):

| gold \ pred | accelerationist | doomer | neutral |
| --- | --- | --- | --- |
| accelerationist | 0 | 3 | 5 |
| doomer | 0 | 10 | 4 |
| neutral | 1 | 12 | 63 |
