# Benchmark Generation Rules

Stage: Bosqich 6 - Benchmark generation

All benchmarks are generated from existing project artifacts. No target counts from the paper are copied. Sizes below are measured from the generated files.

## Embedding Quality Benchmark

- Input: `cognate_groups.jsonl` and `lexicon_master_full.jsonl`.
- Positive pairs: every cross-language member pair inside each cognate group.
- Positive `source` is `lineage` when the cognate group contains an `old_turkic` member, otherwise `cognate`.
- Negative pairs: random cross-language pairs that do not share any `cognate_id`.
- Random seed: `42`.
- Positive pairs: **102947**.
- Negative pairs: **102947**.
- Total rows: **205894**.

## Semantic Search Benchmark

- Input: `cognate_groups.jsonl`.
- One query member is selected per cognate group using deterministic sort order, preferring modern languages over `old_turkic`.
- Relevant results are the other members of the same cognate group.
- Purpose: test whether a surface form retrieves cross-language cognate neighbors.
- Total queries: **147**.

## RAG Retrieval Benchmark

- Input: `lineage_links.jsonl` and `lexicon_master_full.jsonl`.
- One query is selected per Old Turkic-attested lineage group.
- Relevant results include lineage-linked descendants/Old Turkic anchors plus same-language morphological variants sharing the query lemma.
- Difference from semantic search: semantic search uses only cognate group membership, while RAG retrieval combines lineage, cognate, and morphology signals.
- Total queries: **43**.

## QA Benchmark

- Input: `cognate_groups.jsonl`, `lineage_links.jsonl`, and `lexicon_master_full.jsonl`.
- Questions are template-based, not LLM-generated.
- Templates cover shared cognate languages, lemma lookup, and Old Turkic-attested descendant languages.
- Total questions: **197**.
- `lemma_lookup` questions: **7**.
- `lineage_descendant_languages` questions: **43**.
- `shared_cognate_languages` questions: **147**.

## Samples

### Embedding

```json
[
  {
    "form_a": "ayaq",
    "form_b": "аяқ",
    "group_id": "COGNATE_1",
    "label": "positive",
    "lang_a": "azerbaijani",
    "lang_b": "kazakh",
    "pair_id": "EPOS_000001",
    "source": "lineage"
  },
  {
    "form_a": "ayaq",
    "form_b": "аяқда",
    "group_id": "COGNATE_1",
    "label": "positive",
    "lang_a": "azerbaijani",
    "lang_b": "kazakh",
    "pair_id": "EPOS_000002",
    "source": "lineage"
  },
  {
    "form_a": "ayaq",
    "form_b": "аяқды",
    "group_id": "COGNATE_1",
    "label": "positive",
    "lang_a": "azerbaijani",
    "lang_b": "kazakh",
    "pair_id": "EPOS_000003",
    "source": "lineage"
  }
]
```

### Semantic Search

```json
[
  {
    "group_id": "COGNATE_1",
    "query_form": "ayaq",
    "query_lang": "azerbaijani",
    "relevant": [
      {
        "form": "ayaqa",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqda",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqlar",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqlı",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqlıq",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqsiz",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqçı",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqı",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqım",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqın",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "аяқ",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқда",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқды",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқлы",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқлық",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқның",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқсыз",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқтан",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқтар",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқшы",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқы",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқым",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқымыз",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқың",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқға",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "adak",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakdan",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaklar",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaklıg",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaklıq",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaknı",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakqa",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaksız",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakçı",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakı",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakım",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakıŋ",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "ayak",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaka",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakcı",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakda",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakdan",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaklar",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaklı",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaksız",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakı",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakım",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakın",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "aýak",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýaka",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakda",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakdan",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýaklar",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakly",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýaknyň",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakum",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakuň",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakçy",
        "lang": "turkmen",
        "lemma": "aýak"
      }
    ],
    "source": "cognate"
  },
  {
    "group_id": "COGNATE_2",
    "query_form": "ağlı",
    "query_lang": "azerbaijani",
    "relevant": [
      {
        "form": "ақ",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақлы",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақлық",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақсыз",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақша",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақырақ",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ак",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аклуу",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аклык",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аклүү",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аксыз",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "акча",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "акыраак",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "aq",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "aqlıg",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "aqraq",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "aqsız",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "ak",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "akca",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "aklı",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "aklık",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "ak",
        "lang": "turkmen",
        "lemma": "ak"
      },
      {
        "form": "akly",
        "lang": "turkmen",
        "lemma": "ak"
      },
      {
        "form": "aklyk",
        "lang": "turkmen",
        "lemma": "ak"
      },
      {
        "form": "akrak",
        "lang": "turkmen",
        "lemma": "ak"
      }
    ],
    "source": "cognate"
  },
  {
    "group_id": "COGNATE_3",
    "query_form": "ağac",
    "query_lang": "azerbaijani",
    "relevant": [
      {
        "form": "ağaca",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacda",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaclar",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaclı",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaclıq",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacsiz",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacçı",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacı",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacım",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacın",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaç",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaça",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçcı",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçda",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçdan",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçlar",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçlı",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçsız",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçı",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçım",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçın",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "agaç",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaça",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçda",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçdan",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçlar",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçly",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçnyň",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçum",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçuň",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaççy",
        "lang": "turkmen",
        "lemma": "agaç"
      }
    ],
    "source": "cognate"
  }
]
```

