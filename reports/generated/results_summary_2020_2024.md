# Results Snapshot (2020_2024)

## Coverage

- Panel range: `2020-01` to `2024-12`
- Monthly observations: `60`
- Total comments in panel: `386166`
- Average monthly comment volume: `6436.1`

## Classifier (weak-supervision)

- Evaluation type: `held_out`
- Accuracy on held-out weak labels: `0.9111`
- Macro F1: `0.7545`
- Doomer F1: `0.7222`
- Accelerationist F1: `0.5926`
- Neutral F1: `0.9486`
- Weakly labeled training documents: `6115`

## Descriptive Findings

- Peak doomer month: `2023-05` at `2.95%`
- Peak accelerationist month: `2022-01` at `1.95%`
- Average doomer share pre-`2022-12`: `1.27%`
- Average doomer share post-`2022-12`: `1.73%`
- Average accelerationist share pre-`2022-12`: `0.82%`
- Average accelerationist share post-`2022-12`: `0.67%`
- Average neutral share pre-`2022-12`: `19.34%`
- Average neutral share post-`2022-12`: `49.50%`

## Interrupted Time Series (main spec: ChatGPT + GPT-4/board pulses)

### Outcome: `share_doomer` (R² = 0.335)

| Term | Coef | SE | p-value | 95% CI |
| --- | --- | --- | --- | --- |
| `const` | +0.01224 | 0.00152 | 0.0000 | [+0.00927, +0.01521] |
| `t` | +0.00003 | 0.00010 | 0.7957 | [-0.00017, +0.00023] |
| `post` | +0.00433 | 0.00328 | 0.1868 | [-0.00210, +0.01075] |
| `t_post` | -0.00011 | 0.00020 | 0.5896 | [-0.00049, +0.00028] |
| `pulse_gpt4` | +0.00811 | 0.00198 | 0.0000 | [+0.00424, +0.01199] |
| `pulse_board_crisis` | +0.01195 | 0.00115 | 0.0000 | [+0.00970, +0.01421] |

### Outcome: `share_accelerationist` (R² = 0.335)

| Term | Coef | SE | p-value | 95% CI |
| --- | --- | --- | --- | --- |
| `const` | +0.00497 | 0.00066 | 0.0000 | [+0.00367, +0.00627] |
| `t` | +0.00020 | 0.00004 | 0.0000 | [+0.00012, +0.00028] |
| `post` | -0.00387 | 0.00112 | 0.0005 | [-0.00606, -0.00169] |
| `t_post` | -0.00029 | 0.00006 | 0.0000 | [-0.00041, -0.00018] |
| `pulse_gpt4` | +0.00034 | 0.00050 | 0.5009 | [-0.00064, +0.00131] |
| `pulse_board_crisis` | -0.00005 | 0.00033 | 0.8712 | [-0.00070, +0.00059] |

### Pre-trend test (ChatGPT pre-period)

| Outcome | slope/month | SE | p-value | n_pre_months |
| --- | --- | --- | --- | --- |
| `share_doomer` | +0.000026 | 0.000097 | 0.7846 | 34 |
| `share_accelerationist` | +0.000199 | 0.000045 | 0.0000 | 34 |

## Interpretation Notes

- For the doomer share, the GPT-4 release and OpenAI board crisis appear as significant pulses, while the ChatGPT level shift is not detectable in the main spec.
- For the accelerationist share, the pre-trend is significantly positive in the pre-ChatGPT window, so the post-ChatGPT decline must be read relative to that already-rising baseline rather than as an unconditional drop.
- All findings are descriptive event-study evidence, not causally identified. The weak-supervision classifier achieves high held-out accuracy against its own labeling rule, but gold-set validation against human judgment is needed before reporting these numbers as the final measurement.
