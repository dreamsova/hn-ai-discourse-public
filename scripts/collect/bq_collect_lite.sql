-- Cross-source corpus validation query (lite version).
--
-- Returns only the columns needed to compare against the Algolia
-- corpus by comment_id intersection. Skips `comment_text` (~80% of
-- row size), so the result downloads as a small CSV from the BigQuery
-- web console even in sandbox mode.
--
-- Project: hn-ai-discourse-497504

WITH base AS (
  SELECT
    id                                                      AS comment_id,
    time                                                    AS created_at_i,
    FORMAT_DATE('%Y-%m', DATE(TIMESTAMP_SECONDS(time)))     AS year_month,
    LOWER(text)                                             AS lower_text
  FROM `bigquery-public-data.hacker_news.full`
  WHERE type = 'comment'
    AND deleted IS NOT TRUE
    AND text IS NOT NULL
    AND time >= UNIX_SECONDS(TIMESTAMP '2020-01-01 00:00:00 UTC')
    AND time <  UNIX_SECONDS(TIMESTAMP '2025-01-01 00:00:00 UTC')
)
SELECT comment_id, year_month, 'broad_ai' AS bq_query_family
FROM base
WHERE REGEXP_CONTAINS(lower_text,
  r'(artificial intelligence|machine learning|deep learning|neural network)')
UNION ALL
SELECT comment_id, year_month, 'foundation_models' AS bq_query_family
FROM base
WHERE REGEXP_CONTAINS(lower_text,
  r'\b(gpt|llm|chatgpt|openai|claude|gemini)\b')
UNION ALL
SELECT comment_id, year_month, 'doomer' AS bq_query_family
FROM base
WHERE REGEXP_CONTAINS(lower_text,
  r'(ai safety|alignment|misalignment|existential risk|x-risk|p\(doom\))')
UNION ALL
SELECT comment_id, year_month, 'accelerationist' AS bq_query_family
FROM base
WHERE REGEXP_CONTAINS(lower_text,
  r'(e/acc|accelerationism|techno-optimism|abundance agenda|abundance)')
;
