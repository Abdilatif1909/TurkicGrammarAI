# JKSU-CIS Style Guide

Generated for Phase 39 target journal analysis on 2026-06-17.

Target journal: Journal of King Saud University Computer and Information Sciences.

Primary sources reviewed:

- Springer journal page: https://link.springer.com/journal/44443
- Springer submission guidelines: https://link.springer.com/journal/44443/submission-guidelines
- Recent article example: https://link.springer.com/article/10.1007/s44443-026-00887-0
- Crossref metadata for ISSNs `2213-1248` and `1319-1578`.

## Recent Paper Sample

The following 20 recent JKSU-CIS records were reviewed from Springer/Crossref metadata. The sample emphasizes recent online-first/original research papers and excludes correction notices.

| No. | Date | Title | DOI |
| ---: | --- | --- | --- |
| 1 | 2026-06-17 | The bidirectional quantum digital signature with enhanced performance | https://doi.org/10.1007/s44443-026-00646-1 |
| 2 | 2026-06-17 | PEC-Moni: learning to monitor compliance of personal protective equipment usage using joint 2D-3D representation for intelligent laboratory information management | https://doi.org/10.1007/s44443-025-00446-z |
| 3 | 2026-06-16 | A workflow-oriented and risk-aware system for Turkish legal named entity recognition: integrating transformer-based models with legal knowledge graphs | https://doi.org/10.1007/s44443-026-00915-z |
| 4 | 2026-06-16 | FDC-MSA: Feature denoising and conflict decoupling for inconsistent multimodal sentiment analysis | https://doi.org/10.1007/s44443-026-00935-9 |
| 5 | 2026-06-15 | SA-LoRA: Shared-A decoupled low-rank adaptation for class-incremental learning | https://doi.org/10.1007/s44443-026-00925-x |
| 6 | 2026-06-15 | Dynamic offset sampling for small object detection in LiDAR-based 3D perception | https://doi.org/10.1007/s44443-026-00947-5 |
| 7 | 2026-06-15 | Efficient multi-tenant LoRA serving via SGMV-specific operator autotuning | https://doi.org/10.1007/s44443-026-00937-7 |
| 8 | 2026-06-15 | EGCM-SegFormer: An edge-guided cross-scale semantic segmentation method for low-resolution eye images of mining-truck drivers | https://doi.org/10.1007/s44443-026-00933-x |
| 9 | 2026-06-15 | Omnidirectional motion perception inspired artificial crab visual neural network and related multi-object tracking | https://doi.org/10.1007/s44443-026-00908-y |
| 10 | 2026-06-13 | A few-shot point cloud segmentation network with multi-dimensional perception and temporal-frequency domain enhancement | https://doi.org/10.1007/s44443-026-00941-x |
| 11 | 2026-06-13 | GRACE-Agent: a multi-stage LLM agent framework for grammatical error correction in English academic writing with reduced false positives | https://doi.org/10.1007/s44443-026-00859-4 |
| 12 | 2026-06-13 | FedSkinQ: federated skin lesion classification with quantum-inspired token pruning in vision transformers | https://doi.org/10.1007/s44443-026-00881-6 |
| 13 | 2026-06-13 | Progressive feature enhancement network for object detection in low-light conditions | https://doi.org/10.1007/s44443-026-00927-9 |
| 14 | 2026-06-13 | SDOA: A scalable and trustworthy oracle architecture for heterogeneous blockchains | https://doi.org/10.1007/s44443-026-00918-w |
| 15 | 2026-06-13 | DBS-Net: A lightweight dual-brain synergy network for robust chili pepper disease recognition in complex environments | https://doi.org/10.1007/s44443-026-00940-y |
| 16 | 2026-06-12 | A spatially adaptive compressive sensing framework via joint perception-innovation modeling | https://doi.org/10.1007/s44443-026-00928-8 |
| 17 | 2026-06-12 | Iterative self-organizing clustering for software multiple-fault localisation | https://doi.org/10.1007/s44443-026-00845-w |
| 18 | 2026-06-11 | ExpertYARA: Learning discriminative YARA rules using mixture of experts set transformers | https://doi.org/10.1007/s44443-026-00902-4 |
| 19 | 2026-06-11 | Semantic consistency-aware multimodal deep learning for misinformation detection in short-form videos | https://doi.org/10.1007/s44443-026-00887-0 |
| 20 | 2026-06-11 | DMThreatNet: a hybrid data mining framework for early cybersecurity threat detection using ensemble intelligence | https://doi.org/10.1007/s44443-026-00916-y |

