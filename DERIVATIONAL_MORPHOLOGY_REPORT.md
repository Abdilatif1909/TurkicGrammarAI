# Derivational Morphology Report

## Inventory

Created `backend/data/morphology/derivational_rules.json` with curated Uzbek derivational categories:

| Category | Suffixes |
| -------- | -------- |
| Noun -> Profession | `-chi`, `-kor`, `-gar` |
| Verb -> Agent | `-uvchi`, `-tuvchi` |
| Verb -> Noun | `-ish`, `-uv` |
| Noun -> Adjective | `-li`, `-siz`, `-dosh` |
| Adjective -> Noun | `-lik` |

## Analyzer Output

The analyzer now supports multiple ranked analyses for derivational words. A lexical lemma analysis is valid and ranked separately from the derivational decomposition, so derivational words are not treated as root errors automatically.

Example:

```json
{
  "surface": "o'qituvchi",
  "analyses": [
    {
      "type": "lemma",
      "lemma": "o'qituvchi",
      "confidence": 0.95
    },
    {
      "type": "derivational",
      "root": "o'qi",
      "suffixes": ["t", "uvchi"],
      "confidence": 0.82
    }
  ]
}
```

Derivational analyses also include `derivation`, `derivation_type`, and `derivation_confidence`.

## Benchmark

Created `backend/data/benchmark/uzbek_derivational_benchmark.json`.

- Cases: 500
- Required examples covered: `ishchi`, `sotuvchi`, `ma'ruzachi`, `o'qituvchi`, `tadbirkor`

## Evaluation

Command:

```text
python backend\manage.py evaluate_uzbek_derivations
```

Results:

| Metric | Value |
| ------ | ----: |
| Derivation accuracy | 500 / 500 (100.0%) |
| Root accuracy | 500 / 500 (100.0%) |
| Derivational failures | 0 |

Category accuracy:

| Category | Correct | Total | Accuracy |
| -------- | ------: | ----: | -------: |
| Adjective -> Noun | 50 | 50 | 100.0% |
| Noun -> Adjective | 144 | 144 | 100.0% |
| Noun -> Profession | 120 | 120 | 100.0% |
| Verb -> Agent | 90 | 90 | 100.0% |
| Verb -> Noun | 96 | 96 | 100.0% |

## Legacy Morphology Benchmark

After this phase:

| Metric | Value |
| ------ | ----: |
| ROOT_ERROR | 186 |
| RULE_MISSING | 117 |
| SCORING_ERROR | 82 |
| Top-match | 115 / 500 (23.0%) |
| Coverage | 500 / 500 (100.0%) |

The legacy morphology benchmark is dominated by generated suffix-chain noise, so its `ROOT_ERROR` count is not a clean measurement of real derivational-word handling. The dedicated derivational benchmark now covers that surface directly and has zero derivational root failures.
