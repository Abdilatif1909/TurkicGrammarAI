# Ablation Study

## Constraint

No retraining or algorithm changes were performed. This is a proxy ablation based on existing feature availability, benchmark categories, and RAG source contribution. It must not be cited as a controlled ablation experiment.

## Observed Evidence

- ROOT-related evidence: 75429 records contain morphology feature lists; RAG morphology source produced 915 successful hits from 17495 retrieved results.
- COGNATE-related evidence: 23018 records contain cognate groups across 2000 groups; RAG cognate source produced 675 successful hits from 7247 retrieved results.
- LINEAGE-related evidence: 25018 records contain historical lineage entries; RAG historical source produced 675 successful hits from 9000 retrieved results.
- LANGUAGE-related evidence: every embedding record contains a language code; language-specific effectiveness is visible indirectly through cross-language benchmark categories.

## Estimated Contribution

- ROOT features likely support morphology-heavy retrieval, where QA morphology accuracy is 68.8% and RAG morphology Recall@10 is 70.0%.
- COGNATE features likely support cognate retrieval, where semantic cognate Recall@10 is 82.36% and RAG cognate Recall@10 is 90.0%.
- LINEAGE features likely support historical retrieval, where RAG historical Recall@10 is 100.0% and QA historical accuracy is 100.0%.
- LANGUAGE features likely help constrain search space and interpretation, but no controlled language-marker ablation is stored in the repository.

## Hypothesized Effects Requiring Future Controlled Ablation

- Removing ROOT features should reduce morphology category performance first.
- Removing COGNATE features should reduce cognate and cross-language similarity rankings.
- Removing LINEAGE features should reduce historical retrieval and historical QA support.
- Removing LANGUAGE markers may increase cross-language confusion, especially for shared Latin-script forms.

## Publication Caution

This section should be described as a proxy ablation or feature contribution analysis. It is not a substitute for retraining controlled variants.
