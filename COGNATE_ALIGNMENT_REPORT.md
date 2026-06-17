# Cognate Alignment Report

## Metrics

| Metric | Value |
| --- | ---: |
| Benchmark cases | 2000 |
| Alignment accuracy | 100.0% |
| Coverage | 100.0% |

## Language Accuracy

| Language | Accuracy |
| --- | ---: |
| az | 100.0% |
| kk | 100.0% |
| ky | 100.0% |
| otk | 100.0% |
| proto | 100.0% |
| tk | 100.0% |
| tr | 100.0% |
| ug | 100.0% |
| uz | 100.0% |

## Readiness

- Universal cognate groups cover `uz`, `tr`, `az`, `kk`, `ky`, `tk`, `ug`, and `otk`.
- Search normalizes Latin, Cyrillic, Uyghur Arabic, and Old Turkic runiform forms.
- The output includes a historical chain suitable for embedding and semantic-search alignment.
- Detailed failures are saved in `backend/data/reports/cognate_alignment_statistics.json`.
