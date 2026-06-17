# Embedding Architecture Report

## Dataset Schema

The embedding dataset is emitted as JSONL at `backend/data/embeddings/embedding_dataset.jsonl`.

Each record has:

| Field | Description |
| --- | --- |
| `surface_form` | Original word form in its source script. |
| `lemma` | Lemma from universal morphology analysis, falling back to surface form. |
| `root` | Morphological root from the universal analyzer. |
| `language` | One of `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, `otk`. |
| `features` | Universal morphology features such as `PLURAL`, `PAST`, `DERIVATIONAL`. |
| `cognate_group` | Universal cognate identifier from `cross_language_cognates.json`. |
| `historical_lineage` | Proto Turkic, Old Turkic, and selected modern descendants. |

## Feature Schema

`backend/apps/embeddings/embedding_features.py` defines `EmbeddingFeatureEncoder`.

Supported feature spaces:

- language ids
- lemma ids
- root ids
- universal morphology feature ids and multi-hot vectors
- cognate ids

The encoder is intentionally deterministic and vocabulary-based so the training phase can serialize the exact same feature ids used to build experiments.

## Provider Architecture

`backend/apps/embeddings/providers.py` defines the provider contract:

- `EmbeddingProvider`
- `FastTextProvider`
- `Word2VecProvider`
- `TransformerProvider`

The providers expose `fit`, `encode`, `save`, and `load` interfaces. They do not train or load large models in Phase 19. Their current role is to define a stable boundary for the training phase.

## Benchmark Design

`backend/data/embeddings/embedding_benchmark.json` defines three benchmark tasks:

1. Cognate similarity: same cognate group should rank closer than unrelated groups.
2. Morphology similarity: shared normalized morphology features should produce close neighbors.
3. Cross-language similarity: aligned concepts should retrieve across languages and scripts.

Splits are defined by `cognate_group` to avoid leakage between train, validation, and test partitions.

## Readiness

The embedding layer now has dataset construction, feature encoding, provider abstraction, and benchmark design. It is ready for a later training phase without requiring large model training in this phase.
