# PAPER_OUTLINE_JKSU

Working title:

`Cognate-Aware Multilingual Embeddings for Turkic Languages Using Morphological and Historical Linguistic Knowledge`

Target journal:

`Journal of King Saud University Computer and Information Sciences`

## Manuscript Targets

- Target length: 8,000-10,000 words excluding references.
- Abstract: 190-230 words.
- Keywords: 5-6.
- Figures: 5-6.
- Tables: 6-7.
- References: 45-65.
- Heading style: decimal numbering, maximum three levels.
- Reference style: Springer author-date style with DOI links where available.

## Proposed Keywords

- Turkic languages
- multilingual embeddings
- cognate-aware learning
- morphology-aware NLP
- historical linguistics
- low-resource language processing

## Abstract Blueprint

Use one paragraph, 190-230 words:

1. State the low-resource Turkic NLP problem.
2. Explain why generic multilingual embeddings miss cognate, morphology, and historical signals.
3. Introduce the proposed cognate-aware multilingual embedding framework.
4. Describe the resources: lexical data, morphology rules/lemmas, cognate sets, historical forms, and benchmark tasks.
5. State evaluation tasks: morphology, cognate alignment, intrinsic embedding quality, semantic search, RAG retrieval, and QA.
6. Report the strongest quantitative findings from the validated results.
7. Mention ablation/error analysis.
8. Close with limitation-aware significance and reproducibility package availability.

## Publication-Ready Outline

### 1. Introduction

Goal: establish the computational problem and the linguistic motivation.

Content:

- Low-resource NLP remains difficult for Turkic languages despite multilingual models.
- Turkic languages share cognates, agglutinative morphology, and historical correspondences that generic embedding training often underuses.
- Existing multilingual embeddings capture subword regularities but do not explicitly encode structured cognate and historical knowledge.
- This paper proposes a cognate-aware embedding approach that integrates lexical, morphological, cognate, and historical linguistic resources.
- Summarize evaluated tasks: morphology, cognate similarity, intrinsic embeddings, semantic search, RAG retrieval, and QA.

Contribution paragraph:

- A multilingual Turkic resource construction pipeline.
- A cognate-aware embedding strategy using morphology and historical linguistic knowledge.
- A multi-task evaluation protocol across representation and retrieval tasks.
- Ablation and error analysis isolating cognate, morphology, and historical components.
- A reproducibility package with figures, tables, validation reports, and repository artifacts.

Suggested Figure/Table:

- Fig. 1: Overall architecture.
- Table 1: Language distribution.

### 2. Related Work

Goal: connect the paper to JKSU-CIS computer science audiences, not only linguistics audiences.

#### 2.1 Multilingual and low-resource embeddings

Cover FastText/subword embeddings, multilingual representation learning, low-resource NLP, and cross-lingual transfer.

#### 2.2 Morphology-aware representation learning

Discuss agglutinative morphology, subword segmentation, lemma/root features, and morphology-informed embeddings.

#### 2.3 Cognate modeling and historical linguistic knowledge

Discuss cognate detection, language-family-aware modeling, etymological/historical forms, and cross-language lexical alignment.

#### 2.4 Turkic NLP resources

Discuss available Turkic language datasets, gaps, and why a multilingual Turkic-specific setup is needed.

#### 2.5 Retrieval and QA evaluation for linguistic resources

Connect embeddings to semantic search, RAG retrieval, and QA evaluation.

Suggested Table:

- Table 2: Comparison of related work by language coverage, morphology, cognates, historical data, and evaluation tasks.

### 3. Materials and Methods

Goal: describe the system enough for reproducibility.

#### 3.1 Language coverage and data sources

Languages:

- Azerbaijani
- Kazakh
- Kyrgyz
- Old Turkic
- Turkish
- Turkmen
- Uyghur
- Uzbek

Describe lexical records, morphology rules/lemmas, cognate sets, historical forms, benchmark files, and gold candidate datasets.

Suggested Table:

- Table 1: Language distribution and dataset statistics.

#### 3.2 Data normalization and resource construction

Describe canonical language codes, lexical fields, morphology fields, cognate group fields, historical fields, and quality checks.

