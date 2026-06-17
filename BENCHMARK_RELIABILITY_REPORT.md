# Benchmark Reliability Report

Date: 2026-06-11

## Summary

TurkicGrammarAI now has a structured scientific validation framework, but current gold datasets should be treated as expert-review candidates, not completed human-reviewed gold standards.

## Reliability Levels

| Level | Meaning | Current Availability |
| --- | --- | --- |
| Synthetic regression | Generated from rules/resources; useful for regression and coverage checks. | Available |
| Independent candidate | Derived from independent benchmark files or normalized resources; useful for pre-review evaluation. | Available |
| Expert-reviewed gold | Human expert has verified each annotation. | Not yet available |

## Dataset Reliability Assessment

### Morphology

Records: 5,000.

Composition:

- 4,621 independent-derived candidate records.
- 379 synthetic supplement records.

Reliability:

- Good for broad pre-review regression.
- Not sufficient for publication-grade morpheme accuracy because no expert signoff is recorded.

### Cognates

Records: 2,000.

Reliability:

- Strong structural consistency because all records map to explicit `cognate_id` groups.
- Not publication-grade until cognate membership and proto-form claims are expert-reviewed.

### Historical

Records: 1,000.

Reliability:

- Good for lineage pipeline validation.
- Current sources include generated records, so historical claims require expert validation before scientific use.

### QA

Records: 2,000.

Reliability:

- Useful for testing answer/source retrieval behavior.
- Expected answers are term-based and should be expanded into human-written acceptable-answer rubrics.

## Evaluation Reliability

Current evaluator output:

- Morphology: 5,000 cases, Any-Match 78.44%.
- Cognates: 2,000 cases, Alignment 100.0%.
- Historical: 1,000 cases, Lineage 100.0%.
- QA: 200 sampled cases, Answer 99.5%, Source 99.5%.

Interpretation:

- Morphology score is the most informative current metric because it includes more diverse independent-derived examples.
- Cognate and historical 100% scores mainly prove internal consistency between datasets and engines, not external scientific correctness.
- QA score proves pipeline retrieval consistency on expected terms, not full answer quality.

## Leakage Risk

| Area | Leakage Risk | Reason |
| --- | --- | --- |
| Morphology | Medium | 379 synthetic supplement records come from existing synthetic benchmarks. |
| Cognates | High | Gold-candidate cognates are normalized from the same resource used by the cognate engine. |
| Historical | High | Gold-candidate historical chains are normalized from the same backend historical resource. |
| QA | Medium-High | QA expected answers are derived from existing benchmark/cognate resources. |

## Recommendations Before Publication

1. Replace synthetic morphology supplements with independently annotated examples.
2. Have at least two reviewers verify cognate groups and resolve disagreements.
3. Add source citations for historical lineages.
4. Convert QA expected answers into rubric objects with acceptable variants and required citations.
5. Split every gold dataset into locked validation and hidden test partitions.
6. Re-run evaluation only after all candidate records are marked `expert_reviewed`.

## Reliability Verdict

Framework readiness: high.

Current benchmark scientific reliability: medium for engineering validation, low for publication claims.

Publication-ready status: not achieved until expert review is completed.
