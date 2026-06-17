import json
import os
from functools import lru_cache
from typing import Dict, List, Tuple
from apps.morphology.models import MorphologicalRule
from apps.morphology.services.derivational_service import discover_derivations
from apps.morphology.services.lemma_dictionary import LemmaDictionary
from django.db import DatabaseError, OperationalError


BACK_VOWELS = set("a\u0131ou")
FRONT_VOWELS = set("\u0259ei\u00f6\u00fc")
TURKMEN_BACK_VOWELS = set("ayou")
TURKMEN_FRONT_VOWELS = set("\u00e4ei\u00f6\u00fc")
OGHUZ_LANGUAGES = {"tr", "az", "tk"}
KAZAKH_BACK_VOWELS = set("\u0430\u044b\u043e\u04b1")
KAZAKH_FRONT_VOWELS = set("\u04d9\u0435\u0456\u04e9\u04af")
KYRGYZ_BACK_VOWELS = set("\u0430\u044b\u043e\u0443")
KYRGYZ_FRONT_VOWELS = set("\u044d\u0435\u0438\u04e9\u04af")
KIPCHAK_LANGUAGES = {"kk", "ky"}
KARLUK_LANGUAGES = {"uz", "ug"}
HISTORICAL_LANGUAGES = {"otk"}
HARMONY_LANGUAGES = OGHUZ_LANGUAGES | KIPCHAK_LANGUAGES | KARLUK_LANGUAGES | HISTORICAL_LANGUAGES


def _project_root() -> str:
    here = os.path.abspath(__file__)
    return os.path.abspath(os.path.join(here, "..", "..", "..", "..", ".."))


def _last_vowel(text: str) -> str:
    for char in reversed(text.lower()):
        if char in BACK_VOWELS or char in FRONT_VOWELS:
            return char
    return ""


def _oghuz_suffix_harmonizes(stem: str, suffix: str) -> bool:
    """Reject obvious Turkish/Azerbaijani vowel-harmony violations for productive suffixes."""
    if not stem or not suffix:
        return True
    last = _last_vowel(stem)
    first = _last_vowel(suffix)
    if not last or not first:
        return True

    if suffix in {"lar", "da", "dan", "ta", "tan", "sa", "ma", "maz"}:
        return last in BACK_VOWELS
    if suffix in {"ler", "de", "den", "te", "ten", "se", "me", "mez", "lər", "də", "dən", "sə", "mə"}:
        return last in FRONT_VOWELS

    back_unrounded = {"ı", "ımız", "ınız", "ım", "ın", "sı", "mış", "mışam"}
    back_rounded = {"u", "umuz", "unuz", "um", "un", "su", "muş", "muşam"}
    front_unrounded = {"i", "imiz", "iniz", "im", "in", "si", "miş", "mişəm"}
    front_rounded = {"ü", "ümüz", "ünüz", "üm", "ün", "sü", "müş", "müşəm"}
    if suffix in back_unrounded:
        return last in {"a", "ı"}
    if suffix in back_rounded:
        return last in {"o", "u"}
    if suffix in front_unrounded:
        return last in {"\u0259", "e", "i"}
    if suffix in front_rounded:
        return last in {"ö", "ü"}

    return True


def _last_turkmen_vowel(text: str) -> str:
    for char in reversed(text.lower()):
        if char in TURKMEN_BACK_VOWELS or char in TURKMEN_FRONT_VOWELS:
            return char
    return ""


def _turkmen_suffix_harmonizes(stem: str, suffix: str) -> bool:
    """Reject obvious Turkmen Latin vowel-harmony violations."""
    if not stem or not suffix:
        return True
    last = _last_turkmen_vowel(stem)
    first = _last_turkmen_vowel(suffix)
    if not last or not first:
        return True

    back_suffixes = {
        "lar", "da", "dan", "ta", "tan", "a", "y", "ny",
        "ym", "y\u0148", "y", "ymyz", "y\u0148yz", "sy",
        "dy", "ty", "an", "yp", "ar", "jak", "sa", "ma", "maz",
        "\u00e7y", "lyk", "ly", "syz", "da\u015f",
    }
    front_suffixes = {
        "ler", "de", "den", "te", "ten", "e", "i", "ni",
        "im", "i\u0148", "i", "imiz", "i\u0148iz", "si",
        "di", "ti", "en", "ip", "er", "jek", "se", "me", "mez",
        "\u00e7i", "lik", "li", "siz",
    }
    if suffix in {"lar"}:
        return last in TURKMEN_BACK_VOWELS
    if suffix in {"ler"}:
        return last in TURKMEN_FRONT_VOWELS
    return True


