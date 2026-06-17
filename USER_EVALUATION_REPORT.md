# User Evaluation Report

## Scope

Phase 27 adds the first human-evaluation workflow for the QA and retrieval system.

## Benchmark

Created:

- `backend/data/evaluation/human_evaluation_benchmark.json`

Size:

- 500 reviewed seed queries

Categories:

- cognate
- historical
- cross-language
- morphology

Each record includes:

- question
- expected answer terms
- expected source id
- review status
- placeholders for answer usefulness, answer correctness, and citation correctness

## Metrics

The human evaluation workflow measures:

- answer usefulness
- answer correctness
- citation correctness

The current benchmark is a manually curated seed set intended to bootstrap the evaluation process. Full production validation should replace or extend this with independent expert annotations.

## Feedback Loop

User feedback is collected through:

- `POST /api/feedback/`

Low-rated feedback creates QA error logs for review:

- `QaErrorLog`
- `GET /api/admin/qa-errors/`

## Admin Review

Admin dashboard support includes:

- usage statistics
- QA accuracy trends from ratings
- most requested words
- most requested languages
- feedback list
- QA error list

## Evaluation Readiness

| Capability | Status |
| --- | --- |
| Feedback capture | Ready |
| Low-rating QA error logging | Ready |
| Human evaluation benchmark | Ready |
| Source citation review fields | Ready |
| Admin QA trend endpoint | Ready |
| Admin dashboard UI | Ready |

## Next Step

Run a supervised expert review pass over the 500 benchmark questions and fill the metric fields with 1-5 scores for usefulness, correctness, and citation correctness.
