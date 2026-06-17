# Top Reviewer Questions

1. How do you prevent leakage when embedding training data and benchmark generation both draw from the same repository resources?
2. Which lexical records have externally verified provenance, and which are generated or merged internally?
3. Why should synthetic or semi-synthetic benchmark metrics be interpreted as evidence of linguistic validity?
4. Where is the baseline FastText model without cognate/historical/morphological feature injection?
5. Can the reported improvements be quantified without a stored baseline evaluation?
6. How would results change under a controlled ablation removing ROOT, COGNATE, LINEAGE, and LANGUAGE features one at a time?
7. Are cognate groups expert-reviewed, algorithmically inferred, or manually curated, and how is error propagated into embeddings?
8. How are false cognates distinguished from true historical cognates in the benchmark?
9. Does the model distinguish semantic similarity from etymological relatedness?
10. How robust are results across scripts, especially Uyghur Arabic, Cyrillic Kazakh/Kyrgyz, Latin Turkish/Azerbaijani/Uzbek, and Old Turkic runiform?
11. What happens to retrieval quality on unseen words not present in the embedding dataset?
12. Are negative pairs linguistically hard negatives or random negatives?
13. Why are some cluster separation metrics negative, and how does that affect claims about embedding space structure?
14. What external gold standard confirms lemma and root quality across all supported languages?
15. How are dialectal variants and orthographic variants normalized?
16. What is the effect of duplicate or near-duplicate records on nearest-neighbor evaluation?
17. How do semantic search metrics compare against BM25, multilingual sentence transformers, or standard FastText?
18. Does QA accuracy measure factual correctness or only overlap with expected words?
19. Can the RAG latency metric be reproduced on a different machine or deployment environment?
20. How are historical forms validated, and what sources support Proto-Turkic and Old Turkic reconstructions?
21. What proportion of Uyghur coverage comes from direct lexical resources versus cognate/historical expansion?
22. Are benchmark categories balanced enough to support aggregate metric interpretation?
23. How is uncertainty represented for metrics other than simple proportions?
24. Why is Cohen's d not reported for positive vs negative similarities?
25. Which claims in the manuscript would remain valid if all synthetic benchmark results were removed?