def _last_kazakh_vowel(text: str) -> str:
    for char in reversed(text.lower()):
        if char in KAZAKH_BACK_VOWELS or char in KAZAKH_FRONT_VOWELS:
            return char
    return ""


def _kazakh_suffix_harmonizes(stem: str, suffix: str) -> bool:
    """Reject obvious Kazakh Cyrillic vowel-harmony violations."""
    if not stem or not suffix:
        return True
    last = _last_kazakh_vowel(stem)
    first = _last_kazakh_vowel(suffix)
    if not last or not first:
        return True

    back_suffixes = {
        "\u043b\u0430\u0440", "\u0434\u0430\u0440", "\u0442\u0430\u0440",
        "\u0434\u0430", "\u0442\u0430", "\u0434\u0430\u043d", "\u0442\u0430\u043d", "\u043d\u0430\u043d",
        "\u0493\u0430", "\u049b\u0430", "\u0434\u044b", "\u0442\u044b", "\u043d\u044b",
        "\u0441\u0430", "\u043c\u0430", "\u0431\u0430", "\u043f\u0430",
        "\u044b\u043c", "\u044b\u04a3", "\u044b", "\u044b\u043c\u044b\u0437", "\u044b\u04a3\u044b\u0437",
        "\u0441\u044b", "\u043c\u044b\u043d", "\u0493\u0430\u043d", "\u049b\u0430\u043d",
    }
    front_suffixes = {
        "\u043b\u0435\u0440", "\u0434\u0435\u0440", "\u0442\u0435\u0440",
        "\u0434\u0435", "\u0442\u0435", "\u0434\u0435\u043d", "\u0442\u0435\u043d", "\u043d\u0435\u043d",
        "\u0433\u0435", "\u043a\u0435", "\u0434\u0456", "\u0442\u0456", "\u043d\u0456",
        "\u0441\u0435", "\u043c\u0435", "\u0431\u0435", "\u043f\u0435",
        "\u0456\u043c", "\u0456\u04a3", "\u0456", "\u0456\u043c\u0456\u0437", "\u0456\u04a3\u0456\u0437",
        "\u0441\u0456", "\u043c\u0456\u043d", "\u0433\u0435\u043d", "\u043a\u0435\u043d",
    }
    if suffix in {"\u043b\u0430\u0440", "\u0434\u0430\u0440", "\u0442\u0430\u0440"}:
        return last in KAZAKH_BACK_VOWELS
    if suffix in {"\u043b\u0435\u0440", "\u0434\u0435\u0440", "\u0442\u0435\u0440"}:
        return last in KAZAKH_FRONT_VOWELS
    return True


def _last_kyrgyz_vowel(text: str) -> str:
    for char in reversed(text.lower()):
        if char in KYRGYZ_BACK_VOWELS or char in KYRGYZ_FRONT_VOWELS:
            return char
    return ""


def _kyrgyz_vowel_class(vowel: str) -> str:
    if vowel in {"\u0430", "\u044b"}:
        return "back_unrounded"
    if vowel in {"\u043e", "\u0443"}:
        return "back_rounded"
    if vowel in {"\u044d", "\u0435", "\u0438"}:
        return "front_unrounded"
    if vowel in {"\u04e9", "\u04af"}:
        return "front_rounded"
    return ""


def _kyrgyz_suffix_harmonizes(stem: str, suffix: str) -> bool:
    """Reject obvious Kyrgyz Cyrillic vowel-harmony violations."""
    if not stem or not suffix:
        return True
    last = _last_kyrgyz_vowel(stem)
    first = _last_kyrgyz_vowel(suffix)
    if not last or not first:
        return True
    plural_suffixes = {
        "\u043b\u0430\u0440", "\u043b\u0435\u0440", "\u043b\u043e\u0440", "\u043b\u04e9\u0440",
        "\u0434\u0430\u0440", "\u0434\u0435\u0440", "\u0434\u043e\u0440", "\u0434\u04e9\u0440",
        "\u0442\u0430\u0440", "\u0442\u0435\u0440", "\u0442\u043e\u0440", "\u0442\u04e9\u0440",
    }
    if suffix in plural_suffixes:
        return _kyrgyz_vowel_class(last) == _kyrgyz_vowel_class(first)
    return True


