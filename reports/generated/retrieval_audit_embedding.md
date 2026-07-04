# Embedding-based retrieval audit

Anchor sentences encoded with `sentence-transformers/all-MiniLM-L6-v2`. A comment is
labeled **semantically AI** if its embedding has cosine similarity
≥ 0.55 to at least one of the 6
anchors.

## Corpus-wide confusion

| | semantically_ai = True | semantically_ai = False |
| --- | --- | --- |
| lexicon_retrieved = True  | **2,732** (true positive) | 135,006 |
| lexicon_retrieved = False | **46** (lexicon false negative) | 248,382 |

- Estimated retrieval recall: **98.3%**
- Estimated false-negative rate: **1.7%**

Full per-month table: `outputs/retrieval_audit_embedding.csv`.

## Interpretation

This number complements the 200-row gold-set audit. The gold set
measured **lexicon precision** (51% of lexicon-retrieved comments
were `wrong_other` / off-topic). This embedding audit measures
**lexicon recall** (what fraction of semantically-AI comments did the
lexicon miss?). Together they bound the lexicon's signal/noise floor
in both directions.