### RAG Retrieval

```json
[
  {
    "anchor_type": "old_turkic_attested",
    "group_id": "COGNATE_1",
    "lineage_id": "LINEAGE_1",
    "query_form": "ayaq",
    "query_lang": "azerbaijani",
    "query_lemma": "ayaq",
    "relevant": [
      {
        "form": "adak",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adakdan",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adaklar",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adaklıg",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adaklıq",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adaknı",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adakqa",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adaksız",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adakçı",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adakı",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adakım",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "adakıŋ",
        "lang": "old_turkic",
        "lemma": "adak",
        "signal": "lineage"
      },
      {
        "form": "ayaqa",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqda",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqlar",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqlı",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqlıq",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqsiz",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqçı",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqı",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqım",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "ayaqın",
        "lang": "azerbaijani",
        "lemma": "ayaq",
        "signal": "lineage"
      },
      {
        "form": "аяқ",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқда",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқды",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқлы",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқлық",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқның",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқсыз",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқтан",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқтар",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқшы",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқы",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқым",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқымыз",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқың",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "аяқға",
        "lang": "kazakh",
        "lemma": "аяқ",
        "signal": "lineage"
      },
      {
        "form": "ayak",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayaka",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayakcı",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayakda",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayakdan",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayaklar",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayaklı",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayaksız",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayakı",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayakım",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "ayakın",
        "lang": "turkish",
        "lemma": "ayak",
        "signal": "lineage"
      },
      {
        "form": "aýak",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýaka",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýakda",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýakdan",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýaklar",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýakly",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýaknyň",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýakum",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýakuň",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      },
      {
        "form": "aýakçy",
        "lang": "turkmen",
        "lemma": "aýak",
        "signal": "lineage"
      }
    ],
    "source": "lineage+cognate+morphology"
  },
  {
    "anchor_type": "old_turkic_attested",
    "group_id": "COGNATE_10",
    "lineage_id": "LINEAGE_2",
    "query_form": "ay",
    "query_lang": "azerbaijani",
    "query_lemma": "ay",
    "relevant": [
      {
        "form": "ay",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aydan",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylar",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylıg",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylıq",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aynı",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayqa",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aysız",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayçı",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayı",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayım",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayıŋ",
        "lang": "old_turkic",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aya",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayda",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylar",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylı",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylıq",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aysiz",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayçı",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayı",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayım",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayın",
        "lang": "azerbaijani",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ай",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айда",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айды",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлар",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлы",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлық",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айның",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айсыз",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айтан",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айшы",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айы",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айым",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айымыз",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айың",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айға",
        "lang": "kazakh",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "ай",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айга",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айда",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айдан",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айды",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлар",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлуу",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлык",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айлүү",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айнын",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айсыз",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айчы",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айы",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айыбыз",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айым",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "айың",
        "lang": "kyrgyz",
        "lemma": "ай",
        "signal": "lineage"
      },
      {
        "form": "ay",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aya",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aycı",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayda",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aydan",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylar",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aylı",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aysız",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayı",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayım",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "ayın",
        "lang": "turkish",
        "lemma": "ay",
        "signal": "lineage"
      },
      {
        "form": "aý",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýa",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýda",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýdan",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýlar",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýly",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýnyň",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýum",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýuň",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      },
      {
        "form": "aýçy",
        "lang": "turkmen",
        "lemma": "aý",
        "signal": "lineage"
      }
    ],
    "source": "lineage+cognate+morphology"
  },
  {
    "anchor_type": "old_turkic_attested",
    "group_id": "COGNATE_106",
    "lineage_id": "LINEAGE_3",
    "query_form": "кел",
    "query_lang": "kazakh",
    "query_lemma": "кел",
    "relevant": [
      {
        "form": "kel",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keldi",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keler",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelme",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelmez",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelmiş",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keltim",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keltimiz",
        "lang": "old_turkic",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "келген",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келді",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келдік",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келдім",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келдің",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келеді",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келме",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келмейді",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келмін",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келсің",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келу",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келіп",
        "lang": "kazakh",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "кел",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келбе",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келбейт",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келген",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келди",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келдик",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келдим",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келдиң",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келды",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келем",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келет",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келип",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келоо",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "келсиң",
        "lang": "kyrgyz",
        "lemma": "кел",
        "signal": "lineage"
      },
      {
        "form": "kel",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keladi",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keladigan",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelaman",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelamiz",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelasan",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelasiz",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keldi",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keldik",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keldilar",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keldim",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelding",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelgan",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "keling",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelish",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelmas",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelmaydi",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelmoq",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelmoqda",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      },
      {
        "form": "kelyapti",
        "lang": "uzbek",
        "lemma": "kel",
        "signal": "lineage"
      }
    ],
    "source": "lineage+cognate+morphology"
  }
]
```