def _suffix_harmonizes(stem: str, suffix: str, language: str) -> bool:
    if language == "tk":
        return _turkmen_suffix_harmonizes(stem, suffix)
    if language in OGHUZ_LANGUAGES:
        return _oghuz_suffix_harmonizes(stem, suffix)
    if language == "kk":
        return _kazakh_suffix_harmonizes(stem, suffix)
    if language == "ky":
        return _kyrgyz_suffix_harmonizes(stem, suffix)
    if language in KARLUK_LANGUAGES:
        return True
    if language in HISTORICAL_LANGUAGES:
        return True
    return True


@lru_cache(maxsize=8)
def _load_rules(language: str) -> Dict[str, List[Tuple[str, float]]]:
    """Return mapping suffix -> list of (type, confidence) for language.

    Applies pruning and scoring adjustments to prefer curated rules and
    penalize synthetic/long/implausible suffixes.
    """
    rules_list = []
    try:
        qs = MorphologicalRule.objects.filter(language=language)
        for r in qs:
            rules_list.append({
                "suffix": r.suffix,
                "suffix_type": r.suffix_type,
                "confidence_score": float(r.confidence_score),
                "examples": r.examples,
            })
    except (DatabaseError, OperationalError):
        rules_list = []
    if not rules_list:
        rules_path = os.path.join(_project_root(), "backend", "data", "morphology", {
            "uz": "uzbek_rules.json",
            "ug": "uyghur_rules.json",
            "otk": "old_turkic_rules.json",
            "tr": "turkish_rules.json",
            "az": "azerbaijani_rules.json",
            "tk": "turkmen_rules.json",
            "kk": "kazakh_rules.json",
            "ky": "kyrgyz_rules.json",
        }.get(language, f"{language}_rules.json"))
        if os.path.isfile(rules_path):
            with open(rules_path, encoding="utf-8") as fh:
                rules_list = json.load(fh).get("rules", [])
    return build_rules_map_from_list(rules_list)


def build_rules_map_from_list(rules_list: List[Dict]) -> Dict[str, List[Tuple[str, float]]]:
    """Build rules map with pruning and adjusted confidences from a list of rule dicts."""
    d: Dict[str, List[Tuple[str, float]]] = {}

    def is_synthetic(stype: str) -> bool:
        if not stype:
            return False
        s = stype.lower()
        return "autogen" in s or "auto" in s or "combo" in s or s in ("base",)

    def is_curated(stype: str) -> bool:
        # Heuristic: curated types use TitleCase or contain '-' with specific labels
        return bool(stype) and (stype[0].isupper() or "-" in stype)

    for r in rules_list:
        suf = r.get("suffix")
        stype = r.get("suffix_type", "") or ""
        conf = float(r.get("confidence_score", 1.0))

        # Base adjustments
        adj = conf
        if is_synthetic(stype):
            adj = adj - 0.5
        if is_curated(stype):
            adj = adj + 0.7

        # long improbable chains penalty
        if suf and len(suf) > 6:
            adj = adj - 0.3

        # repeated derivational chains penalty (simple heuristic)
        if suf and any(suf.count(part) >= 2 for part in [suf[i:i+2] for i in range(0, max(1, len(suf)-1))]):
            adj = adj - 0.4

        # clamp
        adj = max(min(adj, 1.0), -1.0)

        # prune extremely low-confidence rules
        if adj <= 0.15:
            continue

        d.setdefault(suf, []).append((stype, round(adj, 3)))

    return d


def _discover_analyses(word: str, rules_map: Dict[str, List[Tuple[str, float]]],
                        max_depth: int = 6, language: str = "uz") -> List[Dict]:
    """
    Backtracking discovery: try all suffix matches at the end and produce
    analyses consisting of a root and ordered suffix objects.
    """
    results = []

    def finalize(root: str, collected: List[Dict]):
        score = 1.0
        for s in collected:
            score *= s.get("confidence", 1.0)
        results.append({
            "type": "morphology",
            "root": root or "",
            "lemma": root or "",
            "suffixes": list(reversed(collected)),
            "score": score,
        })

    def backtrack(prefix: str, collected: List[Dict], depth: int):
        if depth > max_depth:
            return
        if language in HARMONY_LANGUAGES and collected and LemmaDictionary.is_lemma(prefix, language=language):
            finalize(prefix, collected)
        matched_any = False
        for suf, types in rules_map.items():
            if prefix.endswith(suf) and prefix != suf:
                remaining = prefix[: -len(suf)]
                if language in HARMONY_LANGUAGES and not _suffix_harmonizes(remaining, suf, language):
                    continue
                matched_any = True
                for t, conf in types:
                    new_collected = collected + [{"suffix": suf, "type": t, "confidence": conf}]
                    backtrack(remaining, new_collected, depth + 1)
        if not matched_any:
            # No further suffixes: finalize an analysis
            finalize(prefix or "", collected)

    backtrack(word, [], 0)
    # also include the identity (no suffix) analysis if not present
    if not any(r["root"] == word and not r["suffixes"] for r in results):
        results.append({"root": word, "lemma": word, "suffixes": [], "score": 0.1})
    # rank by score descending, tie-breaker: prefer fewer suffixes (more lexical root)
    results.sort(key=lambda x: (x["score"], -len(x.get("suffixes", []))), reverse=True)
    return results


