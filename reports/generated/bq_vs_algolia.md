# BigQuery vs Algolia cross-source validation

We collected the same 2020-2024 HN AI-discourse corpus from two
independent cloud sources:

- **Algolia HN Search API** via AWS EC2 t3.small (`collect_hn_shard.py`)
- **Google BigQuery** on `bigquery-public-data.hacker_news.full` (`bq_collect.sql`)

## Row counts

| Source | Unique `comment_id` |
| --- | --- |
| Algolia (residential local run) | **386,166** |
| BigQuery (Google Cloud) | **271,742** |
| Intersection (in both) | **121,048** |
| Algolia-only | 265,118 |
| BigQuery-only | 150,694 |

## Cross-source recall

- **BigQuery recall on Algolia corpus**: 31.3% (fraction of Algolia comment_ids confirmed by BigQuery as still present in HN's official dataset)
- **Algolia recall on BigQuery corpus**: 44.5% (fraction of BigQuery hits that Algolia's search index also surfaced)

## Per-family breakdown

| Family | Algolia | BigQuery |
| --- | --- | --- |
| accelerationist | 69,756 | 7,335 |
| broad_ai | 59,401 | 47,851 |
| doomer | 23,121 | 17,743 |
| foundation_models | 242,434 | 204,760 |

## Interpretation

Disagreement between sources is expected because the two endpoints
use different matching strategies: Algolia is a tokenized search
index (matches surface a ranked subset using its own analyzer),
while BigQuery exposes the raw HN firehose where we apply explicit
regex matches on lowercased text. A high BigQuery-recall-on-Algolia
number ensures the Algolia-collected corpus is faithfully drawn from
the underlying HN dataset; a substantially lower number would suggest
the analytical basis includes comments that no longer exist in HN's
official record (deletions, edits, etc.).