Important: identify generated/projected records and candidate gold data clearly.

Suggested Figure:

- Fig. 2: Data construction and validation pipeline.

#### 3.3 Cognate-aware embedding framework

Describe:

- base lexical corpus,
- subword embedding training,
- cognate group signals,
- morphology-informed tokens/features,
- historical form signals,
- semantic index construction.

Suggested Figure:

- Fig. 1: Architecture diagram.

#### 3.4 Morphological and historical knowledge integration

Explain how roots, lemmas, suffixes, derivational rules, cognate groups, and historical forms are converted into embedding evidence.

#### 3.5 Reproducibility package

Point to:

- repository commit,
- `DATASET_MANIFEST.md`,
- `MODEL_MANIFEST.md`,
- `REPRODUCIBILITY_REPORT.md`,
- `paper_package/`,
- external model/data archive if available.

### 4. Experimental Setup

Goal: make evaluation defensible and easy to reproduce.

#### 4.1 Research questions

RQ1: Does cognate-aware embedding improve multilingual Turkic lexical similarity?

RQ2: Do morphology and historical features improve cognate and semantic retrieval?

RQ3: How does the embedding model affect downstream semantic search, RAG, and QA?

RQ4: Which component contributes most according to ablation?

#### 4.2 Baselines

Recommended baselines:

- vanilla FastText trained on lexical corpus,
- morphology-only variant,
- cognate-only variant,
- historical-only variant,
- combined model,
- available multilingual baseline if reproducible.

#### 4.3 Evaluation tasks and metrics

Tasks:

- morphology evaluation,
- cognate evaluation,
- intrinsic embedding similarity,
- semantic search,
- RAG retrieval,
- QA.

Metrics:

- accuracy/F1 where labels exist,
- precision@k, recall@k, MRR, nDCG for retrieval,
- similarity separation for positive/negative cognate pairs,
- confidence intervals or repeated-run variance where available.

Suggested Table:

- Table 3: Training configuration and evaluation settings.

#### 4.4 Implementation details

Include:

- Python version,
- package versions,
- training parameters,
- hardware if relevant,
- random seeds,
- data split policy,
- repository commit hash.

### 5. Results and Discussion

Goal: report results in table-first, interpretation-second style.

#### 5.1 Dataset and resource coverage

Discuss language balance, resource imbalance, and coverage gaps.

Suggested Figure:

- Fig. 3: Language/resource distribution.

#### 5.2 Embedding quality results

Report intrinsic embedding metrics and baseline comparisons.

Suggested Table:

- Table 4: Embedding evaluation results.

Suggested Figure:

- Fig. 4: Baseline comparison across embedding metrics.

#### 5.3 Cognate alignment and similarity results

Report positive/negative cognate separation, nearest-neighbor examples, and cross-language alignment behavior.

Suggested Figure:

- Fig. 5: Positive vs. negative similarity distributions.

#### 5.4 Semantic search, RAG, and QA results

Report retrieval and QA metrics. Separate regression-style internal benchmarks from independent or expert-reviewed evaluation.

Suggested Table:

- Table 5: Semantic search, RAG, and QA results.

#### 5.5 Linguistic interpretation

Explain where morphology and historical forms help:

- shared roots,
- regular sound correspondences,
- suffix-rich forms,
- language-family-aware retrieval,
- Old Turkic historical anchors.

### 6. Ablation and Error Analysis

Goal: prove each knowledge source has measurable value.

#### 6.1 Ablation design

Variants:

- no cognates,
- no morphology,
- no historical forms,
- lexical-only,
- full combined model.

Suggested Table:

- Table 6: Ablation study summary.

#### 6.2 Error categories

Recommended categories:

- false cognate attraction,
- morphology overgeneration,
- root ambiguity,
- language imbalance,
- historical-form mismatch,
- semantic search leakage,
- QA answer unsupported by evidence.

Suggested Table:

- Table 7: Error analysis and confidence intervals.

#### 6.3 Case studies

Include 3-5 compact examples showing why the model succeeds or fails. Keep examples tied to metrics.

### 7. Threats to Validity

Goal: make reviewer concerns explicit.

