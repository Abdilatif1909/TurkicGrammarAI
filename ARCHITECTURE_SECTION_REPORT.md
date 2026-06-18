# Architecture Section Report

## Deliverable

- Section file: `paper_draft/04_Cognate_Aware_Embedding_Architecture.md`
- Target journal style: Journal of King Saud University – Computer and Information Sciences
- Scope: repository-supported methodology only

## Verification

- Word count: 2,368 words excluding Markdown headings
- Figure referenced: Figure 1
- Table referenced: Table 3

## Architectural Components Described

- Morphological enrichment with surface forms, lemmas, roots, normalized features, and derivational information
- Cognate-group encoding through `COGNATE_<id>` tokens and grouped signal lines
- Historical lineage encoding through `LINEAGE_<stage>` and `LINEAGE_FORM_<form>` tokens
- Construction of the 100,000-record, eight-language JSONL embedding dataset
- FastText corpus preparation and skip-gram training
- FastText subword modeling and repository training configuration
- Semantic-index construction and metadata-aware semantic search
- Heuristic RAG retrieval with component-level evidence scores
- Retrieval-based, template-driven QA integration

## Repository Consistency Controls

- No new architecture modules were introduced.
- No code or model artifacts were modified.
- No evaluation results were added to the methodology section.
- FastText character n-gram settings are described as library defaults because the repository does not override them.
- RAG ranking is identified as manually weighted.
- QA is identified as retrieval-based and template-driven rather than generative.