### QA

```json
[
  {
    "answer_type": "shared_cognate_languages",
    "expected_answer": "kazakh, old_turkic, turkish, turkmen",
    "group_id": "COGNATE_1",
    "question": "Which language(s) share a cognate with 'ayaq' (azerbaijani)?",
    "supporting_entries": [
      {
        "form": "ayaq",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqlar",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqım",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqın",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqı",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqda",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqa",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqsiz",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqlı",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqçı",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "ayaqlıq",
        "lang": "azerbaijani",
        "lemma": "ayaq"
      },
      {
        "form": "аяқ",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқтар",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқым",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқың",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқы",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқымыз",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқда",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқтан",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқға",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқды",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқның",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқсыз",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқлы",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқшы",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "аяқлық",
        "lang": "kazakh",
        "lemma": "аяқ"
      },
      {
        "form": "adak",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaklar",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakım",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakıŋ",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakı",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakdan",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakqa",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaknı",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaksız",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaklıg",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adakçı",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "adaklıq",
        "lang": "old_turkic",
        "lemma": "adak"
      },
      {
        "form": "ayak",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaklar",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakım",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakın",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakı",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakda",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakdan",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaka",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaksız",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayaklı",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "ayakcı",
        "lang": "turkish",
        "lemma": "ayak"
      },
      {
        "form": "aýak",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýaklar",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakum",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakuň",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakda",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakdan",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýaka",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýaknyň",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakly",
        "lang": "turkmen",
        "lemma": "aýak"
      },
      {
        "form": "aýakçy",
        "lang": "turkmen",
        "lemma": "aýak"
      }
    ]
  },
  {
    "answer_type": "shared_cognate_languages",
    "expected_answer": "kazakh, kyrgyz, old_turkic, turkish, turkmen",
    "group_id": "COGNATE_2",
    "question": "Which language(s) share a cognate with 'ağlı' (azerbaijani)?",
    "supporting_entries": [
      {
        "form": "ağlı",
        "lang": "azerbaijani",
        "lemma": "ağ"
      },
      {
        "form": "ақ",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақырақ",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақша",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақлық",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақсыз",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ақлы",
        "lang": "kazakh",
        "lemma": "ақ"
      },
      {
        "form": "ак",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "акыраак",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "акча",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аклык",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аксыз",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аклуу",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "аклүү",
        "lang": "kyrgyz",
        "lemma": "ак"
      },
      {
        "form": "aq",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "aqraq",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "aqlıg",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "aqsız",
        "lang": "old_turkic",
        "lemma": "aq"
      },
      {
        "form": "ak",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "akca",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "aklık",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "aklı",
        "lang": "turkish",
        "lemma": "ak"
      },
      {
        "form": "ak",
        "lang": "turkmen",
        "lemma": "ak"
      },
      {
        "form": "akrak",
        "lang": "turkmen",
        "lemma": "ak"
      },
      {
        "form": "aklyk",
        "lang": "turkmen",
        "lemma": "ak"
      },
      {
        "form": "akly",
        "lang": "turkmen",
        "lemma": "ak"
      }
    ]
  },
  {
    "answer_type": "shared_cognate_languages",
    "expected_answer": "turkish, turkmen",
    "group_id": "COGNATE_3",
    "question": "Which language(s) share a cognate with 'ağac' (azerbaijani)?",
    "supporting_entries": [
      {
        "form": "ağac",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaclar",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacım",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacın",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacı",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacda",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaca",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacsiz",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaclı",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağacçı",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaclıq",
        "lang": "azerbaijani",
        "lemma": "ağac"
      },
      {
        "form": "ağaç",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçlar",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçım",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçın",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçı",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçda",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçdan",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaça",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçsız",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçlı",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "ağaçcı",
        "lang": "turkish",
        "lemma": "ağaç"
      },
      {
        "form": "agaç",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçlar",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçum",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçuň",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçda",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçdan",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaça",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçnyň",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaçly",
        "lang": "turkmen",
        "lemma": "agaç"
      },
      {
        "form": "agaççy",
        "lang": "turkmen",
        "lemma": "agaç"
      }
    ]
  }
]
```