#### 7.1 Internal validity

Discuss implementation assumptions, deterministic heuristics, and possible evaluation leakage.

#### 7.2 Dataset validity

Discuss generated records, projected cognates, candidate gold data, and expert-review status.

#### 7.3 External validity

Discuss generalization beyond the included Turkic languages and beyond FastText-style embeddings.

#### 7.4 Reproducibility validity

Discuss model binaries, embedding indexes, repository commit, external archives, and how reviewers can rerun evaluations.

### 8. Conclusion and Future Work

Recommended conclusion structure:

- Introduce final summary in one sentence.
- State the strongest empirical result.
- State what ablation shows.
- State what the work contributes to Turkic NLP and low-resource multilingual embeddings.
- End with concrete future work:
  - expert-reviewed gold datasets,
  - independent external benchmarks,
  - contextual multilingual encoders,
  - stronger historical reconstruction metadata,
  - archived model artifacts with persistent DOI.

### Statements and Declarations

Include after references or as required by the submission system:

- Funding.
- Competing interests.
- Author contributions.
- Data availability.
- Code availability.
- Ethics approval, if applicable.
- Use of AI tools, if applicable beyond copy editing.

### Data Availability Statement Draft

The datasets, code, evaluation reports, and manuscript preparation artifacts used in this study are available in the TurkicGrammarAI repository at commit `[COMMIT_HASH]`. The reproducibility package includes figures, tables, analysis notes, validation reports, dataset manifests, model manifests, and reviewer-facing documentation. Large model binaries and generated embedding indexes are distributed separately at `[ARCHIVE_DOI_OR_URL]` because they are not suitable for direct Git tracking.

### Code Availability Statement Draft

The source code for data processing, morphology evaluation, cognate evaluation, embedding evaluation, semantic search, RAG retrieval, and QA evaluation is available in the TurkicGrammarAI repository at commit `[COMMIT_HASH]`.

## Figure Plan

| Figure | Title | Purpose |
| ---: | --- | --- |
| Fig. 1 | Cognate-aware multilingual embedding architecture | Show the proposed method and data flow. |
| Fig. 2 | Linguistic resource construction pipeline | Show lexical, morphology, cognate, and historical artifact generation. |
| Fig. 3 | Language and resource coverage | Show dataset balance and coverage gaps. |
| Fig. 4 | Embedding performance comparison | Compare full model with baselines. |
| Fig. 5 | Cognate similarity separation | Show positive/negative pair separation or nearest-neighbor behavior. |
| Fig. 6 | Ablation or error category impact | Optional if results need visual explanation. |

## Table Plan

| Table | Title | Purpose |
| ---: | --- | --- |
| Table 1 | Language distribution | Establish data scale and language coverage. |
| Table 2 | Research resource inventory | Document lexical, morphology, cognate, historical, benchmark, and gold candidate resources. |
| Table 3 | Training and evaluation configuration | Make experiments reproducible. |
| Table 4 | Intrinsic embedding evaluation | Report embedding quality against baselines. |
| Table 5 | Retrieval and QA evaluation | Report semantic search, RAG, and QA metrics. |
| Table 6 | Ablation study | Isolate contribution of cognate, morphology, and historical signals. |
| Table 7 | Error analysis and confidence intervals | Show robustness and known failure modes. |

## Claim Calibration

Use:

- "cognate-aware multilingual embedding framework"
- "low-resource Turkic NLP"
- "reproducible research prototype"
- "improves internal benchmark performance"
- "candidate gold datasets requiring expert review"

Avoid unless independently proven:

- "state-of-the-art"
- "fully validated"
- "production-ready"
- "human-level"
- "universal Turkic language model"

## Final Pre-Submission Checklist

- Abstract is 150-250 words.
- Keywords are 4-6 terms.
- All abbreviations are defined at first use.
- Headings use decimal numbering and no more than three levels.
- Every figure and table is cited in order.
- All figures have `Fig.` captions and no embedded titles.
- All tables have captions and footnotes where needed.
- References use author-date style and DOI links where available.
- Data Availability Statement includes repository commit and archive DOI/URL.
- Claims are aligned with expert-review and benchmark limitations.
