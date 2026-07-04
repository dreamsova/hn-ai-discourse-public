# Final Presentation Script (5 minutes, ~650 spoken words)

Target deck: [`deliverables/hn-ai-discourse-final-presentation-2020-2024.pptx`](../deliverables/hn-ai-discourse-final-presentation-2020-2024.pptx). The deck has 8 slides. A pace around 125 to 135 words per minute should fit comfortably.

---

## Slide 1 - Title (~25s)

Hi everyone. My project is called *Mapping the Discursive Battle Over AI on Hacker News*. I study Hacker News comments from 2020 through 2024, covering 60 months and roughly 411,000 retrieved comments.

The basic question is: after ChatGPT, did AI discussion among technologists become more dominated by doom-oriented language, accelerationist optimism, or something else?

## Slide 2 - Research question (~35s)

Hacker News is not just a random comment section. It is a technical public sphere where engineers, founders, researchers, and policy-adjacent people argue about new technologies early.

So I treat HN as a place where frames around AI become visible before they are fully settled in mainstream discourse. The two main frames are doomer discourse, meaning existential risk or alignment failure, and accelerationist discourse, meaning rapid deployment, abundance, and build-faster optimism.

The harder question is whether that answer stays stable when we measure the same corpus in different ways.

## Slide 3 - Why large-scale computing matters (~40s)

This became a scalable computing project for three reasons.

First, data collection was naturally parallel. I split it into 1,260 year-month by keyword-family shards.

Second, classification had to be repeated across the corpus. I scored the same comments using a lexicon rule, TF-IDF logistic regression, zero-shot DeBERTa, and fine-tuned DistilBERT.

Third, I benchmarked the computing itself. I recomputed the same monthly panel with pandas, local Dask, multi-node Dask on Slurm, and PySpark.

## Slide 4 - Pipeline (~40s)

The pipeline has six stages. Collection ran off-cluster because Midway compute nodes could not reliably access the Algolia API from inside Slurm. I used local parallel collection and an AWS EC2 plus S3 path, then moved the data onto Midway.

After that, the heavy work happened on Midway. Slurm array jobs cleaned raw JSON, deduplicated comments, and wrote Parquet files. CPU jobs handled TF-IDF inference, while GPU jobs handled transformer classifiers and the embedding atlas.

The outputs are monthly panels, event-study estimates, validation reports, and public dashboards.

## Slide 5 - Backend benchmark (~40s)

I ran four aggregation backends over the same 1,260 inference Parquet files. Serial pandas took about 62 seconds. PySpark was fastest at about 23 seconds. Multi-node Dask was also faster than pandas, at about 36 seconds.

But local Dask was slower than pandas, around 152 seconds. That was useful. It shows that distributed computing is not automatically better. At this size, partition overhead and shuffle costs can overwhelm parallelism.

## Slide 6 - Cross-method event study (~50s)

Across the four classifiers, most headline event-study coefficients do not agree. In several cases, the sign changes. One method might suggest accelerationist framing rose around an event, while another suggests it fell.

That matters because if I had reported only one classifier, the project would have looked cleaner than it really is. The stronger conclusion is that AI-discourse measurement is sensitive to the instrument.

The most stable finding is the OpenAI board crisis. Across methods, that event is the clearest doomer pulse. The corpus gives stronger support for a short spike in risk and governance language around the board crisis than for a simple permanent post-ChatGPT shift.

## Slide 7 - Gold-set validation (~45s)

To check the measurement, I hand-labelled a 200-comment gold set. This was useful, and honestly a little humbling. About 51 percent of lexicon hits were labelled `wrong_other`, meaning they were not actually about AI or were too ambiguous to use.

Among AI-related rows, neutral comments were much easier to classify than the two ideological frames. The TF-IDF model did well on neutral comments, but struggled with accelerationist ones because the frame is often more implicit.

So validation did not just evaluate the model. It showed where the conclusions need caution.

## Slide 8 - Contribution and closing (~35s)

Substantively, Hacker News does show moments of increased AI risk discourse, especially around the OpenAI board crisis. Methodologically, the bigger takeaway is that classifier choice changes the story.

So my final answer is not just "HN became more doomer" or "HN became more accelerationist." It is that large-scale discourse analysis needs scalable computing and measurement robustness together. This pipeline makes that visible by running the same question across multiple classifiers, multiple aggregation backends, and a manually validated gold set.

Thank you.
