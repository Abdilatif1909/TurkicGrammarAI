import json
import os
from functools import lru_cache
from typing import Dict, List


def _project_root() -> str:
    here = os.path.abspath(__file__)
    return os.path.abspath(os.path.join(here, "..", "..", "..", ".."))


@lru_cache(maxsize=4)
def load_derivational_rules(language: str = "uz") -> List[Dict]:
    if language == "otk":
        rules = [
            {
                "suffix": suffix,
                "derivation": suffix,
                "category": category,
                "description": description,
                "confidence_score": confidence,
            }
            for suffix, category, description, confidence in [
                ("\U00010c3c\U00010c34", "Noun -> Profession", "Old Turkic runiform agent/profession suffix", 0.94),
                ("\U00010c3c\U00010c3c\U00010c34\U00010c35", "Adjective -> Noun", "Old Turkic abstract nominal suffix", 0.9),
                ("\U00010c3d\U00010c34\U00010c35", "Adjective -> Noun", "Old Turkic abstract nominal suffix", 0.9),
                ("\U00010c3d\U00010c34\U00010c3a", "Adjective -> Noun", "Old Turkic front abstract nominal suffix", 0.9),
                ("\U00010c3d\U00010c30\U00010c3a", "Noun -> Adjective", "Old Turkic privative suffix", 0.9),
            ]
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language == "ug":
        rules = [
            {
                "suffix": suffix,
                "derivation": suffix,
                "category": category,
                "description": description,
                "confidence_score": confidence,
            }
            for suffix, category, description, confidence in [
                ("\u0686\u0649", "Noun -> Profession", "Uyghur agent/profession suffix", 0.96),
                ("\u0686\u0649\u0644\u0649\u0642", "Noun -> Noun", "Uyghur profession/collective nominal suffix", 0.94),
                ("\u0644\u0649\u0642", "Adjective -> Noun", "Uyghur abstract/location noun suffix", 0.94),
                ("\u0644\u0649\u0643", "Adjective -> Noun", "Uyghur abstract/location noun suffix", 0.94),
                ("\u0633\u0649\u0632", "Noun -> Adjective", "Uyghur privative adjective suffix", 0.94),
                ("\u062f\u0627\u0634", "Noun -> Noun", "Uyghur associative companion suffix", 0.9),
            ]
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language == "tk":
        rules = [
            {
                "suffix": suffix,
                "derivation": suffix,
                "category": category,
                "description": description,
                "confidence_score": confidence,
            }
            for suffix, category, description, confidence in [
                ("\u00e7y", "Noun -> Profession", "Turkmen agent/profession suffix", 0.96),
                ("\u00e7i", "Noun -> Profession", "Turkmen agent/profession suffix", 0.96),
                ("lyk", "Adjective -> Noun", "Turkmen abstract/location noun suffix", 0.94),
                ("lik", "Adjective -> Noun", "Turkmen abstract/location noun suffix", 0.94),
                ("li", "Noun -> Adjective", "Turkmen adjective suffix meaning with/from", 0.94),
                ("syz", "Noun -> Adjective", "Turkmen privative adjective suffix", 0.94),
                ("siz", "Noun -> Adjective", "Turkmen privative adjective suffix", 0.94),
                ("da\u015f", "Noun -> Noun", "Turkmen associative companion suffix", 0.9),
            ]
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language == "ky":
        rules = [
            {
                "suffix": suffix,
                "derivation": suffix,
                "category": category,
                "description": description,
                "confidence_score": confidence,
            }
            for suffix, category, description, confidence in [
                ("\u0447\u044b", "Noun -> Profession", "Kyrgyz agent/profession suffix", 0.96),
                ("\u0447\u0438", "Noun -> Profession", "Kyrgyz agent/profession suffix", 0.96),
                ("\u043b\u044b\u043a", "Adjective -> Noun", "Kyrgyz abstract/location noun suffix", 0.94),
                ("\u043b\u0438\u043a", "Adjective -> Noun", "Kyrgyz abstract/location noun suffix", 0.94),
                ("\u043b\u0443\u043a", "Adjective -> Noun", "Kyrgyz rounded abstract/location noun suffix", 0.94),
                ("\u043b\u04af\u043a", "Adjective -> Noun", "Kyrgyz rounded abstract/location noun suffix", 0.94),
                ("\u0441\u044b\u0437", "Noun -> Adjective", "Kyrgyz privative adjective suffix", 0.94),
                ("\u0441\u0438\u0437", "Noun -> Adjective", "Kyrgyz privative adjective suffix", 0.94),
                ("\u0441\u0443\u0437", "Noun -> Adjective", "Kyrgyz rounded privative adjective suffix", 0.94),
                ("\u0441\u04af\u0437", "Noun -> Adjective", "Kyrgyz rounded privative adjective suffix", 0.94),
                ("\u0434\u043e\u0448", "Noun -> Noun", "Kyrgyz associative companion suffix", 0.9),
                ("\u0434\u04e9\u0448", "Noun -> Noun", "Kyrgyz rounded associative companion suffix", 0.9),
            ]
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language == "kk":
        rules = [
            {
                "suffix": suffix,
                "derivation": suffix,
                "category": category,
                "description": description,
                "confidence_score": confidence,
            }
            for suffix, category, description, confidence in [
                ("\u0448\u044b", "Noun -> Profession", "Kazakh agent/profession suffix", 0.96),
                ("\u0448\u0456", "Noun -> Profession", "Kazakh agent/profession suffix", 0.96),
                ("\u043b\u044b\u049b", "Adjective -> Noun", "Kazakh abstract/location noun suffix", 0.94),
                ("\u043b\u0456\u043a", "Adjective -> Noun", "Kazakh abstract/location noun suffix", 0.94),
                ("\u0434\u044b\u049b", "Adjective -> Noun", "Kazakh consonant-harmonized abstract noun suffix", 0.9),
                ("\u0434\u0456\u043a", "Adjective -> Noun", "Kazakh consonant-harmonized abstract noun suffix", 0.9),
                ("\u0442\u044b\u049b", "Adjective -> Noun", "Kazakh consonant-harmonized abstract noun suffix", 0.9),
                ("\u0442\u0456\u043a", "Adjective -> Noun", "Kazakh consonant-harmonized abstract noun suffix", 0.9),
                ("\u0434\u044b", "Noun -> Adjective", "Kazakh adjective suffix meaning with/characterized by", 0.9),
                ("\u0434\u0456", "Noun -> Adjective", "Kazakh adjective suffix meaning with/characterized by", 0.9),
                ("\u043b\u044b", "Noun -> Adjective", "Kazakh adjective suffix meaning with/characterized by", 0.9),
                ("\u043b\u0456", "Noun -> Adjective", "Kazakh adjective suffix meaning with/characterized by", 0.9),
                ("\u0441\u044b\u0437", "Noun -> Adjective", "Kazakh privative adjective suffix", 0.94),
                ("\u0441\u0456\u0437", "Noun -> Adjective", "Kazakh privative adjective suffix", 0.94),
            ]
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language == "az":
        rules = [
            {
                "suffix": suffix,
                "derivation": suffix,
                "category": category,
                "description": description,
                "confidence_score": confidence,
            }
            for suffix, category, description, confidence in [
                ("\u00e7i", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.96),
                ("\u00e7\u0131", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.96),
                ("\u00e7u", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.96),
                ("\u00e7\u00fc", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.96),
                ("ci", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.94),
                ("c\u0131", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.94),
                ("cu", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.94),
                ("c\u00fc", "Noun -> Profession", "Azerbaijani agent/profession suffix", 0.94),
                ("\u0131\u00e7\u0131", "Verb -> Agent", "Azerbaijani verbal agent/instrument suffix", 0.94),
                ("ici", "Verb -> Agent", "Azerbaijani verbal agent/instrument suffix", 0.94),
                ("ucu", "Verb -> Agent", "Azerbaijani verbal agent/instrument suffix", 0.94),
                ("\u00fc\u00e7\u00fc", "Verb -> Agent", "Azerbaijani verbal agent/instrument suffix", 0.94),
                ("l\u0131q", "Adjective -> Noun", "Azerbaijani abstract/location noun suffix", 0.94),
                ("lik", "Adjective -> Noun", "Azerbaijani abstract/location noun suffix", 0.94),
                ("luq", "Adjective -> Noun", "Azerbaijani abstract/location noun suffix", 0.94),
                ("l\u00fck", "Adjective -> Noun", "Azerbaijani abstract/location noun suffix", 0.94),
                ("li", "Noun -> Adjective", "Azerbaijani adjective suffix meaning with/from", 0.94),
                ("l\u0131", "Noun -> Adjective", "Azerbaijani adjective suffix meaning with/from", 0.94),
                ("lu", "Noun -> Adjective", "Azerbaijani adjective suffix meaning with/from", 0.94),
                ("l\u00fc", "Noun -> Adjective", "Azerbaijani adjective suffix meaning with/from", 0.94),
                ("siz", "Noun -> Adjective", "Azerbaijani privative adjective suffix", 0.94),
                ("s\u0131z", "Noun -> Adjective", "Azerbaijani privative adjective suffix", 0.94),
                ("suz", "Noun -> Adjective", "Azerbaijani privative adjective suffix", 0.94),
                ("s\u00fcz", "Noun -> Adjective", "Azerbaijani privative adjective suffix", 0.94),
                ("da\u015f", "Noun -> Noun", "Azerbaijani associative companion suffix", 0.9),
                ("sal", "Noun -> Adjective", "Azerbaijani relational adjective suffix", 0.9),
                ("s\u0259l", "Noun -> Adjective", "Azerbaijani relational adjective suffix", 0.9),
                ("im", "Verb -> Noun", "Azerbaijani deverbal noun suffix", 0.9),
                ("\u0131m", "Verb -> Noun", "Azerbaijani deverbal noun suffix", 0.9),
                ("um", "Verb -> Noun", "Azerbaijani deverbal noun suffix", 0.9),
                ("\u00fcm", "Verb -> Noun", "Azerbaijani deverbal noun suffix", 0.9),
            ]
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language == "tr":
        rules = [
            {
                "suffix": "ci",
                "derivation": "ci",
                "category": "Noun -> Profession",
                "description": "Turkish agent/profession suffix",
                "confidence_score": 0.95,
            },
            {
                "suffix": "cı",
                "derivation": "cı",
                "category": "Noun -> Profession",
                "description": "Turkish agent/profession suffix",
                "confidence_score": 0.95,
            },
            {
                "suffix": "cu",
                "derivation": "cu",
                "category": "Noun -> Profession",
                "description": "Turkish agent/profession suffix",
                "confidence_score": 0.95,
            },
            {
                "suffix": "cü",
                "derivation": "cü",
                "category": "Noun -> Profession",
                "description": "Turkish agent/profession suffix",
                "confidence_score": 0.95,
            },
            {
                "suffix": "çi",
                "derivation": "çi",
                "category": "Noun -> Profession",
                "description": "Turkish devoiced agent/profession suffix",
                "confidence_score": 0.96,
            },
            {
                "suffix": "çı",
                "derivation": "çı",
                "category": "Noun -> Profession",
                "description": "Turkish devoiced agent/profession suffix",
                "confidence_score": 0.96,
            },
            {
                "suffix": "çu",
                "derivation": "çu",
                "category": "Noun -> Profession",
                "description": "Turkish devoiced agent/profession suffix",
                "confidence_score": 0.96,
            },
            {
                "suffix": "çü",
                "derivation": "çü",
                "category": "Noun -> Profession",
                "description": "Turkish devoiced agent/profession suffix",
                "confidence_score": 0.96,
            },
            {
                "suffix": "ıcı",
                "derivation": "ıcı",
                "category": "Verb -> Agent",
                "description": "Turkish verbal agent/instrument suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "ici",
                "derivation": "ici",
                "category": "Verb -> Agent",
                "description": "Turkish verbal agent/instrument suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "ucu",
                "derivation": "ucu",
                "category": "Verb -> Agent",
                "description": "Turkish verbal agent/instrument suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "ücü",
                "derivation": "ücü",
                "category": "Verb -> Agent",
                "description": "Turkish verbal agent/instrument suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "men",
                "derivation": "men",
                "category": "Verb -> Agent",
                "description": "Turkish occupational suffix in lexicalized agent nouns",
                "confidence_score": 0.88,
            },
            {
                "suffix": "lik",
                "derivation": "lik",
                "category": "Adjective -> Noun",
                "description": "Turkish abstract/location noun suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "lık",
                "derivation": "lık",
                "category": "Adjective -> Noun",
                "description": "Turkish abstract/location noun suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "luk",
                "derivation": "luk",
                "category": "Adjective -> Noun",
                "description": "Turkish abstract/location noun suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "lük",
                "derivation": "lük",
                "category": "Adjective -> Noun",
                "description": "Turkish abstract/location noun suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "li",
                "derivation": "li",
                "category": "Noun -> Adjective",
                "description": "Turkish adjective suffix meaning with/from",
                "confidence_score": 0.94,
            },
            {
                "suffix": "lı",
                "derivation": "lı",
                "category": "Noun -> Adjective",
                "description": "Turkish adjective suffix meaning with/from",
                "confidence_score": 0.94,
            },
            {
                "suffix": "lu",
                "derivation": "lu",
                "category": "Noun -> Adjective",
                "description": "Turkish adjective suffix meaning with/from",
                "confidence_score": 0.94,
            },
            {
                "suffix": "lü",
                "derivation": "lü",
                "category": "Noun -> Adjective",
                "description": "Turkish adjective suffix meaning with/from",
                "confidence_score": 0.94,
            },
            {
                "suffix": "siz",
                "derivation": "siz",
                "category": "Noun -> Adjective",
                "description": "Turkish privative adjective suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "sız",
                "derivation": "sız",
                "category": "Noun -> Adjective",
                "description": "Turkish privative adjective suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "suz",
                "derivation": "suz",
                "category": "Noun -> Adjective",
                "description": "Turkish privative adjective suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "süz",
                "derivation": "süz",
                "category": "Noun -> Adjective",
                "description": "Turkish privative adjective suffix",
                "confidence_score": 0.94,
            },
            {
                "suffix": "daş",
                "derivation": "daş",
                "category": "Noun -> Noun",
                "description": "Turkish associative companion suffix",
                "confidence_score": 0.9,
            },
            {
                "suffix": "sel",
                "derivation": "sel",
                "category": "Noun -> Adjective",
                "description": "Turkish relational adjective suffix",
                "confidence_score": 0.9,
            },
            {
                "suffix": "sal",
                "derivation": "sal",
                "category": "Noun -> Adjective",
                "description": "Turkish relational adjective suffix",
                "confidence_score": 0.9,
            },
            {
                "suffix": "im",
                "derivation": "im",
                "category": "Verb -> Noun",
                "description": "Turkish deverbal noun suffix",
                "confidence_score": 0.9,
            },
            {
                "suffix": "ım",
                "derivation": "ım",
                "category": "Verb -> Noun",
                "description": "Turkish deverbal noun suffix",
                "confidence_score": 0.9,
            },
            {
                "suffix": "um",
                "derivation": "um",
                "category": "Verb -> Noun",
                "description": "Turkish deverbal noun suffix",
                "confidence_score": 0.9,
            },
            {
                "suffix": "üm",
                "derivation": "üm",
                "category": "Verb -> Noun",
                "description": "Turkish deverbal noun suffix",
                "confidence_score": 0.9,
            },
        ]
        return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)

    if language != "uz":
        return []

    path = os.path.join(_project_root(), "backend", "data", "morphology", "derivational_rules.json")
    if not os.path.isfile(path):
        path = os.path.join(_project_root(), "data", "morphology", "derivational_rules.json")
    if not os.path.isfile(path):
        return []

    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)

    rules = []
    for category, items in data.get("categories", {}).items():
        for item in items:
            rule = dict(item)
            rule["category"] = category
            rules.append(rule)

    return sorted(rules, key=lambda r: len(r.get("suffix", "")), reverse=True)


def _root_candidates(base: str, rule: Dict) -> List[str]:
    roots = [base]
    for transform in rule.get("stem_transforms", []) or []:
        surface_suffix = transform.get("surface_stem_suffix", "")
        root_suffix = transform.get("root_suffix", "")
        if surface_suffix and base.endswith(surface_suffix):
            roots.append(base[: -len(surface_suffix)] + root_suffix)
    return list(dict.fromkeys(r for r in roots if r))


def _derivational_suffixes(rule: Dict) -> List[str]:
    derivation = rule.get("derivation") or rule.get("suffix", "")
    if derivation == "tuvchi":
        return ["t", "uvchi"]
    return [derivation] if derivation else []


def discover_derivations(word: str, language: str = "uz") -> List[Dict]:
    analyses = []
    for rule in load_derivational_rules(language):
        suffix = rule.get("suffix")
        if not suffix or not word.endswith(suffix) or word == suffix:
            continue

        base = word[: -len(suffix)]
        for root in _root_candidates(base, rule):
            if len(root) < int(rule.get("min_root_length", 1)):
                continue
            confidence = float(rule.get("confidence_score", 0.9))
            analysis_confidence = round(confidence * 0.85, 2)
            analyses.append({
                "type": "derivational",
                "root": root,
                "lemma": root,
                "word": word,
                "derivation": rule.get("derivation", suffix),
                "derivation_suffix_length": len(suffix),
                "derivation_type": rule.get("category"),
                "derivation_confidence": confidence,
                "suffixes": _derivational_suffixes(rule),
                "confidence": analysis_confidence,
                "score": analysis_confidence,
            })

    analyses.sort(
        key=lambda x: (
            x.get("derivation_suffix_length", 0),
            x.get("score", 0.0),
            len(x.get("root", "")),
        ),
        reverse=True,
    )
    return analyses