## Journal Positioning

The journal is an open access, refereed international computer science journal covering foundations and practical applications of computing. The Springer page lists SCOPUS and SCIE indexing and reports a 2024 Journal Impact Factor of 6.1. The journal currently publishes original papers, research papers, and review papers.

For the Turkic embeddings paper, position the manuscript as an original computational linguistics/NLP paper with an engineering contribution, empirical evaluation, and reproducibility package.

## Title Patterns

Observed patterns:

- Method acronym followed by descriptive expansion: `FDC-MSA: Feature denoising...`, `GRACE-Agent: ...`, `DBS-Net: ...`.
- Contribution-first method titles: `A workflow-oriented and risk-aware system for...`.
- Problem plus method phrase: `... for ... using ...`.
- Domain-specific application phrase near the end: `... for misinformation detection`, `... for traffic flow prediction`, `... for Turkish legal named entity recognition`.
- Titles are long but specific, often 12-22 words.

Recommended title pattern:

`Cognate-Aware Multilingual Embeddings for Turkic Languages Using Morphological and Historical Linguistic Knowledge`

Optional acronym variant:

`CAMEL-Turkic: Cognate-Aware Multilingual Embeddings for Turkic Languages Using Morphological and Historical Linguistic Knowledge`

Use the acronym only if the paper repeatedly names the method and the acronym does not look forced.

## Abstract Structure

Journal guideline: abstract should be 150-250 words, with no undefined abbreviations or unspecified references.

Observed recent abstract pattern:

1. Problem context: one or two sentences explaining the practical/research challenge.
2. Gap: state what existing methods miss.
3. Proposed method: introduce the named method and its components.
4. Evaluation setup: datasets, baselines, tasks, and metrics.
5. Main result: report quantitative improvements or strongest finding.
6. Validation/analysis: ablation, error analysis, robustness, or statistical evidence.
7. Limitation/future work: one sentence when appropriate.

Recommended abstract for this paper should be 190-230 words and follow exactly that seven-part flow.

## Section Structure

Springer guideline: use decimal heading numbering and no more than three heading levels.

Recommended JKSU-CIS structure:

1. Introduction
2. Related work
3. Materials and methods
4. Experimental setup
5. Results and discussion
6. Ablation and error analysis
7. Threats to validity
8. Conclusion and future work
9. Statements and declarations
10. References

For this target, do not bury the contribution in a broad survey. The introduction should end with a short contribution list and a paper organization paragraph.

## Figure Style

Springer requirements:

- Number figures with Arabic numerals.
- Cite figures in consecutive order.
- Use `Fig.` captions.
- Keep captions in the manuscript text, not inside the image file.
- Use legible lettering, preferably Helvetica or Arial.
- Do not place titles or captions inside illustrations.
- Use RGB color for color figures.
- Use patterns or redundant encodings where color carries meaning.
- Prepare figures at column-fitting sizes.

Observed/current JKSU-CIS pattern:

- Architecture diagrams for proposed models.
- Dataset or pipeline diagrams.
- Bar/line charts for benchmark comparisons.
- Ablation plots or component comparison figures.
- Confusion/error-analysis figures when the task is classification/retrieval-heavy.

Recommended figures for this paper:

- Fig. 1: Overall cognate-aware embedding architecture.
- Fig. 2: Turkic lexical/morphological/historical data construction pipeline.
- Fig. 3: Language distribution and evaluation-task coverage.
- Fig. 4: Embedding quality comparison across baselines.
- Fig. 5: Positive/negative cognate similarity separation or retrieval performance.
- Optional Fig. 6: Error categories or ablation impact visualization.

Target figure count: 5-6.

## Table Style

Springer requirements:

