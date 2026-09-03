# FastText Corpus Format



Stage: Bosqich 5 - FastText training corpus



Each line in `data/processed/fasttext_corpus.txt` is one training sentence derived from one `LexicalEntry` in `lexicon_master_full.jsonl`.



Token order:



1. `surface_form`

2. `LANG_<language>`

3. `lemma`, only when `lemma != surface_form`

4. zero or more `COGNATE_<id>` tokens

5. zero or more `LINEAGE_<id>` tokens

6. `POS_<pos>`



The corpus contains one line per lexical entry. Tokens are separated with a single ASCII space.



## Real Examples



```text
kitab LANG_azerbaijani COGNATE_40 POS_noun
```

```text
kitablar LANG_azerbaijani kitab COGNATE_40 POS_noun
```

```text
kitabım LANG_azerbaijani kitab COGNATE_40 POS_noun
```

```text
kitabın LANG_azerbaijani kitab COGNATE_40 POS_noun
```

```text
kitabı LANG_azerbaijani kitab COGNATE_40 POS_noun
```
