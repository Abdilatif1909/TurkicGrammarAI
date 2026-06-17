import json
import os
from typing import List, Optional


def _find_project_root(start_path: str) -> str:
    p = os.path.abspath(start_path)
    candidate = None
    # walk up and prefer directory that contains README.md (repo root). If not found, pick highest manage.py
    while True:
        if os.path.isfile(os.path.join(p, "README.md")):
            return p
        if os.path.isfile(os.path.join(p, "manage.py")):
            candidate = p
        parent = os.path.dirname(p)
        if parent == p:
            return candidate or os.path.abspath(start_path)
        p = parent


def _find_lemma_file(project_root: str, language: str = "uz") -> Optional[str]:
    filename = {
        "uz": "uzbek_lemmas.json",
        "ug": "uyghur_lemmas.json",
        "otk": "old_turkic_lemmas.json",
        "tr": "turkish_lemmas.json",
        "az": "azerbaijani_lemmas.json",
        "tk": "turkmen_lemmas.json",
        "kk": "kazakh_lemmas.json",
        "ky": "kyrgyz_lemmas.json",
    }.get(language, f"{language}_lemmas.json")
    candidates = []
    for dirpath, _, filenames in os.walk(project_root):
        if filename in filenames:
            candidates.append(os.path.join(dirpath, filename))
    if not candidates:
        return None
    # prefer the candidate with most lemmas
    best = None
    best_count = -1
    for c in candidates:
        try:
            with open(c, encoding="utf-8") as fh:
                data = json.load(fh)
            count = 0
            lem = data.get("lemmas")
            if isinstance(lem, list):
                count = len(lem)
            if count > best_count:
                best_count = count
                best = c
        except Exception:
            continue
    return best


class LemmaDictionary:
    _lemmas = None
    _sorted = None
    _meta = None
    _by_language = {}
    _sorted_by_language = {}
    _meta_by_language = {}

    @classmethod
    def load(cls, path: Optional[str] = None, language: str = "uz"):
        if path is None and language in cls._by_language:
            return
        if path:
            src = path
        else:
            project_root = _find_project_root(__file__)
            found = _find_lemma_file(project_root, language)
            if found:
                src = found
            else:
                filename = {
                    "uz": "uzbek_lemmas.json",
                    "ug": "uyghur_lemmas.json",
                    "otk": "old_turkic_lemmas.json",
                    "tr": "turkish_lemmas.json",
                    "az": "azerbaijani_lemmas.json",
                    "tk": "turkmen_lemmas.json",
                    "kk": "kazakh_lemmas.json",
                    "ky": "kyrgyz_lemmas.json",
                }.get(language, f"{language}_lemmas.json")
                src = os.path.join(project_root, "backend", "data", "morphology", filename)
        if not os.path.isfile(src):
            cls._by_language[language] = set()
            cls._sorted_by_language[language] = []
            cls._meta_by_language[language] = {}
            if language == "uz":
                cls._lemmas = cls._by_language[language]
                cls._sorted = cls._sorted_by_language[language]
                cls._meta = cls._meta_by_language[language]
            return
        with open(src, encoding="utf-8") as fh:
            data = json.load(fh)
        lemmas = data.get("lemmas", [])
        meta = {}
        lemma_list = []
        # support two formats: list of strings or list of dicts {lemma, category, freq}
        if lemmas and isinstance(lemmas[0], dict):
            for item in lemmas:
                lemma = item.get("lemma")
                if not lemma:
                    continue
                lemma_list.append(lemma)
                meta[lemma] = {k: item.get(k) for k in (
                    "category",
                    "freq",
                    "latin_transliteration",
                    "historical_lineage",
                    "cognate_set",
                )}
        else:
            for lemma in lemmas:
                lemma_list.append(lemma)
                meta[lemma] = {"category": None, "freq": None}

        cls._by_language[language] = set(lemma_list)
        cls._meta_by_language[language] = meta
        cls._sorted_by_language[language] = sorted(list(cls._by_language[language]), key=lambda x: len(x), reverse=True)
        if language == "uz":
            cls._lemmas = cls._by_language[language]
            cls._sorted = cls._sorted_by_language[language]
            cls._meta = cls._meta_by_language[language]

    @classmethod
    def is_lemma(cls, word: str, language: str = "uz") -> bool:
        if language not in cls._by_language:
            cls.load(language=language)
        return word in cls._by_language.get(language, set())

    @classmethod
    def longest_prefix(cls, surface: str, language: str = "uz") -> Optional[str]:
        if language not in cls._sorted_by_language:
            cls.load(language=language)
        for lemma in cls._sorted_by_language.get(language, []):
            if surface.startswith(lemma):
                return lemma
        return None

    @classmethod
    def get_meta(cls, lemma: str, language: str = "uz"):
        if language not in cls._meta_by_language:
            cls.load(language=language)
        return cls._meta_by_language.get(language, {}).get(lemma, {})


if __name__ == "__main__":
    LemmaDictionary.load()
    print(len(LemmaDictionary._lemmas or []))