- Number tables with Arabic numerals.
- Cite tables in consecutive order.
- Supply a concise table caption explaining components.
- Use table footnotes with superscript lower-case letters or asterisks for statistical values.
- Use the table function in Word rather than spreadsheet screenshots.

Observed/current JKSU-CIS pattern:

- Dataset summary tables.
- Baseline comparison tables.
- Hyperparameter/training configuration tables.
- Metric result tables with best values highlighted.
- Ablation tables.
- Runtime/complexity or robustness tables when relevant.

Recommended tables for this paper:

- Table 1: Language distribution and corpus/resource statistics.
- Table 2: Lexical, morphological, cognate, and historical resource inventory.
- Table 3: Training configuration and embedding model settings.
- Table 4: Embedding intrinsic evaluation results.
- Table 5: Semantic search, RAG, and QA evaluation results.
- Table 6: Ablation study over cognate, morphology, and historical features.
- Table 7: Error analysis or confidence intervals.

Target table count: 6-7.

## Result Reporting Style

Expected pattern:

- State the metric first, then the comparison target.
- Report absolute values and relative improvements where defensible.
- Include baseline names and dataset/task names in the same paragraph.
- Avoid unsupported claims such as "state-of-the-art" unless all competing systems and datasets are independently comparable.
- Pair each major table with an interpretive paragraph: what improved, where it failed, and why the feature helped.
- Include ablation to prove that cognate, morphology, and historical signals are not decorative.
- Include confidence intervals or repeated-run statistics if available.

Recommended phrasing discipline:

- Use "improves over the strongest baseline by X on Y" only when the baseline and metric are directly comparable.
- Use "suggests" or "indicates" for synthetic/internal benchmarks.
- Use "candidate gold data" or "expert review pending" where applicable.
- Keep limitations visible instead of moving them only to supplementary material.

## Limitation Sections

Recent abstracts often include a final sentence about limits or future work. For this paper, include a dedicated `Threats to validity` section because dataset provenance, benchmark leakage, and expert-review status matter for reviewers.

Recommended limitation categories:

- Dataset provenance and generated/projected records.
- Expert-review status of gold data.
- Benchmark leakage risk for semantic search, RAG, and QA.
- FastText-specific limitations compared with contextual multilingual encoders.
- Low-resource language imbalance.
- Historical reconstruction uncertainty.
- Generalization beyond the eight Turkic languages in the repository.

## Conclusion Patterns

Observed pattern:

- Restate the problem and method in one sentence.
- Summarize the strongest empirical result.
- Mention ablation/analysis confirmation.
- State practical implication.
- End with concrete future work, not a broad promise.

Recommended conclusion flow:

1. "This paper introduced..."
2. "Across intrinsic embedding, cognate, semantic search, RAG, and QA evaluations..."
3. "Ablation results show..."
4. "The findings indicate..."
5. "Future work will focus on expert-reviewed gold datasets, independent external benchmarks, and contextual embedding models."

## Declarations and Data Availability

The submission guidelines require statements and declarations after the references. Original research must include a Data Availability Statement. For this repository-backed paper, include:

- Funding.
- Competing interests.
- Author contributions.
- Data availability with repository URL, commit hash, and archive DOI when available.
- Code availability with exact commit hash.
- Use of AI tools only if generative AI contributed beyond copy editing.

## Recommended Manuscript Targets

- Target length: 8,000-10,000 words excluding references, or about 22-28 double-spaced manuscript pages.
- Abstract: 190-230 words.
- Keywords: 5-6.
- Figures: 5-6.
- Tables: 6-7.
- References: 45-65, with emphasis on 2021-2026 NLP, multilingual embeddings, Turkic NLP, morphology-aware embeddings, cognate modeling, FastText/subword embeddings, low-resource evaluation, and reproducibility.

## Fit Assessment

The paper fits JKSU-CIS if framed as:

- a novel method for multilingual NLP representation learning,
- evaluated across multiple computational tasks,
- supported by reproducible datasets and code,
- honest about limitations and validation status.

The main risk is not topic fit; it is claim calibration. Avoid overclaiming publication-readiness of internal benchmarks unless independent validation is complete.
