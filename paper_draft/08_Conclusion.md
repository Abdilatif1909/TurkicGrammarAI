# 8. Conclusion

## 8.1 Summary of the Study

This study addressed the problem of constructing multilingual lexical representations for Turkic languages when available resources are limited, unevenly distributed, and linguistically heterogeneous. General subword embeddings can model orthographic and distributional regularities, but they do not explicitly encode the morphological structure, cognate relations, and historical links that are relevant to related and productively suffixing languages. The study therefore examined a repository-supported framework that combines these sources of evidence within a shared embedding and retrieval pipeline.

The proposed approach integrates lexical forms, lemmas, roots, normalized morphological features, cognate-group identifiers, and historical lineage records. These attributes are converted into explicit training tokens and grouped signal lines for a FastText skip-gram model. The trained vectors are combined with a semantic index that preserves word, lemma, root, cognate, feature, and lineage mappings. This representation is subsequently used by semantic search, metadata-enhanced RAG retrieval, and a retrieval-based structured QA component.

The scope of the work is a reproducible research framework rather than a claim of complete linguistic coverage or externally validated superiority. The reported experiments are based on repository resources and internal benchmarks, several of which require independent and expert review.

## 8.2 Main Findings

The lexical resource contains 100,000 embedding records across Uzbek, Turkish, Azerbaijani, Kazakh, Kyrgyz, Turkmen, Uyghur, and Old Turkic. It includes 88,712 unique surface forms, 26,797 unique lemmas, and 26,798 unique roots. Morphological features occur in 75,429 records, 23,018 records are associated with 2,000 cognate groups, and 25,018 records contain historical lineage information. This provides broad multilingual coverage, although normalization, provenance, and review status are not uniform across languages and resource types.

On the 5,000-pair intrinsic benchmark, the cognate-aware FastText model achieved Top-1, Top-5, and Top-10 accuracies of 40.80%, 73.66%, and 86.06%. Positive pairs had a mean cosine similarity of 0.595108, compared with 0.472318 for negative pairs, giving a mean separation margin of 0.122790. These results indicate useful pair-level organization within the internal benchmark. They do not demonstrate uniform global clustering: cognate and language-family cluster separation was negative, whereas morphological cluster separation was positive.

Semantic search achieved Recall@1 of 36.25%, Recall@5 of 72.95%, Recall@10 of 82.30%, and an MRR of 0.529888 on 2,000 queries. RAG retrieval achieved Recall@1 of 27.00%, Recall@5 of 65.90%, Recall@10 of 84.30%, and an MRR of 0.455756 on 1,000 queries. The retrieval-based QA evaluation reported answer accuracy of 83.80%, source accuracy of 99.70%, and support coverage of 83.80% on 1,000 questions.

The results consistently show stronger recovery within the first ten candidates than at the first rank. Historical retrieval benefited from explicit lineage mappings, while cross-language ranking and morphology-oriented QA remained weaker areas. Because no comparable baseline evaluation was reported, improvement over vanilla FastText or other embedding models cannot be computed.

## 8.3 Scientific Contributions

The first contribution is a unified data representation that connects modern and historical Turkic lexical resources with morphology and cognate metadata. The resulting schema retains the linguistic evidence required for both embedding training and downstream retrieval.

The second contribution is a cognate-aware corpus-construction strategy that injects `COGNATE`, `ROOT`, `FEATURE`, `LANG`, and `LINEAGE` markers into FastText training data. This approach combines character-level subword modeling with explicit repository-defined linguistic relations without introducing unsupported architectural modules.

The third contribution is an end-to-end evaluation framework spanning intrinsic embedding quality, semantic search, RAG retrieval, and structured QA. The framework records category-level behavior, error cases, source traces, and feature-contribution proxies. The proxy analysis does not replace controlled ablation, but it makes the participation of different evidence paths inspectable.

The fourth contribution is the reproducibility package. Figures, tables, benchmark files, evaluator scripts, stored metrics, manifests, traceability reports, and validity audits are organized for manuscript preparation and reviewer inspection. This package also documents which findings are measured, derived, provisional, or unsupported.

## 8.4 Future Work

The highest priority is the creation of expert-reviewed datasets. Cognate membership, Proto Turkic and Old Turkic forms, morphological analyses, lemmas, roots, and QA answer rubrics require specialist verification. Candidate datasets should be converted into locked validation and hidden test partitions after review, with item-level provenance, citations, licenses, and reviewer metadata.

Independent external evaluation is also required. Future experiments should use benchmarks that are not generated from the training dataset or semantic index, include linguistically difficult negative pairs, and represent non-cognate translation equivalence. Comparisons should include a vanilla FastText model trained under matched conditions and other reproducible lexical or multilingual embedding baselines. Controlled retraining experiments should remove morphology, cognate, lineage, and language signals individually.

Stronger representation models may be examined after independent evaluation data are established. Contextual multilingual encoders and sentence-level models could be compared with the current FastText framework, particularly for semantic disambiguation and cross-language ranking. Such comparisons should preserve the distinction between distributional similarity, morphological relatedness, cognacy, and historical lineage.

Language and domain coverage should be expanded beyond the eight current varieties to additional Turkic languages, dialects, orthographic variants, and naturally occurring corpora. Evaluation should include noisy OCR, social-media text, and unseen lexical data. Uyghur normalization requires completion, and historical resources require stronger source documentation, reviewed reconstructions, and more reliable links among historical stages and modern descendants.

## 8.5 Final Remarks

The study demonstrates a transparent method for integrating morphological, cognate, and historical evidence into a multilingual Turkic embedding and retrieval pipeline. Its internal results support continued investigation, while the documented limitations define the evidence still required. Expert-reviewed resources, independent benchmarks, matched baselines, and broader language coverage are necessary before stronger claims about comparative performance or linguistic validity can be made.
