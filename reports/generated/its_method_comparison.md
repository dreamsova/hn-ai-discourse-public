# ITS coefficient comparison across measurement instruments

Main specification: `share_<label> ~ t + post + t_post + pulse_gpt4 + pulse_board_crisis`, fit by WLS with Newey-West HAC(3) standard errors. Weights: `n_ai_in_scope` for the v2 panels.

Coefficients flagged with ✱ are significant at α=0.05.

| Outcome | Term | DistilBERT fine-tuned | TF-IDF baseline | Zero-shot DeBERTa (gated) | Zero-shot DeBERTa (ungated) | Methods agree? |
| --- | --- | --- | --- | --- | --- | --- |
| share_doomer_of_ai | Board crisis pulse | +0.0781 (p=0.000) ✱ | +0.0123 (p=0.000) ✱ | +0.1305 (p=0.000) ✱ | +0.0805 (p=0.000) ✱ | agree |
| share_doomer_of_ai | GPT-4 pulse | +0.0254 (p=0.000) ✱ | +0.0015 (p=0.604) | +0.0840 (p=0.000) ✱ | +0.0659 (p=0.000) ✱ | **disagree** |
| share_doomer_of_ai | Level shift @ ChatGPT | +0.0071 (p=0.234) | -0.0186 (p=0.143) | +0.0470 (p=0.006) ✱ | +0.0130 (p=0.173) | **disagree** |
| share_doomer_of_ai | Slope change @ ChatGPT | -0.0007 (p=0.112) | -0.0005 (p=0.351) | -0.0026 (p=0.009) ✱ | -0.0024 (p=0.000) ✱ | **disagree** |
| share_accelerationist_of_ai | Board crisis pulse | -0.0238 (p=0.000) ✱ | -0.0030 (p=0.002) ✱ | +0.0043 (p=0.000) ✱ | +0.0049 (p=0.000) ✱ | **disagree** |
| share_accelerationist_of_ai | GPT-4 pulse | -0.0627 (p=0.000) ✱ | -0.0044 (p=0.018) ✱ | +0.0055 (p=0.000) ✱ | +0.0060 (p=0.000) ✱ | **disagree** |
| share_accelerationist_of_ai | Level shift @ ChatGPT | -0.0664 (p=0.000) ✱ | -0.0348 (p=0.000) ✱ | -0.0023 (p=0.212) | +0.0017 (p=0.057) | **disagree** |
| share_accelerationist_of_ai | Slope change @ ChatGPT | -0.0027 (p=0.000) ✱ | -0.0012 (p=0.000) ✱ | -0.0003 (p=0.006) ✱ | -0.0001 (p=0.070) | **disagree** |

**Reading guide.** Methods 'agree' if the coefficient has the same sign AND the same significance verdict (both p<α or both p≥α). 'Disagree' rows are the ones whose headline interpretation depends on the measurement instrument and therefore deserve the most scrutiny in any narrative summary.