def analyze(surface: str, language: str, max_results: int = 5) -> List[Dict]:
    # Load lemma dictionary first; derivational analysis is file-backed.
    LemmaDictionary.load(language=language)

    analyses: List[Dict] = []

    # Step 1: exact lemma lookup
    surface_is_lemma = LemmaDictionary.is_lemma(surface, language=language)
    if surface_is_lemma or language in HARMONY_LANGUAGES:
        meta = LemmaDictionary.get_meta(surface, language=language)
        lemma_value = meta.get("latin_transliteration") if language in HISTORICAL_LANGUAGES and meta.get("latin_transliteration") else surface
        lexical_score = 0.95 if surface_is_lemma else 0.12
        analyses.append({
            "type": "lemma",
            "surface": surface,
            "root": surface,
            "lemma": lemma_value,
            "suffixes": [],
            "confidence": lexical_score,
            "score": lexical_score,
        })
        if language in HISTORICAL_LANGUAGES:
            analyses[-1]["latin_transliteration"] = meta.get("latin_transliteration")
            analyses[-1]["historical_lineage"] = meta.get("historical_lineage")
            analyses[-1]["cognate_set"] = meta.get("cognate_set")

    derivational = discover_derivations(surface, language)
    analyses.extend(derivational)
    if language not in HARMONY_LANGUAGES and analyses and all(a.get("type") in ("lemma", "derivational") for a in analyses):
        analyses.sort(
            key=lambda x: (
                1 if x.get("type") == "lemma" else 0,
                x.get("derivation_suffix_length", 0),
                x.get("confidence", x.get("score", 0.0)),
            ),
            reverse=True,
        )
        return analyses[:max_results]

    rules_map = _load_rules(language)

    # Step 2: longest matching lemma as prefix
    longest = LemmaDictionary.longest_prefix(surface, language=language)
    if longest:
        # if longest equals entire surface handled above; else prefer analyses that keep longest intact
        discovered = _discover_analyses(surface, rules_map, language=language)
        analyses.extend(discovered)
        has_known_root_split = any(
            a.get("suffixes") and LemmaDictionary.is_lemma(a.get("root"), language=language)
            for a in analyses
        )
        # boost analyses whose root == longest
        for a in analyses:
            if a.get("root") == longest:
                a["score"] = a.get("score", 0.0) + 1.0
            if a.get("suffixes") and LemmaDictionary.is_lemma(a.get("root"), language=language):
                a["score"] = a.get("score", 0.0) + 1.2
            if language in HARMONY_LANGUAGES and a.get("type") == "morphology" and a.get("root") == longest:
                a["score"] = a.get("score", 0.0) + 0.25 + (0.04 * len(a.get("suffixes", [])))
            if has_known_root_split and a.get("type") == "lemma" and a.get("root") == surface:
                a["score"] = a.get("score", 0.0) - 0.9
            a.setdefault("type", "morphology")
            a.setdefault("confidence", round(float(a.get("score", 0.0)), 3))
        analyses.sort(key=lambda x: (x["score"], len(x.get("suffixes", []))), reverse=True)
        return analyses[:max_results]

    # Step 3/4: fallback to discovery
    discovered = _discover_analyses(surface, rules_map, language=language)
    analyses.extend(discovered)
    # apply lemma bonus if any analysis root is a known lemma
    for a in analyses:
        if LemmaDictionary.is_lemma(a.get("root"), language=language):
            a["score"] = a.get("score", 0.0) + 1.0
            if language in HARMONY_LANGUAGES and a.get("type") == "morphology":
                a["score"] = a.get("score", 0.0) + 0.25 + (0.04 * len(a.get("suffixes", [])))
        a.setdefault("type", "morphology")
        a.setdefault("confidence", round(float(a.get("score", 0.0)), 3))
    analyses.sort(key=lambda x: (x["score"], len(x.get("suffixes", []))), reverse=True)
    return analyses[:max_results]


def batch_analyze(words: List[str], language: str, max_results: int = 5) -> List[List[Dict]]:
    return [analyze(w, language, max_results=max_results) for w in words]
