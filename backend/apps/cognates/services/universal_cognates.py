import json
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, List, Optional

from apps.morphology.services.universal_morphology import universal_analyze


SUPPORTED_LANGUAGES = ["uz", "tr", "az", "kk", "ky", "tk", "ug", "otk"]


@dataclass
class UniversalCognateGroup:
    cognate_id: str
    proto_form: str
    semantic_domain: str
    forms: Dict[str, str]
    confidence: float

    def to_dict(self) -> Dict:
        return asdict(self)


CYRILLIC_TO_LATIN = {
    "а": "a", "ә": "a", "б": "b", "в": "v", "г": "g", "ғ": "g", "д": "d",
    "е": "e", "ё": "yo", "ж": "j", "з": "z", "и": "i", "і": "i", "й": "y",
    "к": "k", "қ": "q", "л": "l", "м": "m", "н": "n", "ң": "ng", "о": "o",
    "ө": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u", "ұ": "u",
    "ү": "u", "ф": "f", "х": "h", "һ": "h", "ц": "ts", "ч": "ch", "ш": "sh",
    "щ": "sh", "ы": "y", "э": "e", "ю": "yu", "я": "ya",
}

ARABIC_TO_LATIN = {
    "ا": "a", "ە": "e", "ې": "e", "ى": "i", "ي": "y", "و": "o", "ۇ": "u",
    "ۈ": "u", "ۆ": "o", "ب": "b", "پ": "p", "ت": "t", "د": "d", "ر": "r",
    "ز": "z", "س": "s", "ش": "sh", "غ": "g", "ق": "q", "ك": "k", "گ": "g",
    "ڭ": "ng", "ل": "l", "م": "m", "ن": "n", "چ": "ch", "ج": "j", "خ": "h",
    "ھ": "h",
}

RUNIFORM_TO_LATIN = {
    "\U00010c00": "a", "\U00010c03": "i", "\U00010c05": "e", "\U00010c07": "o",
    "\U00010c10": "b", "\U00010c13": "d", "\U00010c16": "y", "\U00010c1a": "k",
    "\U00010c1e": "z", "\U00010c20": "l", "\U00010c22": "m", "\U00010c23": "n",
    "\U00010c2d": "ng", "\U00010c30": "d", "\U00010c34": "g", "\U00010c3c": "r",
    "\U00010c45": "t",
}

EQUIVALENT_NORMALS = {
    "tangri": "tengri",
    "tanri": "tengri",
    "tanry": "tengri",
    "tangry": "tengri",
    "tengri": "tengri",
    "teŋri": "tengri",
}


def _data_root() -> Path:
    return Path(__file__).resolve().parents[3] / "data"


def _strip_combining(value: str) -> str:
    return "".join(ch for ch in unicodedata.normalize("NFKD", value) if not unicodedata.combining(ch))


def normalize_query(value: str) -> str:
    value = (value or "").strip().lower().lstrip("*")
    value = _strip_combining(value)
    value = value.replace("ı", "i").replace("ə", "e").replace("ä", "a")
    value = value.replace("ö", "o").replace("ü", "u").replace("ý", "y")
    value = value.replace("ň", "ng").replace("ŋ", "ng").replace("'", "")
    mapped = []
    for ch in value:
        mapped.append(CYRILLIC_TO_LATIN.get(ch, ARABIC_TO_LATIN.get(ch, RUNIFORM_TO_LATIN.get(ch, ch))))
    normalized = "".join(mapped)
    normalized = "".join(ch for ch in normalized if ch.isalnum())
    return EQUIVALENT_NORMALS.get(normalized, normalized)


class UniversalCognateService:
    _groups: Optional[List[UniversalCognateGroup]] = None
    _index: Optional[Dict[str, List[UniversalCognateGroup]]] = None

    @classmethod
    def load_groups(cls) -> List[UniversalCognateGroup]:
        if cls._groups is not None:
            return cls._groups
        path = _data_root() / "cognates" / "cross_language_cognates.json"
        with path.open(encoding="utf-8") as fh:
            raw_groups = json.load(fh)
        cls._groups = [
            UniversalCognateGroup(
                cognate_id=item["cognate_id"],
                proto_form=item["proto_form"],
                semantic_domain=item.get("semantic_domain", "general"),
                forms=item.get("forms", {}),
                confidence=float(item.get("confidence", 0.0)),
            )
            for item in raw_groups
        ]
        return cls._groups

    @classmethod
    def build_index(cls) -> Dict[str, List[UniversalCognateGroup]]:
        if cls._index is not None:
            return cls._index
        index: Dict[str, List[UniversalCognateGroup]] = {}
        for group in cls.load_groups():
            candidates = [group.proto_form, *group.forms.values()]
            for candidate in candidates:
                normalized = normalize_query(candidate)
                if normalized:
                    index.setdefault(normalized, []).append(group)
        cls._index = index
        return index

    @classmethod
    def search(cls, query: str, language: Optional[str] = None, limit: int = 10) -> List[Dict]:
        if not query:
            return []
        normalized_query = normalize_query(query)
        index = cls.build_index()
        ranked = []
        exact_groups = index.get(normalized_query, [])
        scan_groups = exact_groups if exact_groups else cls.load_groups()
        for group in scan_groups:
            candidates = [group.proto_form]
            candidates.extend(group.forms.values())
            if language and language in group.forms:
                candidates.insert(0, group.forms[language])
            normalized_candidates = {normalize_query(candidate) for candidate in candidates if candidate}
            if normalized_query in normalized_candidates:
                score = 1.0
            elif any(normalized_query in candidate or candidate in normalized_query for candidate in normalized_candidates):
                score = 0.72
            else:
                continue
            ranked.append((score * group.confidence, group))
        ranked.sort(key=lambda item: item[0], reverse=True)
        return [cls._format_result(group, score) for score, group in ranked[:limit]]

    @staticmethod
    def _format_result(group: UniversalCognateGroup, score: float) -> Dict:
        return {
            **group.to_dict(),
            "score": round(score, 3),
            "historical_chain": {
                "proto_turkic": group.proto_form,
                "old_turkic": group.forms.get("otk"),
                "uyghur": group.forms.get("ug"),
                "uzbek": group.forms.get("uz"),
                "turkish": group.forms.get("tr"),
                "kazakh": group.forms.get("kk"),
            },
        }

    @staticmethod
    def morphology_context(form: str, language: str) -> Dict:
        try:
            return universal_analyze(form, language).to_dict()
        except Exception:
            return {"language": language, "surface_form": form, "features": []}
